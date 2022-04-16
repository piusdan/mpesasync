import pytest
import pytest_asyncio

from mpesasync import MpesaEnvironment, MpesaResponse
from mpesasync.lipa_na_mpesa import STKPush, InitiateSTKPushResponse, QueryLipaNaMpesaOnlineResponse


@pytest_asyncio.fixture
async def mpesa_express() -> STKPush:
    mpesa_app = STKPush(
        Environment=MpesaEnvironment.sandbox,
        BusinessShortCode=174379,
        CallBackURL="https://mydomain.com/path",
        PassKey="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    )
    await mpesa_app.authorize(consumer_key="Azs2KejU1ARvIL5JdJsARbV2gDrWmpOB",
                              consumer_secret="hipGvFJbOxri330c")
    return mpesa_app


@pytest.mark.asyncio
async def test_can_send_stk_push(mpesa_express: STKPush):
    resp = await mpesa_express.stk_push(
        amount=1.0, phone_number="254708374149"
    )
    assert isinstance(resp, MpesaResponse)
    assert resp.data is not None
    assert isinstance(resp.data, InitiateSTKPushResponse)


@pytest.mark.asyncio
async def test_can_verfiy_transaction(mpesa_express: STKPush):
    transaction = await mpesa_express.stk_push(
        amount=1.0, phone_number="254708374149"
    )
    resp = await mpesa_express.verify(transaction.data.CheckoutRequestID)
    assert isinstance(resp, MpesaResponse)
    assert resp.data is not None
    assert isinstance(resp.data, QueryLipaNaMpesaOnlineResponse)
