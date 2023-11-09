from enum import StrEnum


class ReportType(StrEnum):
    CROSS_VISIT = 'cross_visit'
    EXPENDITURE = 'expenditure'
    WALLET_SHARE = 'wallet_share'
    CUSTOMER_VOLUME = 'customer_volume'
    TRANSACTION = 'transaction'
