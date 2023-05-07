import geopandas as gpd
import pandas as pd
import shapely

from map_with_stats.utils import _check_cols_in_df


def filter_xy(
    df: pd.DataFrame, ch_x_min: float, ch_y_min: float, ch_x_max: float, ch_y_max: float
) -> pd.DataFrame:
    _check_cols_in_df(df, ["X", "Y"])
    mask_x = df["X"].between(ch_x_min, ch_x_max)
    mask_y = df["Y"].between(ch_y_min, ch_y_max)
    mask_in_range = mask_x & mask_y
    return df[mask_in_range]


def create_geo_df_with_hectar_polygons(
    df: pd.DataFrame, col_value: str, crs_out: str = "EPSG:4326"
) -> gpd.GeoDataFrame:
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
