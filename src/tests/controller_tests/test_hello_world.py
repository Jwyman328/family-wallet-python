import os, sys

parent = os.path.abspath(".")
sys.path.insert(1, parent)


import bdkpython as bdk
from unittest import TestCase, mock
from src.injection import ServiceContainer
from src.services.wallet.wallet import WalletService
from src.app import create_app


class TestHelloWorldController(TestCase):
    def setUp(self):
        self.mock_wallet_service = mock.Mock(WalletService)
        self.mock_online_wallet = mock.Mock(bdk.OnlineWallet)

        self.app = create_app()
        self.test_client = self.app.test_client()

    def test_hello_world_controller_returns_balance(self):
        with ServiceContainer.wallet_service.override(
            self.mock_wallet_service
        ), mock.patch.object(
            WalletService, "connect_wallet", return_value=self.mock_online_wallet
        ), mock.patch.object(
            self.mock_online_wallet, "get_balance", return_value="10000"
        ):

            response = self.test_client.get("/worlds/")
            assert response.status == "200 OK"
            assert response.data == b"Wallet balance is: 10000"
