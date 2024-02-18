import bdkpython as bdk
from typing import Tuple, Union
from src.types import (
    OutpointType,
    TxOutType,
    TransactionDetailsType,
    ScriptType,
    LocalUtxoType,
    TxBuilderResultType,
)
from src.services.wallet.raw_output_script_examples import (
    p2pkh_raw_output_script,
    p2pk_raw_output_script,
    p2sh_raw_output_script,
    p2wpkh_raw_output_script,
    p2wsh_raw_output_script,
)


class WalletService:
    def __init__(self):
        self.wallet = WalletService.connect_wallet()

    @classmethod
    def connect_wallet(cls) -> bdk.Wallet:
        descriptor = bdk.Descriptor(
            "wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)",
            bdk.Network.TESTNET,
        )

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

    def get_all_utxos(self):
        utxos = self.wallet.list_unspent()
        return utxos

    def build_transaction(
        self,
        outpoint: OutpointType,
        utxo: TxOutType,
        sats_per_vbyte: int,
        raw_output_script: str,
    ) -> Union[Tuple[str, TransactionDetailsType], None]:
        try:
            tx_builder = bdk.TxBuilder()
            tx_builder = tx_builder.add_utxo(outpoint)
            tx_builder = tx_builder.fee_rate(sats_per_vbyte)
            binary_script = bytes.fromhex(raw_output_script)

            script = bdk.Script(binary_script)
            # use half the amount of the utxo so that the transaction can be
            # created used alone for a single transaction
            # in other words so that the input amount can cover both
            # the amount and the fees
            transaction_amount = utxo.value / 2

            tx_builder = tx_builder.add_recipient(script, transaction_amount)
            built_transaction: TxBuilderResultType = tx_builder.finish(self.wallet)
            return (built_transaction.psbt, built_transaction.transaction_details)

        except Exception as e:
            print(f"Error adding utxo: {e}")
            return None

    def get_fee_estimate_for_utxo(
        self, local_utxo: LocalUtxoType, script_type: ScriptType, sats_per_vbyte: int
    ) -> Union[Tuple[float, int], None]:
        example_scripts = {
            ScriptType.P2PKH: p2pkh_raw_output_script,
            ScriptType.P2SH: p2sh_raw_output_script,
            ScriptType.P2WPKH: p2wpkh_raw_output_script,
            ScriptType.P2WSH: p2wsh_raw_output_script,
            ScriptType.P2PK: p2pk_raw_output_script,
        }
        example_script = example_scripts[script_type]
        tx_response = self.build_transaction(
            local_utxo.outpoint, local_utxo.txout, sats_per_vbyte, example_script
        )

        if tx_response is not None:
            (_, transaction) = tx_response
            fee = transaction.fee
            if fee is not None:
                percent_fee_is_of_utxo: float = (fee / local_utxo.txout.value) * 100
                return (percent_fee_is_of_utxo, fee)
        else:
            return None
