from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import BROWSER_SETTINGS, HEADLESS_MODE
import undetected_chromedriver as uc

def setup_browser():
    """配置并启动浏览器"""
    options = webdriver.ChromeOptions()
    
    # 添加反检测配置
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 设置用户代理
    if BROWSER_SETTINGS.get("user_agent"):
        options.add_argument(f'user-agent={BROWSER_SETTINGS["user_agent"]}')
    
    # 添加其他浏览器配置
    if BROWSER_SETTINGS.get("disable_gpu"):
        options.add_argument('--disable-gpu')
    if BROWSER_SETTINGS.get("no_sandbox"):
        options.add_argument('--no-sandbox')
    if BROWSER_SETTINGS.get("disable_dev_shm"):
        options.add_argument('--disable-dev-shm-usage')
    
    # 设置无头模式
    if HEADLESS_MODE:
        options.add_argument('--headless=new')
    
    # 设置窗口大小
    if BROWSER_SETTINGS.get("window_size"):
        width = BROWSER_SETTINGS["window_size"]["width"]
        height = BROWSER_SETTINGS["window_size"]["height"]
        options.add_argument(f'--window-size={width},{height}')
    
    # 创建浏览器实例
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # 注入 JavaScript 来禁用 webdriver 检测
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en']
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        '''
    })
    
    return driver 