import geopandas as gpd
import pandas as pd
import shapely

from map_with_stats.utils import _check_cols_in_df


def filter_xy(
    df: pd.DataFrame, ch_x_min: float, ch_y_min: float, ch_x_max: float, ch_y_max: float
) -> pd.DataFrame:
    """Filter input data to be within range of X and Y coordinates.

    Args:
        df (pd.DataFrame): inout data. The code expects to find the following columns: _"X", "Y"_.
        ch_x_min (float): minimum value of X
        ch_y_min (float): minimum value of Y
        ch_x_max (float): maximum value of X
        ch_y_max (float): maximum value of Y

    Returns:
        pd.DataFrame: input data with the restricted _"X", "Y"_ values
    """
    _check_cols_in_df(df, ["X", "Y"])
    mask_x = df["X"].between(ch_x_min, ch_x_max)
    mask_y = df["Y"].between(ch_y_min, ch_y_max)
    mask_in_range = mask_x & mask_y
    return df[mask_in_range]


def create_geo_df_with_hectar_polygons(
    df: pd.DataFrame, col_value: str, crs_out: str = "EPSG:4326"
) -> gpd.GeoDataFrame:
    """Given a pandas dataframe with _"X", "Y"_ coordinates of the bottom-left (south-west) corner
    of the hectares and a column `col_value` with values, create a geopandas geodataframe with
    hectare polygons and the selected column with values

    Args:
        df (pd.DataFrame): input data. The code expects to find the following columns: _"X", "Y", `col_value`_.
        col_value (str): column name with some values
        crs_out (_type_, optional): coordinate system to which output polygons are transformed.
            Defaults to "EPSG:4326".

    Returns:
        gpd.GeoDataFrame: a table with hectare polygons and the values.
    """
    _check_cols_in_df(df, ["X", "Y", col_value])
    polygons = []
    for row in df.itertuples():
        x, y = row.X, row.Y
        polygons.append(
            shapely.Polygon([(x, y), (x + 100, y), (x + 100, y + 100), (x, y + 100)])
        )
    gdf_stats = gpd.GeoDataFrame(
        {
            "geometry": polygons,
            "value": df[col_value],
            "hectare_id": df["X"] // 100 * 10_000 + df["Y"] // 100,
            "X": df["X"],
            "Y": df["Y"],
        },
        index=df.index,
        crs="EPSG:21781",  # LV03 coordinate system
    )
    # transform into the desired coordinate system
    gdf_stats = gdf_stats.to_crs(crs_out)
    return gdf_stats
