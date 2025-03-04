import random

import questionary
from questionary import Choice

import settings
from modules.actions import *
from modules.logger import logger
from modules.utils import read_file, sleep


def get_action() -> str:
    choices = [
        Choice("Random action", random_action),
        Choice("Swap on Velodrome", swap_velodrome),
        Choice("Swap on Sonus", swap_sonus),
        Choice("Wrap/unwrap ETH", wrap_eth),
        Choice("Supply ETH on Sake Finance", supply_eth_sake),
        Choice("Toggle collateral on Sake Finance", toggle_collateral_sake),
        Choice("Create Asset Manager on Kyo Finance", create_asset_manager_kyo),
        Choice("Check-in with Owlto", checkin_owlto),
        Choice("Check-in with TiltPlay", checkin_tiltplay),
        Choice("Check-in with OnChainGM", send_gm_onchaingm),
        Choice("Mint Arcas Champions SBT", mint_arcas_champions),
        Choice("Mint OmniHub x Soneium", mint_omnihub),
        Choice(">>> Quit", "quit"),
    ]

    custom_style = questionary.Style(
        [
            ("qmark", "fg:#47A6F9 bold"),
            ("pointer", "fg:#47A6F9 bold"),
            ("selected", "fg:#47A6F9"),
            ("highlighted", "fg:#808080"),
            ("answer", "fg:#808080 bold"),
            ("instruction", "fg:#8c8c8c italic"),
        ]
    )

    action = questionary.select(
        "Action",
        choices=choices,
        style=custom_style,
    ).ask()

    if action == "quit" or action == None:
        quit()

    return action


def get_accounts() -> list[dict]:
    keys = read_file("keys.txt")
    proxies = read_file("proxies.txt", prefix="http://")

    if not keys:
        logger.warning("keys.txt is empty")
        quit()

    if not proxies and settings.USE_PROXY:
        logger.warning("proxies.txt is empty")
        quit()

    accounts = [
        {
            "pk": key,
            "proxy": proxies[index % len(proxies)] if settings.USE_PROXY else None,
            "_id": None,  # To be set after shuffling
        }
        for index, key in enumerate(keys)
    ]

    if settings.SHUFFLE_WALLETS:
        random.shuffle(accounts)

    for index, account in enumerate(accounts, start=1):
        account["_id"] = f"[{index}/{len(accounts)}]"

    return accounts


def run(action, account):
    try:
        return action(account)
    except Exception as err:
        logger.error(f"Error: {err}")


def main():
    action = get_action()
    accounts = get_accounts()

    for index, account in enumerate(accounts, start=1):
        tx_status = run(action, account)

        if tx_status and index < len(accounts):
            sleep(*settings.SLEEP_BETWEEN_WALLETS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Cancelled by user")
