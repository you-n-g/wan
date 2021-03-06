import os
import subprocess
import sys
import time
from functools import partial
from pathlib import Path

import fire
import psutil
import yaml
from loguru import logger
from notifiers import get_notifier

from .utils import get_pid_via_fzf, is_buzy


class Notifier:
    def __init__(self, config_path: str = '~/.dotfiles/.notifiers.yaml', idle=False):
        """__init__.

        Parameters
        ----------
        config_path : str
            The path to config file with yaml type. The config will be used buy [notifiers](https://github.com/liiight/notifiers)
            For example
            ```yaml
            provider: telegram
            kwargs:
                chat_id: <Your Chat ID>
                token: <Your token>
            ```

            If you need proxy for your provider, please use the config below.
            The env will be updated when running `ntf` method
            [This solution](https://github.com/liiight/notifiers/issues/236) is proposed by notifiers
            ```
            env:
                HTTP_PROXY: 'http://IP:PORT'
                HTTPS_PROXY: 'http://IP:PORT'
            ```
        """
        # TODO: DEBUG mode
        path = Path(config_path).expanduser()
        if not path.exists():
            msg = f'Can\'t find the config file for notifiers: {path}'
            logger.warning(msg)
            raise FileExistsError(msg)
        else:
            with path.open() as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        logger.remove()
        log_level = self.config.get('log_level', 'INFO')
        logger.add(sys.stderr, level=log_level)
        logger.debug(f"log level: {log_level}")
        self._provider = get_notifier(self.config['provider'])
        kwargs = self.config['kwargs']
        self._ntf = partial(self._provider.notify, **kwargs)

        self.env = self.config.get('env', {})

        self._idle = idle

    def ntf(self, *messages):
        message = " ".join(messages)
        logger.debug("Sending message: {}".format(message))
        if len(message) == 0:
            logger.warning("Blank message.")

        # set proxy if needed
        env_back = os.environ.copy()
        os.environ.update(self.env)
        self._ntf(message=message)
        for k, v in self.env.items():
            if k not in env_back:
                del os.environ[k]
            else:
                os.environ[k] = env_back[k]

    @staticmethod
    def _get_process_info(pid):
        process_info = ":"
        try:
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            process_info = ""
        else:
            process_info = ":" + ' '.join(p.cmdline())
        return process_info

    def wait(self, pid=None, message=None, idle=False, patience=20, sleep=3):
        """wait.

        Parameters
        ----------
        pid :
            pid
        message :
            message
        idle :
            will it notify me if the process become idle
        patience :
            How many idle status is ignored before reguard the process as stopped
        sleep :
            sleep
        """
        logger.debug(f"Idle: {self._idle or idle}; patience: {patience}; sleep: {sleep}")

        if pid is None:
            pid = get_pid_via_fzf()
            if pid is None:
                logger.info('No process selected, You can used --pid to specify the process')
                return

        process_info = self._get_process_info(pid)

        logger.info(f'Process[{pid}{process_info}] selected')

        cp = 0
        while True:
            try:
                p = psutil.Process(pid)
                p_status = p.status()
                # If the process has been stopped then we'll break the while loop
                # 1) No such PID
                # 2) Become Zombie
                # 3) Idle for a long time
                if p_status == psutil.STATUS_ZOMBIE:
                    break
            except psutil.NoSuchProcess:
                logger.info(f'The process[PID] has ended')
                break
            else:
                logger.debug(f'status: {p_status}, patience: {cp}')
                if (self._idle or idle) and not is_buzy(p):
                    cp += 1
                    if cp > patience:
                        logger.info(f'The process is idle, status: {p_status}')
                        break
                else:
                    cp = 0
            time.sleep(sleep)
        if message is None:
            message = f'The Process[{pid}{process_info}] has stopped or become idle now.'
        self.ntf(message)

    def cmd(self, *cmd):
        """
        Run command directly and notify after cmd stop or become idle
        """
        logger.info(f"run command: {cmd}")
        if len(cmd) > 0:
            jcmd = ' '.join(str(c) for c in cmd)
            proc = subprocess.Popen(jcmd, shell=True)
            self.wait(proc.pid)
            code = proc.wait()
            return code

    def wc(self, *cmd):
        """
        Wait a process to end and then start a command
        """
        logger.info(f"command queued: {cmd}")
        if len(cmd) > 0:
            self.wait()
            return self.cmd(*cmd)

    def pid(self):
        return get_pid_via_fzf()


def ntf(message):
    # notify with the call stack
    Notifier().ntf(message)


def run():
    fire.Fire(Notifier)


if __name__ == '__main__':
    run()
