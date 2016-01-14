#input essential info:
#1.server info
#2.user name + user password
#3.initial environment

from urlparse import urlparse
from splinter import Browser
import threading,json,random,re,time


#constant
arrFiled = []
i = 0
while i < 18:
    i = i + 1
    arrFiled.append("http://ts3.travian.com/build.php?id=" + str(i))

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
        'Praetorian' : [100, 130, 160, 70]
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
                print "Current ", arrName[i] ," is ",tempArray[i]
                i = i + 1

            if  tempArray[0] > boostSoldier.Type[0] and tempArray[1] > boostSoldier.Type[1] and tempArray[2] > boostSoldier.Type[2] and tempArray[3] > boostSoldier.Type[3]:
                print "\033[31;1m" + "Good, we have enough resources to boost more soilders \n" + "\033[0m"

                o = urlparse(self.browser.url )
                boostUrl = "http://" + o.netloc + "/build.php?id=32"
                self.browser.visit(boostUrl)

                def soldierChoose(x):
                    switcher = {
                        'legionnaire' : 't1',
                        'Praetorian' : 't2'
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

        print "\033[41;1m",arrFiled[p],"\033[0m"
        urlBuild = arrFiled[p]
        self.browser.visit(urlBuild)

        buildBtn = self.browser.find_by_css('button .button-content')

        if buildBtn:
            buildBtn.click()
            print "\033[31;1m","Push build request to queue","\033[0m"
        else:
            print "\033[31;1m","Still not ready to build","\033[0m"

#    TODO:
#    def stop():


#instance input browserType + which server + username + password
user = init('firefox', 3, 'max.g.laboratory@gmail.com', '1266Mg96')
boostSoldier = boostSoldier(user.browser, "Praetorian")
upgradeField = upgradeField(user.browser)

#run boost soldier or upgradefield
user.establish()
#loop(boostSoldier.reloadPage, boostSoldier.boost, 10, 25)
loop(upgradeField.reloadPage, upgradeField.upgrade, 120, 180)

