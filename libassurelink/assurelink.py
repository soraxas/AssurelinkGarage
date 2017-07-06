import requests
import configparser

from const import AssurelinkURL, AspNet

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
        response = requests.post(AssurelinkURL.BASE.value, json=post_data,
                                 headers=headers, allow_redirects=False)

        # These three variabels indicates the success of login process.
        if (response.status_code != 302 or
            AspNet.ASPNET_COOKIE.value not in response.cookies or
            AspNet.ASPNET_SESSION_ID.value not in response.cookies):
            self._logged = False
            raise ValueError("login failed")
        else:
            # Retrieve the needed AspNet cookies and session id.
            self._aspnetCookie = response.cookies[AspNet.ASPNET_COOKIE.value]
            self._aspnetSessionId = response.cookies[AspNet.ASPNET_SESSION_ID.value]
            self._logged = True

    def renewToken(self):
        self._logged = False
        self.login()

    def getCookieHeader(self):
        header = {
            'Cookie' : '{0}={1};{2}={3}'.format(AspNet.ASPNET_COOKIE.value,
                                                self.aspnetCookie,
                                                AspNet.ASPNET_SESSION_ID.value,
                                                self.aspnetSessionId)
        }
        return header

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

    def __init__(self, openerStatus, accountToken):
        self._accountToken = accountToken

        self._name                 = openerStatus['Name'] # "Garage Opener"
        self._gatewayId            = openerStatus['GatewayId'] # 32734230
        self._deviceId             = openerStatus['MyQDeviceId'] # 32734231
        self._gatewayLocation      = openerStatus['Gateway'] # "Hornsby"
        self._deviceTypeId         = openerStatus['DeviceTypeId'] # 17
        self._imagesource          = openerStatus['Imagesource'] # "icon_door_2.png"
        self._statesince           = openerStatus['Statesince'] # 1499322848545
        self._displayStatesince    = openerStatus['DisplayStatesince'] # "Closed for 7 minutes"
        self._lastUpdatedDateTime  = openerStatus['LastUpdatedDateTime'] # "2017-07-06T06:34:08.5450000Z"
        self._state                = openerStatus['State'] # "2"
        self._monitorOnly          = openerStatus['MonitorOnly'] # false
        self._lowBattery           = openerStatus['LowBattery'] # false
        self._sensorError          = openerStatus['SensorError'] # false
        self._openError            = openerStatus['OpenError'] # false
        self._closeError           = openerStatus['CloseError'] # false
        self._disableControl       = openerStatus['DisableControl'] # false
        self._stateName            = openerStatus['StateName'] # "Closed"
        self._toggleAttributeName  = openerStatus['ToggleAttributeName'] # "desireddoorstate"
        self._toggleAttributeValue = openerStatus['ToggleAttributeValue'] # "1"}]
        self._error                = openerStatus['Error'] # false
        self._errorStatus          = openerStatus['ErrorStatus'] # null
        self._errorMessage         = openerStatus['ErrorMessage'] # null
        # self._name                 : openerStatus['Name'] # "Garage Opener"
        # self._gatewayId            : openerStatus['GatewayId'] # 32734230
        # self._deviceId             : openerStatus['MyQDeviceId'] # 32734231
        # self._gatewayLocation      : openerStatus['Gateway'] # "Hornsby"
        # self._deviceTypeId         : openerStatus['DeviceTypeId'] # 17
        # self._imagesource          : openerStatus['Imagesource'] # "icon_door_2.png"
        # self._statesince           : openerStatus['Statesince'] # 1499322848545
        # self._displayStatesince    : openerStatus['DisplayStatesince'] # "Closed for 7 minutes"
        # self._lastUpdatedDateTime  : openerStatus['LastUpdatedDateTime'] # "2017-07-06T06:34:08.5450000Z"
        # self._state                : openerStatus['State'] # "2"
        # self._monitorOnly          : openerStatus['MonitorOnly'] # false
        # self._lowBattery           : openerStatus['LowBattery'] # false
        # self._sensorError          : openerStatus['SensorError'] # false
        # self._openError            : openerStatus['OpenError'] # false
        # self._closeError           : openerStatus['CloseError'] # false
        # self._disableControl       : openerStatus['DisableControl'] # false
        # self._stateName            : openerStatus['StateName'] # "Closed"
        # self._toggleAttributeName  : openerStatus['ToggleAttributeName'] # "desireddoorstate"
        # self._toggleAttributeValue : openerStatus['ToggleAttributeValue'] # "1"}]
        # self._error                : openerStatus['Error'] # false
        # self._errorStatus          : openerStatus['ErrorStatus'] # null
        # self._errorMessage         : openerStatus['ErrorMessage'] # null

    def getStatus(self):
        url = AssurelinkURL.BASE.value + AssurelinkURL.GET_DEVICE.value
        headers = self.accountToken.getCookieHeader()
        payload = {
            'brandName'    : 'Craftsman',
            'SerialNumber' : self.deviceId
        }
        responses = requests.post(url, headers=headers, params=payload)
        return responses

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._gatewayLocation

    @property
    def deviceId(self):
        return  self._deviceId

    @property
    def accountToken(self):
        return  self._accountToken



def getDevices(accountToken):
    url = AssurelinkURL.BASE.value + AssurelinkURL.GET_ALL_DEVICES.value
    headers = accountToken.getCookieHeader()
    payload = {
        'brandName' : 'Craftsman'
    }
    responses = requests.get(url, headers=headers, params=payload)
    openers = []
    for r in responses.json():
        openers.append(garageOpener(r, accountToken))
    return openers





acc = CraftsmanAccount(email, password)
print(acc)

openers = getDevices(acc)

print(openers)

for device in openers:
    print('----')
    print(device.name)
    print(device.location)
    print(device.deviceId)
    print(device.getStatus())
    print(device.getStatus().text)


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
