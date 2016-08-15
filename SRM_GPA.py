import os
import urllib2 as ul
from bs4 import BeautifulSoup as bs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import getpass

grades = {"A+":10,"A":9.5,"A-":9,"B+":8.5,"B":8,"B-":7.5,"C+":7,"C":6.5,"C-":6,"D+":5.5,"D":5,"D-":4.5,"E":4,"S":10,"U":0,"W":0,"I":0}
username = raw_input('Email address you wish to use to mail the marksheet:\t')#'abc@gmail.com'
password = getpass.getpass('Enter the passwd (hidden):\t')
smtpObj = smtplib.SMTP('smtp.gmail.com:587')
smtpObj.starttls()
smtpObj.login(username,password)

receivers = ""

def sendMail(source,gpa):
    
    sender = 'abc@gmail.com'
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Your GPA is "+str(gpa)
        msg['From'] = sender
        msg['To'] = receivers

        
        text = "Your GPA is"+str(gpa)
        html = source


        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        smtpObj.sendmail(sender, receivers, msg.as_string())
        print "Successfully sent email"
    except Exception as e:
        print e

def getSource(url):
    opener = ul.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    source = opener.open(url)
    return source

def getUserMarks(source):
    
    soup = bs(source)
    sukh = soup
    marksTable = soup.findAll('table',{'id':'table1'})[0]
    soup = bs(str(marksTable))
    rows = soup.findAll('tr')
    rows.pop(0)
    values = []
    values.append(userID)
    total = 0
    totalcredit = 0
    temp = ""

    
    for row in rows:
        eachRow = bs(str(row),'html.parser')
        subject = eachRow.findAll('td')[3]
        subject = subject.text.replace(" ","_");
        credit = eachRow.findAll('td')[4]
        grade = eachRow.findAll('td')[8]
        totalcredit = totalcredit + int(credit.text)
        total = total + ( float(grades[grade.text]) * int(credit.text))
        temp = subject+"_"+str(float(grades[grade.text]))+","+str(credit.text)
        values.append(str(temp))
    gpa = total/totalcredit
    for tag in sukh.find_all('table')[0]:
        tag.replaceWith('')
    sukh = str(sukh)
    sendMail(sukh,gpa)
    values.append(str(gpa))

 
    print "Your GPA is %s"%str(gpa)

while 1:
    key = raw_input('Enter the Mail ID:\t')
    value = raw_input('Enter the Uni ID:\t')
    users = {key:value}
    for key, value in users.iteritems():
        userID = str(value)
        receivers = str(key)
        print userID
        print receivers 
        url = "http://evarsity.srmuniv.ac.in/srmwebonline/exam/onlineResultInner.jsp?registerno="+userID+"&frmdate='or''='&iden=1"
        source = getSource(url)
        getUserMarks(source)
    users.clear()
smtpObj.quit()