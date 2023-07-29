from typing import Optional, Union

from pydantic import BaseModel


class APIResponse(BaseModel):
    message: str = ""
    data: Optional[Union[str, list, dict]]


class CreateSubBills(BaseModel):
    amount: float
    reference: Optional[str]


class CreateBills(BaseModel):
    total: float
    sub_bills: list[CreateSubBills]


class SubBillResponse(BaseModel):
    amount: float
    reference: Optional[str]

    class Config:
        orm_mode = True


class BillResponse(BaseModel):
    id: int
    total: float
    sub_bills: list[SubBillResponse]

    class Config:
        orm_mode = True
