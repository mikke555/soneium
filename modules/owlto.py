from datetime import datetime

from modules.config import OWLTO
from modules.wallet import Wallet


class Owlto(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "Owlto |"
        contract_abi = [
            {
                "type": "function",
                "name": "checkIn",
                "inputs": [{"name": "date", "type": "uint256"}],
            }
        ]
        self.contract = self.get_contract(OWLTO, abi=contract_abi)

    def check_in(self):
        date = int(datetime.now().strftime("%Y%m%d"))

        contract_tx = self.contract.functions.checkIn(date).build_transaction(
            self.get_tx_data()
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Check-in",
        )
