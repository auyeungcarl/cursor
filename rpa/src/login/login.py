from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc
import json
import os
import time
from pathlib import Path
from ..utils.logger import setup_logger
from config.settings import (
    USERNAME, 
    PASSWORD,
    WAIT_TIME,
    VERIFY_CODE_WAIT_TIME,
    COOKIES_PATH,
    BROWSER_SETTINGS
)

logger = setup_logger(__name__)

class ZhihuLogin:
    """知乎登录类"""
    
    def __init__(self):
        """初始化登录类"""
        self.driver = None
        self.wait_time = WAIT_TIME
        self.url = "https://www.zhihu.com/signin"
        self.cookies_path = Path(COOKIES_PATH) / "zhihu_cookies.json"
        
        # 确保cookies目录存在
        self.cookies_path.parent.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        """上下文管理器入口"""
        options = uc.ChromeOptions()
        
        # 设置用户代理
        if BROWSER_SETTINGS.get("user_agent"):
            options.add_argument(f'user-agent={BROWSER_SETTINGS["user_agent"]}')
        
        # 设置窗口大小
        if BROWSER_SETTINGS.get("window_size"):
            width = BROWSER_SETTINGS["window_size"]["width"]
            height = BROWSER_SETTINGS["window_size"]["height"]
            options.add_argument(f'--window-size={width},{height}')
        
        self.driver = uc.Chrome(options=options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口，确保浏览器正确关闭"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")

    def save_cookies(self):
        """保存cookies到文件"""
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookies_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            logger.info("Cookies已保存到: {}".format(self.cookies_path))
            return True
        except Exception as e:
            logger.error("保存Cookies失败: {}".format(str(e)))
            return False

    def load_cookies(self):
        """从文件加载cookies"""
        try:
            if self.cookies_path.exists():
                with open(self.cookies_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                logger.info("Cookies加载成功")
                return True
            logger.info("未找到已保存的Cookies")
            return False
        except Exception as e:
            logger.error(f"加载Cookies失败: {str(e)}")
            return False

    def check_login_status(self):
        """检查是否登录成功"""
        try:
            # 首先检查窗口是否还存在
            try:
                self.driver.current_url
            except:
                raise Exception("浏览器窗口已关闭")

            # 等待个人头像元素出现
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.AppHeader-profile'))
            )
            return True
        except TimeoutException:
            logger.warning("登录状态检查超时")
            return False
        except Exception as e:
            logger.error(f"检查登录状态时出错: {str(e)}")
            raise

    def login_with_cookies(self):
        """使用cookies尝试登录"""
        try:
            self.driver.get(self.url)
            if self.load_cookies():
                self.driver.refresh()
                if self.check_login_status():
                    logger.info("使用Cookies登录成功")
                    return True
            logger.info("使用Cookies登录失败")
            return False
        except Exception as e:
            logger.error(f"使用Cookies登录时出错: {str(e)}")
            return False

    def login_with_sms(self):
        """使用短信验证码登录"""
        try:
            # 点击短信登录按钮
            try:
                sms_login_button = WebDriverWait(self.driver, self.wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.SignFlow-tab'))
                )
                sms_login_button.click()
                logger.info("已切换到短信登录")
            except:
                logger.warning("未找到短信登录按钮或点击失败")
            
            # 等待手机号输入框出现
            try:
                phone_input = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.SignFlow-accountInput input'))
                )
                
                # 确保元素可交互
                WebDriverWait(self.driver, self.wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.SignFlow-accountInput input'))
                )

                # 输入手机号
                phone_input.clear()
                self.driver.execute_script("arguments[0].value = arguments[1]", phone_input, USERNAME)
                logger.info("已输入手机号")

                # 点击发送验证码按钮
                send_code_button = WebDriverWait(self.driver, self.wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.SignFlow-smsInput button'))
                )
                send_code_button.click()
                logger.info("已点击发送验证码按钮")

                # 等待用户手动输入验证码并点击登录
                logger.warning("请在{}秒内完成以下操作：".format(VERIFY_CODE_WAIT_TIME))
                logger.warning("1. 输入收到的验证码")
                logger.warning("2. 点击登录按钮")
                
                check_interval = 2
                for i in range(VERIFY_CODE_WAIT_TIME // check_interval):
                    try:
                        if self.check_login_status():
                            logger.info("登录成功！")
                            self.save_cookies()
                            return True
                        time.sleep(check_interval)
                        if i % 5 == 0:  # 每10秒提醒一次
                            remaining = VERIFY_CODE_WAIT_TIME - (i * check_interval)
                            logger.info("请在{}秒内完成验证...".format(remaining))
                    except Exception as e:
                        if "no such window" in str(e):
                            logger.error("浏览器窗口已关闭，终止登录")
                            return False
                        raise

                logger.error("验证码登录超时")
                return False

            except Exception as e:
                logger.error("短信验证码登录过程中出错: {}".format(str(e)))
                return False

        except Exception as e:
            logger.error("登录过程中出错: {}".format(str(e)))
            return False

    def login_with_password(self):
        """使用账号密码登录"""
        try:
            # 等待账号输入框出现
            try:
                # 等待账号输入框
                username_input = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.NAME, 'username'))
                )
                
                # 等待密码输入框
                password_input = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.NAME, 'password'))
                )

                # 清空并输入账号密码
                username_input.clear()
                password_input.clear()
                time.sleep(1)  # 稍微等待一下
                
                # 模拟人工输入
                for char in USERNAME:
                    username_input.send_keys(char)
                    time.sleep(0.1)  # 模拟人工输入速度
                for char in PASSWORD:
                    password_input.send_keys(char)
                    time.sleep(0.1)
                    
                logger.info("已输入账号密码")

                # 点击登录按钮
                login_button = WebDriverWait(self.driver, self.wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
                )
                time.sleep(1)  # 等待一下再点击
                login_button.click()
                logger.info("已点击登录按钮")

                # 处理可能出现的验证码
                time.sleep(2)  # 等待可能的验证码出现
                if "验证码" in self.driver.page_source:
                    logger.warning("检测到验证码，请在{}秒内手动完成验证".format(VERIFY_CODE_WAIT_TIME))
                    check_interval = 2
                    for i in range(VERIFY_CODE_WAIT_TIME // check_interval):
                        try:
                            if self.check_login_status():
                                logger.info("验证码验证成功，登录成功！")
                                self.save_cookies()
                                return True
                            time.sleep(check_interval)
                            if i % 5 == 0:  # 每10秒提醒一次
                                remaining = VERIFY_CODE_WAIT_TIME - (i * check_interval)
                                logger.info("请在{}秒内完成验证...".format(remaining))
                        except Exception as e:
                            if "no such window" in str(e):
                                logger.error("浏览器窗口已关闭，终止登录")
                                return False
                            raise

                # 检查登录结果
                if self.check_login_status():
                    logger.info("密码登录成功")
                    self.save_cookies()
                    return True
                
                logger.error("密码登录失败")
                return False

            except Exception as e:
                logger.error("密码登录过程中出错: {}".format(str(e)))
                return False

        except Exception as e:
            logger.error("登录过程中出错: {}".format(str(e)))
            return False

    def login(self):
        """登录主函数"""
        try:
            # 首先尝试使用cookies登录
            if self.login_with_cookies():
                return True
            
            # cookies登录失败，尝试使用密码登录
            logger.info("尝试使用密码登录")
            self.driver.get(self.url)
            if self.login_with_password():
                return True
            
            # 密码登录失败，尝试使用短信验证码登录
            logger.info("尝试使用短信验证码登录")
            if self.login_with_sms():
                return True
            
            logger.error("所有登录方式均失败")
            return False
            
        except Exception as e:
            logger.error("登录过程中出错: {}".format(str(e)))
            return False

def main():
    """主函数"""
    with ZhihuLogin() as zhihu:
        if not zhihu.login():
            logger.error("登录失败！")
            return False
        logger.info("登录成功！")
        return True

if __name__ == "__main__":
    main() 