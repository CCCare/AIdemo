from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化Chrome驱动
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 打开百度首页
    driver.get("https://www.baidu.com")

    # 定位搜索框并输入'LangChain测试'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "kw"))
    )
    search_box.send_keys("LangChain测试")
    search_box.send_keys(Keys.RETURN)

    # 验证结果包含'教程'
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '教程')]"))
    )
    print("验证成功：搜索结果包含'教程'")

except Exception as e:
    print(f"执行过程中出现错误: {e}")

finally:
    # 关闭浏览器
    driver.quit()