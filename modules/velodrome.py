import random

from eth_abi import encode
from eth_utils import to_bytes
from web3 import constants

import settings
from modules.config import (
    VELODROME_POOL_ABI,
    VELODROME_POOL_FACTORY,
    VELODROME_POOL_FACTORY_ABI,
    VELODROME_UNIVERSAL_ROUTER,
    VELODROME_UNIVERSAL_ROUTER_ABI,
)
from modules.logger import logger
from modules.utils import ether, random_sleep, wei
from modules.wallet import Wallet

commands = {"WRAP_SWAP": "0x0b00", "SWAP_UNWRAP": "0x000c"}
FEE_BIPS = 100  # 0.01% fee tier


class Velodrome(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "Velodrome |"
        self.router = self.get_contract(
            VELODROME_UNIVERSAL_ROUTER,
            abi=VELODROME_UNIVERSAL_ROUTER_ABI,
        )
        self.pool_factory = self.get_contract(
            VELODROME_POOL_FACTORY, abi=VELODROME_POOL_FACTORY_ABI
        )

    def _get_pool(self, token_in: str, token_out: str, stable=False) -> str:
        pool_address = self.pool_factory.functions.getPool(
            token_in, token_out, stable
        ).call()

        if pool_address == constants.ADDRESS_ZERO:
            logger.warning(f"No pool found")
            raise ValueError(f"No pool found")

        return pool_address

    def _get_amount_out(
        self, amount_in: int, token_in: str, token_out: str, slippage: float = 0.1
    ) -> int:
        token_in = self.w3.to_checksum_address(token_in)
        token_out = self.w3.to_checksum_address(token_out)

        pool_address = self._get_pool(token_in, token_out)
        pool_contract = self.get_contract(pool_address, abi=VELODROME_POOL_ABI)

        amount_out = pool_contract.functions.getAmountOut(amount_in, token_in).call()
        min_amount_out = int(amount_out * (1 - slippage))

        if amount_out <= 0:
            raise ValueError("Invalid quoted amount")

        return min_amount_out

    def _build_swap_path(self, token_in: str, token_out: str) -> bytes:
        return to_bytes(
            hexstr=self.w3.to_checksum_address(token_in)[2:].lower()
            + f"{FEE_BIPS:06x}"
            + self.w3.to_checksum_address(token_out)[2:].lower()
        )

    def _build_eth_swap(self, amount_in: int, token_in: str, token_out: str):
        """ETH → WETH → USDC swap construction"""
        # 1. Wrap ETH parameters
        wrap_params = encode(["address", "uint256"], [self.router.address, amount_in])

        # 2. Swap parameters
        path = self._build_swap_path(token_in, token_out)
        amount_out = self._get_amount_out(amount_in, token_in, token_out)

        swap_params = encode(
            ["address", "uint256", "uint256", "bytes", "bool"],
            [self.address, amount_in, amount_out, path, False],
        )

        return commands["WRAP_SWAP"], [wrap_params, swap_params], amount_in

    def _build_erc20_swap(self, amount_in: int, token_in: str, token_out: str):
        """USDC → WETH → ETH swap construction"""
        # 1. Swap parameters
        path = self._build_swap_path(token_in, token_out)
        amount_out = self._get_amount_out(amount_in, token_in, token_out)

        swap_params = encode(
            ["address", "uint256", "uint256", "bytes", "bool"],
            [self.router.address, amount_in, amount_out, path, True],
        )

        # 2. Unwrap parameters
        unwrap_params = encode(["address", "uint256"], [self.address, amount_out])

        return commands["SWAP_UNWRAP"], [swap_params, unwrap_params], 0

    def swap_eth(self, token_in: str, token_out: str):
        amount_in = wei(random.uniform(*settings.SWAP_AMOUNT))
        token_out_symbol = self.get_token(token_out, dict=True)["symbol"]

        commands, inputs, value = self._build_eth_swap(amount_in, token_in, token_out)

        contract_tx = self.router.functions.execute(commands, inputs).build_transaction(
            self.get_tx_data(value=value)
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Swap {ether(amount_in):.6f} ETH -> {token_out_symbol} [{self.tx_count}]",
            gas_multiplier=1.1,
        )

    def swap_erc20(self, token_in: str, token_out: str):
        balance, decimals, symbol = self.get_token(token_in)
        amount_in = int(balance * random.uniform(*settings.SWAP_BACK_PERCENTAGE))

        if not balance:
            logger.warning(f"{self.label} No {symbol} tokens to swap \n")
            return

        commands, inputs, value = self._build_erc20_swap(amount_in, token_in, token_out)

        tx_label = f"Approve {amount_in / 10 ** decimals:.6f} {symbol}"
        self.approve(
            token_in,
            self.router.address,
            amount_in,
            tx_label=f"{self.label} {tx_label} [{self.tx_count}]",
        )

        contract_tx = self.router.functions.execute(commands, inputs).build_transaction(
            self.get_tx_data(value=value)
        )

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
