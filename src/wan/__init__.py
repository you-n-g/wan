from pathlib import Path
import subprocess
import time
from typing import Optional, Union

import fire
from loguru import logger
import psutil

from .notify import Notifier
from .utils import get_pid_via_fzf, is_buzy
from .watch import watch_file


class CLI:
    # TODO: process related features can decouple from CLI
    def __init__(self, idle=False) -> None:
        self.ntf = Notifier()
        self._idle = idle

    @staticmethod
    def _get_process_info(pid):
        process_info = ":"
        try:
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            process_info = ""
        else:
            process_info = ":" + " ".join(p.cmdline())
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
                logger.info("No process selected, You can used --pid to specify the process")
                return

        process_info = self._get_process_info(pid)

        logger.info(f"Process[{pid}{process_info}] selected")
        start_time = time.time()

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
                logger.info(f"The process[PID] has ended")
                break
            else:
                logger.debug(f"status: {p_status}, patience: {cp}")
                if (self._idle or idle) and not is_buzy(p):
                    cp += 1
                    if cp > patience:
                        logger.info(f"The process is idle, status: {p_status}")
                        break
                else:
                    cp = 0
            time.sleep(sleep)
        if message is None:
            message = f"The Process[{pid}{process_info}] has stopped or become idle now."
        self.ntf(f"[{time.time() - start_time:.1f}s] {message}")

    def cmd(self, *cmd):
        """
        Run command directly and notify after cmd stop or become idle
        """
        logger.info(f"run command: {cmd}")
        if len(cmd) > 0:
            jcmd = " ".join(str(c) for c in cmd)
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

    def watch(self, path: Union[str, Path], pattern: Optional[str] =None):
        """
        watch the change of the file system
        """
        path = Path(path)
        watch_file(path, pattern=pattern)


def ntf(message, config_path: str = "~/.dotfiles/.notifiers.yaml"):
    # notify with the call stack
    Notifier(config_path=config_path)(message)


def run():
    fire.Fire(CLI)


if __name__ == "__main__":
    run()
