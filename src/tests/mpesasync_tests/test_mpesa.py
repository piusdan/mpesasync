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
    await mpesa_app.authorize(consumer_key="Azs2KejU1ARvIL5JdJsARbV2gDrWmpOB", consumer_secret="hipGvFJbOxri330c")
    return mpesa_app


@pytest_asyncio.fixture
async def transaction() -> MpesaTransaction:
    mpesa_app = MpesaTransaction(InitiatorName="testapi",
                                 SecurityCredential=MpesaTransaction.get_security_credential(
                                     MpesaEnvironment.sandbox,
                                     "Safaricom990!"),
                                 OrganizationShortcode="600990",
                                 QueueTimeOutURL="https://mydomain.com/TransactionStatus/result/",
                                 ResultURL="https://mydomain.com/TransactionStatus/queue/",
                                 Environment=MpesaEnvironment.sandbox)

    await mpesa_app.authorize(consumer_key="Azs2KejU1ARvIL5JdJsARbV2gDrWmpOB", consumer_secret="hipGvFJbOxri330c")

    return mpesa_app


@pytest.mark.asyncio
async def test_can_get_transaction_status(transaction: MpesaTransaction):
    sut = await transaction.transaction_status(transactionId="OEI2AK4Q16",
                                               identfierType=IdentifierType.OrganizationShortCode)
    assert isinstance(sut, MpesaResponse)
    assert isinstance(sut.data, TransactionStatus)
