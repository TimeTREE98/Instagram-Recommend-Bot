import os
import re
import time
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element as elem


def getNumber(val):
    if "천" in val:
        return int(float(val[:-1])) * 1000
    elif "백만" in val:
        return int(float(val[:-2])) * 1000000
    elif "십만" in val:
        return int(float(val[:-2])) * 100000
    elif "만" in val:
        return int(float(val[:-1])) * 10000
    ## 그 이상 조건 추가 필요
    else:
        val = int(val.replace(",", ""))
        return val


class instagramBot:
    def __init__(self):  # Auth, Keyword, Driver Setting
        self.myId = ""
        self.myPw = ""
        self.log = True
        if not os.path.isfile("./myKeywords"):
            raise Exception("myKeywords 파일 미 존재")
        myKeywordFile = open("./myKeywords", "r")
        self.myKeywords = list(map(lambda x: x[:-1], myKeywordFile.readlines()))
        myKeywordFile.close()
        # Debug Chrome 실행 필요
        # WIN :
        # MAC : /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=".chrome_debug"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not sock.connect_ex(("127.0.0.1", 9222)) == 0:
            raise Exception("Chrome 미 실행")
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        options.add_argument("User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        driver = webdriver.Chrome("./chromedriver", options=options)  # Browser Runf
        driver.set_window_position(0, 0)  # Browser Position Setting
        driver.set_window_size(1020, 1100)  # Browser Size Setting
        self.driver = driver

    def waitForFind(self, elemType, elemPath, waitTime):
        startTime = time.time()
        try:
            elem = False
            if elemType == "xpath":
                elem = WebDriverWait(self.driver, waitTime).until(EC.presence_of_element_located((By.XPATH, elemPath)))
        finally:
            if self.log:
                print("요소 탐색", end=" | ")
                print("걸린 시간 : ", time.time() - startTime, end=" | ")
                print("요소 : ", elemPath)
            return elem

    def loginChk(self):  # Login Check
        startTime = time.time()
        self.driver.get("https://www.instagram.com/accounts/login/")
        loginStatus = self.waitForFind("xpath", elem.loginIdInput, 3)
        if self.log:
            print("로그인 검증", end=" | ")
            print("걸린 시간 : ", time.time() - startTime)
        if loginStatus:
            return False  # is Logout
        else:
            return True  # is Login

    def login(self):  # Login
        startTime = time.time()
        loginIdInput = self.waitForFind("xpath", elem.loginIdInput, 3)
        loginIdInput.send_keys(self.myId)
        loginPwInput = self.waitForFind("xpath", elem.loginPwInput, 3)
        loginPwInput.send_keys(self.myPw)
        loginPwInput.send_keys(Keys.RETURN)
        if self.waitForFind("xpath", elem.firstNoti, 7):
            self.waitForFind("xpath", elem.firstNotiBtn, 3).click()
        self.waitForFind("xpath", elem.profileImg, 3).click()
        self.waitForFind("xpath", elem.profileBtn, 3).click()
        if self.log:
            print("로그인 시도", end=" | ")
            print("걸린 시간 : ", time.time() - startTime)

    def getUserInfo(self, getType, userId):
        startTime = time.time()
        userType = self.waitForFind("xpath", elem.PrivateMsg, 2)  # False 일 경우, Follow, Follower 버튼 a 태그 미 존재
        if getType == "move":  # URL 처리 해야되는 작업
            self.driver.get("https://www.instagram.com/" + userId)
        intro = self.waitForFind("xpath", elem.userInfo, 5) and self.waitForFind("xpath", elem.userInfo, 5).text or ""  # User Intro
        postCnt = getNumber(self.waitForFind("xpath", elem.postCnt, 3).text)  # 게시물 개수
        if self.waitForFind("xpath", elem.followCnt, 3):
            followCnt = getNumber(self.waitForFind("xpath", elem.followCnt, 3).text)
            followerCnt = getNumber(self.waitForFind("xpath", elem.followerCnt, 3).text)
        else:
            followCnt = getNumber(self.waitForFind("xpath", elem.followCnt_un, 3).text)
            followerCnt = getNumber(self.waitForFind("xpath", elem.followerCnt_un, 3).text)
        return {
            "intro": intro,
            "postCnt": postCnt,
            "followCnt": followCnt,
            "followerCnt": followerCnt,
        }

    def start(self):
        if not self.loginChk():
            self.login()


try:
    Bot = instagramBot()
    Bot.start()
except Exception as e:
    print(e)


"""

try:
    driver.get("https://www.instagram.com/explore/people/suggested/")
    waitForFind("xpath", elem.suggestUserFollowBtn1, 3)
    for i in range(3):
        suggestUsers = waitForFind("xpaths", elem.suggestUserList, 3)
        driver.execute_script("arguments[0].scrollIntoView(true);", suggestUsers[-1])
        time.sleep(3)
    suggestUserList = []
    suggestUsers = waitForFind("xpaths", elem.suggestUserList, 3)
    suggestUsers = list(map(lambda x: x.text.split("\n")[0], suggestUsers))
    for idx, userId in enumerate(suggestUsers):
        totalScore = 0
        postScore = 0
        followScore = 0
        keywordScore = 0
        driver.get("https://www.instagram.com/" + userId)
        userInfo = getUserInfo()
        postCnt = userInfo["postCnt"]
        if postCnt > 50:
            postScore += 0.3
        elif postCnt > 30:
            postScore += 0.2
        elif postCnt > 10:
            postScore += 0.1
        followRatio = userInfo["followCnt"] / userInfo["followerCnt"]
        if followRatio > 1:  # 팔로우, 팔로워 비율에 따른 점수 부여
            followScore += 1
        elif followRatio > 0.8:
            followScore += 0.6
        elif followRatio > 0.6:
            followScore += 0.4
        intro = userInfo["intro"].lower()
        for keyword in myKeywords:  # 내 키워드에 따른 점수 부여
            if keyword in intro:
                keywordScore += 2
                break
        totalScore = postScore + followScore + keywordScore
        print("-" * 30)
        print(userId)
        print("   postScore : ", postScore, end=" | ")
        print("followScore : ", followScore, end=" | ")
        print("keywordScore : ", keywordScore)
        print("  totalScore : ", totalScore)
        if totalScore > 3:
            suggestUserList.append(userId)
            print("'" + userId + "' 이 유저를 추천합니다!")
        elif totalScore > 2.6:
            print("이 유저도 고려해보세요!")
        elif totalScore > 2:
            print("음... 한번 봐도 나쁘지 않을 것 같아요!")
    print("추천 유저는 아래와 같아요!")
    for u in suggestUserList:
        print(u, end=", ")
    print("-" * 30)
except Exception as e:
    print(e)
 """
