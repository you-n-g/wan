import os
import sys
from functools import partial
from pathlib import Path
from typing import Any

import yaml
from loguru import logger
from notifiers import get_notifier


class Notifier:
    def __init__(self, config_path: str = "~/.dotfiles/.notifiers.yaml"):
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
            msg = f"Can't find the config file for notifiers: {path}"
            logger.warning(msg)
            raise FileExistsError(msg)
        else:
            with path.open() as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        logger.remove()
        log_level = self.config.get("log_level", "INFO")
        logger.add(sys.stderr, level=log_level)
        logger.debug(f"log level: {log_level}")
        self._provider = get_notifier(self.config["provider"])
        kwargs = self.config["kwargs"]
        self._ntf = partial(self._provider.notify, **kwargs)

        self.env = self.config.get("env", {})

    def ntf(self, *messages):
        message = " ".join(str(m)for m in messages)
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

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.ntf(*args, **kwds)
