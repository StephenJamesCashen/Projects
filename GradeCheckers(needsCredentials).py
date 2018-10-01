from twill import get_browser#For Webbrowsing
from twill.commands import * #For Webbrowsing
from bs4 import BeautifulSoup #For HTML Parsing
import twill #For Webbrowsing
import time #for wainting period
from slackclient import SlackClient
token = [Slack-Api-Token]
sc = SlackClient(token)
b = get_browser()
Period=30 #minutes
list=[]
while(True):
    clear_cookies()
    b.go("https://ssc.adm.ubc.ca/sscportal/servlets/SRVAcademicRecord?context=html")
    formvalue(2,"username","UBC CWL username")
    formvalue(2,"password","UBC CWL Password")
    submit() # We just logged in
    class DevNull(object):
        def write(self, str):
            pass
            twill.set_output(DevNull()) #Cleaner Log
    html = show()

    bs=BeautifulSoup
    soup=bs(html, 'html.parser')
    table=soup.find(id="allSessionsGrades")
    tlist=[]

    for row in table.find_all('tr')[1:7]:
        tlist.append(row.find_all('td')[2].get_text())
    plist = ["Phys 328: %s" %tlist[0],"Phys 305: %s" %tlist[1],"Phys 215: %s" %tlist[2],"Math 317: %s" %tlist[3],"Math 307: %s" %tlist[4],"Math 225: %s" %tlist[5]]

    if bool(set(list).intersection(tlist))!=True:
        print "You're grades have changed since I last checked, you're new grades are %s" %tlist
        sc.api_call('chat.postMessage', channel="#notifications",
                        text="You're grades have changed since I last checked, you're new grades are %s" %plist, username='My Sweet Bot',
                        icon_emoji=':robot_face:')
    if bool(set(list).intersection(tlist)):
        print "You're grades have not changed :("
    #    sc.api_call('chat.postMessage', channel="#notifications",
    #                    text="You're grades have not changed :(", username='My Sweet Bot',
    #                    icon_emoji=':robot_face:')
    list=tlist
    time.sleep(Period*60)
