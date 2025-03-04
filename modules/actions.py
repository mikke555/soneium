import random

import settings
from modules.logger import logger

from .arcas_champions import ArcasChampions
from .config import SONUS_TOKENS, VELODROME_TOKENS, WETH
from .gm import OnChainGM
from .kyo_finance import KyoFinance
from .omnihub import OmniHub
from .owlto import Owlto
from .sake_finance import SakeFinance
from .sonus import Sonus
from .tiltplay import TiltPlay
from .utils import get_random_token, random_sleep
from .velodrome import Velodrome
from .wrapper import Wrapper


def swap_velodrome(account):
    dapp = Velodrome(**account)

    token_in = WETH
    token_out = get_random_token(VELODROME_TOKENS)

    return dapp.swap(token_in, token_out)


def swap_sonus(account):
    dapp = Sonus(**account)

    token_in = WETH
    token_out = get_random_token(SONUS_TOKENS)

    return dapp.swap(token_in, token_out)


def wrap_eth(account):
    dapp = Wrapper(**account)
    return dapp.deposit_and_redeem()


def toggle_collateral_sake(account):
    dapp = SakeFinance(**account)

    if not dapp.toggle_collateral():
        return False

    random_sleep(*settings.SLEEP_BETWEEN_ACTIONS)
    return dapp.toggle_collateral(use_as_collateral=True)


def supply_eth_sake(account):
    dapp = SakeFinance(**account)

    if not dapp.deposit_eth():
        return False

    random_sleep(*settings.SLEEP_BETWEEN_ACTIONS)
    return toggle_collateral_sake(account)


def checkin_owlto(account):
    dapp = Owlto(**account)
    return dapp.check_in()


def checkin_tiltplay(account):
    dapp = TiltPlay(**account)
    return dapp.check_in()


def mint_omnihub(account):
    dapp = OmniHub(**account)
    return dapp.mint()


def send_gm_onchaingm(account):
    dapp = OnChainGM(**account)
    return dapp.send_gm()


def create_asset_manager_kyo(account):
    dapp = KyoFinance(**account)
    return dapp.create_asset_manager()


def mint_arcas_champions(account):
    dapp = ArcasChampions(**account)
    return dapp.mint()


class RandomActionSelector:
    """Selects and executes a random action until one returns a value other than False."""

    def __init__(self):
        self.modules = [
            swap_velodrome,
            swap_sonus,
            wrap_eth,
            toggle_collateral_sake,
            supply_eth_sake,
            checkin_owlto,
            checkin_tiltplay,
            mint_omnihub,
            send_gm_onchaingm,
            create_asset_manager_kyo,
            # mint_arcas_champions,  # mint closed
        ]

    def __call__(self, account):
        available_modules = self.modules.copy()
        random.shuffle(available_modules)

        for action in available_modules:
            try:
                result = action(account)
            except Exception as e:
                logger.error(f"Action {action.__name__} failed with error: {e} \n")
                continue

            if result is not False:
                return result

        return False  # All actions have returned False


random_action = RandomActionSelector()
