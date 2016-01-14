#input essential info:
#1.server info
#2.user name + user password
#3.initial environment

from urlparse import urlparse
from splinter import Browser
import threading,json,random,re,time


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

    t = threading.Timer(frequency, loop(func1, func2, minloop, maxloop))
    t.start()


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

#class upgradeField:



#instance input browserType + which server + username + password
instance1 = init('firefox', 3, 'max.g.laboratory@gmail.com', '1266Mg96')
boostInstance1 = boostSoldier(instance1.browser, "Praetorian")

#run
instance1.establish()
loop(boostInstance1.reloadPage,boostInstance1.boost,10,25)

#threading.Timer(4,instance1.destory).start()


