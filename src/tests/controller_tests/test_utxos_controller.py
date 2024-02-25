from unittest import TestCase
from unittest.mock import MagicMock
from src.app import AppCreator
from src.services.wallet.wallet import GetFeeEstimateForUtxoResponseType, WalletService
from src.types.bdk_types import FeeDetails
from src.tests.mocks import local_utxo_mock
import json

from src.types.script_types import ScriptType


class TestUtxosController(TestCase):
    def setUp(self):
        app_creator = AppCreator()
        self.app = app_creator.create_app()
        self.test_client = self.app.test_client()
        self.mock_wallet_service = MagicMock(WalletService)
        self.mock_wallet_class = MagicMock(
            WalletService, return_value=self.mock_wallet_service
        )

    def test_get_utxos(self):
        utxos_mock = [local_utxo_mock]
        get_all_utxos_mock = MagicMock(return_value=utxos_mock)
        with self.app.container.wallet_service.override(self.mock_wallet_service):
            self.mock_wallet_service.get_all_utxos = get_all_utxos_mock
            get_utxo_response = self.test_client.get("/utxos/")

            get_all_utxos_mock.assert_called_once()
            expected_utxos = [
                {
                    "txid": local_utxo_mock.outpoint.txid,
                    "vout": local_utxo_mock.outpoint.vout,
                    "amount": local_utxo_mock.txout.value,
                }
            ]

            assert get_utxo_response.status == "200 OK"
            assert json.loads(get_utxo_response.data) == {"utxos": expected_utxos}

    def test_get_fee_for_utxo_success(self):
        self.mock_fee_details = FeeDetails(0.1, 100)
        mock_get_fee_estimate_for_utxo = MagicMock(
            return_value=GetFeeEstimateForUtxoResponseType(
                "success", self.mock_fee_details
            )
        )
        with self.app.container.wallet_service.override(self.mock_wallet_service):
            self.mock_wallet_service.get_all_utxos.return_value = [local_utxo_mock]

            self.mock_wallet_service.get_fee_estimate_for_utxo = (
                mock_get_fee_estimate_for_utxo
            )

            fee_rate = 5
            transaction_id = local_utxo_mock.outpoint.txid
            vout = local_utxo_mock.outpoint.vout

            response = self.test_client.get(
                f"/utxos/fees/{transaction_id}/{vout}?feeRate={fee_rate}"
            )

            mock_get_fee_estimate_for_utxo.assert_called_with(
                local_utxo_mock, ScriptType.P2PKH, fee_rate
            )

            assert json.loads(response.data) == {
                "spendable": True,
                "percent_fee_is_of_utxo": self.mock_fee_details.percent_fee_is_of_utxo,
                "fee": self.mock_fee_details.fee,
            }

    def test_get_fee_for_utxo_unspendable_error(self):
        mock_get_fee_estimate_for_utxo = MagicMock(
            return_value=GetFeeEstimateForUtxoResponseType("unspendable", None)
        )
        with self.app.container.wallet_service.override(self.mock_wallet_service):
            self.mock_wallet_service.get_all_utxos.return_value = [local_utxo_mock]

            self.mock_wallet_service.get_fee_estimate_for_utxo = (
                mock_get_fee_estimate_for_utxo
            )

            fee_rate = 5
            transaction_id = local_utxo_mock.outpoint.txid
            vout = local_utxo_mock.outpoint.vout

            response = self.test_client.get(
                f"/utxos/fees/{transaction_id}/{vout}?feeRate={fee_rate}"
            )

            mock_get_fee_estimate_for_utxo.assert_called_with(
                local_utxo_mock, ScriptType.P2PKH, fee_rate
            )

            assert json.loads(response.data) == {
                "error": "unspendable",
                "spendable": False,
            }

    def test_get_fee_for_utxo_error(self):
        mock_get_fee_estimate_for_utxo = MagicMock(
            return_value=GetFeeEstimateForUtxoResponseType("error", None)
        )
        with self.app.container.wallet_service.override(self.mock_wallet_service):
            self.mock_wallet_service.get_all_utxos.return_value = [local_utxo_mock]

            self.mock_wallet_service.get_fee_estimate_for_utxo = (
                mock_get_fee_estimate_for_utxo
            )

            fee_rate = 5
            transaction_id = local_utxo_mock.outpoint.txid
            vout = local_utxo_mock.outpoint.vout

            response = self.test_client.get(
                f"/utxos/fees/{transaction_id}/{vout}?feeRate={fee_rate}"
            )

            mock_get_fee_estimate_for_utxo.assert_called_with(
                local_utxo_mock, ScriptType.P2PKH, fee_rate
            )

            assert json.loads(response.data) == {
                "error": "error getting fee estimate for utxo",
                "spendable": False,
            }
