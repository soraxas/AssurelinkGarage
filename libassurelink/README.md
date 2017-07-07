# Assurelink Craftsman Garage Opener Python library

This Python 3.4+ library allow you to control [Assurelink Craftsman](https://assurelink.craftsman.com/) devices.

## Status

Currently most basic functionality have been implemented, feel free to PR or fire an issue if you encountered any.

### Devices supported

Assurelink Craftsman Internet enabled devices, aka devices that you can control via [website](https://assurelink.craftsman.com/).

## Features

The following feature are supported:

* Ge the current status of the garage opener
* Open the garage door
* Close the garage door

## Quick start

```python
from libassurelink import assurelink

account = CraftsmanAccount(EMAIL, PASSWORD)

# check login status
if not account.logged:
  print('Login failed.')

garageOpeners = account.get_devices()

# Controlling the first available device
garageOpener = garageOpeners[0]

# get status
garageOpener.get_status()

# open garage door
garageOpener.open_garage()

# close garage door
garageOpener.close_garage()
```
