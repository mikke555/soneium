import random

import settings
from modules.config import WETH
from modules.logger import logger
from modules.utils import random_sleep, wei
from modules.wallet import Wallet


class Wrapper(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "WETH |"
        contract_abi = [
            {"type": "function", "name": "deposit", "inputs": []},
            {
                "type": "function",
                "name": "withdraw",
                "inputs": [{"name": "amount", "type": "uint256"}],
            },
        ]
        self.contract = self.get_contract(WETH, abi=contract_abi)

    def deposit(self):
        amount = wei(random.uniform(*settings.WRAP_AMOUNT))

        contract_tx = self.contract.functions.deposit().build_transaction(
            self.get_tx_data(value=amount)
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Deposit {amount / 10**18:.6f} WETH",
        )

    def redeem(self):
        balance, decimals, symbol = self.get_token(self.contract.address)
        amount = balance

        if not balance:
            logger.warning(f"{self.label} no {symbol} balance to withdraw \n")
            return

        contract_tx = self.contract.functions.withdraw(amount).build_transaction(
            self.get_tx_data()
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Redeem {amount / 10 ** decimals:.6f} {symbol}",
        )

    def deposit_and_redeem(self):
        if not self.deposit():
            return

        random_sleep(*settings.SLEEP_BETWEEN_ACTIONS)
        return self.redeem()
