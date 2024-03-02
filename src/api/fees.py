from dataclasses import dataclass
import requests


@dataclass
class FeeEstimates:
    low: int
    medium: int
    high: int


def get_fees() -> FeeEstimates:
    # Define the API endpoint URL
    # TODO make this some type of env variable
    url = "http://localhost:3000/fee-estimates"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            # TODO figure out how to fill the nigiri memool so that there is a fee market
            # todo also add better logging everywhere
            # todo add tests
            data = response.json()
            print("fee data gotten", data)
            # get in next block
            high = data.get("1", 1)
            # get in block in 2 hours
            medium = data.get("12", 1)
            # get in block in 24 hours
            low = data.get("144", 1)
            # Process the data as needed
            # todo use real data not mock data
            return FeeEstimates(low=low, medium=medium, high=high)
        else:
            # If the request was unsuccessful, print the error message
            print(f"Error: {response.status_code}")
            raise Exception("error")
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("making request to get fees failed")
