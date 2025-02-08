from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time


def click_usage_option():
    option_button_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[4]/div[1]/a'
    option_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, option_button_xpath))
    )
    option_button.click()

def click_period_option():
    second_option_button_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[4]/div[2]/a'
    second_option_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, second_option_button_xpath))
    )
    second_option_button.click()

def click_last_option():
    last_option_button_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[4]/div[3]/a'
    last_option_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, last_option_button_xpath))
    )
    last_option_button.click()


# WebDriver 설정
driver = webdriver.Chrome()  # ChromeDriver 경로 설정이 필요할 수 있습니다

# 웹페이지 접속
url = "https://smartstore.naver.com/dosiraksim/products/6345953859"
driver.get(url)

try:
    # 사용량 버튼 클릭
    click_usage_option()

    # 사용량 옵션 목록 가져오기
    option_list_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[4]/div[1]/ul'
    option_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, option_list_xpath))
    )
    option_items = option_list.find_elements(By.TAG_NAME, 'li')

    # 사용량 항목 이름 추출
    options = []
    for item in option_items:
        option_name = item.find_element(By.TAG_NAME, "a").text
        options.append(option_name)

    count = 0
    # 반복문을 통해 사용량 옵션을 한바퀴 돌기
    for i in range(len(options)):
        print(options[i])
        if i != 0:
            # 첫 번째 항목이 아닌 경우 다시 클릭
            click_usage_option()
         # 사용량 옵션 목록 다시 가져오기
        option_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, option_list_xpath))
        )
        option_items = option_list.find_elements(By.TAG_NAME, 'li')
        first_option_item = option_items[i]  # 항상 첫 번째 항목을 클릭하도록 수정
        first_option_item.click()
        
        click_period_option()

        # 기간 목록 가져오기
        second_option_list_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[4]/div[2]/ul'
        second_option_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, second_option_list_xpath))
        )

        # 기간 항목 가져오기
        second_option_items = second_option_list.find_elements(By.TAG_NAME, 'li')

        second_options = []
        for item in second_option_items:
            option_name = item.find_element(By.TAG_NAME, "a").text
            second_options.append(option_name)

        # 기간 이름 추출 및 선택
        for j in range(len(second_options)):
            count += 1
            if j != 0:
                # Click the first option button again if not the first iteration

                click_usage_option()

                # Re-fetch the option items after clicking again
                option_list = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, option_list_xpath))
                )
                option_items = option_list.find_elements(By.TAG_NAME, 'li')
                first_option_item = option_items[i]  # Re-fetch the specific item again
                first_option_item.click()

                click_period_option()
            # Re-fetch the option items after clicking again
            second_option_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, second_option_list_xpath))
            )
            second_option_items = second_option_list.find_elements(By.TAG_NAME, 'li')
            second_option_item = second_option_items[j]  # Re-fetch the specific item again

            second_option_item.click()

            click_last_option()

            # 마지막 옵션 목록 가져오기
            last_option_list_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[4]/div[3]/ul'
            last_option_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, last_option_list_xpath))
            )

            # 마지막 가져오기
            last_option_items = last_option_list.find_elements(By.TAG_NAME, 'li')

            # 옵션 최종 선택 및 가격 출력
            last_option_item = last_option_items[0]
            last_option_item.click()
            price_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[5]/ul/li/div/div/span/span'
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, price_xpath))
            )
            price = price_element.text

            print(options[i], " ", second_options[j], " 가격: ", price)

            if count == 20:
                count = 0
                driver.refresh()

except TimeoutException:
    print("요소를 찾는 데 실패했습니다. 페이지 로딩이 너무 오래 걸리거나 요소가 없을 수 있습니다.")

finally:
    driver.quit()