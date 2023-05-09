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


The package allows to display an **interactive map with a choropleth
displaying some statistics as color per hectare** (100x100 meter square).

![Example map](https://github.com/mlisovyi/map_with_stats/raw/main/docs/figs/map_screenshot.jpeg)

!!! question "What is the use-case?"

      The typical use-case would be to visualise and do plausibility checks of hectare-level data
      as well as to compare statistics between geographic areas.

The package is created and tested to work for the **Switzerland coordinates**,
however, one could try to use it for any other map with hectare statistics.


Read about usage in [Quick start guide](https://mlisovyi.github.io/map_with_stats/quick_start)