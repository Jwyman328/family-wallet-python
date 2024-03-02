from dependency_injector import containers, providers
from src.services import WalletService, FeeService


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".views"])

    wallet_service = providers.Factory(WalletService)
    fee_service = providers.Factory(FeeService)
