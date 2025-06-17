# config.json (与脚本同目录下，存放配置信息，请勿提交含真实密码的版本到公共仓库)
{
    "username": "2023211759",
    "password": "Wyy7929797690",
    "login_url": "https://ids.hit.edu.cn/authserver/login?service=http%3A%2F%2Fjwts.hitwh.edu.cn%2FloginCAS",
    "selection_url": "https://jwts.hitwh.edu.cn/loginCAS",
    "target_course_code": "CS101",
    "retry_interval_seconds": 5
}

# course_selector.py（加载 config.json，用户名/密码与脚本分离）
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidElementStateException


def load_config(path="config.json"):
    """
    从指定的 JSON 文件加载配置信息。
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def login(driver, username, password, login_url):
    driver.get(login_url)
    wait = WebDriverWait(driver, 15)

    # 切换账号登录
    wait.until(EC.element_to_be_clickable((By.ID, "userNameLogin_a"))).click()

    # 输入用户名
    user_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    driver.execute_script("arguments[0].removeAttribute('readonly')", user_field)
    user_field.clear()
    user_field.send_keys(username)

    # 输入密码
    pwd_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    driver.execute_script("arguments[0].removeAttribute('readonly')", pwd_field)
    pwd_field.clear()
    pwd_field.send_keys(password)

    # 点击登录按钮，用 JS 保底
    btn = wait.until(EC.element_to_be_clickable((By.ID, "login_submit")))
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btn)

    # 等待跳转完成
    wait.until(EC.url_changes(login_url))
    print("🎉 登录成功！")
    return True


def navigate_to_selection_page(driver):
    wait = WebDriverWait(driver, 10)
    # 点击 “学生选课”
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'学生选课')]"))).click()
    time.sleep(1)
    # 点击 “文化素质核心”
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'文化素质核心')]") )).click()

    # 切换到 iframe
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
    # 点击查询
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick,'queryLike')]") )).click()
    print("✅ 查询按钮点击成功，课程列表已加载。")
    return True


def find_and_select_course(driver, course_code, retry_interval):
    print(f"开始寻找目标课程: {course_code}")
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            xpath_expr = f"//tr[contains(., '{course_code}')]//button[text()='选择']"
            select_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expr)))
            print(f"🎉 找到课程 {course_code}，正在点击...")
            select_btn.click()
            print("✅ 选课成功！")
            break
        except Exception:
            now = time.strftime("%H:%M:%S")
            print(f"[{now}] 课程 {course_code} 暂不可选，{retry_interval}s 后重试...")
            time.sleep(retry_interval)


if __name__ == '__main__':
    print("脚本启动...")
    # 加载外部配置
    CONFIG = load_config()

    # 启动浏览器
    service = webdriver.ChromeService()
    driver = webdriver.Chrome(service=service)

    try:
        # 登录
        if login(driver, CONFIG['username'], CONFIG['password'], CONFIG['login_url']):
            # 导航到选课页面
            if navigate_to_selection_page(driver):
                # 抢课
                print("接下来准备选课")
                #find_and_select_course(driver, CONFIG['target_course_code'], CONFIG['retry_interval_seconds'])
            else:
                print("因导航失败，无法执行后续任务。")
        else:
            print("因登录失败，无法执行后续任务。")
    finally:
        print("脚本执行完毕，将在15秒后自动关闭浏览器...")
        time.sleep(15)
        driver.quit()
        print("浏览器已关闭。")
