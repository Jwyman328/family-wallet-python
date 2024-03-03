from flask import Blueprint, request

from dependency_injector.wiring import inject
import structlog
import json

from src.services.wallet.wallet import WalletService

wallet_api = Blueprint("wallet", __name__, url_prefix="/wallet")

LOGGER = structlog.get_logger()


@wallet_api.route("/", methods=["POST"])
@inject
def create_wallet(wallet_class: type = WalletService):
    """
    Set the global level wallet descriptor.
    """

    descriptor = json.loads(request.data)
    wallet_class.set_global_descriptor(descriptor["descriptor"])

    return {"message": "wallet created successfully", "descriptor": descriptor}
