from mpesasync import *
from mpesasync.restlib import *
from mpesasync.types import IdentifierType, CommandId


class TransactionStatus(BaseModel):
    OriginatorConversationID: str
    ConversationID: str
    ResponseCode: str
    ResponseDescription: str


class MpesaTransaction(Mpesa):
    SecurityCredential: str
    InitiatorName: str
    OrganizationShortcode: str
    ResultURL: str
    QueueTimeOutURL: str

    async def transaction_status(self,
                                 transactionId: str,
                                 identfierType: IdentifierType) -> MpesaResponse[TransactionStatus]:
        if identfierType not in [IdentifierType.MSISDN, IdentifierType.OrganizationShortCode,
                                 IdentifierType.TillNumber]:
            raise ValueError("Identifier type should be on of [%s, %s, %s]" % (
                IdentifierType.MSISDN, IdentifierType.OrganizationShortCode, IdentifierType.TillNumber))

        payload = {
            "Initiator": self.InitiatorName,
            "SecurityCredential": self.SecurityCredential,
            "CommandID": CommandId.TransactionStatusQuery.value,
            "TransactionID": transactionId,
            "PartyA": self.OrganizationShortcode,
            "IdentifierType": identfierType.value,
            "ResultURL": self.ResultURL,
            "QueueTimeOutURL": self.QueueTimeOutURL,
            "Remarks": "my remarks",
            "Occassion": "null",
        }
        ENDPOINT = self.base_url + "/mpesa/transactionstatus/v1/query"
        resp = await HttpClient.HttpPost(url=ENDPOINT,
                                         data=payload,
                                         access_token=self.AccessToken)
        if resp.error is None:
            return MpesaResponse[TransactionStatus](
                data=TransactionStatus.parse_obj(resp.data))
        return MpesaResponse[TransactionStatus](error=resp.error)
