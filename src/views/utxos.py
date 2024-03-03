from flask import Blueprint, request

from src.services import WalletService
from dependency_injector.wiring import inject, Provide
from src.injection import ServiceContainer
from src.types.bdk_types import OutpointType
from src.types.script_types import ScriptType
from typing import Dict, cast
import json
import structlog

utxo_page = Blueprint("get_utxos", __name__, url_prefix="/utxos")

LOGGER = structlog.get_logger()


@utxo_page.route("/fees", methods=["POST"])
@inject
def get_fee_for_utxo(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
):
    """
    Get a fee estimate for any number of utxos as input.
    To find the utxos, we need to know the txid and vout values.
    """
    fee_rate: str = request.args.get(
        "feeRate",
        default="1",
    )

    # this is the perfect place that pydantic would go
    transactions_json = request.data

    if transactions_json is None:
        LOGGER.error("no transactions were supplied")
        return {"error": "no transactions were supplied"}

    transactions: list[Dict[str, str]] = json.loads(transactions_json)

    LOGGER.info(
        "utxo fee data",
        transactions=transactions,
        fee_rate=fee_rate,
    )

    utxos_wanted = []
    for tx in transactions:
        tx_formatted = cast(Dict[str, str], tx)
        utxos_wanted.append(OutpointType(tx_formatted["id"], int(tx_formatted["vout"])))

    utxos = wallet_service.get_utxos_info(utxos_wanted)

    # todo: get this value from query param
    mock_script_type = ScriptType.P2PKH
    fee_estimate_response = wallet_service.get_fee_estimate_for_utxos(
        utxos, mock_script_type, int(fee_rate)
    )
    if (
        fee_estimate_response.status == "success"
        and fee_estimate_response.data is not None
    ):
        return {
            "spendable": True,
            "percent_fee_is_of_utxo": fee_estimate_response.data.percent_fee_is_of_utxo,
            "fee": fee_estimate_response.data.fee,
        }
    elif fee_estimate_response.status == "unspendable":
        return {"error": "unspendable", "spendable": False}
    else:
        return {"error": "error getting fee estimate for utxo", "spendable": False}


@utxo_page.route("/")
@inject
def get_utxos(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
):
    """
    Get all utxos in the wallet.
    """
    try:
        utxos = wallet_service.get_all_utxos()

        utxos_formatted = [
            {
                "txid": utxo.outpoint.txid,
                "vout": utxo.outpoint.vout,
                "amount": utxo.txout.value,
            }
            for utxo in utxos
        ]

        return {
            "utxos": utxos_formatted,
        }
    except Exception as e:
        LOGGER.error("Error getting utxos", error=e)
        return {"error": "error getting utxos"}
