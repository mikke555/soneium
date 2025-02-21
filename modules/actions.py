import random

from .config import SONUS_TOKENS, VELODROME_TOKENS, WETH
from .owlto import Owlto
from .sonus import Sonus
from .tiltplay import TiltPlay
from .utils import get_random_token
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


def checkin_owlto(account):
    dapp = Owlto(**account)
    return dapp.check_in()


def checkin_tiltplay(account):
    dapp = TiltPlay(**account)
    return dapp.check_in()


def random_action(account):
    modules = [swap_velodrome, swap_sonus, wrap_eth, checkin_owlto, checkin_tiltplay]
    action = random.choice(modules)

    return action(account)
