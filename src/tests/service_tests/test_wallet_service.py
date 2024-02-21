from unittest.case import TestCase
import os
from src.services import WalletService
import bdkpython as bdk
from src.types import OutpointType, TxOutType

# Get the value of a specific environment variable
wallet_descriptor = os.getenv("WALLET_DESCRIPTOR", "")
# TODO probably should mock the bdk stuff? That sure would be easier


class TestWalletService(TestCase):
    def setUp(self):
        self.wallet_service = WalletService(wallet_descriptor, bdk.Network.TESTNET)

    def test_connect_wallet(self):
        wallet = WalletService.connect_wallet(wallet_descriptor, bdk.Network.TESTNET)
        assert wallet is not None

    def test_get_all_utxos(self):
        # TODO figure out how to test this since using the database setup through ngiri.
        utxos = self.wallet_service.get_all_utxos()
        print("utxos: ", utxos)
        assert utxos is not None

    def test_build_transaction(self):
        # TODO finish this but lets first use mocking of bdk
        outpoint = OutpointType(txid="txid", vout=0)
        utxo = TxOutType(
            value=1000,
            script_pubkey="mock_script_pubkey",
        )
        sats_per_vbyte = 4
        raw_output_script = ""
        # built_transaction = self.wallet_service.build_transaction(
        #     outpoint, utxo, sats_per_vbyte, raw_output_script
        # )
        # assert built_transaction is not None
