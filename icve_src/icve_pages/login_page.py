from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self):
        # 初始化 WebDriver
        self.driver = webdriver.Chrome()
        self.url = "https://zjy2.icve.com.cn/index"
        self.driver.get(self.url)

        # 定义元素定位器为类属性
        self.button_go_login_locator = (By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]")
        self.input_account_locator = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[1]/div/div[2]/div[3]/form/div[1]/div/div[1]/input')
        self.input_password_locator = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[1]/div/div[2]/div[3]/form/div[2]/div/div/input')
        self.checkbox_locator = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[1]/div/div[2]/div[3]/form/div[4]/label/span/span')
        self.button_login_locator = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[1]/div/div[2]/div[3]/form/div[5]')
        self.button_login_locator = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[1]/div/div[2]/div[3]/form/div[5]')

    def wait_for_element(self, locator):
        """等待元素可用"""
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))

    def login(self, account, password):
        self.driver.maximize_window()
        # 等待并获取元素
        self.wait_for_element(self.button_go_login_locator).click()
        input_account = self.wait_for_element(self.input_account_locator)
        input_password = self.wait_for_element(self.input_password_locator)
        checkbox = self.wait_for_element(self.checkbox_locator)
        button_login = self.wait_for_element(self.button_login_locator)

        # 输入账号和密码
        input_account.send_keys(account)
        input_password.send_keys(password)
        checkbox.click()
        button_login.click()
        return self.driver

