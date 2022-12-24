from flask import Blueprint
from flask import g
from ..services.wallet.wallet import WalletService
from dependency_injector.wiring import inject, Provider
from ..injection import ServiceContainer

hello_world_page = Blueprint("hello_world", __name__, url_prefix="/worlds")

# TODO make this a depedency injection?
# also type it
@hello_world_page.route("/")
@inject
def hello_world(
    wallet_service: WalletService = Provider[ServiceContainer.wallet_service],
):
    # wallet = walletService.wallet
    # balance = wallet.get_balance()
    # print(f"Wallet balance is: {balance}")
    butter = wallet_service
    print(f"Wallet  is: {butter.get_hi()}")
    # print(f"Wallet hi is: {wallet_service().hi}")

    return f"Wallet balance is: ahhh"
