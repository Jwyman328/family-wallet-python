from flask import Blueprint, request

from src.services import WalletService
from dependency_injector.wiring import inject, Provide
from src.containers.service_container import ServiceContainer
from src.types.bdk_types import OutpointType
from src.types.script_types import ScriptType
import structlog
import json
from pydantic import BaseModel, Field, ValidationError

utxo_page = Blueprint("get_utxos", __name__, url_prefix="/utxos")

LOGGER = structlog.get_logger()


class TransactionDto(BaseModel):
    id: str
    vout: str


class GetUtxosRequestDto(BaseModel):
    fee_rate: str = Field(default="1")
    transactions: list[TransactionDto]


@utxo_page.route("/fees", methods=["POST"])
@inject
def get_fee_for_utxo(
    wallet_service: WalletService = Provide[ServiceContainer.wallet_service],
):
    """
    Get a fee estimate for any number of utxos as input.
    To find the utxos, we need to know the txid and vout values.
    """

    try:
        transactions_request_data = request.data or b"[]"
        print("transactions_request_data", transactions_request_data)
        get_utxos_request_dto = GetUtxosRequestDto.model_validate(
            dict(
                fee_rate=request.args.get("feeRate"),
                transactions=json.loads(transactions_request_data),
            )
        )
        if len(get_utxos_request_dto.transactions) == 0:
            LOGGER.error("no transactions were supplied")
            return {"error": "no transactions were supplied"}

        LOGGER.info(
            "utxo fee data",
            transactions=get_utxos_request_dto.transactions,
            fee_rate=get_utxos_request_dto.fee_rate,
        )

        utxos_wanted = []
        for tx in get_utxos_request_dto.transactions:
            utxos_wanted.append(OutpointType(tx.id, int(tx.vout)))

        utxos = wallet_service.get_utxos_info(utxos_wanted)

        # todo: get this value from query param
        mock_script_type = ScriptType.P2PKH
        fee_estimate_response = wallet_service.get_fee_estimate_for_utxos(
            utxos, mock_script_type, int(get_utxos_request_dto.fee_rate)
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
            return {"errors": ["unspendable"], "spendable": False}
        else:
            return {
                "errors": ["error getting fee estimate for utxo"],
                "spendable": False,
            }
    except ValidationError as e:
        return {
            "message": "Error getting fee estimate for utxos",
            "spendable": False,
            "errors": e.errors(),
        }, 400


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
