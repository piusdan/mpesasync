import pytest

pytest_plugins = ('pytest_asyncio',)

from mpesasync import MpesaEnvironment, Mpesa


@pytest.fixture
def sandbox_app():
    return Mpesa(
        Environment=MpesaEnvironment.sandbox
    )


@pytest.mark.asyncio
async def test_can_authorize(sandbox_app: Mpesa):
    await sandbox_app.authorize(
        consumer_key="Azs2KejU1ARvIL5JdJsARbV2gDrWmpOB",
        consumer_secret="hipGvFJbOxri330c")
    assert sandbox_app.AccessToken is not None


@pytest.mark.asyncio
@pytest.mark.raises()
async def test_returns_error_with_invalid_credentials(sandbox_app: Mpesa):
    await sandbox_app.authorize(
        consumer_key="Azs2KejU1ARvIL5JdJsARbV2gDrWmpOB",
        consumer_secret="hipGvFJbOrfgri330c")
