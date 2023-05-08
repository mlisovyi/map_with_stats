# Map with statistics


<!-- [![coverage report](https://git.intern.migros.net/analytics/optimizers/store_profile_common/badges/main/coverage.svg)](https://git.intern.migros.net/analytics/optimizers/store_profile_common/-/commits/main) -->
[![release @ PYPI](http://img.shields.io/pypi/v/map_with_stats?color=brightgreen&logo=pypi&logoColor=949DA5)](https://pypi.python.org/pypi/map_with_stats)
[![python version](https://img.shields.io/badge/python-3.7,3.8,3.9,3.10,3.11-blue.svg?logo=python&logoColor=949DA5)](https://www.python.org/downloads/)
![platform](https://img.shields.io/badge/platform-linux%20|%20macos%20|%20windows-lightgray.svg)
[![CI status](https://github.com/mlisovyi/map_with_stats/actions/workflows/test.yml/badge.svg?labelColor=555555?event=push)](https://github.com/mlisovyi/map_with_stats)
[![Docs status](https://github.com/mlisovyi/map_with_stats/actions/workflows/docs.yml/badge.svg)](https://github.com/mlisovyi/map_with_stats)
[![linter](https://img.shields.io/badge/code%20linting-pylint-blue.svg)](https://github.com/PyCQA/pylint)
[![testing](https://img.shields.io/badge/code%20testing-pytest-blue.svg)](https://github.com/pytest-dev/pytest)
[![typing](https://img.shields.io/badge/code%20typing-mypy-blue.svg)](http://mypy-lang.org/)
[![docs](https://img.shields.io/badge/documentation-mkdocs--material-blue.svg)](https://squidfunk.github.io/mkdocs-material/)
[![versioning](https://img.shields.io/badge/versioning-setuptools--scm-blue.svg)](https://github.com/pypa/setuptools_scm)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![documentation](https://img.shields.io/badge/_-documentation-blueviolet?logo=githubpages)](https://mlisovyi.github.io/map_with_stats)


The package allows to display an interactive map with a choropleth
displaying some statistics as color per hectare (100x100 meter square).

The package is created and tested to work for the **Switzerland coordinates**,
however, one could try to use it for any other map with hectare statistics.

![Example map](https://github.com/mlisovyi/map_with_stats/raw/main/docs/figs/map_screenshot.png)


## Installation

```bash
pip install map_with_stats
```

## Quick guide

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
   # `hectare2xy` is a helper function that extracts X,Y coordinates from the hectare ID
   data = mws.hectare2xy(data, "RELI")
   # `create_geo_df_with_hectar_polygons` is a helper function that creates GeoDataFrame with a polygon for each hectare
   gdf_stats = mws.create_geo_df_with_hectar_polygons(data, "B21BTOT", crs_out="EPSG:4326")

   # restrict data to the Zürich neighbourhood - this step is optional
   mask_x = data["X"].between(6700_00, 7000_00)
   mask_y = data["Y"].between(2330_00, 2630_00)
   gdf = gdf_stats[mask_x & mask_y]

   # `build_map` is the main helper function that will create a map with a coropleth layer
   title = "Dummy data"  # the to be used as data description in the tooltip and colormap
   map = mws.build_map(gdf, title, "equidistant", n_bins=5)
   map.save("map.html")
   ```
