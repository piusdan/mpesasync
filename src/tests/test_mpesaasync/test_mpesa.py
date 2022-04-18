import pytest
import pytest_asyncio

from mpesasync import *
from mpesasync import MpesaResponse
from mpesasync.mpesa_business import MpesaTransaction, TransactionStatus


@pytest_asyncio.fixture
async def mpesa_app() -> Mpesa:
    mpesa_app = Mpesa(
        Environment=MpesaEnvironment.sandbox
    )
    await mpesa_app.authorize(consumer_key=os.environ["CONSUMER_KEY"], consumer_secret=os.environ["CONSUMER_SECRET"])
    return mpesa_app


@pytest_asyncio.fixture
async def transaction() -> MpesaTransaction:
    mpesa_app = MpesaTransaction(InitiatorName="testapi",
                                 SecurityCredential=MpesaTransaction.get_security_credential(
                                     MpesaEnvironment.sandbox,
                                     os.environ["INITIATOR_NAME"]),
                                 OrganizationShortcode=os.environ["ORGANIZATION_SHORTCODE"],
                                 QueueTimeOutURL="https://mydomain.com/TransactionStatus/result/",
                                 ResultURL="https://mydomain.com/TransactionStatus/queue/",
                                 Environment=MpesaEnvironment.sandbox)

    await mpesa_app.authorize(consumer_key=os.environ["CONSUMER_KEY"], consumer_secret=os.environ["CONSUMER_SECRET"])

    return mpesa_app


@pytest.mark.asyncio
async def test_can_get_transaction_status(transaction: MpesaTransaction):
    sut = await transaction.transaction_status(transactionId="OEI2AK4Q16",
                                               identfierType=IdentifierType.OrganizationShortCode)
    assert isinstance(sut, MpesaResponse)
    assert isinstance(sut.data, TransactionStatus)
