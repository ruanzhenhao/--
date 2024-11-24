from time import sleep
from .course_page import CoursePage
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LearnPage:
    def __init__(self, driver):
        self.driver = driver
        self.next = (By.CLASS_NAME, "next")


    def process_Pop_up_window(self):
        try:
            wait = WebDriverWait(self.driver, 3)
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "el-message-box")))

            confirm_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/button[2]')
            confirm_button.click()
        except:
            return

    # 切换课件
    def change_learn(self):
        next_link = self.driver.find_element(By.CSS_SELECTOR, ".preOrNext .next .el-link")

        if next_link.text == "暂无":
            r = (WebDriverWait(driver=self.driver,timeout=10)
                 .until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[4]/div[3]/div/div[1]/div/div/div[2]'))))
            r.click()
            course_page = CoursePage(self.driver)
            course_page.get_course_list()
            self.judge_file_ro_video()

        else:
            print("下一个课件"+next_link.text)
            next_link.click()
            self.process_Pop_up_window()
            self.judge_file_ro_video()



    def learn_video(self):

        video_element = self.driver.find_element(By.CSS_SELECTOR, "video.vjs-tech")

        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "vjs-big-play-button"))
        )
        play_button.click()


        self.move()
        print("开启视频")

        # 循环检查视频播放状态
        while True:
            current_time = float(self.driver.execute_script("return arguments[0].currentTime;", video_element))
            duration = float(self.driver.execute_script("return arguments[0].duration;", video_element))

            # 检查视频是否播放完毕
            if current_time >= duration:
                break

            # 等待一段时间后再检查
            sleep(1)
        self.change_learn()


    def move(self):
        next_link = self.driver.find_element(By.CSS_SELECTOR, ".preOrNext .next .el-link")
        ActionChains(self.driver).move_to_element(next_link).perform()

    def learn_file(self):
        sleep(2)
        self.move()

        # 获取页码信息
        page_info = self.driver.find_element(By.CLASS_NAME, 'page').text
        match = re.search(r'(\d+)\s*/\s*(\d+)', page_info)

        if match:
            current_page = int(match.group(1))  # 当前页
            total_pages = int(match.group(2))  # 总页数
            print(f'当前页: {current_page}, 总页数: {total_pages}')
        else:
            print('未找到页码信息')
            return

        # 计算需要点击的次数
        click_count = total_pages - current_page + 2
        next_button = self.driver.find_element(By.CLASS_NAME, 'next')
        for i in range(click_count):
            # 找到下一页按钮并点击
            next_button.click()


            # 可选: 等待页面加载，确保内容更新
            self.driver.implicitly_wait(2)  # 或者使用 WebDriverWait


        self.change_learn()

        # 如果你需要移动到特定的页码，使用以下逻辑
        target_page = ...  # 设定目标页码
        if 1 <= target_page <= total_pages:
            while current_page != target_page:
                if current_page < target_page:
                    next_button.click()
                    current_page += 1
                else:
                    # 如果有返回按钮，点击返回
                    prev_button = self.driver.find_element(By.CLASS_NAME, 'prev')  # 假设 'prev' 是上一页按钮的类名
                    prev_button.click()
                    current_page -= 1

        print(f'已移动至目标页: {target_page}')

    def judge_file_ro_video(self):
        try:
            self.process_Pop_up_window()
            WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located(self.next))
            self.learn_file()
            return
        except:
            print("非文件类型")
            self.process_Pop_up_window()
            self.learn_video()
            self.change_learn()