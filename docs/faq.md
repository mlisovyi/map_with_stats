## Why does one need to restrict the data?

!!! question
    The example in the [quick start quide](quick_start.md#usage-example) used a **subset of data for visualisation**.
    What is the reason and what shall I know about it?

The reason is that `folium` + `leaflet` do not seem to handle well large choropleth displayed.
On my laptop I managed to visualise 100k-200k hectares in a choropleth
and afterwards the map didn't open.

The way to work around this limitations could be:

* restrict displayed statistics to some area, for example around the starting point,
  like it has been done in the example
* do not constrain geographic location but restrict the choropleth to include only the top-N
  hectares. This can be achieved by providing `max_n_hectares_to_display` argument to `mws.build_map()`.
  This will identify an additional constraint _statistic value > X_ and use it to display
  only hectares with "large" statistics values.

## How to change the starting location and the zoom?

!!! question
    By default the map will be showing Zürich city.
    How could I change it?

The starting coordinates are passed as `coordinates_start` argument and the zoom as `zoom_start`.

## How to reduce the size of the HTML file?

!!! question
    The output HTML file could be large.
    Is there a way to reduce it?

Yes, one could use `optimise_choropleth_size` argument.
This will reduce precision of the longitude and latitude coordinates that are dumped as
floats with multiple digits after the comma into the HTML.
The rounding precision has been optimised to lead less than 1 meter bias in the LV03 coordinate system.

## How to optimise the color bar

!!! question
    The resulting color bar is too squeezed and does not deliver insights into differences between hectares.
    What can I do about it?

Typically this would happen for a very non-uniform distribution in the data, in particular
in the presence of outliers.
One could play with he following arguments:

* `bins_type`: choose between _"equidistant"_ and _"quantiles"_ that would define bins
  either on the linear or on the quantile scale.
* `clip_quantile`: this will define the quantile on both sides of the distribution to be
  clipped/winsorised. This would eliminate any outliers in long tails.

!!! question
    I have categorical data and the number of categories is higher than the number of colors.
    What can I do about it?

Use `n_bins` to define as many bins as there are categories.
`bins_type="equidistant"` would be optimal in this case.
