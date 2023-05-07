__all__ = ["hectare2xy"]

from typing import List, Tuple

import pandas as pd
import shapely
import shapely.ops


def hectare2xy(df: pd.DataFrame, col_hectare: str = "hectare_id") -> pd.DataFrame:
    _check_cols_in_df(df, [col_hectare])
    df_out = df.copy(deep=True)
    df_out["X"] = df_out[col_hectare] // 10_000 * 100
    df_out["Y"] = df_out[col_hectare] % 10_000 * 100
    return df_out


def _check_cols_in_df(df: pd.DataFrame, cols: List[str]) -> None:
    cols_missing = [c for c in cols if c not in df]
    if cols_missing:
        raise KeyError(
            f"Columns {cols_missing} are missing among {df.columns.tolist()}"
        )


def _round_coordinates(
    geom: shapely.Geometry, n_digits_after_comma: int
) -> shapely.Geometry:
    def _round_coords(x: float, y: float) -> Tuple[float, float]:
        x = round(x, n_digits_after_comma)
        y = round(y, n_digits_after_comma)
        return (x, y)

    geom_transformed = shapely.ops.transform(_round_coords, geom)
    return geom_transformed
