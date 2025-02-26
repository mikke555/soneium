from modules.config import ONCHAINGM
from modules.utils import wei
from modules.wallet import Wallet


class OnChainGM(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "onChainGM |"
        self.value = 0.000029
        contract_abi = [{"type": "function", "name": "onChainGM", "inputs": []}]
        self.contract = self.get_contract(ONCHAINGM, abi=contract_abi)

    def send_gm(self):
        contract_tx = self.contract.functions.onChainGM().build_transaction(
            self.get_tx_data(value=wei(self.value))
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} send GM",
        )
