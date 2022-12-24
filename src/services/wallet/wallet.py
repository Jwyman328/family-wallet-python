import bdkpython as bdk
from functools import wraps


def start_bdk() -> bdk.OnlineWallet:
    descriptor = "wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)"
    db_config = bdk.DatabaseConfig.MEMORY("my junk")
    blockchain_config = bdk.BlockchainConfig.ELECTRUM(
        bdk.ElectrumConfig("127.0.0.1:50000", None, 5, None, 100)
    )

    wallet = bdk.OnlineWallet(
        descriptor,
        blockchain_config=blockchain_config,
        change_descriptor=None,
        network=bdk.Network.REGTEST,
        database_config=db_config,
    )

    address_info = wallet.get_new_address()

    print(f"New BIP84 testnet address: {address_info}")

    # print wallet balance
    class MyProgress(bdk.BdkProgress):
        def update(self, progress, message):
            print("the progress", progress, "and the message", message)

    wallet.sync(MyProgress(), 120)
    balance = wallet.get_balance()
    print(f"Wallet balance is: {balance}")

    return wallet


def wallet_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        wallet = start_bdk()
        return f(wallet=wallet, *args, **kwargs)

    return decorated_function


class WalletService:
    def __init__(self):
        # self.wallet = WalletService.connect_wallet()
        self.hi = "hi"
        # print("got a wallet?", self.wallet)

    @classmethod
    def connect_wallet() -> bdk.OnlineWallet:
        descriptor = "wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)"

        db_config = bdk.DatabaseConfig.MEMORY("my junk")
        blockchain_config = bdk.BlockchainConfig.ELECTRUM(
            bdk.ElectrumConfig("127.0.0.1:50000", None, 5, None, 100)
        )

        wallet = bdk.OnlineWallet(
            descriptor,
            blockchain_config=blockchain_config,
            change_descriptor=None,
            network=bdk.Network.REGTEST,
            database_config=db_config,
        )

        address_info = wallet.get_new_address()

        print(f"New BIP84 testnet address: {address_info}")

        # print wallet balance
        class MyProgress(bdk.BdkProgress):
            def update(self, progress, message):
                print("the progress", progress, "and the message", message)

        wallet.sync(MyProgress(), 120)
        balance = wallet.get_balance()
        print(f"Wallet balance is: {balance}")

        return wallet

    def get_hi(self):
        return self.hi
