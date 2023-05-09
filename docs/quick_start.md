## Installation

```bash
pip install map_with_stats
```

## Usage example

For visualisation you will need some statistics per hectare.
Individual hectares are defined by the X,Y coordinates
in the [LV03](https://en.wikipedia.org/wiki/Swiss_coordinate_system#LV03) coordinate system
of the bottom-left (=south-west) corner.

1. Such data could be for example downloaded from
   the [BFS website](https://www.bfs.admin.ch/bfs/de/home/dienstleistungen/geostat/geodaten-bundesstatistik).
   * For example, one can get population data per hectare for year 2021 from
     [here](https://www.bfs.admin.ch/bfs/de/home/dienstleistungen/geostat/geodaten-bundesstatistik/gebaeude-wohnungen-haushalte-personen/bevoelkerung-haushalte-ab-2010.assetdetail.23528269.html).
2. Download and extract _STATPOP2021.csv_ from the archive.
3. Generate the HTML with the map:
   ```python
   import pandas as pd

   import map_with_stats as mws


   data_raw = pd.read_csv("STATPOP2021.csv", sep=";")
   data = data_raw[["RELI", "B21BTOT"]]
   data = mws.hectare2xy(data, "RELI")  # (1)!
   gdf_stats = mws.create_geo_df_with_hectar_polygons(data, "B21BTOT", crs_out="EPSG:4326")  # (2)!

   # restrict data to the Zürich neighbourhood
   mask_x = data["X"].between(6700_00, 7000_00)
   mask_y = data["Y"].between(2330_00, 2630_00)
   gdf = gdf_stats[mask_x & mask_y]  # (3)!

   # `build_map` is the main helper function that will create a map with a coropleth layer
   title = "Dummy data"  # (4)!
   map = mws.build_map(gdf, title , "equidistant")
   map.save("map.html")
   ```
      1. `hectare2xy` is a helper function that extracts X,Y coordinates from the hectare ID
      2. `create_geo_df_with_hectar_polygons` is a helper function that creates GeoDataFrame with a polygon for each hectare
      3. This step is optional- read FAQ for more details
      4.  Title will be used as data description in the tooltip and colormap