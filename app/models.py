
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.utils.base_model import BaseModel


class Bill(BaseModel):
    __tablename__ = "bills"
    total = Column(Float)


class SubBill(BaseModel):
    __tablename__ = "sub_bills"
    amount = Column(Float, nullable=False)
    reference = Column(
        String(10),
        nullable=True,
        unique=True,
    )
    bill = relationship("Bill", backref="sub_bills")

    bill_id = Column(Integer, ForeignKey("bills.id"))
