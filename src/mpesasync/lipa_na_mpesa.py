import base64
import datetime

from pydantic import BaseModel

from mpesasync import Mpesa, MpesaResponse
from mpesasync.restlib import HttpClient


class InitiateSTKPushResponse(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResponseDescription: str
    ResponseCode: str
    CustomerMessage: str


class QueryLipaNaMpesaOnlineResponse(BaseModel):
    ResponseCode: str
    ResponseDescription: str
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: str
    ResultDesc: str


class STKPush(Mpesa):
    BusinessShortCode: str
    CallBackURL: str
    PassKey: str

    def get_password(self, timestamp: str):
        secret_string = "%s%s%s" % (self.BusinessShortCode, self.PassKey, timestamp)
        return base64.b64encode(secret_string.encode()).decode()

    @classmethod
    def get_timestamp(cls) -> str:
        return (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%Y%m%d%H%M%S")

    async def stk_push(self,
                       amount: float,
                       phone_number: str,
                       account_reference=None,
                       transaction_description=None,
                       callback_url=None
                       ) -> MpesaResponse[InitiateSTKPushResponse]:

        if account_reference is None:
            account_reference = phone_number
        if transaction_description is None:
            transaction_description = "Customer Payment"

        timestamp = self.get_timestamp()

        self.validate_phonenumber(phone_number)

        request_data = {
            "BusinessShortCode": self.BusinessShortCode,
            "Password": self.get_password(timestamp),
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.BusinessShortCode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url or self.CallBackURL,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_description
        }

        ENDPOINT = self.base_url + "/mpesa/stkpush/v1/processrequest"
        resp = await HttpClient.HttpPost(url=ENDPOINT, data=request_data, access_token=self.AccessToken)
        if resp.error is None:
            resp.data = InitiateSTKPushResponse.parse_obj(resp.data)
        return resp

    async def verify(self, checkout_request_id: str) -> MpesaResponse[QueryLipaNaMpesaOnlineResponse]:
        """Check the status of a Lipa Na M-Pesa Online Payment."""
        timestamp = self.get_timestamp()
        request_data = {
            "BusinessShortCode": self.BusinessShortCode,
            "Password": self.get_password(timestamp), "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        ENDPOINT = self.base_url + "/mpesa/stkpushquery/v1/query"
        resp = await HttpClient.HttpPost(
            url=ENDPOINT,
            data=request_data,
            access_token=self.AccessToken
        )
        if resp.error is None:
            resp.data = QueryLipaNaMpesaOnlineResponse.parse_obj(resp.data)
        return resp

    @classmethod
    def process_callback(cls, data: dict):
        raise NotImplementedError
