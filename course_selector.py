# 导入必要的库
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidElementStateException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# --- 1. 配置信息 (根据你的侦察结果修改) ---
# 警告: 仅用于练习，不要在公共代码库中存储真实密码
CONFIG = {
    "username": "2023211759",
    "password": "Wyy7929797690",
    "login_url": "https://ids.hit.edu.cn/authserver/login?service=http%3A%2F%2Fjwts.hitwh.edu.cn%2FloginCAS",  # 你的学校登录页面URL
    "selection_url": "https://jwts.hitwh.edu.cn/loginCAS", # 你的学校选课页面URL
    "target_course_code": "CS101", # 目标课程的代码
    "retry_interval_seconds": 5 # 每次尝试之间等待的秒数
}

def login(driver, username, password, login_url):
    driver.get(login_url)
    wait = WebDriverWait(driver, 15)

    # 1. 账号登录标签
    wait.until(EC.element_to_be_clickable((By.ID, "userNameLogin_a"))).click()

    # 2. 填用户名
    user = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    driver.execute_script("arguments[0].removeAttribute('readonly')", user)
    user.clear()
    user.send_keys(username)

    # 3. 填密码
    pwd = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    driver.execute_script("arguments[0].removeAttribute('readonly')", pwd)
    pwd.clear()
    pwd.send_keys(password)

    # 4. 点登录（用 JS，规避遮挡/动画）
    btn = wait.until(EC.element_to_be_clickable((By.ID, "login_submit")))
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click()", btn)

    # 5. 等待跳转成功
    wait.until(EC.url_changes(login_url))
    print("🎉 登录成功！")
    return True


def navigate_to_selection_page(driver):
    """
    在主页上完成一系列点击，最终进入 "文化素质核心" 课程列表的框架页。
    """
    wait = WebDriverWait(driver, 10)

    # 点击“学生选课”
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'学生选课')]"))).click()
    time.sleep(1)
    # 点击“文化素质核心”
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'文化素质核心')]"))).click()

    # 切到正确的 iframe（请自行替换下面的 name/id，或直接用 TAG_NAME）
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

    # 点击“查询”
    query_xpath = "//a[contains(@onclick,'queryLike')]"
    wait.until(EC.element_to_be_clickable((By.XPATH, query_xpath))).click()
    print("✅ 查询按钮点击成功，课程列表应该加载出来了")
    return True

# 注意，函数参数减少了一个
def find_and_select_course(driver, course_code): 
    """循环查找并选择课程"""
    # 我们注释掉 driver.get() 这一行，因为导航函数已经帮我们进入了页面
    # print(f"导航到选课页面，目标课程: {course_code}")
    # driver.get(selection_url) 
    
    print(f"已进入选课框架，开始寻找目标课程: {course_code}")
    
    while True:
        try:
            # 【重要】大多数教务系统，这里的刷新可能需要特殊处理
            # 简单的 driver.refresh() 可能会让你跳出 iframe，导致后续失败
            # 第一次测试时可以先不刷新，或者找到框架内的刷新按钮来点击
            print("在当前页面寻找可选名额...")
            # driver.refresh() # 暂时注释掉刷新，以防出错

            wait = WebDriverWait(driver, 10)
            
            # ... 后续的 XPath 和抢课逻辑保持不变 ...
            xpath_expression = f"//tr[contains(., '{course_code}')]//button[text()='选择']"
            select_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
            
            print(f"🎉 找到课程 {course_code} 的可选名额！正在点击...")
            select_button.click()
            
            print("✅ 选课成功！脚本任务完成。")
            break

        except Exception:
            current_time = time.strftime("%H:%M:%S")
            print(f"[{current_time}] 课程 {course_code} 暂不可选。将在 {CONFIG['retry_interval_seconds']} 秒后重试...")
            time.sleep(CONFIG['retry_interval_seconds'])

# --- 主程序入口 ---
if __name__ == "__main__":
    print("脚本启动...")

    service = webdriver.ChromeService()
    driver = webdriver.Chrome(service=service)

    try:
        # 步骤 1: 登录
        if login(driver, CONFIG["username"], CONFIG["password"], CONFIG["login_url"]):
            
            # 步骤 2: 导航到选课页面 (新增加的步骤)
            if navigate_to_selection_page(driver):
                
                # 步骤 3: 开始抢课
                # 注意：我们不再需要传入 selection_url，因为我们已经通过点击进入了
                print("可以抢课")
                #find_and_select_course(driver, CONFIG["target_course_code"])
            
            else:
                print("因导航失败，无法执行后续任务。")
        else:
            print("因登录失败，无法执行后续任务。")
    
    finally:
        print("脚本执行完毕，将在15秒后自动关闭浏览器...")
        time.sleep(15)
        driver.quit()
        print("浏览器已关闭。")

