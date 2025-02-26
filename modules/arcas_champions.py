from modules.config import ARCAS_CHAMPIONS_SBT
from modules.logger import logger
from modules.wallet import Wallet


class ArcasChampions(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "Arcas Champions |"
        contract_abi = [{"type": "function", "name": "mint", "inputs": []}]
        self.contract = self.get_contract(ARCAS_CHAMPIONS_SBT, abi=contract_abi)

    @property
    def minted_qty(self) -> int:
        return self.get_balance(ARCAS_CHAMPIONS_SBT)

    def mint(self):
        if self.minted_qty > 0:
            logger.warning(f"{self.label} Already minted {self.minted_qty}\n")
            return False

        contract_tx = self.contract.functions.mint().build_transaction(
            self.get_tx_data()
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Mint",
        )
