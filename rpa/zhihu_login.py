from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import random
from config.settings import USERNAME, PASSWORD, WAIT_TIME, VERIFY_CODE_WAIT_TIME

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # 将日志写入文件，使用UTF-8编码以支持中文
        logging.FileHandler('login.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ZhihuLogin:
    def __init__(self):
        """初始化浏览器驱动和配置"""
        self.driver = None
        self.wait_time = WAIT_TIME
        self.url = "https://www.zhihu.com/signin"
        
    def setup_driver(self):
        """设置并启动浏览器驱动"""
        try:
            options = webdriver.ChromeOptions()
            
            # 添加反检测配置
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--start-maximized')
            
            # 随机 User-Agent
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
            ]
            options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            # 添加实验性选项
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # 添加其他反检测参数
            options.add_argument('--disable-webgl')
            options.add_argument('--disable-reading-from-canvas')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # 注入 JavaScript 来绕过检测
            stealth_js = """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.navigator.chrome = {runtime: {}};
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            """
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_js
            })
            
            logger.info("浏览器驱动初始化成功")
        except Exception as e:
            logger.error("浏览器驱动初始化失败: {}".format(str(e)))
            raise

    def human_like_type(self, element, text):
        """模拟人类输入"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # 随机延迟

    def login(self):
        """执行登录操作"""
        try:
            self.setup_driver()
            self.driver.get(self.url)
            logger.info("成功打开知乎登录页面")
            time.sleep(random.uniform(1, 2))  # 随机等待

            # 等待账号输入框
            username_input = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            
            # 等待密码输入框
            password_input = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )

            # 清空输入框
            username_input.clear()
            password_input.clear()
            time.sleep(random.uniform(0.5, 1))

            # 模拟人工输入
            self.human_like_type(username_input, USERNAME)
            time.sleep(random.uniform(0.5, 1))
            self.human_like_type(password_input, PASSWORD)
            
            logger.info("已输入账号密码")
            time.sleep(random.uniform(0.5, 1))

            # 点击登录按钮
            login_button = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            time.sleep(random.uniform(0.5, 1))
            
            # 模拟真实点击
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new MouseEvent('mouseover', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true
                }));
            """, login_button)
            time.sleep(random.uniform(0.1, 0.3))
            login_button.click()
            
            logger.info("已点击登录按钮")

            # 处理可能出现的验证码
            time.sleep(2)
            if "验证码" in self.driver.page_source:
                logger.warning("检测到验证码，请在{}秒内手动完成验证".format(VERIFY_CODE_WAIT_TIME))
                for i in range(VERIFY_CODE_WAIT_TIME):
                    if self.check_login_status():
                        logger.info("验证码验证成功，登录成功！")
                        return True
                    time.sleep(1)
                    if i % 5 == 0:
                        logger.info("请在{}秒内完成验证...".format(VERIFY_CODE_WAIT_TIME - i))

            # 检查登录结果
            if self.check_login_status():
                logger.info("登录成功！")
                return True
            else:
                logger.error("登录失败！")
                return False

        except Exception as e:
            logger.error("登录过程中出现错误: {}".format(str(e)))
            return False
        finally:
            if self.driver:
                self.driver.quit()

    def check_login_status(self):
        """检查是否登录成功"""
        try:
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.AppHeader-profile'))
            )
            return True
        except TimeoutException:
            return False

if __name__ == "__main__":
    zhihu = ZhihuLogin()
    zhihu.login() 