from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
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

    def wait_and_find_element(self, by, value, timeout=None, wait_for_clickable=False):
        """等待并查找元素，处理StaleElementReferenceException"""
        if timeout is None:
            timeout = self.wait_time
            
        for i in range(3):  # 最多重试3次
            try:
                if wait_for_clickable:
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((by, value))
                    )
                else:
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((by, value))
                    )
                return element
            except StaleElementReferenceException:
                if i == 2:  # 最后一次重试
                    raise
                time.sleep(1)
                continue

    def safe_click(self, element):
        """安全点击元素"""
        try:
            # 首先尝试直接点击
            element.click()
        except:
            try:
                # 如果直接点击失败，尝试使用JavaScript点击
                self.driver.execute_script("arguments[0].click();", element)
            except:
                try:
                    # 如果JavaScript点击失败，尝试使用ActionChains点击
                    ActionChains(self.driver).move_to_element(element).click().perform()
                except Exception as e:
                    logger.error(f"所有点击方法都失败: {str(e)}")
                    raise

    def human_like_type(self, element, text, retry_count=3):
        """模拟人类输入"""
        for attempt in range(retry_count):
            try:
                # 重新获取元素
                if attempt > 0:
                    element = self.wait_and_find_element(
                        By.CSS_SELECTOR, 
                        element.get_attribute("css selector"),
                        wait_for_clickable=True
                    )
                
                # 首先尝试使用JavaScript清空输入框
                self.driver.execute_script("arguments[0].value = '';", element)
                time.sleep(0.5)
                
                # 然后使用selenium的clear方法
                element.clear()
                time.sleep(0.5)
                
                # 最后逐字输入
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                # 验证输入是否成功
                current_value = self.driver.execute_script("return arguments[0].value;", element)
                if current_value == text:
                    return True
                    
            except Exception as e:
                if attempt == retry_count - 1:  # 最后一次尝试
                    logger.error(f"输入文本失败: {str(e)}")
                    raise
                time.sleep(1)
                continue
        return False

    def check_login_status(self):
        """检查是否登录成功"""
        try:
            # 首先检查当前URL是否已经是登录后的页面
            current_url = self.driver.current_url
            if "signin" not in current_url:
                # 尝试访问一个需要登录的页面
                self.driver.get("https://www.zhihu.com/notifications")
                time.sleep(2)
                
                # 如果URL没有被重定向回登录页，说明已经登录成功
                if "signin" not in self.driver.current_url:
                    return True
            
            # 如果还在登录页面，检查是否有登录成功的标志
            try:
                self.wait_and_find_element(
                    By.CSS_SELECTOR, 
                    '.AppHeader-profile',
                    timeout=5
                )
                return True
            except (TimeoutException, StaleElementReferenceException):
                return False
                
        except Exception as e:
            logger.error(f"检查登录状态时出错: {str(e)}")
            return False

    def handle_captcha(self):
        """处理验证码"""
        try:
            logger.warning("检测到验证码，请在{}秒内手动完成验证".format(VERIFY_CODE_WAIT_TIME))
            
            # 每隔一段时间检查登录状态
            check_interval = 2
            for i in range(VERIFY_CODE_WAIT_TIME // check_interval):
                try:
                    if self.check_login_status():
                        logger.info("验证码验证成功，登录成功！")
                        return True
                        
                    # 如果还没成功，检查是否还在验证码页面
                    if "验证码" not in self.driver.page_source:
                        # 如果不在验证码页面但也没登录成功，可能需要重新点击登录
                        login_button = self.driver.execute_script("""
                            var btn = document.querySelector('button[type="submit"]') ||
                                    document.querySelector('.SignFlow-submitButton') ||
                                    document.querySelector('.Login-content button[type="submit"]');
                            if (btn) {
                                btn.click();
                                return true;
                            }
                            return false;
                        """)
                        if login_button:
                            logger.info("重新点击登录按钮")
                    
                    time.sleep(check_interval)
                    if i % 5 == 0:  # 每10秒提醒一次
                        remaining = VERIFY_CODE_WAIT_TIME - (i * check_interval)
                        logger.info("请在{}秒内完成验证...".format(remaining))
                        
                except Exception as e:
                    if "no such window" in str(e):
                        logger.error("浏览器窗口已关闭，终止登录")
                        return False
                    logger.error(f"验证码处理过程中出错: {str(e)}")
                    continue
            
            logger.error("验证码验证超时")
            return False
            
        except Exception as e:
            logger.error(f"验证码处理过程中出错: {str(e)}")
            return False

    def wait_for_page_load(self, timeout=10):
        """等待页面加载完成"""
        try:
            # 等待页面加载完成
            self.driver.execute_script("""
                return new Promise((resolve) => {
                    if (document.readyState === 'complete') {
                        resolve(true);
                    } else {
                        window.addEventListener('load', () => {
                            resolve(true);
                        });
                    }
                });
            """)
            
            # 等待主要元素出现
            for _ in range(timeout):
                page_source = self.driver.page_source
                if 'SignFlow' in page_source or 'Login-content' in page_source:
                    return True
                time.sleep(1)
            
            return False
        except Exception as e:
            logger.error(f"等待页面加载时出错: {str(e)}")
            return False

    def login(self):
        """执行登录操作"""
        try:
            self.setup_driver()
            self.driver.get(self.url)
            logger.info("成功打开知乎登录页面")

            # 等待页面加载完成
            if not self.wait_for_page_load():
                logger.error("页面加载超时")
                return False

            # 获取页面源码，用于调试
            page_source = self.driver.page_source
            logger.info("当前页面内容: {}".format(page_source[:500]))  # 只显示前500个字符

            # 直接使用JavaScript设置输入框的值
            input_success = self.driver.execute_script("""
                // 等待元素出现
                function waitForElement(selector, timeout = 5000) {
                    return new Promise((resolve) => {
                        if (document.querySelector(selector)) {
                            return resolve(document.querySelector(selector));
                        }
                        
                        const observer = new MutationObserver(() => {
                            if (document.querySelector(selector)) {
                                resolve(document.querySelector(selector));
                                observer.disconnect();
                            }
                        });
                        
                        observer.observe(document.body, {
                            childList: true,
                            subtree: true
                        });
                        
                        setTimeout(() => {
                            observer.disconnect();
                            resolve(null);
                        }, timeout);
                    });
                }
                
                // 查找所有可能的用户名输入框选择器
                var usernameSelectors = [
                    'input[name="username"]',
                    '.SignFlow-account input',
                    '.Login-content input[name="username"]',
                    '.SignContainer-content input[name="username"]',
                    '.SignContainer input[name="username"]',
                    '.SignFlow input[name="username"]',
                    '#username'  // 添加ID选择器
                ];
                
                // 查找所有可能的密码输入框选择器
                var passwordSelectors = [
                    'input[name="password"]',
                    '.SignFlow-password input',
                    '.Login-content input[name="password"]',
                    '.SignContainer-content input[name="password"]',
                    '.SignContainer input[name="password"]',
                    '.SignFlow input[name="password"]',
                    '#password'  // 添加ID选择器
                ];
                
                // 等待并查找用户名输入框
                var usernameInput = null;
                for (var selector of usernameSelectors) {
                    usernameInput = await waitForElement(selector);
                    if (usernameInput) {
                        console.log('找到用户名输入框:', selector);
                        break;
                    }
                }
                
                // 等待并查找密码输入框
                var passwordInput = null;
                for (var selector of passwordSelectors) {
                    passwordInput = await waitForElement(selector);
                    if (passwordInput) {
                        console.log('找到密码输入框:', selector);
                        break;
                    }
                }
                
                // 如果没有找到输入框，尝试遍历所有input元素
                if (!usernameInput || !passwordInput) {
                    var inputs = document.getElementsByTagName('input');
                    console.log('所有input元素:', inputs.length);
                    for (var input of inputs) {
                        console.log('input元素:', input.outerHTML);
                    }
                }
                
                // 设置输入框的值
                if (usernameInput && passwordInput) {
                    // 清空输入框
                    usernameInput.value = '';
                    passwordInput.value = '';
                    
                    // 模拟输入
                    usernameInput.value = arguments[0];
                    passwordInput.value = arguments[1];
                    
                    // 触发输入事件
                    usernameInput.dispatchEvent(new Event('input', { bubbles: true }));
                    passwordInput.dispatchEvent(new Event('input', { bubbles: true }));
                    
                    // 触发change事件
                    usernameInput.dispatchEvent(new Event('change', { bubbles: true }));
                    passwordInput.dispatchEvent(new Event('change', { bubbles: true }));
                    
                    return true;
                }
                return false;
            """, USERNAME, PASSWORD)
            
            if not input_success:
                # 获取JavaScript的console.log输出
                logs = self.driver.get_log('browser')
                for log in logs:
                    logger.info("浏览器日志: {}".format(log))
                    
                logger.error("未找到输入框")
                return False
                
            logger.info("已输入账号密码")
            time.sleep(1)

            # 使用JavaScript点击登录按钮
            login_success = self.driver.execute_script("""
                // 等待元素出现
                function waitForElement(selector, timeout = 5000) {
                    return new Promise((resolve) => {
                        if (document.querySelector(selector)) {
                            return resolve(document.querySelector(selector));
                        }
                        
                        const observer = new MutationObserver(() => {
                            if (document.querySelector(selector)) {
                                resolve(document.querySelector(selector));
                                observer.disconnect();
                            }
                        });
                        
                        observer.observe(document.body, {
                            childList: true,
                            subtree: true
                        });
                        
                        setTimeout(() => {
                            observer.disconnect();
                            resolve(null);
                        }, timeout);
                    });
                }
                
                // 查找所有可能的登录按钮选择器
                var buttonSelectors = [
                    'button[type="submit"]',
                    '.SignFlow-submitButton',
                    '.Login-content button[type="submit"]',
                    '.SignContainer-content button[type="submit"]',
                    '.SignContainer button[type="submit"]',
                    '.SignFlow button[type="submit"]',
                    'button.submit'  // 添加class选择器
                ];
                
                // 等待并查找登录按钮
                var loginButton = null;
                for (var selector of buttonSelectors) {
                    loginButton = await waitForElement(selector);
                    if (loginButton) {
                        console.log('找到登录按钮:', selector);
                        break;
                    }
                }
                
                // 如果没有找到按钮，尝试遍历所有button元素
                if (!loginButton) {
                    var buttons = document.getElementsByTagName('button');
                    console.log('所有button元素:', buttons.length);
                    for (var button of buttons) {
                        console.log('button元素:', button.outerHTML);
                    }
                }
                
                if (loginButton) {
                    // 模拟鼠标移动到按钮上
                    loginButton.dispatchEvent(new MouseEvent('mouseover', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    }));
                    
                    // 触发焦点事件
                    loginButton.dispatchEvent(new Event('focus', { bubbles: true }));
                    
                    // 短暂延迟后点击
                    setTimeout(() => {
                        loginButton.click();
                        
                        // 触发其他可能的事件
                        loginButton.dispatchEvent(new Event('mousedown', { bubbles: true }));
                        loginButton.dispatchEvent(new Event('mouseup', { bubbles: true }));
                    }, 100);
                    
                    return true;
                }
                return false;
            """)
            
            if not login_success:
                # 获取JavaScript的console.log输出
                logs = self.driver.get_log('browser')
                for log in logs:
                    logger.info("浏览器日志: {}".format(log))
                    
                logger.error("未找到登录按钮")
                return False
                
            logger.info("已点击登录按钮")

            # 等待页面响应
            time.sleep(2)

            # 处理可能出现的验证码
            if "验证码" in self.driver.page_source:
                return self.handle_captcha()

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
                try:
                    self.driver.quit()
                except:
                    pass

if __name__ == "__main__":
    zhihu = ZhihuLogin()
    zhihu.login() 