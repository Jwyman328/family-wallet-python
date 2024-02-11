import bdkpython as bdk


class WalletService:
    def __init__(self):
        self.wallet = WalletService.connect_wallet()

    @classmethod
    def connect_wallet(cls) -> bdk.Wallet:
        descriptor = bdk.Descriptor("wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)", bdk.Network.TESTNET)

        db_config = bdk.DatabaseConfig.MEMORY()
        blockchain_config = bdk.BlockchainConfig.ELECTRUM(
            bdk.ElectrumConfig("127.0.0.1:50000", None, 5, None, 100, True)
        )

        blockchain = bdk.Blockchain(blockchain_config)

        wallet = bdk.Wallet(
            descriptor=descriptor,
            change_descriptor=None,
            network=bdk.Network.TESTNET,
            database_config=db_config,
        )

        address_info = wallet.get_address(bdk.AddressIndex.LAST_UNUSED())

        print(f"New BIP84 testnet address: {address_info}")


        wallet.sync(blockchain, None)
        balance = wallet.get_balance()
        print(f"Wallet balance is: {balance.total}")

        return wallet
