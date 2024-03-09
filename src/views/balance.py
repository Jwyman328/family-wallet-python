from flask import Blueprint
from src.services import WalletService
from dependency_injector.wiring import inject, Provide
from src.containers.ServiceContainer import ServiceContainer
import structlog

LOGGER = structlog.get_logger()


balance_page = Blueprint("get_balance", __name__, url_prefix="/balance")


@balance_page.route("/")
@inject
def get_balance(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
):
    """
    Get the currenct btc balance for the current wallet.
    """
    try:
        wallet = wallet_service.wallet
        balance = wallet.get_balance()

        return {
            "total": balance.total,
            "spendable": balance.spendable,
            "confirmed": balance.confirmed,
        }
    except Exception as e:
        LOGGER.error("error fetching balance", error=e)
        return {"error": "error fetching balance"}
