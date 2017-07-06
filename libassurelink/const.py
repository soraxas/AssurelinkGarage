"""Assurelink Craftsman Opener constants."""

from enum import Enum

class AssurelinkURL(Enum):
    """URL for different querys."""

    BASE = "https://assurelink.craftsman.com/"
    GET_ALL_DEVICES = 'api/MyQDevices/GetAllDevices'
    GET_DEVICE = 'api/MyQDevices/LoadSingleDevice'



class AspNet(Enum):
    """Cookies for account auth"""

    ASPNET_COOKIE = '.AspNet.ApplicationCookie'
    ASPNET_SESSION_ID = 'ASP.NET_SessionId'
