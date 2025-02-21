from modules.config import TILTPLAY
from modules.wallet import Wallet


class TiltPlay(Wallet):
    def __init__(self, pk, counter, proxy):
        super().__init__(pk, counter, proxy)

        self.label += "TiltPlay |"
        contract_abi = [
            {
                "type": "function",
                "name": "completeQuest",
                "inputs": [{"name": "arg", "type": "uint256"}],
            }
        ]
        self.contract = self.get_contract(TILTPLAY, abi=contract_abi)

    def check_in(self):
        contract_tx = self.contract.functions.completeQuest(0).build_transaction(
            self.get_tx_data()
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Check-in",
        )
