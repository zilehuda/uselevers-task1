from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import contains_eager

from app.models import Bill, SubBill
from app.utils.base_repository import BaseRepository


class BillRepository(BaseRepository):
    def create_bills(self, bill_data) -> Bill:
        try:
            bill = Bill(total=bill_data.total)
            self._db.add(bill)
            self._db.flush()

            self.create_sub_bills(bill.id, bill_data.sub_bills)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            raise e
        return bill

    def create_sub_bills(self, bill_id, sub_bills_data):
        for sub_bill_data in sub_bills_data:
            sub_bill = SubBill(
                amount=sub_bill_data.amount,
                reference=sub_bill_data.reference,
                bill_id=bill_id,
            )
            self._db.add(sub_bill)

    def get_total_bills(self):
        return self._db.query(Bill).count()

    def get_bills_with_sub_bills(
        self,
        reference: Optional[str],
        total_from: Optional[int],
        total_to: Optional[int],
        skip: int,
        limit: int,
    ) -> list[Bill]:
        # Query bills based on the case-insensitive reference parameter
        query = self._db.query(Bill)
        if reference:
            query = (
                self._db.query(Bill)
                .join(SubBill)
                .filter(SubBill.reference.ilike(f"%{reference}%"))
                .options(contains_eager(Bill.sub_bills))
            )
        if total_from or total_to:
            subquery = (
                self._db.query(Bill.id, func.sum(SubBill.amount).label("total_amount"))
                .join(SubBill)
                .filter(
                    or_(SubBill.reference.ilike(f"%{reference}%"), reference is None)
                )
                .group_by(Bill.id)
            )

            if total_from:
                subquery = subquery.having(func.sum(SubBill.amount) >= total_from)

            if total_to:
                subquery = subquery.having(func.sum(SubBill.amount) <= total_to)

            subquery = subquery.subquery()
            query = query.join(subquery, Bill.id == subquery.c.id)

        bills = query.offset(skip).limit(limit).all()
        return bills
