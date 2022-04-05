import pytest
import pytest_asyncio

from mpesalib.mpesa_business.mpesa_business import *
from mpesalib.types import CommandId


@pytest_asyncio.fixture
async def mpesa_business() -> MpesaBusiness:
    mpesa_app = MpesaBusiness(InitiatorName="testapi",
                              SecurityCredential=MpesaBusiness.get_security_credential(
                                  MpesaEnvironment.sandbox,
                                  "Safaricom990!"),
                              OrganizationShortcode="600990",
                              QueueTimeOutURL="https://mydomain.com/b2c/queue",
                              ResultUrl="https://mydomain.com/b2c/result",
                              Environment=MpesaEnvironment.sandbox)

    await mpesa_app.authorize(consumer_key="Azs2KejU1ARvIL5JdJsARbV2gDrWmpOB", consumer_secret="hipGvFJbOxri330c")

    return mpesa_app


@pytest.mark.asyncio
async def test_can_simulate_CustomerPayBillOnline(mpesa_business: MpesaBusiness):
    sut = await mpesa_business.simulate_customer_to_business_payment(
        phoneNumber="254708374149",
        amount=100,
        commandId=CommandId.CustomerPayBillOnline,
        billReferenceNumber="1256370"
    )
    assert isinstance(sut, MpesaResponse)
    assert isinstance(sut.data, SimulateCustomerToBizPaymentResponse)


@pytest.mark.asyncio
async def test_can_simulate_CustomerBuyGoodOnline(mpesa_business: MpesaBusiness):
    sut = await mpesa_business.simulate_customer_to_business_payment(
        phoneNumber="254708374149",
        amount=100,
        commandId=CommandId.CustomerBuyGoodsOnline
    )
    assert isinstance(sut, MpesaResponse)
    assert isinstance(sut.data, SimulateCustomerToBizPaymentResponse)


@pytest.mark.asyncio
async def test_business_to_customer_payment(mpesa_business: MpesaBusiness):
    sut = await mpesa_business.business_to_customer(phoneNumber="254708374149",
                                                    amount=100,
                                                    commandId=CommandId.BusinessPayment
                                                    )
    assert isinstance(sut, MpesaResponse)
    assert isinstance(sut.data, BusinessToCustomerPaymentResponse)
