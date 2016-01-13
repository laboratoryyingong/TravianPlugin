#input essential info:
#1.server info
#2.user name + user password
#3.initial environment

from urlparse import urlparse
from splinter import Browser
import threading,json,random,re,time


#funciton summary
#strip string and get value
def commonStrip(var):
    var = var.encode()
    p = re.compile("\d+,\d+?")

    for com in p.finditer(var):
        mm = com.group()
        var = var.replace(mm, mm.replace(",", ""))

    var = int(var)

    return var


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

class boostSolider:

    trigger = 1

    #soilderType array is used to describ how many resource to use
    soilderType = {
        'legionnaire' : [120, 100, 150, 30],
        'Praetorian' : [100, 130, 160, 70]
    }

    def __init__(self, browser, chooseType):
        self.browser = browser
        self.chooseType = chooseType
        boostSolider.Type = boostSolider.soilderType[chooseType]

    def check(self):
        if boostSolider.trigger == 1:

            frequency = random.uniform(15, 25)

            print "Attention: after ", frequency, " seconds, browser will refresh page."
            print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
            print "reload page, continue...... \n"

            t = threading.Timer(frequency, self.browser.reload)
            t.start()

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

            if  tempArray[0] > boostSolider.Type[0] and tempArray[1] > boostSolider.Type[1] and tempArray[2] > boostSolider.Type[2] and tempArray[3] > boostSolider.Type[3]:
                print "\033[31;1m" + "Good, we have enough resources to boost more soilders" + "\033[0m"

                o = urlparse(self.browser.url )
                boostUrl = "http://" + o.netloc + "/build.php?id=32"
                self.browser.visit(boostUrl)

                def soliderChoose(x):
                    switcher = {
                        'legionnaire' : 't1',
                        'Praetorian' : 't2'
                    }
                    return switcher.get(x, 'none')

                self.browser.fill(soliderChoose(self.chooseType), '1')
                soldierBtn = self.browser.find_by_id('s1')
                soldierBtn.click()

            else:
                print "\033[33;1m","Sorry, we do not have enough resources, will try after reload","\033[0m"


    def stop():
        boostSolider.trigger = 0

#instance input browserType + which server + username + password
instance1 = init('firefox', 3, 'max.g.laboratory@gmail.com', '1266Mg96')
boostInstance1 = boostSolider(instance1.browser, "legionnaire")

#run
instance1.establish()
boostInstance1.boost()


#threading.Timer(4,instance1.destory).start()
