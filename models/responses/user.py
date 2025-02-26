from pydantic import BaseModel


class HistoryListItem(BaseModel):
    txHash: str
    chainId: int
    blockDate: str
    points: int
    inBridge: int


class User(BaseModel):
    historyList: list[HistoryListItem]
    transactionCount: int
    isCheckIn: int
