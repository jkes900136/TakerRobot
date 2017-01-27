import urllib2
#import time
import math
from HTMLParser import HTMLParser

totalnum=0
pagenum=0
inloop=0
serialnum=[]
prodnum=[]
shelfid=[]
row=[]
col=[]
#links = []
reserved=[]
class MyHTMLParser(HTMLParser):           
   
    def handle_data(self, data):      
        global inloop
        if self.lasttag == 'h3' and data.strip():
            global totalnum
            global pagenum
            totalnum=int(data)
            pagenum= math.ceil((totalnum/5))     
            self.links.append(data)
            
        if self.lasttag == 'td' and data.strip():
            
            if inloop>=0 and inloop<8:
                if inloop == 0:
                    self.links.append(data)
                if inloop == 1:                   
                    self.links.append(data)
                if inloop == 3:                    
                    self.links.append(data)
                if inloop == 4:
                    
                    self.links.append(data)
                if inloop == 5:                   
                    self.links.append(data)
                if inloop == 6:                   
                    self.links.append(data)
                #print inloop,    
                #print data,
                inloop+=1
            else:                
                inloop=0
#            
            
def extract(url):            
      
    try:
        f = urllib2.urlopen(url)
        html = f.read()
        f.close()
    except urllib2.HTTPError as e:
        print(e, 'while fetching', url)
        return
   # url = "http://isla.shu.edu.tw:8066/gt2016/TakerRobot/nShop/listforbot.php?action=reserved"
    #content = urllib2.urlopen(url).read() 
    parser = MyHTMLParser()
    parser.links = []
    parser.feed(html)
    return parser.links
       
#shipping=extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/nShop/listforbot.php?action=shipping")
#
#reserved=extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/nShop/listforbot.php?action=reserved")
#
#for l in reserved:
#        print(l),
    
