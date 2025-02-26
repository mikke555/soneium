import random

import settings
from modules.config import (
    AWETH,
    SAFE_FINANCE,
    SAKE_FINANCE_ABI,
    SAKE_L2_POOL,
    SAKE_L2_POOL_ABI,
    WETH,
)
from modules.logger import logger
from modules.utils import ether, wei
from modules.wallet import Wallet


class SakeFinance(Wallet):
    def __init__(self, pk, _id, proxy):
        super().__init__(pk, _id, proxy)

        self.label += "Sake Finance |"
        self.contract = self.get_contract(SAFE_FINANCE, abi=SAKE_FINANCE_ABI)
        self.pool_contract = self.get_contract(SAKE_L2_POOL, abi=SAKE_L2_POOL_ABI)

    def get_supplied_balance(self):
        return self.get_balance(AWETH)

    def deposit_eth(self):
        aWETH_balance = self.get_supplied_balance()

        if aWETH_balance:
            logger.warning(
                f"{self.label} Already supplied {ether(aWETH_balance)} ETH \n"
            )
            return False

        amount_in = wei(random.uniform(*settings.SUPPLY_AMOUNT))

        contract_tx = self.contract.functions.depositETH(
            self.pool_contract.address, self.address, 0
        ).build_transaction(self.get_tx_data(value=amount_in))

        return self.send_tx(
            contract_tx,
            gas_multiplier=1.2,
            tx_label=f"{self.label} Deposit {ether(amount_in):.8f} ETH",
        )

    def toggle_collateral(self, use_as_collateral: bool = False):
        aWETH_balance = self.get_supplied_balance()

        if not aWETH_balance:
            logger.warning(f"{self.label} You need to supply collateral first \n")
            return False

        contract_tx = self.pool_contract.functions.setUserUseReserveAsCollateral(
            WETH, use_as_collateral
        ).build_transaction(self.get_tx_data())

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Set Collateral: {use_as_collateral}",
        )
