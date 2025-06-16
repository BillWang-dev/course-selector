# 导入必要的库
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
# 导入库 (确保这些都在文件顶部)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 导入库 (确保这些都在文件顶部)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 导入库 (确保这些都在文件顶部)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidElementStateException # 导入特定的异常类型




# 确保文件顶部有这些导入
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidElementStateException, TimeoutException


# 确保文件顶部有这些导入
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidElementStateException

def login(driver, username, password, login_url):
    print("正在打开登录页面...")
    driver.get(login_url)
    wait = WebDriverWait(driver, 15)

    try:
        # 1. 切换到账号密码登录
        print("等待并点击“账号登录”标签……")
        tab = wait.until(EC.element_to_be_clickable((By.ID, "userNameLogin_a")))
        tab.click()

        # 2. 输入用户名
        print("等待用户名输入框可交互……")
        user_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        user_field.click()  # 触发 onfocus，去掉 readonly
        # 如果页面用 JS 给它加了 readonly，也可以强制去除：
        driver.execute_script("arguments[0].removeAttribute('readonly')", user_field)
        user_field.clear()
        user_field.send_keys(username)
        print("✅ 用户名输入完毕。")

        # 3. 输入密码
        print("等待密码输入框可交互……")
        pwd_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        pwd_field.click()
        driver.execute_script("arguments[0].removeAttribute('readonly')", pwd_field)
        pwd_field.clear()
        pwd_field.send_keys(password)
        print("✅ 密码输入完毕。")

        # 4. 等待盐值字段被 JS 填好
        print("等待 JS 填入 saltPassword……")
        wait.until(lambda d: d.find_element(By.ID, "saltPassword").get_attribute("value"))
        print("✅ saltPassword 已填值。")

        # 5. 点击登录
        print("定位并点击登录按钮……")
        btn = wait.until(EC.element_to_be_clickable((By.ID, "login_submit")))
        btn.click()

        # 6. 等待跳转
        print("等待页面跳转……")
        wait.until(lambda d: d.current_url != login_url)

        # 7. 最后验证
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '学生选课')]")))
        print("🎉 登录成功！")
        return True

    except InvalidElementStateException as e:
        print("❌ 元素状态异常：可能是只读或未启用。", e)
        driver.save_screenshot("login_invalid_state.png")
        print("已截图 login_invalid_state.png。")
        return False

    except TimeoutException:
        print("❌ 登录失败：等待超时，可能是定位器失效或网络问题。")
        driver.save_screenshot("login_timeout_error.png")
        print("已截图 login_timeout_error.png。")
        return False

    except Exception as e:
        print("❌ 登录失败，未知错误：", type(e).__name__, e)
        driver.save_screenshot("login_generic_error.png")
        print("已截图 login_generic_error.png。")
        return False



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

