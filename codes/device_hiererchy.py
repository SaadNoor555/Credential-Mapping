from appium import webdriver

desired_caps = {
    'platformName': 'Android',
    'platformVersion': 'your_platform_version',
    'deviceName': 'emulator-5554',
    'appPackage': 'your_app_package',
    'appActivity': 'your_app_activity'
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# Get the page source
page_source = driver.page_source

print(page_source)  # This will print the XML tree representing the UI hierarchy

driver.quit()
