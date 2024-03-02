from src.api import get_fees
from src.api.fees import FeeEstimates


class FeeService:
    def current_fees(self) -> FeeEstimates:
        try:
            fees = get_fees()
            return fees

        except Exception:
            # todo what should this be
            raise Exception("making request to get fees failed")
