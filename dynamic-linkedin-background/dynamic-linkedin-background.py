from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

curr = 1

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com')

email = driver.find_element(By.ID, 'session_key')
email.send_keys('tomer97klaiman@gmail.com')

pswrd = driver.find_element(By.ID, 'session_password')
pswrd.send_keys('Linkedin97!')
pswrd.send_keys(Keys.RETURN)

driver.get('https://www.linkedin.com/in/tomer-klaiman-46b322172/')
while True:
    time.sleep(5)

    edit = driver.find_element(By.ID, 'ember33')
    edit.click()

    curr = (curr+1)%3
    edit = driver.find_element(By.ID, 'profile-photo-cropper__file-upload-input')
    edit.send_keys("C:/Users/tomer/Documents/fun_projects/background-pics/"+str(curr)+".png")

    time.sleep(2)

    apply = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/footer/div[2]/button")
    apply.click()
