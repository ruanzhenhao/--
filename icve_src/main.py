import pytest

from icve_pages.login_page import LoginPage
from icve_pages.course_page import CoursePage
from data.data import get_user
from icve_pages.learn_page import LearnPage

if __name__ == '__main__':
    for user in get_user():
            login_page = LoginPage()
            driver = login_page.login(user.account, user.password)
            course_page = CoursePage(driver)
            learn_drive = course_page.go_to_my_course()
            learn_page = LearnPage(learn_drive)
            learn_page.judge_file_ro_video()








