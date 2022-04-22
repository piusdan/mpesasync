# Mpesasync

[![Publish MpesaAsync](https://github.com/Piusdan/mpesasync/actions/workflows/python-app.yml/badge.svg)](https://github.com/Piusdan/mpesasync/actions/workflows/python-app.yml)

A asynchronous python library to the Mpesa Daraja API.
[Latest Release](https://pypi.org/project/mpesasync/)

# Features
This includes the following:
1. A python library to accept send and receive MPESA payments in less than 10 lines of code.
2. A sample implementation of the library in fast api.
# Installation
`$ pip install mpesasync`
# Development
* Create a virtual environment `python -m venv venv`
* Activate your virtual environment `$source venv\bin\activate` or in windows `> venv\scripts\activate`
* Install Poetry `pip install poetry`
* Install project `poetry install`
* Run tests `pytest`

# Getting started

To get started you need the following from the [Mpesa Daraja Portal](https://developer.safaricom.co.ke/)

[STK PUSH]
1. Your consumer key.
2. Your consumer secret.
3. The business shortcode.

[B2C/B2B]

5. Your organisation shortcode
6. Initiator name 
7. Security credential
8. QueueTimeOutURL
9. Result url => This has to be a publicly accessible callback that mpesa will send transaction results to.

For testing purposes, you can get test credentials [here](https://developer.safaricom.co.ke/MyApps).
On the sandbox portal, create an new app and use the provided credentials.

# Using the library
## STK Push

1. Initialise and authenticate the STKPush sdk

```python
from mpesasync import Mpesa, MpesaEnvironment
from mpesasync.lipa_na_mpesa import STKPush
mpesa_app = STKPush(
        Environment=MpesaEnvironment.production, # use sandbox to authenticate with sandbox credentials
        BusinessShortCode=1234, 
        CallBackURL="https://mydomain.com/path",
        PassKey="" # use the passkey obtained from the daraja portal
    )
await mpesa_app.authorize(consumer_key="YOUR CONSUMER KEY",
                              consumer_secret="YOUR CONSUMER SECRET")
```
2. Send an STKPush prompt
```python
await mpesa_app.stk_push(
        amount=1.0, phone_number="phone number"
    )
```

_The phone number can be any of +254XXXXXXXXX, 254XXXXXXXXX, 0XXXXXXXXX, the SDK will sanitise the phone numbers for you._

If the transaction is sucessfull, mpesa will send a confirmation to your configured callback url.
You can also use the library to parse the json data.
A callback implemented in [FastAPI](https://fastapi.tiangolo.com/) could look like.
```python
## main.py

from mpesasync.contracts import STKPushResult

from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.post("stkpush/callback")
def stk_push_callback(data: STKPushResult):
    ## do your zing
    print(data)
    return {"OK"}

```
Start the server

`$ uvicorn main:app --reload`

## Business to Customer Payments
Use this SDK to disburse money to your customers

```python
from mpesasync.mpesa_business.mpesa_business import *
from mpesasync.types import CommandId

mpesa_app = MpesaBusiness(InitiatorName="testapi",
                              SecurityCredential=MpesaBusiness.get_security_credential(
                                  initiator_password="YOUR INITIATOR",
                                  mpesa_environment=MpesaEnvironment.production
                            ),
                              OrganizationShortcode="",
                              QueueTimeOutURL="https://mydomain.com/b2c/queue",
                              ResultUrl="https://mydomain.com/b2c/result",
                              Environment=MpesaEnvironment.production)

await mpesa_app.authorize(consumer_key="CONSUMER KEY", consumer_secret="CONSUMER SECRET")

await mpesa_app.business_to_customer(phoneNumber="Phone number",
                                                    amount=100,
                                                    commandId=CommandId.BusinessPayment
                                                    )
```
