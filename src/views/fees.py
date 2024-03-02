# get current fees,
from flask import Blueprint
from dependency_injector.wiring import inject, Provide
from src.injection import ServiceContainer
from src.services import FeeService
from src.api.fees import FeeEstimates

fees_api = Blueprint("fees", __name__, url_prefix="/fees")


@fees_api.route(
    "/current",
)
@inject
def get_fee_for_utxo(
    fee_service: FeeService = Provide[ServiceContainer.fee_service],
):
    try:
        fees: FeeEstimates = fee_service.current_fees()
        return {"low": fees.low, "medium": fees.medium, "high": fees.high}
    except Exception as e:
        print("e", e)
        return {"error": "error fetching current fees"}
