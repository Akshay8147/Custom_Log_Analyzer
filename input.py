from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Key
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import select
import time

driver = webdriver.Chrome()
driver.get("htts://www.google.com")
driver.maximize_window()

driver.implicitly_wait(10)

wait = WebDriverWait(driver, 10)

first = wait.until(EC.presence_of_element_located((By.ID,"q")))

down= select(driver.find_element(By.ID,"j"))
down.select_by_index(2)

driver.execute_script("alert('this is an alert message')")
alert = wait.until(EC.alert_is_present())
alert.accept()

iframe=driver.find_element(By.TAG_NAME,"a")
driver.switch_to.frame(iframe)
print("Inside iframe:", driver.title)
driver.switch_to.default_content()

main_window=driver.current_window_handle
driver.execute_script("window.open('url','_blank')")
for handle in driver.window_handles:
    if handle!=main_window:
        driver.switch_to.window(handle)
        print("page title:",driver.title)
        driver.close()
driver.switch_to.window(main_window)

drag=driver.find_element(By.XPATH,"q")
drop=driver.find_element(By.XPATH,"w")
actions=ActionChains(driver)
actions.drag_and_drop(drag,drop).perform()