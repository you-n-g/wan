import fire
import yaml
from pathlib import Path
from loguru import logger
from notifiers import get_notifier
from functools import partial
from .utils import get_pid_via_fzf
import psutil
import time


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
        self._provider = get_notifier(self.config['provider'])
        kwargs = self.config['kwargs']
        self._ntf = partial(self._provider.notify, **kwargs)

    def ntf(self, message):
        self._ntf(message=message)

    def wait(self, pid=None, message=None, idle=True, patience=20):
        """wait.
        wati the proces to stop or idle

        Parameters
        ----------
        pid :
            pid
        idle :
            will it notify me if the process become idle
        """
        if pid is None:
            pid = get_pid_via_fzf()
        logger.info(f'PID[{pid}] selected')

        cp = 0
        while True:
            try:
                p = psutil.Process(pid)
            except psutil.NoSuchProcess:
                logger.debug('The process has ended')
                break
            else:
                # TODO: get the information of subprocess
                p_status = p.status()
                if idle and p_status not in {psutil.STATUS_RUNNING, psutil.STATUS_DISK_SLEEP}:
                    cp += 1
                    if cp > patience:
                        logger.debug(f'The process is not running, status: {p_status}')
                        break
                else:
                    cp = 0
            time.sleep(2)
        if message is None:
            # TODO: auto get some information of the process
            message = 'The process has stopped or become idle now.'
        self.ntf(message)


def run():
    fire.Fire(Notifier)


if __name__ == '__main__':
    run()
