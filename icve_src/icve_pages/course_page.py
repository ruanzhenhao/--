from docutils.nodes import list_item
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from time import sleep


class CoursePage:
    def __init__(self, driver):
        self.driver = driver
        self.my_course_locator = (By.XPATH, '//*[@id="app"]/div[1]/div[4]/div[1]/div/div/div[2]/span/div[1]/div[1]')
        self.item_locator = (By.XPATH, '//*[@id="app"]/div[1]/div[4]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]')
        self.my_course_url = "https://zjy2.icve.com.cn/study/coursePreview/spoccourseIndex"

    def wait_for_element(self, locator, timeout=3):
        """等待元素可用"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def wait_for_element30(self, locator, timeout=30):
        """等待元素可用"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def not_learn(self):
        # 等待所有项加载完成，先尝试查找 fItem
        try:
            items = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "fItem"))
            )
        except TimeoutException:
            print("未找到带有类名 'fItem' 的元素，尝试查找 'fwi'。")
            # 如果未找到 fItem，则查找 fwi
            items = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "fwi"))
            )

        return self.for_item(items)



    def for_item(self, items):
        print(len(items))
        if len(items) == 0:
            r = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.r"))
            )
            print("此课程已全部完成")

            self.go_to_my_course()
        for item in items:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", item)
                # 等待进度元素可用
                progress_text = WebDriverWait(item, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ziProgress"))
                ).text
                print(progress_text)

                # 检查是否未完成
                if "100%" not in progress_text:
                    # 获取文件名元素
                    file_name_element = item.find_element(By.CLASS_NAME, "name")

                    # 滚动到第一个未完成项目并点击
                    self.driver.execute_script("arguments[0].scrollIntoView();", file_name_element)
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of(file_name_element)
                    )

                    # 使用 JavaScript 点击
                    self.driver.execute_script("arguments[0].click();", file_name_element)
                    print("已点击项目：", file_name_element.text)

                    return self.driver # 找到第一个未完成项目后直接返回

            except Exception as e:
                print("查找元素时发生错误：", e)

        print("没有未完成的项目可点击。")





    def get_course_list(self):
        try:
            # 等待主列表加载完成
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-38786641] img.pic"))
            )
            num = 0
            while num<=3:
                # 尝试选择图像
                num+=1
                if not self.select_img():
                    break  # 如果没有图像可选择，则退出循环
                # app > div.teacherLayout > div.main > div.r > div > div.coursePreviewIndex > div.courseDataTree > div.list > div:nth-child(1) > div:nth-child(2) > div.items.iChild > div > img

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
            return self.not_learn()

        except TimeoutException:

            print("等待超时，未能找到图像元素。")
            r = (WebDriverWait(driver=self.driver, timeout=10)
                 .until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[4]/div[3]/div/div[1]/div/div/div[2]'))))
            print(1)
            r.click()

            self.go_to_my_course()

        except Exception as e:
            print("发生错误：", e)

    def select_img(self):
        """选择图像并点击"""
        target_src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAAAXNSR0IArs4c6QAAARVJREFUOE9jZCATMJKpj4HKGo1nsjKLsa9iYPzP+Pflr1CGs+m/0V2GxcYGJmZP+WUMDIzKEMX/7/7d/jCKgaHhH7JmDI3Mngtm/mf4b/Pv+y97kEImTraDjAwMR/9uT0zDqZHJY34XAwNDyD8WJluGLfFPwQp9Fkoz/fl3mIGBYc2/HYllMM1wG5k851cxMDDk/GNgtGXYnnAXxU+eC5SZGP6DNE/5tz2xDSQH1sjkMT+LkZGhmZmRweHXtsTL2KKIzWu+7t//DAf+MzDW/NueMJ2R2XNBNAPD/2lMjMxuv7fFncQXr6xei8z//f+7i4GBMYuRxXPBZYb/DAV/diTsJSYxsHgscGZgZJhA5QRAhNVk2wgA6AtSFpFbCkkAAAAASUVORK5CYII="

        try:
            # 获取所有图像元素
            divs_with_images = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-38786641] img.pic")

            if divs_with_images:
                for img in divs_with_images:
                    try:
                        # 使用显式等待确保元素可用
                        WebDriverWait(self.driver, 10).until(EC.visibility_of(img))

                        img_src = img.get_attribute("src")
                        if img_src == target_src:
                            # 滚动到元素位置并点击
                            self.driver.execute_script("arguments[0].scrollIntoView();", img)
                            self.driver.execute_script("arguments[0].click();", img)

                            # 等待新内容加载
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-38786641] img.pic"))
                            )

                    except StaleElementReferenceException:
                        print("元素引用过期，正在重新查找图像...")
                        return True  # 捕获到异常，返回 True，继续循环
                    except Exception as e:
                        print("发生错误：", e)
                        return False  # 发生其他错误时退出

                return True  # 如果成功处理所有图像
            else:
                print("未找到任何图像。")
                return False  # 没有图像可选择
        except Exception as e:
            print("发生错误：", e)
            return False  # 处理过程中发生错误



    def go_to_my_course(self, retries=3):
        """点击我的课程并检查 URL 是否变化"""
        self.wait_for_element30(self.my_course_locator).click()
        self.hint("请选择课程")
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.current_url == self.my_course_url
            )
            print("当前课程为: " + self.my_course_url)
            return self.get_course_list()
        except TimeoutException:
            if retries > 0:
                print(f"URL 变化错误，当前 URL 为: {self.driver.current_url}，重试次数剩余: {retries}")
                self.show_error_alert("URL 变化错误，正在重试...")
                self.go_to_my_course(retries - 1)
            else:
                print("达到最大重试次数，停止重试。")
                self.show_error_alert("达到最大重试次数，无法访问课程页面。")

    def show_error_alert(self, msg):
        """显示错误提示弹窗"""
        self.driver.execute_script(f"alert('{msg}');")
        sleep(1)  # 等待弹窗出现
        self.driver.switch_to.alert.accept()  # 接受弹窗

    def hint (self,msg):
        self.driver.execute_script(f"alert('{msg+"请勿点击，即将自动跳转"}');")

        # 等待弹窗出现
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        # 处理弹窗
        alert = self.driver.switch_to.alert
        sleep(1)
        alert.accept()  # 接受弹窗
