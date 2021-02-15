import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import elem

accountId = ""
accountPw = ""
myKeywords = []

options = Options()
# MAC : /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/.chrome_debug"
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument(
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
)
driver = webdriver.Chrome("./chromedriver", options=options)  # driver Setting
driver.set_window_position(0, 0)  # Browser Position Setting
driver.set_window_size(1020, 1000)  # Browser Size Setting


def waitForFind(elemType, elemVal, waitTime):  # Wait for Elem find
    findStatus = True
    startTime = time.time()
    loadingWaitTime = waitTime  # wait time Setting
    while findStatus:
        if time.time() - startTime > loadingWaitTime:
            break
        try:
            if elemType == "xpath":
                findElem = driver.find_element_by_xpath(elemVal)
            if elemType == "xpaths":
                findElem = driver.find_elements_by_xpath(elemVal)
            if elemType == "css":
                findElem = driver.find_element_by_css_selector(elemVal)
            findStatus = False  # elem Find Success
        except:
            findStatus = True  # elem Find Fail
    if not findStatus:  # True > Find Fail, False > Find Success
        # print("소요시간 : ", time.time() - startTime)
        return findElem
    else:
        return False


def loginChk():  # Login Check
    driver.get("https://www.instagram.com/accounts/login/")
    if waitForFind("xpath", elem.loginIdInput, 5):
        return False  # Logout Status
    else:
        return True  # Login Status


def login():  # Login Process
    driver.get("https://www.instagram.com/")
    loginIdInput = waitForFind("xpath", elem.loginIdInput, 5)
    loginIdInput.send_keys(accountId)
    loginPwInput = waitForFind("xpath", elem.loginPwInput, 5)
    loginPwInput.send_keys(accountPw)
    loginPwInput.send_keys(Keys.RETURN)
    if waitForFind("xpath", elem.firstNoti, 5):
        waitForFind("xpath", elem.firstNotiBtn, 5).click()
    waitForFind("xpath", elem.profileImg, 3).click()
    waitForFind("xpath", elem.profileBtn, 3).click()


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


def getUserInfo():
    intro = (
        waitForFind("xpath", elem.userInfo, 5)
        and waitForFind("xpath", elem.userInfo, 5).text
        or ""
    )  # User Intro
    postCnt = getNumber(waitForFind("xpath", elem.postCnt, 3).text)  # 게시물 개수
    if waitForFind("xpath", elem.followCnt, 3):
        followCnt = getNumber(waitForFind("xpath", elem.followCnt, 3).text)
        print(waitForFind("xpath", elem.followerCnt, 3).text)
        followerCnt = getNumber(waitForFind("xpath", elem.followerCnt, 3).text)
    else:
        followCnt = getNumber(waitForFind("xpath", elem.followCnt_un, 3).text)
        followerCnt = getNumber(waitForFind("xpath", elem.followerCnt_un, 3).text)
    return {
        "intro": intro,
        "postCnt": postCnt,
        "followCnt": followCnt,
        "followerCnt": followerCnt,
    }


try:
    startTime = time.time()
    loginStatus = loginChk()
    if not loginStatus:
        print("로그인 실시")
        login()
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