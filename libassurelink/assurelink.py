"""Assurelink Craftsman Garage Opene library."""

# pylint: disable=useless-super-delegation

import requests
from .const import AssurelinkURL, AspNet, RequestDoorState


class CraftsmanAccount:
    """Account Token for assurelink session"""

    def __init__(self, email, password):
        """Create an Assurelink account Token

        :param email: user email for login
        :param password: user password for login
        """
        self._email = email
        self._password = password
        self._logged = False
        # Call class method to login into account.
        self.login()

    def login(self):
        """RESTful request for posting account details."""

        post_data = {
            'Email'   : self._email,
            'Password': self._password
            }
        # Defining user agent as broswer for better compatibility.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        }
        response = requests.post(AssurelinkURL.BASE.value, json=post_data,
                                 headers=headers, allow_redirects=False)
        # These three variabels indicates the success of login process.
        if (response.status_code != 302 or
                AspNet.ASPNET_COOKIE.value not in response.cookies or
                AspNet.ASPNET_SESSION_ID.value not in response.cookies):
            self._logged = False
        else:
            # Retrieve the needed AspNet cookies and session id.
            self._aspnet_cookie = response.cookies[AspNet.ASPNET_COOKIE.value]
            self._aspnet_session_id = response.cookies[AspNet.ASPNET_SESSION_ID.value]
            self._logged = True
        return self.logged

    def renew_token(self):
        """Renew the cookies token."""

        self._logged = False
        return self.login()

    def get_cookie_header(self):
        """Return the formatted headers with the cookie and session ID."""
        header = {
            'Cookie' : '{0}={1};{2}={3}'.format(AspNet.ASPNET_COOKIE.value,
                                                self.aspnet_cookie,
                                                AspNet.ASPNET_SESSION_ID.value,
                                                self.aspnet_session_id)
        }
        return header

    def get_devices(self):
        """Method to return a list of devices associated to the account.

        param account_token: account token of the account after login."""

        if not self.logged:
            raise AssurelinknNotLoggedException()

        url = AssurelinkURL.BASE.value + AssurelinkURL.GET_ALL_DEVICES.value
        headers = self.get_cookie_header()
        payload = {
            'brandName' : 'Craftsman'
        }
        responses = requests.get(url, headers=headers, params=payload)
        openers = []
        for response in responses.json():
            openers.append(GarageOpener(response, self))
        return openers

    def __repr__(self):
        return "CraftsmanAccount('" + self._email + "','" + self._password + "')"

    @property
    def logged(self):
        """Indicates if account had successfully logged in."""
        return self._logged

    @property
    def aspnet_cookie(self):
        """AspNet Cookie for account auth."""
        return self._aspnet_cookie

    @property
    def aspnet_session_id(self):
        """AspNet Session ID for account auth."""
        return  self._aspnet_session_id


class GarageOpener:
    """Garage Opener object that controls each aspects of its status."""

    def __init__(self, openerStatus, accountToken):
        self._account_token = accountToken

        self._name = openerStatus['Name']
        self._gateway_location = openerStatus['Gateway']
        self._device_id = openerStatus['MyQDeviceId']
        self._gateway_id = openerStatus['GatewayId']

    def get_status(self):
        """Return current status as reported from REST request."""

        url = AssurelinkURL.BASE.value + AssurelinkURL.GET_DEVICE.value
        headers = self._account_token.get_cookie_header()
        payload = {
            'brandName'    : 'Craftsman',
            'SerialNumber' : self.device_id
        }
        responses = requests.post(url, headers=headers, params=payload)
        return responses

    def open_garage(self):
        """Open the garage door."""
        return self._garage_control(RequestDoorState.OPEN.value)

    def close_garage(self):
        """Close the garage door."""
        return self._garage_control(RequestDoorState.CLOSE.value)

    def _garage_control(self, desire_door_state):
        """The main method to send REST request to control the garage door.

        param desire_door_state: The int that indicates which position the door
                                 should be in."""
        url = AssurelinkURL.BASE.value + AssurelinkURL.GARAGE_CONTROL.value
        headers = self._account_token.get_cookie_header()
        payload = {
            'SerialNumber'   : self.device_id,
            'attributename'  : 'desireddoorstate',
            'attributevalue' : desire_door_state
        }
        responses = requests.post(url, headers=headers, params=payload)
        return responses

    def __repr__(self):
        key = ['Name', 'Gateway', 'MyQDeviceId', 'GatewayId']
        val = map(str, [self.name, self.location, self.device_id, self.gateway_id])
        json = "','".join(["':'".join(pair) for pair in list(zip(key, val))])
        json = "{'" + json + "'}"
        return 'GarageOpener(' + json + ',' + self._account_token.__repr__() + ")"

    @property
    def name(self):
        """Name of the garage door."""
        return self._name

    @property
    def location(self):
        """Location of the garage door."""
        return self._gateway_location

    @property
    def device_id(self):
        """Garage door ID."""
        return  self._device_id

    @property
    def gateway_id(self):
        """The internew gateway ID."""
        return  self._gateway_id

class AssurelinknNotLoggedException(Exception):
    """Not logged to Assurelink Web Services Exception."""

    def __init__(self):
        """Assurelink not logged Exception."""
        super(AssurelinknNotLoggedException, self).__init__()
