import requests
import configparser

# simple way to retrieve username and password

config = configparser.ConfigParser()
config.read('./config.ini')
accountDict = config.options('AccountDetails')
email = config.get('AccountDetails','email')
password = config.get('AccountDetails','password')

if (email=='' or password=='' or
    email=='ACCOUNT_EMAIL' or password=='ACCOUNT_PASSWORD'):
    print('Please configure the username and password in config.ini')
    exit(1)


class CraftsmanAccount:
    """Account Token for assurelink session"""

    URL = "https://assurelink.craftsman.com/"
    ASPNET_COOKIE = '.AspNet.ApplicationCookie'
    ASPNET_SESSION_ID = 'ASP.NET_SessionId'

    def __init__(self, email, password):
        # Set the variables for reuse later in renewing token.
        self._email = email
        self._password = password
        self._logged = False
        # Call class method to login into account.
        self.login()


    def login(self):
        # RESTful request for posting account details.
        post_data = {
            'Email'   : self._email,
            'Password': self._password
            }
        # Defining user agent as broswer for better compatibility.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        }
        # Disallow redirects to intercept the returned cookies and validate response code.
        response = requests.post(CraftsmanAccount.URL, json=post_data,
                                 headers=headers, allow_redirects=False)

        print(response)
        print('--------')
        print(response.headers)
        print('--------')
        print(response.cookies)
        print('--------')

        print(response.status_code)
        # These three variabels indicates the success of login process.
        if (response.status_code != 302 or
            CraftsmanAccount.ASPNET_COOKIE not in response.cookies or
            CraftsmanAccount.ASPNET_SESSION_ID not in response.cookies):
            self._logged = False
            raise ValueError("login failed")
        else:
            # Retrieve the needed AspNet cookies and session id.
            self._aspnetCookie = response.cookies[CraftsmanAccount.ASPNET_COOKIE]
            self._aspnetSessionId = response.cookies[CraftsmanAccount.ASPNET_SESSION_ID]

    def renewToken(self):
        self.login()

    @property
    def logged(self):
        return self._logged

    @property
    def aspnetCookie(self):
        return self._aspnetCookie

    @property
    def aspnetSessionId(self):
        return  self._aspnetSessionId


class garageOpener:
    def __init__(self, openerStatus):
        self.gatewayId = openerStatus['GatewayId']
        self.location = openerStatus['Gateway']


def getDevices(account):
    url = 'https://assurelink.craftsman.com/api/MyQDevices/GetAllDevices?brandName=Craftsman'
    headers = {
        'Cookie' : '{0}={1};{2}={3}'.format(account.ASPNET_COOKIE,
                                            account.aspnetCookie,
                                            account.ASPNET_SESSION_ID,
                                            account.aspnetSessionId)
    }

    print('=======')
    print(headers)
    print('=======')


    response = requests.get(url, headers=headers, allow_redirects=True)
    #
    print(response)
    print('--------')
    print(response.headers)
    print('--------')
    print(response.cookies)
    print('--------')
    print(response.text)





a = CraftsmanAccount(email, password)
getDevices(a)
exit()






print(response.cookies[ASPNET_COOKIE])
print(response.cookies[ASPNET_SESSION_ID])

aspnetCookie = response.cookies[ASPNET_COOKIE]
aspnetSessionId = response.cookies[ASPNET_SESSION_ID]

headers = {
    'Cookie' : '{0}={1};{2}={3}'.format(ASPNET_COOKIE, aspnetCookie, ASPNET_SESSION_ID, aspnetSessionId)
}

print('=======')
print(headers)
print('=======')


response = requests.get(url, headers=headers, allow_redirects=True)
#
print(response)
print('--------')
print(response.headers)
print('--------')
print(response.cookies)
print('--------')
print(response.text)
# import urllib
# import urllib2
# # import json
# import re
# import ssl
#
#
# # monkey patching..............
# ssl._create_default_https_context = ssl._create_unverified_context
#
# # global var for storing cookies
# global cookies
#
# # custom catcher for headers
# class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
#     def http_error_302(self, req, fp, code, msg, headers):
#         global cookies
#         cookies = headers['set-cookie']
#         return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
#     http_error_301 = http_error_303 = http_error_307 = http_error_302
# cookieprocessor = urllib2.HTTPCookieProcessor()
# opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
# urllib2.install_opener(opener)
#
# # user variables
# post_data = {
#     'Email': USER_EMAIL,
#     'Password': USER_PASSWD
#     }
# data = urllib.urlencode(post_data)
# headers = {
#     # 'Content-Type': "application/x-www-form-urlencoded",
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
# }
# url = "https://assurelink.craftsman.com/"
# # request
# req = urllib2.Request(url, data, headers)
# response = urllib2.urlopen(req)
# # response = urllib2.urlopen(url + '?' + data +)
#
# # retrieve required cookies headers
# match = re.search('(ASP.NET_SessionId=).+?;', cookies)
# sessionId = match.group(0)
#
# match = re.search('(.AspNet.ApplicationCookie=).+?;', cookies)
# appCookie = match.group(0)
#
# print(sessionId)
# print(appCookie)
