from unittest.case import TestCase
import os
from unittest.mock import MagicMock, patch
from src.services import WalletService
import bdkpython as bdk
from src.types.bdk_types import (
    FeeDetails,
    LocalUtxoType,
    OutpointType,
    TxBuilderResultType,
    TxOutType,
)
from src.types.script_types import ScriptType
from src.tests.mocks import local_utxo_mock, transaction_details_mock
from typing import cast


wallet_descriptor = os.getenv("WALLET_DESCRIPTOR", "")


class TestWalletService(TestCase):
    def setUp(self):
        self.bdk_wallet_mock = MagicMock()
        self.unspent_utxos: list[LocalUtxoType] = [local_utxo_mock]
        self.bdk_wallet_mock.list_unspent.return_value = self.unspent_utxos
        with patch.object(
            WalletService, "connect_wallet", return_value=self.bdk_wallet_mock
        ):
            self.wallet_service = WalletService(wallet_descriptor, bdk.Network.TESTNET)

    def test_get_all_utxos(self):
        utxos = self.wallet_service.get_all_utxos()
        list_unspent: MagicMock = self.bdk_wallet_mock.list_unspent

        list_unspent.assert_called_with()
        print("utxos: ", utxos)
        assert utxos is self.unspent_utxos

    def test_build_transaction(self):
        outpoint = OutpointType(txid="txid", vout=0)
        utxo = TxOutType(
            value=1000,
            script_pubkey="mock_script_pubkey",
        )
        sats_per_vbyte = 4
        raw_output_script = ""

        tx_builder_mock = MagicMock()
        with patch.object(
            bdk, "TxBuilder", return_value=tx_builder_mock
        ) as mock_tx_builder:
            built_transaction_mock = TxBuilderResultType(
                psbt="mock_psbt", transaction_details=transaction_details_mock
            )
            tx_builder_mock.add_utxo.return_value = tx_builder_mock
            tx_builder_mock.fee_rate.return_value = tx_builder_mock
            tx_builder_mock.add_recipient.return_value = tx_builder_mock

            tx_builder_mock.finish.return_value = built_transaction_mock

            mock_tx_builder.return_value = tx_builder_mock

            build_transaction_response = self.wallet_service.build_transaction(
                outpoint, utxo, sats_per_vbyte, raw_output_script
            )
            assert build_transaction_response.status == "success"
            assert build_transaction_response.data is built_transaction_mock

    def test_get_fee_estimate_for_utxo(self):
        tx_builder_mock = MagicMock()
        with patch.object(
            bdk, "TxBuilder", return_value=tx_builder_mock
        ) as mock_tx_builder:
            built_transaction_mock = TxBuilderResultType(
                psbt="mock_psbt", transaction_details=transaction_details_mock
            )
            tx_builder_mock.add_utxo.return_value = tx_builder_mock
            tx_builder_mock.fee_rate.return_value = tx_builder_mock
            tx_builder_mock.add_recipient.return_value = tx_builder_mock

            tx_builder_mock.finish.return_value = built_transaction_mock

            mock_tx_builder.return_value = tx_builder_mock

            fee_estimate_response = self.wallet_service.get_fee_estimate_for_utxo(
                local_utxo_mock, ScriptType.P2PKH, 4
            )

            assert fee_estimate_response.status == "success"
            fee: int = cast(int, transaction_details_mock.fee)
            expected_fee_percent = (fee / local_utxo_mock.txout.value) * 100
            assert fee_estimate_response.data == FeeDetails(expected_fee_percent, fee)
