# 知乎自动化工具集

这是一个基于Python的知乎自动化工具集，提供自动登录、数据抓取、内容管理等功能。

## 功能特点

- 多种登录方式支持：
  - Cookie登录（优先使用）
  - 短信验证码登录
  - 账号密码登录
- 智能验证码处理
- 完善的日志记录
- 稳定的浏览器自动化

## 安装步骤

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd zhihu-automation
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置账号信息：
编辑 `config/settings.py` 文件，填入你的知乎账号信息：
```python
USERNAME = "你的知乎账号"
PASSWORD = "你的知乎密码"
```

## 使用方法

1. 运行登录测试：
```bash
python -m src.login.login
```

2. 登录成功后，cookies将自动保存在 `data/cookies` 目录下

## 项目结构

```
.
├── config/             # 配置文件目录
│   └── settings.py     # 主配置文件
├── src/               # 源代码目录
│   ├── login/         # 登录模块
│   └── utils/         # 工具类模块
├── data/              # 数据存储目录
│   └── cookies/       # cookies存储目录
├── logs/              # 日志目录
├── requirements.txt   # 项目依赖
└── README.md         # 项目说明文档
```

## 注意事项

1. 首次登录时建议不要使用无头模式（HEADLESS_MODE = False）
2. 如果出现验证码，需要在限定时间内手动完成验证
3. 登录成功后的cookies会自动保存，下次登录优先使用已保存的cookies

## 常见问题

1. 如果遇到浏览器驱动问题，请确保已安装最新版Chrome浏览器
2. 验证码识别失败时，可以尝试使用短信验证码登录方式
3. 如果cookies失效，系统会自动切换到其他登录方式

## 开发计划

- [ ] 添加更多自动化功能
- [ ] 优化验证码处理机制
- [ ] 添加更多数据抓取功能
- [ ] 支持更多登录方式
