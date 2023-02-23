# 使用教程
> 您需要一个基础的[Python](https://www.python.org/downloads/)环境并安装pip。
> 如需更详细说明请使用搜索引擎。

## 1.安装EINS

Clone或下载[本库](https://github.com/Wrg1t/EINS/archive/refs/heads/master.zip)并保存到您喜欢的目录下。

并且在EINS目录内执行：

`pip install -r requirements.txt`

## 2.安装go-cqhttp
从go-cqhttp的[最新Release](https://github.com/Mrs4s/go-cqhttp/releases)处选择适合您平台的版本下载并放置到EINS所处的同一目录下。

由于平台不同，下方的**go-cqhttp.exe**可能是其它名称，但是此时您的项目目录应该像是这样：

```
EINS
├─ bot.py
├─ eins_config.py
├─ config.yml
├─ docs
│  └─ setup.md
├─ eins
│  └─ plugins
│     └─ eqinfo
│        ├─ config.ini
│        ├─ api.py
│        └─ __init__.py
├─ go-cqhttp.exe
├─ LICENSE
├─ README.md
└─ res
   └─ demo.png
```


## 3.配置

### go-cqhttp

放置好之后您需要配置目录下的`config.yml`，本项目默认本地运行，则您只需要修改：

```
account: # 账号相关
  uin:  # QQ账号
  password: '' # 密码为空时使用扫码登录
  encrypt: false  # 是否开启密码加密
```

为您所需要的内容，其他配置参考[go-cqhttp文档](https://docs.go-cqhttp.org/guide/config.html#配置信息)。
但并不推荐您直接在该处填入密码，为方便服务器部署，推荐在本地登录后一并将目录中的`session.token`上传到服务器，并且建议[使用Aoki](#4.Aoki)。

### EINS
除了go-cqhttp的配置文件外，您还需要修改`eins\plugins\eqinfo\config.ini`中的`gids`，在列表内填入您需要广播QQ群号。

## 4.Aoki

[使用方法](https://github.com/MrXiaoM/Aoki)

在本项目处使用Aoki是为了生成真实的`device.json`文件，有利于避免被腾讯风控检测。

## 5.运行

在一切都准备好了之后，分别运行`go-cqhttp`和`bot.py`。如果一切顺利，您就可以在QQ中收取到地震情报了。
