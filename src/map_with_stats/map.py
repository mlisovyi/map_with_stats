from typing import List, Optional, Tuple, Union

import folium
import geopandas as gpd

from map_with_stats.utils import _check_cols_in_df, _round_coordinates


def build_map(
    gdf_stats: gpd.GeoDataFrame,
    title: str,
    bins_type: str,
    n_bins: int = 5,
    clip_quantile: Optional[float] = 0.01,
    map_tiles_provider: str = "OpenStreetMap",
    optimise_choropleth_size: bool = True,
    coordinates_start: Tuple[float, float] = (47.39, 8.53),
    zoom_start: int = 15,
    max_n_hectares_to_display: Optional[int] = None,
) -> folium.Map:
    _check_cols_in_df(gdf_stats, ["geometry", "value", "X", "Y"])

    # make a copy to avoid modifying input data in-place
    gdf = gdf_stats.copy(deep=True)

    ch_map = folium.Map(
        location=coordinates_start, zoom_start=zoom_start, tiles=map_tiles_provider
    )

    # optimise the number of hectares to be displayed as choropleth
    # display becomes very slow and sometimes stops work for a very large number fo elements
    if max_n_hectares_to_display:
        cumsum = gdf_stats["value"].value_counts().sort_index(ascending=False).cumsum()
        min_value = cumsum[cumsum <= max_n_hectares_to_display].index[-1]
        gdf = gdf[gdf["value"] >= min_value]
    # coordinates of the vetrices of hectares are stores with double precision,
    # that is more  than neccessary and will lead to wasted space, when stored in html
    # the number of digits after comma has been optimised to lead differences less than 1m in LV03 CRS
    if optimise_choropleth_size:
        gdf["geometry"] = gdf["geometry"].apply(
            _round_coordinates, n_digits_after_comma=6
        )
    # get values to be used for colors in the choropleth
    cliped_values = gdf["value"]
    if clip_quantile is not None:
        clip_min, clip_max = cliped_values.quantile((clip_quantile, 1 - clip_quantile))
        cliped_values = cliped_values.clip(clip_min, clip_max)
    # get either number of equidistant bins or bins defined by quantiles
    bins: Union[int, List[float]]
    if bins_type == "quantiles":
        quantiles = [i / (n_bins) for i in range(n_bins + 1)]
        bins = list(cliped_values.quantile(quantiles))
    elif bins_type == "equidistant":
        bins = n_bins
    else:
        raise ValueError(f"Unexpected type of bins: {bins_type}")

    # coloured square with the colour reflecting the statistics value
    choropleth = folium.Choropleth(
        geo_data=gdf,
        data=cliped_values,
        key_on="feature.id",  # index of the geodataframe is transformed into `id` field
        fill_color="YlOrBr",
        fill_opacity=0.6,
        bins=bins,
        line_weight=0,  # no line around hectare
        nan_fill_opacity=1,  # fully transparent hectares if the valueis mising
        legend_name=title,  # title under the color scale
        name=title,  # name of thew layer, e.g. in the layer control
    ).add_to(ch_map)

    # add tooltip to appear, when pointing at a hectar
    tooltip = folium.GeoJsonTooltip(
        # column names with values to be displayed
        fields=["X", "Y", "value"],
        # text to be shown explaining each value
        aliases=["LV03 X:", "LV03 Y:", f"{title}:"],
        localize=True,
        max_width=800,
    )
    tooltip.add_to(choropleth.geojson)

    folium.LayerControl().add_to(ch_map)
    return ch_map
