from datetime import datetime

from models.responses.user import User
from modules.config import OWLTO
from modules.logger import logger
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

    def get_user_data(self) -> User | bool:
        now = datetime.now()
        params = {"address": self.address, "year": now.year, "month": now.month}

        url = f"https://owlto.finance/api/lottery/maker/sign/user"
        resp = self.get(url, params=params)

        if resp.status_code != 200:
            logger.error(f"{self.label} {resp.text}")
            return False

        return User(**resp.json()["data"])

    def check_in(self):
        user: User = self.get_user_data()

        if user.isCheckIn:
            logger.warning(f"{self.label} Already checked-in today")
            return False

        date = int(datetime.now().strftime("%Y%m%d"))

        contract_tx = self.contract.functions.checkIn(date).build_transaction(
            self.get_tx_data()
        )

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.label} Check-in",
        )
