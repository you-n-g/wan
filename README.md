

# Wait And Notify(WAN)
This package is under development.  We will release it soon in the future.



# Installation

[fzf](https://github.com/junegunn/fzf) is required

## config

Please config your [notifiers](https://github.com/liiight/notifiers).
`wan` will read the setting in ` ~/.dotfiles/.notifers.yaml` as the arguments for notifiers.

Here is a config example of telegram
```yaml
provider: telegram
kwargs:
    chat_id: <Your Chat id from  `@myidbot` by sending `/getid`>
    token: <Your token from `@BotFather` by sending `/newbot`>
```

Other configs:
```yaml
log_level: DEBUG  # the default level is INFO
```


# Usage

## Use in python code
```python
<Your code which takes a lot of time>
from wan import ntf; ntf('Finished')
```
