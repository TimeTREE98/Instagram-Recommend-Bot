loginIdInput = "//*[@id='loginForm']/div/div[1]/div/label/input"
loginPwInput = "//*[@id='loginForm']/div/div[2]/div/label/input"
firstNoti = "//*[contains(text(),'회원님을 팔로우하거나 사진에 좋아요 또는 댓글을 남기면 바로 알 수 있습니다.')]"
firstNotiBtn = "//*[contains(text(),'나중에 하기')]"
profileImg = "//*[@style='width: 22px; height: 22px;']"
profileBtn = "//*[contains(text(),'프로필')]"
followerBtn = "//*[contains(text(),'팔로워')]"
followerList = "/html/body/div[4]/div/div/div[2]/ul/div"
postCnt = "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span"
followCnt = "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span"
followCnt_un = (
    "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/span/span"
)
followerCnt = "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"
followerCnt_un = (
    "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/span/span"
)
userName = "//*[@id='react-root']/section/main/div/header/section/div[2]/h1"
userInfo = "//*[@id='react-root']/section/main/div/header/section/div[2]/span"
userWebFollow = "//*[@id='react-root']/section/main/div/header/section/div[2]/a"
userStory = "//*[@id='react-root']/section/main/div/div[1]/div/div/div/ul/li[3]/div"
userPostDiv = "//*[@id='react-root']/section/main/div/div[2]/article/div[1]/div/div"
userPostDiv_story = "//*[@id='react-root']/section/main/div/div[3]/article/div/div/div"
suggestUserList = "//*[@id='react-root']/section/main/div/div[2]/div/div/div"
suggestUserFollowBtn1 = (
    "//*[@id='react-root']/section/main/div/div[2]/div/div/div[1]/div[3]/button"
)


def suggestUserName(divCnt):
    return (
        "//*[@id='react-root']/section/main/div/div[2]/div/div/div["
        + str(divCnt)
        + "]/div[2]/div[1]/div/span/a"
    )


def userPost(userType, divCnt):
    divCnt = str(divCnt)
    if userType == "default":
        return (
            "//*[@id='react-root']/section/main/div/div[2]/article/div[1]/div/div["
            + divCnt
            + "]/div"
        )
    elif userType == "story":
        return (
            "//*[@id='react-root']/section/main/div/div[3]/article/div/div/div["
            + divCnt
            + "]/div"
        )


content = "/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]"
contentTime = "/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/div/div/time"
contentNextBack = "/html/body/div[4]/div[1]/div/div/a"
contentClose = "/html/body/div[4]/div[3]/button"