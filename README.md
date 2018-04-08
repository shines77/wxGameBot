wxGameBot
-------------

[![Join the chat at https://gitter.im/shines77/Lobby](https://badges.gitter.im/shines77/Lobby.svg)](https://gitter.im/shines77/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Gitter][gitter-picture]][gitter] ![py27][py27] ![py35][py35] [English version][english-version]

# 中文 (Chinese)

`wxGameBot`：一个关于扑克牌猜大小游戏的微信机器人程序，使用 `python` 开发。

## 依赖库

本程序依赖于 [wxpy](https://github.com/youfou/wxpy) 库（一个可能是最优雅的微信个人号 API / 优秀的微信机器人），同时，[wxpy](https://github.com/youfou/wxpy) 又是基于 [itchat](https://github.com/littlecodersh/ItChat) 开发的。

注：安装 `wxpy` 时会自动安装 `itchat` 库。

### 安装 wxpy 库

`wxpy` 支持 Python 3.4-3.6，同时也支持 2.7 版本。

将下方命令中的 "pip" 替换为 "pip3" 或 "pip2"，可确保安装到对应的 Python 版本中。

1. 从 PYPI 官方源下载安装 (在国内可能比较慢或不稳定)：

```
$ pip install -U wxpy
```

2. 从豆瓣 PYPI 镜像源下载安装 (推荐国内用户选用)：

```
$ pip install -U wxpy -i "https://pypi.doubanio.com/simple/"
```

# English

`wxGameBot`: A Wechat bot about `PokerGuess` game, developed with `python`.

# Repository

* [https://github.com/shines77/wxGameBot](https://github.com/shines77/wxGameBot)

# Credits

* [shines77](https://github.com/shines77/)

[gitter-picture]: https://badges.gitter.im/littlecodersh/ItChat.svg
[gitter]: https://gitter.im/shines77/wxGameBot?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[py27]: https://img.shields.io/badge/python-2.7-ff69b4.svg
[py35]: https://img.shields.io/badge/python-3.5-red.svg
[english-version]: https://github.com/shines77/wxGameBot/blob/master/README_EN.md
