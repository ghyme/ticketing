# -*- coding: utf-8 -*-
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


def open_brower():
    driver = webdriver.Chrome()
    # opt = webdriver.ChromeOptions() 
    # opt.add_argument("headless")
    # driver = webdriver.Chrome(options=opt)
    # driver.get("https://www.google.com/")
    return driver

def login(driver, login_id, login_psw):
    driver.get("http://www.letskorail.com/korail/com/login.do")
    # driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')

    # while len(driver.window_handles) > 1:
    #     driver.switch_to.window(driver.window_handles[1]) # 첫 번째 팝업 창으로 제어권 옮기기
    #     driver.close()                                    # 첫 번째 팝업 창 닫기     

    driver.implicitly_wait(15)
    driver.find_element(By.ID, 'txtMember').send_keys(str(login_id))
    driver.find_element(By.ID, 'txtPwd').send_keys(str(login_psw))
    # driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
    driver.find_element(By.XPATH, '//*[@id="loginDisplay1"]/ul/li[3]/a/img').click()
    driver.find_element(By.CSS_SELECTOR, "#header > div.lnb > div.lnb_m01 > h3 > a > img").click()
    driver.implicitly_wait(5)

    return driver

def search_train(driver, dpt_stn, arr_stn, dpt_dt, dpt_tm, check_only = False, check_from=1, check_to=3, want_reserve=False):
    is_booked = False # 예약 완료 되었는지 확인용
    cnt_refresh = 0 # 새로고침 회수 기록

    # driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do') # 기차 조회 페이지로 이동
    # driver.implicitly_wait(5)
    # 출발지/도착지/출발날짜/출발시간 입력
    elm_dpt_stn = driver.find_element(By.ID, 'start')
    elm_dpt_stn.clear()
    elm_dpt_stn.send_keys(dpt_stn) # 출발지
    elm_dpt_stn.send_keys(Keys.RETURN)

    elm_arr_stn = driver.find_element(By.ID, 'get')
    elm_arr_stn.clear()
    elm_arr_stn.send_keys(arr_stn) # 도착지
    elm_arr_stn.send_keys(Keys.RETURN)

    dpt_dy = dpt_dt[:4]
    dpt_dm = dpt_dt[4:6]
    dpt_dd = dpt_dt[6:]


    if int(dpt_tm) < 12:
        dpt_tm = "%s (오전%s)" % (dpt_tm, dpt_tm)
    else:
        dpt_tm = "%s (오후%02d)" % (dpt_tm, int(dpt_tm)-12)

    # elm_dptDy = driver.find_element(By.ID, "s_year")
    # driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
    Select(driver.find_element(By.ID,"s_year")).select_by_value(dpt_dy) # 출발년
    Select(driver.find_element(By.ID,"s_month")).select_by_value(dpt_dm) # 출발월
    Select(driver.find_element(By.ID,"s_day")).select_by_value(dpt_dd) # 출발일
    # elm_dptTm = driver.find_element(By.ID, "dptTm")
    # driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
    Select(driver.find_element(By.ID, "s_hour")).select_by_visible_text(dpt_tm) # 출발시간

    print("기차를 조회합니다")
    print(f"출발역:{dpt_stn} , 도착역:{arr_stn}\n날짜:{dpt_dy}-{dpt_dm}-{dpt_dd}, 시간: {dpt_tm}시 이후\n{check_from}번~{check_to}번 사이의 기차 중 예약")
    print(f"예약 대기 사용: {want_reserve}")

    # driver.find_element(By.XPATH, "//input[@value='조회하기']").click() # 조회하기 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, "#center > form > div > p > a > img").click()
    driver.implicitly_wait(5)

    ## close all popup windows
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1]) # 첫 번째 팝업 창으로 제어권 옮기기
        driver.close()                                    # 첫 번째 팝업 창 닫기     
        driver.switch_to.window(driver.window_handles[0]) # 첫 번째 팝업 창으로 제어권 옮기기
    time.sleep(1)

    print("\n조회 리스트중에서 아래 시간만 예약")
    for i in range(check_from, check_to+1):
        text_arr_time = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%d]/td[3]" % i).text.replace("\n"," ")
        text_dpt_time = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%d]/td[4]" % i).text.replace("\n"," ")
        print("[%d]: (%s) > (%s)" % (i, text_arr_time, text_dpt_time))
    print()

    if check_only:
        input("Press Enter to continue...")
        return driver
    time.sleep(1)

    is_reserve = None
    while True:
        for i in range(check_from, check_to+1):
            is_reserve = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%d]/td[6]//img" % i).get_attribute("alt")
            if is_reserve == "예약하기":
                driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%d]/td[6]/a[1]/img" % i).click()
                time.sleep(2)
                try:
                    sancheon_popup_iframe = driver.find_element(By.ID, "embeded-modal-traininfo")
                    driver.switch_to.frame(sancheon_popup_iframe)
                    driver.find_element(By.XPATH, "/html/body/div/div[2]/p[3]/a").click()
                    time.sleep(2)
                finally:
                    ## close all alerts
                    while True:
                        try:
                            result = driver.switch_to.alert()
                            result.accept()
                        except:
                            break
                    print("예약 성공")
                    is_booked = True
                    time.sleep(1)
                    break
            else:
                print("잔여석 없음. 다시 검색")

        if not is_booked:
            driver.find_element(By.CSS_SELECTOR, ".btn_inq > a:nth-child(1) > img:nth-child(1)").click()
            time.sleep(randint(2, 4)) #2~4초 랜덤으로 기다리기
        else:
            break

    return driver

if __name__ == "__main__":
    driver = open_brower()
    driver = login(driver, '1041034058', 'han2kdel#')
    search_train(driver, "서울", "대전", "20230926", "18", True, 3, 4) #기차 출발 시간은 반드시 짝수
