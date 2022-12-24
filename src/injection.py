from dependency_injector import containers, providers
from .services.wallet.wallet import WalletService


class ServiceContainer(containers.DeclarativeContainer):
    # containers.WiringConfiguration(packages=[".views"])
    wiring_config = containers.WiringConfiguration(modules=[".views.hello_world"])

    wallet_service = providers.Factory(WalletService)
