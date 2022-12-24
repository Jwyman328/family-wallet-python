from flask import Blueprint
from flask import g
from ..services.wallet.wallet import WalletService
from dependency_injector.wiring import inject, Provide
from ..injection import ServiceContainer

hello_world_page = Blueprint("hello_world", __name__, url_prefix="/worlds")


@hello_world_page.route("/")
@inject
def hello_world(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
):
    wallet = wallet_service.wallet
    balance = wallet.get_balance()

    return f"Wallet balance is: {balance}"
