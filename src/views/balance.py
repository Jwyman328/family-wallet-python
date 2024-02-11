from flask import Blueprint
from flask import g
from src.services import WalletService
from dependency_injector.wiring import inject, Provide
from src.injection import ServiceContainer
balance_page = Blueprint("get_balance", __name__, url_prefix="/balance")


@balance_page.route("/")
@inject
def get_balance(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
):
    wallet = wallet_service.wallet
    balance = wallet.get_balance()
    print(f'testing info log {balance}')

    return {"total": balance.total, "spendable", "confirmed": balance.confirmed} 
