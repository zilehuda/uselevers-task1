import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import APIResponse, BillResponse, CreateBills
from app.services import bill_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=APIResponse)
async def create_bills(request: CreateBills, db: Session = Depends(get_db)):
    logger.info("Create Bill request received")
    bill = bill_service.create_bill_with_sub_bills(db, request)
    data = BillResponse.from_orm(bill)
    logger.info("Bill created successfully")
    return APIResponse(message="Bill created successfully", data=data)


@router.get("/")
async def get_bills(
    db: Session = Depends(get_db),
    reference: str = Query(None, alias="reference"),
    total_from: int = Query(None, alias="total_from"),
    total_to: int = Query(None, alias="total_to"),
    skip: int = 0,
    limit: int = 10,
):
    logger.info(
        f"Get Bills request received with reference: {reference} & total_from: {total_from}"  # noqa: E501
    )
    bills = bill_service.get_bills_with_sub_bills(
        db, reference, total_from, total_to, skip, limit
    )
    data = {"bills": bills, "total": bill_service.get_total_bills(db)}
    logger.info("Bill Fetched successfully")
    return APIResponse(data=data)
