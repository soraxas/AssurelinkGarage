"""Assurelink Craftsman Opener constants."""

from enum import Enum

class AssurelinkURL(Enum):
    """URL for different querys."""

    BASE = "https://assurelink.craftsman.com/"
    GET_ALL_DEVICES = 'api/MyQDevices/GetAllDevices'
    GET_DEVICE = 'api/MyQDevices/LoadSingleDevice'
    GARAGE_CONTROL = 'Device/TriggerStateChange'


class AspNet(Enum):
    """Cookies for account auth"""

    ASPNET_COOKIE = '.AspNet.ApplicationCookie'
    ASPNET_SESSION_ID = 'ASP.NET_SessionId'

class DoorState(Enum):
    """Indicates what state the garage is currently in."""

    OPENED = '1'
    CLOSED = '2'
    OPENING = '4'
    CLOSING = '5'

class RequestDoorState(Enum):
    """Send request to the desire door state."""
    
    CLOSE = '0'
    OPEN = '1'
