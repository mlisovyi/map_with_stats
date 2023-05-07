import geopandas as gpd
import numpy as np
import pandas as pd
import pytest

import map_with_stats as mws
from map_with_stats.utils import _check_cols_in_df


@pytest.fixture
def dummy_data() -> pd.DataFrame:
    np.random.seed(42)
    n = 1000
    X = np.random.randint(1_000, 10_000, size=n)
    Y = np.random.randint(1_000, 10_000, size=n)
    df = pd.DataFrame({"X": X * 100, "Y": Y * 100, "V": 0})
    return df


def test_create_geo_df_with_hectar_polygons(dummy_data):
    gdf = mws.create_geo_df_with_hectar_polygons(dummy_data, "V", "EPSG:21781")
    # validate that new as well as original columns are in place
    _check_cols_in_df(gdf, ["geometry", "value", "hectare_id"])
    # check output type
    assert isinstance(gdf, gpd.GeoDataFrame)
    # check that geometry contains hectares
    areas = gdf["geometry"].area
    area_diff = (areas - 10_000).abs()
    assert (area_diff <= 1).all()
