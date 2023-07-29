import factory

from app.models import Bill, SubBill
from testdbconfig import TestingSessionLocal

db = TestingSessionLocal()


# Factory Boy model for Bill
class BillFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Bill
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "commit"


# Factory Boy model for SubBill
class SubBillFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SubBill
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "commit"

    amount = factory.Faker("pyfloat", positive=True, right_digits=2)
    reference = factory.Faker(
        "bothify", text="???-####"
    )  # Three random letters followed by four random digits
    bill = factory.SubFactory(BillFactory)
