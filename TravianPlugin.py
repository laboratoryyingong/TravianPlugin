#input essential info:
#1.server info
#2.user name + user password
#3.initial environment

from urlparse import urlparse
from splinter import Browser
import threading,json,random,re,time,getpass


#constant
arrFiled = []
i = 0
while i < 18:
    i = i + 1
    arrFiled.append("http://ts3.travian.com/build.php?id=" + str(i))

userInfo = []

#funciton summary
def commonStrip(var):
    var = var.encode()
    p = re.compile("\d+,\d+?")

    for com in p.finditer(var):
        mm = com.group()
        var = var.replace(mm, mm.replace(",", ""))

    var = int(var)

    return var


def loop(func1, func2, minloop, maxloop):
    frequency = random.uniform(minloop, maxloop)

    print "\033[34;1m" + "Attention: after ", frequency, " seconds, browser will refresh page." + "\033[0m"
    print "\033[35;1m" + time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())) + "\033[0m"
    print "\033[36;1m" + "reload page, continue...... \n" + "\033[0m"

    func1()
    func2()

    time.sleep(frequency)
    loop(func1, func2, minloop, maxloop)

#menu driven interface

def getChoice():
    print "\033[1;32;41;1m" + "\nWelcome to MAD MAX World" + "\n(I)nput your account + password" + "\n(S)tart new game" + "\n(U)pgrade your field" + "\n(B)oost your soldier" + "\n(Q)uit" + "\033[0m"
    choose = raw_input(">>> ")
    choice = choose.lower()

    return choice

def info():

    global userInfo

    print "\033[35;1m" + "Please input your account: " + "\033[0m"
    accountName = raw_input()
    print "\033[35;1m" + "Please input your password: " + "\033[0m"
    accountPassword = getpass.getpass()
    print "\033[35;1m" + "Please input your server number: " + "\033[0m"
    accoutServerNum = raw_input()

    userInfo.append('firefox')
    userInfo.append(accoutServerNum)
    userInfo.append(accountName)
    userInfo.append(accountPassword)

    print "\033[1;32;41;1m" + "Have collected your info, please choose what to do: " + "\033[0m"

def openBrowser():
    global user

    user = init(userInfo[0], userInfo[1], userInfo[2], userInfo[3])
    print "\033[36;1m" + "We will start game for you" + "\033[0m"


def boost():
    global boostSoldier,user

    print "\033[36;1m" + "Which solider you want to boost: ('legionnaire' or 'Praetorian')" + "\033[0m"
    soliderName = raw_input()

    user = init(userInfo[0], userInfo[1], userInfo[2], userInfo[3])
    user.establish()
    boostSoldier = boostSoldier(user.browser, soliderName)
    loop(boostSoldier.reloadPage, boostSoldier.boost, 15, 25)


def upgrade():
    global upgradeField,user

    print "\033[36;1m" + "You want to upgrade your field? " + "\033[0m"

    user = init(userInfo[0], userInfo[1], userInfo[2], userInfo[3])
    user.establish()
    upgradeField = upgradeField(user.browser)
    loop(upgradeField.reloadPage, upgradeField.upgrade, 60, 80)


#main class
class init:

    loginUserCounter = 0

    def __init__(self, browserType, serverNum, username, password):
        self.browserType = browserType
        self.serverNum = serverNum
        self.username = username
        self.password = password
        init.browser = Browser(browserType)
        init.loginUserCounter += 1

    def establish(self):
        url = 'http://ts' + str(self.serverNum) + '.travian.com/'

        #open browser and into game
        init.browser.visit(url)

        #fill username and password
        init.browser.fill('name',self.username)
        init.browser.fill('password',self.password)

        btnLogin = init.browser.find_by_name('s1')
        btnLogin.click()

    def destory(self):
        window = init.browser.windows[0]

        if window.title == 'Travian com3':
            window.close()
        else:
            window = window.next

class boostSoldier:

    trigger = 1

    #soldierType is used to describ how many resource to use
    soldierType = {
        'legionnaire' : [120, 100, 150, 30],
        'Praetorian' : [100, 130, 160, 70],
        'Imperian' : [150, 160, 210, 80]
    }

    def __init__(self, browser, chooseType):
        self.browser = browser
        self.chooseType = chooseType
        boostSoldier.Type = boostSoldier.soldierType[chooseType]

    def reloadPage(self):
        if boostSoldier.trigger == 1:
            self.browser.reload()

        else:
            print "Boost process has been stopped!"

    def boost(self):

            tempArray = []
            arrName = ['Lumber','Clay','Iron','Crop']
            i = 0

            lumber = self.browser.find_by_id('l1').value
            clay = self.browser.find_by_id('l2').value
            iron = self.browser.find_by_id('l3').value
            crop = self.browser.find_by_id('l4').value

            #strip and prepare all data
            lumber = commonStrip(lumber)
            clay = commonStrip(clay)
            iron = commonStrip(iron)
            crop = commonStrip(crop)

            tempArray.append(lumber)
            tempArray.append(clay)
            tempArray.append(iron)
            tempArray.append(crop)

            #output all essential data
            while i < 4:
                print "Current " + arrName[i] + " is " + str(tempArray[i])
                i = i + 1

            if  tempArray[0] > boostSoldier.Type[0] and tempArray[1] > boostSoldier.Type[1] and tempArray[2] > boostSoldier.Type[2] and tempArray[3] > boostSoldier.Type[3]:
                print "\033[31;1m" + "Good, we have enough resources to boost more soilders \n" + "\033[0m"

                o = urlparse(self.browser.url )
                boostUrl = "http://" + o.netloc + "/build.php?id=32"
                self.browser.visit(boostUrl)

                def soldierChoose(x):
                    switcher = {
                        'legionnaire' : 't1',
                        'Praetorian' : 't2',
                        'Imperian' : 't3'
                    }
                    return switcher.get(x, 'none')

                self.browser.fill(soldierChoose(self.chooseType), '1')
                soldierBtn = self.browser.find_by_id('s1')
                soldierBtn.click()

            else:
                print "\033[33;1m" + "Sorry, we do not have enough resources, will try after reload \n" + "\033[0m"


    def stop():
        boostSoldier.trigger = 0

class upgradeField:

    position = 0

    def __init__(self, browser):
        self.browser = browser

    def reloadPage(self):
        self.browser.reload()

    def upgrade(self):
        p = upgradeField.position % 18
        upgradeField.position += 1

        print "\033[41;1m" + arrFiled[p] + "\033[0m"
        urlBuild = arrFiled[p]
        self.browser.visit(urlBuild)

        buildBtn = self.browser.find_by_css('.green .build')

        if buildBtn:
            buildBtn.click()
            print "\033[31;1m" + "Push build request to queue" + "\033[0m"
        else:
            print "\033[31;1m" + "Still not ready to build" + "\033[0m"

#    TODO:
#    def stop():


#run
choice = getChoice()

while choice != "q":
    if choice == "i":
        info()
    elif choice == "s":
        openBrowser()
    elif choice == "u":
        upgrade()
    elif choice == "b":
        boost()
    else:
        print("Invalid choice, please choose again")
        print("\n")

    choice = getChoice()
