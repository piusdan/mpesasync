import enum
import uuid
from datetime import datetime
from typing import TypeVar, Optional, Generic, List

import pydantic
from pydantic import validator, Field
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class BaseModel(pydantic.BaseModel):
    def to_json(self) -> str:
        return self.json()

    @classmethod
    def from_json(cls, obj: str):
        return cls.parse_raw(obj)

    class Config:
        use_enum_values = True
        json_encoders = {
            uuid.UUID: lambda v: str(v),
            enum: lambda v: v.value,
            datetime: lambda v: str(v)
        }


class MpesaError(BaseModel):
    requestId: Optional[str]
    errorCode: str
    errorMessage: Optional[str]


class MpesaResponse(GenericModel, Generic[DataT]):
    """
    Generic model to hold both error and data responses from the safaricom API
    """
    data: Optional[DataT]
    error: Optional[MpesaError]

    @validator('error', always=True)
    def check_consistency(cls, v, values):
        if v is not None and values.get('data') is not None:
            raise ValueError('must not provide both data and error')
        if v is None and values.get('data') is None:
            raise ValueError('must provide data or error')
        return v


class CallBackMetadataItem(BaseModel):
    Item: List[dict] = Field(default_factory=list)

    def get_item(self, key):
        for item in self.Item:
            if item["Name"] == key:
                return item["Value"]
        return None

    @classmethod
    def empty(cls):
        return cls()


class STKCallBack(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
    CallbackMetadata: CallBackMetadataItem = Field(default_factory=CallBackMetadataItem)


class STKPushResultBody(BaseModel):
    stkCallback: STKCallBack


class STKPushResult(BaseModel):
    """
    STK Push result received from safaricom
    """
    Body: STKPushResultBody
