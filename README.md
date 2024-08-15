# WAN

Wait and notify conveniently



[![CI](https://github.com/you-n-g/wan/actions/workflows/ci.yml/badge.svg)](https://github.com/you-n-g/wan/actions/workflows/ci.yml)
[![CommitLint](https://github.com/you-n-g/wan/actions/workflows/commitlint.yml/badge.svg)](https://github.com/you-n-g/wan/actions/workflows/commitlint.yml)
[![DevContainer](https://github.com/you-n-g/wan/actions/workflows/devcontainer.yml/badge.svg)](https://github.com/you-n-g/wan/actions/workflows/devcontainer.yml)
[![Release](https://github.com/you-n-g/wan/actions/workflows/release.yml/badge.svg)](https://github.com/you-n-g/wan/actions/workflows/release.yml)
[![Renovate](https://github.com/you-n-g/wan/actions/workflows/renovate.yml/badge.svg)](https://github.com/you-n-g/wan/actions/workflows/renovate.yml)
[![Semantic Release](https://github.com/you-n-g/wan/actions/workflows/semantic-release.yml/badge.svg)](https://github.com/you-n-g/wan/actions/workflows/semantic-release.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://you-n-g.github.io/wan/_static/badges/coverage.json)](https://you-n-g.github.io/wan/reports/coverage)
[![Release](https://img.shields.io/github/v/release/you-n-g/wan)](https://github.com/you-n-g/wan/releases)
[![PyPI](https://img.shields.io/pypi/v/wan)](https://pypi.org/project/wan/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wan)](https://pypi.org/project/wan/)
[![GitHub](https://img.shields.io/github/license/you-n-g/wan)](https://github.com/you-n-g/wan/blob/main/LICENSE)

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/5697b1e4c4a9790ece607654e6c02a160620c7e1/docs/badge/v2.json)](https://pydantic.dev)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
[![Serious Scaffold Python](https://img.shields.io/endpoint?url=https://serious-scaffold.github.io/ss-python/_static/badges/logo.json)](https://serious-scaffold.github.io/ss-python)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/you-n-g/wan)

> [!IMPORTANT]
> _WAN_ is in the **Beta** phase.
> Changes and potential instability should be anticipated.
> Any feedback, comments, suggestions and contributions are welcome!



# Wait And Notify(WAN)
This package is under development.  We will release it soon in the future.



# Installation

You can install wan with **one** of the following command

<!-- [fzf](https://github.com/junegunn/fzf) is required -->
```shell
# 1)
# pip install wan  # TODO: upload this to pip source
# 2)
pip install git+https://github.com/you-n-g/wan.git@main
# 3)
python setup.py install
# 4)
python setup.py develop  # It is recommended if you want to develop wan
```

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

* Call the function in python code directly.
```python
<Your code which takes a lot of time>
from wan import ntf; ntf('Finished')
```

* Call the function in shell directly
```shell
> sleep 10 ; wan ntf sleep finished
```


## 📜 License

MIT License, for more details, see the [LICENSE](https://github.com/you-n-g/wan/blob/main/LICENSE) file.
