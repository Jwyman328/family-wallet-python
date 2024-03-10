from flask import Blueprint, request

from src.services import GlobalDataStore
from dependency_injector.wiring import inject, Provide
from src.containers.global_data_store_container import GlobalStoreContainer

import structlog
import json

wallet_api = Blueprint("wallet", __name__, url_prefix="/wallet")

LOGGER = structlog.get_logger()


@wallet_api.route("/", methods=["POST"])
@inject
def create_wallet(
    global_data_store: GlobalDataStore = Provide[
        GlobalStoreContainer.global_data_store
    ],
):
    """
    Set the global level wallet descriptor.
    """

    # TODO use pydantic here
    data = json.loads(request.data)

    global_data_store.set_global_descriptor(data["descriptor"])
    global_data_store.set_global_network(data["network"])
    global_data_store.set_global_electrum_url(data["electrumUrl"])

    return {
        "message": "wallet created successfully",
        "descriptor": data["descriptor"],
        "network": data["network"],
        "electrumUrl": data["electrumUrl"],
    }
