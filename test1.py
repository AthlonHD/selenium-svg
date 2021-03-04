from selenium import webdriver

executor = "http://127.0.0.1:50363"
session_id = "d7950b5210419651926dc06118b5817b"

from ReuseChrome import ReuseChrome
r_driver = ReuseChrome(command_executor=executor, session_id=session_id)
print(r_driver.current_url)

r_driver.get('http://hdtoolkit.icu:5000/test01')
