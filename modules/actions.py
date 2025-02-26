import random

import settings

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
        return

    random_sleep(*settings.SLEEP_BETWEEN_ACTIONS)
    return dapp.toggle_collateral(use_as_collateral=True)


def supply_eth_sake(account):
    dapp = SakeFinance(**account)

    if not dapp.deposit_eth():
        return

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


def random_action(account):
    modules = [
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
        mint_arcas_champions,
    ]
    action = random.choice(modules)

    return action(account)
