from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import re

# 숫자만 추출하는 함수
def extract_number(text):
    num = re.sub(r"[^0-9]", "", text)
    return int(num)

# 상품옵션 버튼 클릭
def click_review_option_button():
    review_option_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[1]/div/button'
    review_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, review_option_xpath))
    )
    review_option.click()

# 플랜 버튼 클릭
def click_plan_button():
    plan_button_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/div[1]/div/ul/li[1]/button'
    plan_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, plan_button_xpath))
    )
    plan_button.click()

# 용량 버튼 클릭
def click_volume_button():
    volume_button_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/div[1]/div/ul/li[2]/button'
    volume_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, volume_button_xpath))
    )
    volume_button.click()
    time.sleep(0.1)

# 기간 버튼 클릭
def click_period_button():
    period_button_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/div[1]/div/ul/li[3]/button'
    period_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, period_button_xpath))
    )
    period_button.click()
    time.sleep(0.1)

# 용량 옵션 클릭
def click_volume_option(i):
    volume_list_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/ul'
    volume_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, volume_list_xpath))
    )
    volume_items = volume_list.find_elements(By.TAG_NAME, 'li')
    volume_items[i].click()
    time.sleep(0.1)

# 용량 옵션 클릭
def click_period_option(i):
    period_list_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/ul'
    period_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, period_list_xpath))
    )
    period_items = period_list.find_elements(By.TAG_NAME, 'li')
    period_items[i].click()
    time.sleep(0.1)

# 토글다운 옵션 클릭
def click_toggledown_option(i):
    toggledown_list_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/ul'
    toggledown_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, toggledown_list_xpath))
    )
    toggledown_items = toggledown_list.find_elements(By.TAG_NAME, 'li')
    toggledown_items[i].click()
    time.sleep(0.1)

# 초기화 버튼 클릭
def click_clear_button():
    clear_button_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/div[2]/button[1]'
    clear_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, clear_button_xpath))
    )
    clear_button.click()
    time.sleep(0.1)

# 리뷰 수 읽기
def read_review():
    try:
        review_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/div[2]/button[2]'
        review = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, review_xpath))
        )
        return driver.find_element(By.XPATH, review_xpath).text
    except TimeoutException:
        return "리뷰 없음"
    
# 스크롤 다운
def scroll_down():
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 6500);")

# WebDriver 설정
driver = webdriver.Chrome()

# 웹페이지 접속
url = "https://smartstore.naver.com/esimeasy/products/10213382519"
driver.get(url)

country_Array = ["일본", "태국", "베트남", "홍콩/마카오", "대만", "중국"]
country = country_Array[3]
company_Array = ["유심사", "도시락 이심", "로밍도깨비(로밍)", "로밍도깨비(로컬)", "이심이지(로밍)", "이심이지(로컬)"]
company = company_Array[4]

try:
    # 리뷰로 스크롤 다운 후 "상품 옵션" 버튼 클릭
    scroll_down()
    click_review_option_button()
    time.sleep(0.1)
    total_review = extract_number(read_review())
    review_counts_plan = []

    # 용량 버튼 클릭
    click_volume_button()

    # 용량 목록 가져오기
    volume_list_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/ul'
    volume_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, volume_list_xpath))
    )
    volume_items = volume_list.find_elements(By.TAG_NAME, 'li')

    # 용량 항목 이름 추출
    volumes = []
    review_counts_volume = []
    for item in volume_items:
        volume_name = item.find_element(By.TAG_NAME, "span").text
        volumes.append(volume_name)

    # 반복문으로 용량 항목 클릭
    for j in range(len(volumes)):
        if j != 0:
            click_volume_button()
            volume_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, volume_list_xpath))
            )
            volume_items = volume_list.find_elements(By.TAG_NAME, 'li')
        volume_items[j].click()
        review_count_volume = extract_number(read_review())

        while review_count_volume == total_review:
            time.sleep(0.1)
            review_count_volume = extract_number(read_review())
        review_counts_volume.append(review_count_volume)

        print(country, " : ", company, " : ", volumes[j], " :: ", review_counts_volume[j])
        # 리뷰 수가 0인 경우 다음 용량으로 넘어감
        if review_count_volume == 0:
            click_clear_button()
            continue
        click_period_button()

        # 기간 목록 가져오기
        period_list_xpath = '//*[@id="REVIEW"]/div/div[3]/div[1]/div[2]/div[3]/div/ul'
        period_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, period_list_xpath))
        )
        period_items = period_list.find_elements(By.TAG_NAME, 'li')

        # 기간 항목 이름 추출
        periods = []
        review_counts_period = []
        for item in period_items:
            period_name = item.find_element(By.TAG_NAME, "span").text
            periods.append(period_name)

        for l in range(len(periods)):
            click_toggledown_option(l)
            review_count_period = extract_number(read_review())
            for k in range(3):
                if review_count_period == review_counts_volume[j]:
                    time.sleep(0.4)
                    review_count_period = extract_number(read_review())
            review_counts_period.append(review_count_period)
            if review_count_period != 0:
                print(country, " : ", company, " : ", volumes[j], " : ", periods[l], " : ", review_counts_period[l])
            click_toggledown_option(l)
        click_clear_button()

except TimeoutException:
    print("요소를 찾는 데 실패했습니다. 페이지 로딩이 너무 오래 걸리거나 요소가 없을 수 있습니다.")

finally:
    driver.quit()