import fire
import yaml
from pathlib import Path
from loguru import logger
from notifiers import get_notifier
from functools import partial
from .utils import get_pid_via_fzf, is_buzy
import psutil
import time
import sys


class Notifier:
    def __init__(self, config_path: str = '~/.dotfiles/.notifers.yaml'):
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

    def ntf(self, *messages):
        message = " ".join(messages)
        logger.debug("Sending message: {}".format(message))
        self._ntf(message=message)

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
        logger.debug(f"idle: {idle}; patience: {patience}; sleep: {sleep}")

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
            except psutil.NoSuchProcess:
                logger.info(f'The process[PID] has ended')
                break
            else:
                p_status = p.status()
                logger.debug(f'status: {p_status}, patience: {cp}')
                if idle and not is_buzy(p):
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


def ntf(message):
    # notify with the call stack
    Notifier().ntf(message)


def run():
    fire.Fire(Notifier)


if __name__ == '__main__':
    run()
