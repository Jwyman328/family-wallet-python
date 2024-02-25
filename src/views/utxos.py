from flask import Blueprint, request

from src.services import WalletService
from dependency_injector.wiring import inject, Provide
from src.injection import ServiceContainer
from src.types.script_types import ScriptType
from typing import Optional


utxo_page = Blueprint("get_utxos", __name__, url_prefix="/utxos")


@utxo_page.route("/fees/<txid>/<vout>")
@inject
def get_fee_for_utxo(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
    txid: Optional[str] = None,
    vout: Optional[str] = None,
):
    """
    Get a fee estimate for a given utxo.
    To find the utxo, we need to know the txid and vout value.
    """
    print("in here?")
    # TODO if the tx is unspendable then return that info somehow

    utxos = wallet_service.get_all_utxos()
    print("any utxos", utxos)

    fee_rate: str = request.args.get(
        "feeRate",
        default="1",
    )
    # now find the utxo that matches the tx id and vout value
    # use pydantic to validate the query params
    utxo = [
        utxo
        for utxo in utxos
        if utxo.outpoint.txid == txid and str(utxo.outpoint.vout) == vout
    ]
    local_utxo = utxo[0] if utxo else None

    if local_utxo is None:
        return {"error": "utxo not found"}

    mock_script_type = ScriptType.P2PKH
    # get this value from query param
    fee_estimate_response = wallet_service.get_fee_estimate_for_utxo(
        local_utxo, mock_script_type, int(fee_rate)
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
        print(f"Error calling build_transaction with outpoint: {e}")
        return {"error": "error getting utxos"}
