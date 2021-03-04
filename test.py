from selenium import webdriver

chrome_path = './chromedriver'
driver = webdriver.Chrome(executable_path=chrome_path)

print(driver.command_executor._url)
print(driver.session_id)
