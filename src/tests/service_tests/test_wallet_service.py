from unittest.case import TestCase
import os
from unittest.mock import MagicMock, patch
from src.services import WalletService
import bdkpython as bdk
from src.services.wallet.wallet import BuildTransactionResponseType
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

        self.outpoint_mock = OutpointType(txid="txid", vout=0)
        self.utxo_mock = TxOutType(
            value=1000,
            script_pubkey="mock_script_pubkey",
        )
        self.sats_per_vbyte_mock = 4
        self.raw_output_script_mock = ""
        with patch.object(
            WalletService, "connect_wallet", return_value=self.bdk_wallet_mock
        ):
            self.wallet_service = WalletService(wallet_descriptor, bdk.Network.TESTNET)

    def test_get_all_utxos(self):
        utxos = self.wallet_service.get_all_utxos()
        list_unspent: MagicMock = self.bdk_wallet_mock.list_unspent

        list_unspent.assert_called_with()
        assert utxos is self.unspent_utxos

    def test_build_transaction(self):
        tx_builder_mock = MagicMock()
        with patch.object(bdk, "TxBuilder", return_value=tx_builder_mock):
            built_transaction_mock = TxBuilderResultType(
                psbt="mock_psbt", transaction_details=transaction_details_mock
            )
            tx_builder_mock.add_utxos.return_value = tx_builder_mock
            tx_builder_mock.fee_rate.return_value = tx_builder_mock
            tx_builder_mock.add_recipient.return_value = tx_builder_mock

            tx_builder_mock.finish.return_value = built_transaction_mock

            build_transaction_response = self.wallet_service.build_transaction(
                [local_utxo_mock],
                self.sats_per_vbyte_mock,
                self.raw_output_script_mock,
            )
            assert build_transaction_response.status == "success"
            assert build_transaction_response.data is built_transaction_mock

    def test_build_transaction_with_insufficientFundsError(self):
        tx_builder_mock = MagicMock()
        with patch.object(bdk, "TxBuilder", return_value=tx_builder_mock):
            tx_builder_mock.add_utxos.return_value = tx_builder_mock
            tx_builder_mock.fee_rate.return_value = tx_builder_mock
            tx_builder_mock.add_recipient.return_value = tx_builder_mock
            tx_builder_mock.finish.side_effect = bdk.BdkError.InsufficientFunds()
            build_transaction_response = self.wallet_service.build_transaction(
                [local_utxo_mock],
                self.sats_per_vbyte_mock,
                self.raw_output_script_mock,
            )

            assert build_transaction_response.status == "unspendable"
            assert build_transaction_response.data == None

    def test_build_transaction_with_Error(self):
        mock_tx_builder = MagicMock()
        with patch.object(bdk, "TxBuilder", return_value=mock_tx_builder):
            mock_tx_builder.add_utxos.return_value = mock_tx_builder
            mock_tx_builder.fee_rate.return_value = mock_tx_builder
            mock_tx_builder.add_recipient.return_value = mock_tx_builder
            mock_tx_builder.finish.side_effect = Exception("error")

            build_transaction_response = self.wallet_service.build_transaction(
                [local_utxo_mock],
                self.sats_per_vbyte_mock,
                self.raw_output_script_mock,
            )

            assert build_transaction_response.status == "error"
            assert build_transaction_response.data == None

    def test_get_fee_estimate_for_utxos(self):
        tx_builder_mock = MagicMock()
        with patch.object(
            bdk, "TxBuilder", return_value=tx_builder_mock
        ) as mock_tx_builder:
            built_transaction_mock = TxBuilderResultType(
                psbt="mock_psbt", transaction_details=transaction_details_mock
            )
            tx_builder_mock.add_utxos.return_value = tx_builder_mock
            tx_builder_mock.fee_rate.return_value = tx_builder_mock
            tx_builder_mock.add_recipient.return_value = tx_builder_mock

            tx_builder_mock.finish.return_value = built_transaction_mock

            mock_tx_builder.return_value = tx_builder_mock

            fee_estimate_response = self.wallet_service.get_fee_estimate_for_utxos(
                [local_utxo_mock], ScriptType.P2PKH, 4
            )

            assert fee_estimate_response.status == "success"
            fee: int = cast(int, transaction_details_mock.fee)
            expected_fee_percent = (fee / (transaction_details_mock.sent + fee)) * 100
            assert fee_estimate_response.data == FeeDetails(expected_fee_percent, fee)

    def test_get_fee_estimate_for_utxo_with_build_tx_unspendable(self):
        build_transaction_error_response = BuildTransactionResponseType(
            "unspendable", None
        )
        with patch.object(
            WalletService,
            "build_transaction",
            return_value=build_transaction_error_response,
        ):
            get_fee_estimate_response = self.wallet_service.get_fee_estimate_for_utxos(
                [local_utxo_mock], ScriptType.P2PKH, 4
            )

            assert get_fee_estimate_response.status == "unspendable"
            assert get_fee_estimate_response.data == None

    def test_get_fee_estimate_for_utxo_with_build_tx_error(self):
        build_transaction_error_response = BuildTransactionResponseType("error", None)
        with patch.object(
            WalletService,
            "build_transaction",
            return_value=build_transaction_error_response,
        ):
            get_fee_estimate_response = self.wallet_service.get_fee_estimate_for_utxos(
                [local_utxo_mock], ScriptType.P2PKH, 4
            )

            assert get_fee_estimate_response.status == "error"
            assert get_fee_estimate_response.data == None
