from modules.config import OMNIHUB
from modules.logger import logger
from modules.utils import wei
from modules.wallet import Wallet


class OmniHub(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "OmniHub x Soneium |"
        self.value = 0.0003
        contract_abi = [
            {
                "type": "function",
                "name": "mint",
                "inputs": [{"name": "mintAmount", "type": "uint256"}],
            }
        ]
        self.contract = self.get_contract(OMNIHUB, abi=contract_abi)

    @property
    def minted_qty(self) -> int:
        return self.get_balance(OMNIHUB)

    def mint(self):
        if self.minted_qty > 0:
            logger.warning(f"{self.label} Already minted {self.minted_qty}\n")
            return False

        contract_tx = self.contract.functions.mint(1).build_transaction(
            self.get_tx_data(value=wei(self.value))
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Mint",
        )
