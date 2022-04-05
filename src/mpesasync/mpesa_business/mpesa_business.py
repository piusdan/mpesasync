from typing import Optional

from mpesasync import Mpesa, MpesaEnvironment
from mpesasync.restlib import *
from mpesasync.types import CommandId


class SimulateCustomerToBizPaymentResponse(BaseModel):
    OriginatorCoversationID: str
    ConversationID: Optional[str]
    ResponseDescription: str


class BusinessToCustomerPaymentResponse(BaseModel):
    ConversationID: str
    OriginatorConversationID: str
    ResponseCode: str
    ResponseDescription: str


class GetAccountBalanceResponse(BaseModel):
    OriginatorConverstionID: str
    ConversationID: str
    ResponseDescription: str


class ReverseTransactionResponse(BaseModel):
    OriginatorConversationID: str
    ConversationID: str
    ResponseDescription: str
    ResponseCode: int


class BusinessToBusinessTransferResponse(BaseModel):
    pass


class MpesaBusiness(Mpesa):
    # An API user created by the Business Administrator of the M-PESA Bulk disbursement account that is active and authorized to initiate B2C transactions via API.
    InitiatorName: str
    # value obtained after encrypting the API initiator password.
    SecurityCredential: str
    # This is the organization shortcode.
    OrganizationShortcode: str
    # This is the URL to be specified in your request that will be used by API Proxy to send notification incase the payment request is timed out while awaiting processing in the queue.
    QueueTimeOutURL: str
    # This is the URL to be specified in your request that will be used by M-PESA to send notification upon processing of the payment request.
    ResultUrl: str

    async def simulate_customer_to_business_payment(self, phoneNumber: str,
                                                    amount: int,
                                                    commandId: CommandId,
                                                    billReferenceNumber: str = None) -> \
            MpesaResponse[SimulateCustomerToBizPaymentResponse]:
        if self.Environment != MpesaEnvironment.sandbox:
            raise RuntimeError("This feature is only available on sandbox")

        if commandId not in [commandId.CustomerBuyGoodsOnline, commandId.CustomerPayBillOnline]:
            raise ValueError("Command should be one of [%s,%s]" % (
                commandId.CustomerBuyGoodsOnline, commandId.CustomerPayBillOnline))
        if commandId == commandId.CustomerPayBillOnline and billReferenceNumber is None:
            raise ValueError("Bill reference number is required for customer paybill online request")

        payload = {
            "CommandID": commandId.value,
            "Amount": amount,
            "Msisdn": phoneNumber,
            "BillRefNumber": billReferenceNumber,
            "ShortCode": self.OrganizationShortcode
        }
        ENDPOINT = self.base_url + "/mpesa/c2b/v1/simulate"
        resp = await HttpClient.HttpPost(url=ENDPOINT,
                                         data=payload,
                                         access_token=self.AccessToken)
        if resp.error:
            response = MpesaResponse[SimulateCustomerToBizPaymentResponse](error=resp.error)
        else:
            response = MpesaResponse[SimulateCustomerToBizPaymentResponse](
                data=SimulateCustomerToBizPaymentResponse.parse_obj(resp.data))
        return response

    async def business_to_customer(self,
                                   phoneNumber: str,
                                   amount: int,
                                   commandId: CommandId,
                                   remarks: str = None) -> \
            MpesaResponse[BusinessToCustomerPaymentResponse]:
        """
        Transact between an M-Pesa short code to a phone number registered on M-Pesa
        B2C API is an API used to make payments from a Business to Customers (Pay Outs).
        Also known as Bulk Disbursements.
        B2C API is used in several scenarios by businesses that require to either make Salary Payments, Cashback payments, Promotional Payments(e.g. betting winning payouts), winnings, financial institutions withdrawal of funds, loan disbursements etc.

        ====

        # B2C API transaction process flow

        1. The Merchant (Partner) sets all the required parameters the request and sends it to: https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest
        2. API Management platform receives the request validates, authorizes and authenticates the partner to access the API, sends to M-PESA and an acknowledgement back to the Merchant(Partner).
        3. M-PESA receives the request, validates the initiator details and processes the request.
        4. M-PESA then sends the response back to the Merchant (partner) via the callback URL specified in your request.
        5. M-PESA sends an SMS notification to the customer on the payments received.
        6. NOTE: For you to use this API on production you are required to apply for a Bulk Disbursement Account and get a Short code, you cannot do this payment from a Pay Bill or Buy Goods (Till Number). To apply for a Bulk disbursement account follow this link. https://www.safaricom.co.ke/business/sme/m-pesa-payment-solutions
        """
        self.validate_phonenumber(phoneNumber)
        payload = {
            "InitiatorName": self.InitiatorName,
            "SecurityCredential": self.SecurityCredential,
            "CommandID": commandId.value,
            "Amount": amount,
            "PartyA": self.OrganizationShortcode,
            "PartyB": phoneNumber,
            "Remarks": remarks or "%s remarks" % commandId.value,
            "QueueTimeOutURL": self.QueueTimeOutURL,
            "ResultURL": self.ResultUrl,
            "Occassion": commandId.value
        }
        ENDPOINT = self.base_url + "/mpesa/b2c/v1/paymentrequest"
        resp = await HttpClient.HttpPost(url=ENDPOINT,
                                         data=payload,
                                         access_token=self.AccessToken)
        if resp.error:
            response = MpesaResponse[BusinessToCustomerPaymentResponse](error=resp.error)
        else:
            response = MpesaResponse[BusinessToCustomerPaymentResponse](
                data=BusinessToCustomerPaymentResponse.parse_obj(resp.data))

        return response
