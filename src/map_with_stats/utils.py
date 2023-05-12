__all__ = ["hectare2xy"]

from typing import List, Tuple

import pandas as pd
import shapely
import shapely.ops


def hectare2xy(df: pd.DataFrame, col_hectare: str = "hectare_id") -> pd.DataFrame:
    """Convert hectare ID into (x,y) coorsinates in the LV03 coordinate system.

    Args:
        df (pd.DataFrame): input table.
        col_hectare (str, optional): name of the column with hectare IDs.
            The common convention is that coordinates _x=ABCDEF_, _y=ZYXWVT_
            are represented by a hectare ID _ABCDZYXW_.
            Defaults to "hectare_id".

    Returns:
        pd.DataFrame: input table with _"X", "Y"_ columns added (or overwritten,
            if they existed in the input)
    """
    _check_cols_in_df(df, [col_hectare])
    df_out = df.copy(deep=True)
    df_out["X"] = df_out[col_hectare] // 10_000 * 100
    df_out["Y"] = df_out[col_hectare] % 10_000 * 100
    return df_out


def _check_cols_in_df(df: pd.DataFrame, cols: List[str]) -> None:
    """Check if the input table contains required columns.

    Args:
        df (pd.DataFrame): input table
        cols (List[str]): columns required in the table

    Raises:
        KeyError: some of the required columns are missing.
            The message tells what columns are mising and what are available.
    """
    cols_missing = [c for c in cols if c not in df]
    if cols_missing:
        raise KeyError(
            f"Columns {cols_missing} are missing among {df.columns.tolist()}"
        )


def _round_coordinates(
    geom: shapely.Geometry, n_digits_after_comma: int
) -> shapely.Geometry:
    """Round coordinates of Geometry to a fixed precision after the comma.

    This is useful if one plans to save a map containing those geometris in a text format
    (e.g. HTML) to optimise disk space.

    The code has been copied over from https://gis.stackexchange.com/a/432720/222760.

    Args:
        geom (shapely.Geometry): input geometries
        n_digits_after_comma (int): rounding precision

    Returns:
        shapely.Geometry: output geometries with reduced precision
    """

    def _round_coords(x: float, y: float) -> Tuple[float, float]:
        x = round(x, n_digits_after_comma)
        y = round(y, n_digits_after_comma)
        return (x, y)

    geom_transformed = shapely.ops.transform(_round_coords, geom)
    return geom_transformed
