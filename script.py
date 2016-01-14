from splinter import Browser
import threading,json,random,re,time

#open web browser + start travian
browser = Browser('firefox')
url = "http://ts3.travian.com/"
browser.visit(url)

#fill my name and password
browser.fill('name','max.g.laboratory@gmail.com')
browser.fill('password','1266Mg96')

btnLogin = browser.find_by_name('s1')
btnLogin.click()


#filed address
arrFiled = []
i = 0
j = 0
x = 0
z = 0
while i < 18:
    i = i + 1
    arrFiled.append("http://ts3.travian.com/build.php?id=" + str(i))

#judge which page we stay
#flag = browser.find_by_id('n2')
#flag.click

#enter into solider produce
#url2 = "http://ts3.travian.com/build.php?id=32"
#browser.visit(url2)

#change color
#print "\033[1;5;33;44;4mHello, world\033[0m"

#strip string and get value
def commonStrip(var):
    var = var.encode()
    p = re.compile("\d+,\d+?")

    for com in p.finditer(var):
        mm = com.group()
        var = var.replace(mm, mm.replace(",", ""))

    var = int(var)

    return var

def boostSoldier():
    arr = []
    arrName = ['Lumber','Clay','Iron','Crop']
    i = 0

    lumber = browser.find_by_id('l1').value
    clay = browser.find_by_id('l2').value
    iron = browser.find_by_id('l3').value
    crop = browser.find_by_id('l4').value

#strip and prepare all data
    lumber = commonStrip(lumber)
    clay = commonStrip(clay)
    iron = commonStrip(iron)
    crop = commonStrip(crop)

    arr.append(lumber)
    arr.append(clay)
    arr.append(iron)
    arr.append(crop)

#output all essential data
    while i < 4:
        print "Current ", arrName[i] ," is ",arr[i]
        i = i + 1

    return arr


def reloadPage():
    global z

    browser.reload()
    print "reload page, continue...... \n"

    p = z % 18
    z = z + 1

    print "\033[41;1m",arrFiled[p],"\033[0m"
    urlBuild = arrFiled[p]
    browser.visit(urlBuild)

    buildBtn = browser.find_by_css('button .button-content')

    if buildBtn:
        buildBtn.click()
    else:
        print "\033[31;1m","Still not ready to build","\033[0m"




#boost solider script
    arrResource = boostSoldier()
    if  arrResource[0] > 120 and arrResource[1] > 130 and arrResource[2] > 160 and arrResource[3] > 70:
        print "\033[31;1m","Good, we have enough resources to boost more soilders","\033[0m"
        browser.fill('t2', '1')
        soldierBtn = browser.find_by_id('s1')
        soldierBtn.click()

    else:
        print "\033[33;1m","Sorry, we do not have enough resources, will try after reload","\033[0m"

#random create frequency second 1s--8s
    frequency = random.uniform(15, 25)

    print "After ", frequency, "seconds, we will refresh page."
    print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))

    t = threading.Timer(frequency, reloadPage)
    t.start()

threading.Timer(4,reloadPage).start()


