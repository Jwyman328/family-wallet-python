from typing import Optional
from bdkpython import Network
from src.types.wallet import WalletDetails
from bdkpython import bdk
import structlog

LOGGER = structlog.get_logger()


class GlobalDataStore:
    def __init__(
        self,
        descriptor: Optional[str] = None,
        network: Network = bdk.Network.TESTNET,
        electrum_url="127.0.0.1:50000",
    ):
        self.wallet_details = WalletDetails(
            descriptor=descriptor, network=network, electrum_url=electrum_url
        )

    def set_global_descriptor(
        self,
        descriptor: str,
    ) -> str:
        """Set the flask app level global wallet_descriptor."""

        self.wallet_details.descriptor = descriptor
        LOGGER.info("Global wallet descriptor set", descriptor=descriptor)

        return descriptor
