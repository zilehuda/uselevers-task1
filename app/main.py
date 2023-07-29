import logging
import sys

from fastapi import FastAPI

from app.api.bills_api import router as bill_router

log_format = "%(asctime)s [%(levelname)s] logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s"  # noqa
logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})


app.include_router(
    bill_router,
    prefix="/api/bills",
    tags=["bills"],
)
