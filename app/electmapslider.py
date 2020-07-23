# imports
import geopandas as gpd
import pandas as pd
import json
from bokeh.io import show, curdoc
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool, TapTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.models.widgets import RadioButtonGroup, Slider, RangeSlider, Tabs
import time



def make_dataset(cnt_data, yr, shouldGetAll):
    merged_select = []

    # create 2000 election year data frame
    if shouldGetAll:
        merged_select = cnt_data
    else:
        yr_selected = cnt_data["YEAR"] == yr
        merged_select = cnt_data[yr_selected]

    # Bokeh uses geojson formatting, representing geographical features, with json
    # Convert to json
    merged_json = json.loads(merged_select.to_json())
    #Convert to json preferred string like object
    json_data = json.dumps(merged_json)
    # input GeoJSON source that contains features for plotting
    #geosource_select = GeoJSONDataSource(geojson = merged_select.to_json())
    return(json_data)

def make_plot(geo_src):
    # define color palettes
    palette = brewer["RdYlBu"][8]

    # use reverse order so higher values are darker
    palette = palette[::-1]

    # instantiate LineraColorMapper and manually set low/high end for colorbar
    color_mapper = LinearColorMapper(palette = palette, low = 1,
                                 high = 0)
    # #TapTool
    # tap = TapTool()
    # states_usa = gpd.read_file("bokeh/cb_2018_us_state_20m.shp")
    # states_usa = states_usa.loc[~states_usa["NAME"].isin(["Alaska", "Hawaii"])]
    # geosource_states = GeoJSONDataSource(geojson = states_usa.to_json())
    # def function_geosource(attr, old, new):
    #     try:
    #         selected_index = geosource_states.selected.indices[0]
    #         state_name = states_usa.iloc[selected_index]['NAME']
    #         print(state_name)
    #     except IndexError:
    #         pass
    # geosource_states.selected.on_change('indices', function_geosource)

    # create figure object
    plot = figure(title = "Republican or Democrat Win by County in Presidential Election",
           plot_height = 600, plot_width = 950,
           toolbar_location = "below",
           tools = "pan, wheel_zoom, reset",
           output_backend="webgl")
           # tools = "pan, wheel_zoom, reset, tap")

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    # plot.patches("xs","ys", source = geosource_states, fill_alpha=0.0,
    #             line_color="#884444", line_width=2, line_alpha=0.3)
    # add patch renderer to figure
    counties = plot.patches("xs","ys", source = geo_src,
                       fill_color = {'field' :'WINNING_PARTY_BINARY', 'transform' : color_mapper},
                       line_color = "gray",
                       line_width = 0.25,
                       fill_alpha = 1)
    # create hover tool
    plot.add_tools(HoverTool(renderers = [counties],
                      tooltips = [("County","@NAME"),
                               ("Rep Votes", "@REP_VOTES"), ("Dem Votes","@DEM_VOTES")]))
    return plot

def update(attr, old, new):
        new_src = make_dataset(int(new))

        geo_src.geojson = new_src

        p = make_plot()
        controls = WidgetBox(year_select)
        layout = row(p, controls)
        curdoc().clear()
        curdoc().add_root(layout)

def init_data():
    start = time.time()

    print('init_data()')

    # read in combined dataset
    combined_df = pd.read_csv("data/elections/Input_Output_Jul07.csv", encoding = "ISO-8859-1")

    #winning_party_binary = pd.get_dummies(combined_df["WINNING_PARTY"], drop_first = True)
    #combined_df["WINNING_PARTY_BINARY"] = winning_party_binary
    combined_df['FIPS']=combined_df['STATE_FIPS']*1000 + combined_df['COUNTY_FIPS']
    combined_df = combined_df.loc[~combined_df["STATE_FIPS"].isin( [2, 15])]
    # read in counties shapefile from US Census Bureau
    counties_usa = gpd.read_file("bokeh/cb_2018_us_county_20m.shp")
    print("Counties Shapefile Dimensions: {}".format(counties_usa.shape))
    counties_usa.head()

    # cast GEOID data type to float64 instead of str for merging
    counties_usa["GEOID"] = counties_usa["GEOID"].astype("float64")

    # merge counties shapefile with combined_df
    start = time.time()
    merged_counties = counties_usa.merge(combined_df, left_on="GEOID", right_on="FIPS")
    end = time.time()
    print("Merged Counties Dataframe Dimensions:{}; time={}".format(merged_counties.shape, str(end-start)))
    #merged_counties.head()

    # try to visualize Bladen county
    #merged_counties.iloc[0]["geometry"]

    # drop Alaska and Hawaii
    merged_counties = merged_counties.loc[~merged_counties["STATE"].isin(["Alaska", "Hawaii"])]

    end = time.time()
    print("init_data time={}".format(str(end-start)))

    return merged_counties

def init_electmap_with_controls():

    merged_cnt_data = init_data()

    year_select = Slider(start = 2000, end = 2020,
                         step = 4, value = 2000,
                         title = 'Election Year')

    start = time.time()
    geo_src = GeoJSONDataSource(geojson = make_dataset(merged_cnt_data, year_select.value, True))
    end = time.time()
    print("geo_src time={}".format(str(end-start)))

    start = time.time()
    curr_geo_src = GeoJSONDataSource(geojson = make_dataset(merged_cnt_data, 2000, False))
    end = time.time()
    print("curr_geo_src time={}".format(str(end-start)))

    #slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")


    callback = CustomJS(args=dict(source=geo_src, currsource=curr_geo_src), code="""

    var c_data = source.data;
    var yr = cb_obj.value;

    for(var key in source.data){
      currsource.data[key] = [];
    }

    for (var i = 0; i <= source.data['YEAR'].length; i++){
        if (source.data['YEAR'][i] == yr){
            for(var key in source.data){
                currsource.data[key].push(source.data[key][i]);
            }
        }
    }

    currsource.change.emit();
    """)

    year_select.js_on_change('value', callback)

    p = make_plot(curr_geo_src)
    controls = WidgetBox(year_select)
    layout = row(p, controls)

    return layout

    #curdoc().add_root(layout)
