import os, sys

parent = os.path.abspath(".")
sys.path.insert(1, parent)


import bdkpython as bdk
from unittest import TestCase, mock
from src.injection import ServiceContainer
from src.services import WalletService
from src.app import AppCreator 


class TestBalanceController(TestCase):
    def setUp(self):
        self.mock_wallet_service = mock.Mock(WalletService)
        self.mock_online_wallet = mock.Mock(bdk.OnlineWallet)

        app_creator = AppCreator()
        self.app = app_creator.create_app()
        self.test_client = self.app.test_client()

    def test_hello_world_controller_returns_balance(self):
        with ServiceContainer.wallet_service.override(
            self.mock_wallet_service
        ), mock.patch.object(
            WalletService, "connect_wallet", return_value=self.mock_online_wallet
        ), mock.patch.object(
            self.mock_online_wallet, "get_balance", return_value="10000"
        ):

            response = self.test_client.get("/balance/")
            assert response.status == "200 OK"
            assert response.data == {"total": "10000", 
                                     "spendable: "1000", 
                                     "confirmed": "10000"}
