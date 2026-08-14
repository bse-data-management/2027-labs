import pandas as pd
import pytest
from trips import mean_fare


@pytest.mark.parametrize(
    "fares, expected",
    [
        ([10.0, 20.0], 15.0),
        ([10.0, None, 20.0], 15.0),
        ([5.0], 5.0),
    ],
)
def test_mean_fare(fares, expected):
    trips = pd.DataFrame({"fare": fares})
    assert mean_fare(trips) == expected
