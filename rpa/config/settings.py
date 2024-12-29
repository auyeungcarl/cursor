# 账号配置
USERNAME = "838644308@qq.com"  # 你的知乎账号
PASSWORD = "123123"           # 你的知乎密码

# 浏览器配置
HEADLESS_MODE = False     # 是否启用无头模式
WAIT_TIME = 10           # 页面加载等待时间（秒）
VERIFY_CODE_WAIT_TIME = 30   # 验证码等待时间（秒）

# 文件路径配置
COOKIES_PATH = "data/cookies"  # cookies保存路径
LOG_PATH = "logs"             # 日志保存路径

# 浏览器设置
BROWSER_SETTINGS = {
    "disable_gpu": True,
    "no_sandbox": True,
    "disable_dev_shm": True,
    "disable_automation": True,  # 禁用自动化提示
    "window_size": {"width": 1920, "height": 1080},  # 窗口大小
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"  # 设置UA
} 