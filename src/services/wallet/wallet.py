from dataclasses import dataclass
import bdkpython as bdk
from typing import Literal, Optional, cast, List
from src.types import (
    OutpointType,
    ScriptType,
    LocalUtxoType,
    TxBuilderResultType,
    FeeDetails,
)
from src.services.wallet.raw_output_script_examples import (
    p2pkh_raw_output_script,
    p2pk_raw_output_script,
    p2sh_raw_output_script,
    p2wpkh_raw_output_script,
    p2wsh_raw_output_script,
)


@dataclass(frozen=True)
class BuildTransactionResponseType:
    status: Literal["success", "unspendable", "error"]
    data: Optional[TxBuilderResultType]


@dataclass(frozen=True)
class GetFeeEstimateForUtxoResponseType:
    status: Literal["success", "unspendable", "error"]
    data: Optional[FeeDetails]


class WalletService:
    def __init__(
        self,
        descriptor="wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)",
        network=bdk.Network.TESTNET,
        electrum_url="127.0.0.1:50000",
    ):
        self.wallet = WalletService.connect_wallet(descriptor, network, electrum_url)

    @classmethod
    def connect_wallet(
        cls,
        descriptor="wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)",
        network=bdk.Network.TESTNET,
        electrum_url="127.0.0.1:50000",
    ) -> bdk.Wallet:
        descriptor = bdk.Descriptor(descriptor, network)

        db_config = bdk.DatabaseConfig.MEMORY()
        blockchain_config = bdk.BlockchainConfig.ELECTRUM(
            bdk.ElectrumConfig(electrum_url, None, 5, None, 100, True)
        )

        blockchain = bdk.Blockchain(blockchain_config)

        wallet = bdk.Wallet(
            descriptor=descriptor,
            change_descriptor=None,
            network=network,
            database_config=db_config,
        )

        wallet.sync(blockchain, None)

        return wallet

    def get_all_utxos(self) -> List[LocalUtxoType]:
        utxos = self.wallet.list_unspent()
        return utxos

    def get_utxos_info(self, utxos_wanted: List[OutpointType]) -> List[LocalUtxoType]:
        existing_utxos = cast(List[LocalUtxoType], self.get_all_utxos())
        utxo_dict = {
            f"{utxo.outpoint.txid}_{utxo.outpoint.vout}": utxo
            for utxo in existing_utxos
        }

        utxos_wanted_that_exist = []
        for utxo in utxos_wanted:
            utxo_key = f"{utxo.txid}_{utxo.vout}"
            if utxo_dict[utxo_key]:
                utxos_wanted_that_exist.append(utxo_dict[utxo_key])

        return utxos_wanted_that_exist

    def build_transaction(
        self,
        utxos: List[LocalUtxoType],
        sats_per_vbyte: int,
        raw_output_script: str,
    ) -> BuildTransactionResponseType:
        try:
            tx_builder = bdk.TxBuilder()
            outpoints = [utxo.outpoint for utxo in utxos]
            tx_builder = tx_builder.add_utxos(outpoints)
            tx_builder = tx_builder.fee_rate(sats_per_vbyte)
            binary_script = bytes.fromhex(raw_output_script)

            script = bdk.Script(binary_script)

            # use half the amount of the utxo so that the transaction can be
            # created used alone for a single transaction
            # in other words so that the input amount can cover both
            # the amount and the fees
            total_utxos_amount = sum(utxo.txout.value for utxo in utxos)
            transaction_amount = total_utxos_amount / 2

            tx_builder = tx_builder.add_recipient(script, transaction_amount)
            built_transaction: TxBuilderResultType = tx_builder.finish(self.wallet)
            return BuildTransactionResponseType(
                "success",
                built_transaction,
            )

        except bdk.BdkError.InsufficientFunds:
            return BuildTransactionResponseType("unspendable", None)
        except Exception as e:
            print(f"Error adding utxo: {e}")
            return BuildTransactionResponseType("error", None)

    def get_fee_estimate_for_utxos(
        self,
        local_utxos: List[LocalUtxoType],
        script_type: ScriptType,
        sats_per_vbyte: int,
    ) -> GetFeeEstimateForUtxoResponseType:
        example_scripts = {
            ScriptType.P2PKH: p2pkh_raw_output_script,
            ScriptType.P2SH: p2sh_raw_output_script,
            ScriptType.P2WPKH: p2wpkh_raw_output_script,
            ScriptType.P2WSH: p2wsh_raw_output_script,
            ScriptType.P2PK: p2pk_raw_output_script,
        }

        example_script = example_scripts[script_type]
        tx_response = self.build_transaction(
            local_utxos, sats_per_vbyte, example_script
        )

        if tx_response.status == "success" and tx_response.data is not None:
            built_transaction = tx_response.data
            fee = built_transaction.transaction_details.fee

            if fee is not None:
                total = fee + built_transaction.transaction_details.sent
                percent_fee_is_of_utxo: float = (fee / total) * 100
                return GetFeeEstimateForUtxoResponseType(
                    "success", FeeDetails(percent_fee_is_of_utxo, fee)
                )
            else:
                return GetFeeEstimateForUtxoResponseType("error", None)
        else:
            return GetFeeEstimateForUtxoResponseType(tx_response.status, None)
