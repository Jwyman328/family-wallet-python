from dependency_injector import containers, providers
from src.services import WalletService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".views"])

    wallet_service = providers.Factory(WalletService)
