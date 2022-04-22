import os

import pytest
import pytest_asyncio

from mpesasync import MpesaEnvironment, MpesaResponse
from mpesasync.lipa_na_mpesa import STKPush, InitiateSTKPushResponse, QueryLipaNaMpesaOnlineResponse


@pytest_asyncio.fixture
async def mpesa_express() -> STKPush:
    mpesa_app = STKPush(
        Environment=MpesaEnvironment.sandbox,
        BusinessShortCode=os.environ["BUSSINESS_SHORTCODE"],
        CallBackURL="https://mydomain.com/path",
        PassKey=os.environ["PASSKEY"]
    )
    await mpesa_app.authorize(consumer_key="Azs2KejU1ARvIL5JdJsARbV2gDrWmpOB",
                              consumer_secret="hipGvFJbOxri330c")
    return mpesa_app


@pytest.mark.asyncio
async def test_can_send_stk_push(mpesa_express: STKPush):
    resp = await mpesa_express.stk_push(
        amount=1.0, phone_number="254703554404"
    )
    assert isinstance(resp, MpesaResponse)
    assert resp.data is not None
    assert isinstance(resp.data, InitiateSTKPushResponse)
