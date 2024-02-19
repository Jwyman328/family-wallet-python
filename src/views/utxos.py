from flask import Blueprint
from src.services import WalletService
from dependency_injector.wiring import inject, Provide
from src.injection import ServiceContainer
from src.types.script_types import ScriptType


utxo_page = Blueprint("get_utxos", __name__, url_prefix="/utxos")


@utxo_page.route("/fees")
@inject
def get_fee_for_utxo(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
):
    utxos = wallet_service.get_all_utxos()
    # now find the utxo that matches the tx id and vout value
    # use pydantic to validate the query params
    local_utxo = utxos[0]
    mock_script_type = ScriptType.P2PKH
    # get this value from query param
    sats_per_vbyte = 4
    fee_estimate_response = wallet_service.get_fee_estimate_for_utxo(
        local_utxo, mock_script_type, sats_per_vbyte
    )
    if fee_estimate_response is not None:
        (percent_fee_is_of_utxo, fee) = fee_estimate_response

        return {"percent_fee_is_of_utxo": percent_fee_is_of_utxo, "fee": fee}
    else:
        return {"error": "error getting fee estimate"}


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
