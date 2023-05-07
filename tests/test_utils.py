import pandas as pd
import pytest

import map_with_stats as mws
from map_with_stats.utils import _check_cols_in_df


@pytest.mark.parametrize(
    "hectare_id, x, y", [(6000_4000, 6000_00, 4000_00), (4000_6000, 4000_00, 6000_00)]
)
def test(hectare_id, x, y):
    df = pd.DataFrame({"hid": [hectare_id], "dummy": ["dummy"]})
    df = mws.hectare2xy(df, "hid")
    # validate that new as well as original columns are in place
    _check_cols_in_df(df, ["X", "Y", "hid", "dummy"])
    # validate extracted values
    assert df["X"].item() == x
    assert df["Y"].item() == y
