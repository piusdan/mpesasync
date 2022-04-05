import enum


class CommandId(enum.Enum):
    SalaryPayment = "SalaryPayment"
    BusinessPayment = "BusinessPayment"
    PromotionPayment = "PromotionPayment"
    BusinessBuyGoods = "BusinessBuyGoods"
    BusinessPayBill = "BusinessPayBill"
    DisburseFundsToBusiness = "DisburseFundsToBusiness"
    BusinessToBusinessTransfer = "BusinessToBusinessTransfer"
    BusinessTransferFromMMFToUtility = "BusinessTransferFromMMFToUtility"
    BusinessTransferFromUtilityToMMF = "BusinessTransferFromUtilityToMMF"
    MerchantToMerchantTransfer = "MerchantToMerchantTransfer"
    MerchantTransferFromMerchantToWorking = "MerchantTransferFromMerchantToWorking"
    MerchantTransferFromWorkingToMerchant = "MerchantTransferFromWorkingToMerchant"
    OrgBankAccountWithdrawal = "OrgBankAccountWithdrawal"
    OrgRevenueSettlement = "OrgRevenueSettlement"
    MerchantServicesMMFAccountTransfer = "MerchantServicesMMFAccountTransfer"
    AgencyFloatAdvance = "AgencyFloatAdvance"
    CustomerPayBillOnline = "CustomerPayBillOnline"
    CustomerBuyGoodsOnline = "CustomerBuyGoodsOnline"
    TransactionStatusQuery = "TransactionStatusQuery"


class IdentifierType(enum.Enum):
    MSISDN = 1
    TillNumber = 2
    SPShortCode = 3
    OrganizationShortCode = 4
    IdentityID = 5
    O2CLink = 6
    SPOperatorCode = 7
    POSNumber = 8
    OrganizationOperatorUserName = 9
    OrganizationOperatorCode = 10
    VoucherCode = 11
