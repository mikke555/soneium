import random
import time

import settings
from modules.config import SONUS_ROUTER, SONUS_ROUTER_ABI
from modules.logger import logger
from modules.utils import ether, random_sleep, wei
from modules.wallet import Wallet


class Sonus(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "Sonus |"
        self.router = self.get_contract(SONUS_ROUTER, abi=SONUS_ROUTER_ABI)

    def _get_amount_out(self, amount_in: int, path: list[str], slippage: float = 0.05):
        amount_out = self.router.functions.getAmountsOut(amount_in, path).call()[1]
        min_amount_out = int(amount_out * (1 - slippage))

        if amount_out <= 0:
            raise ValueError("Invalid quoted amount")

        return min_amount_out

    def _get_tx_deadline(self):
        # Calculate roughly 55.2 years in seconds
        wait_time = int(55 + random.random() * 365.2425 * 86400)
        current_time = int(time.time())
        return current_time + wait_time

    def swap_eth(self, token_in: str, token_out: str):
        path = [token_in, token_out]
        amount_in = wei(random.uniform(*settings.SWAP_AMOUNT))
        amount_out = self._get_amount_out(amount_in, path)
        token_out_symbol = self.get_token(token_out, dict=True)["symbol"]

        contract_tx = self.router.functions.swapExactETHForTokens(
            amount_out, path, self.address, self._get_tx_deadline()
        ).build_transaction(self.get_tx_data(value=amount_in))

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Swap {ether(amount_in):.6f} ETH -> {token_out_symbol} [{self.tx_count}]",
            gas_multiplier=1.1,
        )

    def swap_erc20(self, token_in: str, token_out: str):
        balance, decimals, symbol = self.get_token(token_in)
        amount_in = int(balance * random.uniform(*settings.SWAP_BACK_PERCENTAGE))

        path = [token_in, token_out]
        amount_out = self._get_amount_out(amount_in, path)

        if not balance:
            logger.warning(f"{self.label} No {symbol} tokens to swap \n")
            return

        # Make approve
        tx_label = f"Approve {amount_in / 10 ** decimals:.6f} {symbol}"
        self.approve(
            token_in,
            self.router.address,
            amount_in,
            tx_label=f"{self.label} {tx_label} [{self.tx_count}]",
        )

        # Build transaction
        contract_tx = self.router.functions.swapExactTokensForETH(
            amount_in, amount_out, path, self.address, self._get_tx_deadline()
        ).build_transaction(self.get_tx_data())

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Swap {amount_in / 10**decimals:.8f} {symbol} -> ETH [{self.tx_count}]",
            gas_multiplier=1.1,
        )

    def swap(self, token_in, token_out):
        if not self.swap_eth(token_in, token_out):
            return

        token_in, token_out = token_out, token_in

        random_sleep(*settings.SLEEP_BETWEEN_ACTIONS)
        return self.swap_erc20(token_in, token_out)
