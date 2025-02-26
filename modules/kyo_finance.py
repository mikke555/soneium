from web3 import constants

from modules.config import KYO_ASSET_MANAGER_ABI, KYO_FINANCE
from modules.logger import logger
from modules.wallet import Wallet


class KyoFinance(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "Kyo Finance |"
        self.contract = self.get_contract(KYO_FINANCE, abi=KYO_ASSET_MANAGER_ABI)

    def get_asset_manager(self) -> str:
        return self.contract.functions.getPersonalAssetManager(self.address).call()

    def create_asset_manager(self):
        mgr = self.get_asset_manager()

        if mgr != constants.ADDRESS_ZERO:
            logger.warning(f"{self.label} Personal Asset Manager already exists \n")
            return False

        contract_tx = self.contract.functions.create(self.address).build_transaction(
            self.get_tx_data()
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Create Asset Manager",
        )
