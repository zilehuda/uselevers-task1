import logging
from typing import Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Bill
from app.repositories.bill_repository import BillRepository
from app.schemas import CreateBills, SubBillResponse

logger = logging.getLogger(__name__)


def create_bill_with_sub_bills(db: Session, bill_data: CreateBills) -> Bill:
    try:
        # Create a new Bill instance
        bill_repository = BillRepository(db)
        bill: Bill = bill_repository.create_bills(bill_data)
        return bill

    except IntegrityError as e:
        logger.error(f"Error creating bills: {str(e)}")
        raise HTTPException(
            400,
            detail="Bill with sub-bills already exists (Unique constraint violation)",
        )
    except Exception as e:
        logger.error(f"Error creating bills: {str(e)}")
        raise HTTPException(400, detail="Error creating bills")


def get_total_bills(db: Session) -> int:
    bill_repository = BillRepository(db)
    return bill_repository.get_total_bills()


def get_bills_with_sub_bills(
    db: Session,
    reference: Optional[str],
    total_from: Optional[int],
    total_to: Optional[int],
    skip: int,
    limit: int,
):
    try:
        # Instantiate the BillRepository to perform database operations
        bill_repository = BillRepository(db)

        # Fetch bills based on the provided reference and total_from parameters
        bills: list[Bill] = bill_repository.get_bills_with_sub_bills(
            reference, total_from, total_to, skip, limit
        )

        # Prepare the JSON response
        response: list = []
        for bill in bills:
            sum(sub_bill.amount for sub_bill in bill.sub_bills)
            bill_data: dict = {
                "id": bill.id,
                "total": bill.total,
                "sub_bills": [
                    SubBillResponse(
                        amount=sub_bill.amount,
                        reference=sub_bill.reference,
                    )
                    for sub_bill in bill.sub_bills
                ],
            }
            response.append(bill_data)

        return response

    except Exception as e:
        logger.error(f"Error fetching bills: {str(e)}")
        raise HTTPException(400, detail="Error fetching bills")
