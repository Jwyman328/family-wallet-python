from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
from src.app import AppCreator
from src.services.wallet.wallet import WalletService
from src.tests.mocks import local_utxo_mock
import bdkpython as bdk
import json


# do I need the unittest.TestCase inheritance?
class TestUtxosController(TestCase):
    def setUp(self):
        app_creator = AppCreator()
        self.app = app_creator.create_app()
        self.test_client = self.app.test_client()
        self.mock_wallet_service = MagicMock(WalletService)
        self.mock_wallet_class = MagicMock(
            WalletService, return_value=self.mock_wallet_service
        )

        # self.mock_wallet_service = Mock(WalletService)
        self.mock_online_wallet = Mock(bdk.Wallet)

    def test_get_utxos(self):
        utxos_mock = [local_utxo_mock]
        get_all_utxos_mock = MagicMock(return_value=utxos_mock)
        with patch.object(WalletService, "connect_wallet", MagicMock), patch.object(
            WalletService, "get_all_utxos", get_all_utxos_mock
        ):
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

            get_utxo_response.status == "200 OK"
            print("get utxos response", get_utxo_response.data)
            assert json.loads(get_utxo_response.data) == {"utxos": expected_utxos}
