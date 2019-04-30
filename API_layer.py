from flask import Flask, render_template
import xmlrpc.client
import pandas as pd
from altair import Chart, X, Y, Axis, Data, DataFormat
import pygeohash as pgh
from transport import RequestsTransport
import json

app = Flask(__name__)
proxy = xmlrpc.client.ServerProxy('http://0.0.0.0:2228/', transport=RequestsTransport())

month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

height = 150
width = 200


@app.route("/")
def index():
    return render_template('./index.html')

@app.route('/correlation')
def correlation():
    return render_template('correlation.html')


@app.route('/interactive')
def interactive():
    return render_template('interactive.html')

@app.route('/corr/<this>/<that>')
def serve_corr(this, that):
    return str(proxy.summarizer.correlation_matrix.get_correlation(this, that))

@app.route('/corr_matrix')
def correlation_matrix():
    matrix = proxy.summarizer.correlation_matrix.get_matrix()

    columns = ['UTC_DATE',
               'UTC_TIME',
               'LONGITUDE',
               'LATITUDE',
               'AIR_TEMPERATURE',
               'PRECIPITATION',
               'SOLAR_RADIATION',
               'SURFACE_TEMPERATURE',
               'RELATIVE_HUMIDITY']
    x1 = []
    x2 = []
    correlations = []
    for i, row in enumerate(matrix):
        for j, item in enumerate(row):
            x1.append(columns[i])
            x2.append(columns[j])
            correlations.append(matrix[i][j])

    source = pd.DataFrame({'x1': x1,
                           'x2': x2,
                           'correlation': correlations})
    chart = Chart(source, height=600, width=600).mark_rect().encode(
        x='x1:O',
        y='x2:O',
        color='correlation:Q'
    )

    return chart.to_json()

@app.route('/max/<day>/<feature>')
def serve_max_for_day(day, feature):
    day = int(day)
    return str(proxy.summarizer.getMaxForDay(day, feature))

@app.route('/min/<day>/<feature>')
def serve_min_for_day(day, feature):
    day = int(day)
    return str(proxy.summarizer.getMinForDay(day, feature))

@app.route('/mean/<day>/<feature>')
def serve_mean_for_day(day, feature):
    day = int(day)
    return str(proxy.summarizer.getMeanForDay(day, feature))

@app.route('/variance/<day>/<feature>')
def serve_variance_for_day(day, feature):
    day = int(day)
    return str(proxy.summarizer.getVarianceForDay(day, feature))

@app.route('/showLocations')
def serve_unique_location():
    locations = proxy.summarizer.getUniqueLocation()
    return str(locations)

    # lat_long_vals = [pgh.decode(i) for i in locations]
    # d = pd.DataFrame(lat_long_vals)
    # states = alt.topo_feature(data.us_10m.url, 'states')
    #
    # # US states background
    # background = alt.Chart(states).mark_geoshape(
    #     fill='lightgray',
    #     stroke='white'
    # ).properties(
    #     title='US State Capitols',
    #     width=700,
    #     height=400
    # ).project('albersUsa')
    #
    # # Points and text
    # hover = alt.selection(type='single', on='mouseover', nearest=True,
    #                       fields=['lat', 'lon'])
    #
    # base = alt.Chart(d).encode(
    #     longitude='0:Q',
    #     latitude='1:Q'
    # )
    #
    # points = base.mark_point().encode(
    #     color=alt.value('black'),
    #     size=alt.condition(~hover, alt.value(30), alt.value(100))
    # ).add_selection(hover)
    #
    # return (background + points).to_json()



# @app.route('/meanStats/<feature>')
# def serve_mean_stats(feature):
#     print(feature)
#     result = proxy.summarizer.getMeanStats(feature)
#     result_array = str(result).split()
#     list_name = ['l' + str(x) for x in range(1, 367)]
#     df_list = pd.DataFrame({'data': result_array, 'name': list_name})
#     print(list_name)
#     print(result_array)
#     print("printing!!!")
#     print(len(result_array), len(list_name))  # Print all of them out here
#
#     chart = Chart(data=df_list, height=height, width=width).mark_bar(color='lightgreen').encode(
#         X('name', axis=Axis(title='Sample')),
#         Y('data', axis=Axis(title='Value'))
#     )
#     # return chart.to_json()
#     return str(result)

#
# @app.route('/varStats/<feature>')
# def serve_var_stats(feature):
#     result = proxy.summarizer.getvarStatsByMonth(feature)
#     result_array = str(result).split()
#     list_name = ['' + str(x) for x in range(1, 13)]
#     df_list = pd.DataFrame({'data': result_array, 'name': list_name})
#
#     chart = Chart(data=df_list, height=height, width=width).mark_bar(color='lightgreen').encode(
#         X('name', axis=Axis(title='Sample')),
#         Y('data', axis=Axis(title='Value'))
#     )
#     # return chart.to_json()
#     return str(result)


@app.route('/maxStats/AIR_TEMPERATURE')
def serve_max_stats_air_temp():
    maxStatsByMonth = proxy.summarizer.getMaxStatsByMonth('AIR_TEMPERATURE')
    df_list = pd.DataFrame({'data': maxStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#ff0000', 'Month', 'Maximum values', 'AIR_TEMPERATURE')

@app.route('/maxStats/PRECIPITATION')
def serve_max_stats_prep():
    maxStatsByMonth = proxy.summarizer.getMaxStatsByMonth('PRECIPITATION')
    df_list = pd.DataFrame({'data': maxStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#0039e6', 'Month', 'Maximum values', 'PRECIPITATION')

@app.route('/maxStats/SOLAR_RADIATION')
def serve_max_stats_solar_radiation():
    maxStatsByMonth = proxy.summarizer.getMaxStatsByMonth('SOLAR_RADIATION')
    df_list = pd.DataFrame({'data': maxStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#26734d', 'Month', 'Maximum values', 'SOLAR_RADIATION')

@app.route('/maxStats/SURFACE_TEMPERATURE')
def serve_max_stats_surface_temp():
    maxStatsByMonth = proxy.summarizer.getMaxStatsByMonth('SURFACE_TEMPERATURE')
    df_list = pd.DataFrame({'data': maxStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#993d00', 'Month', 'Maximum values', 'SURFACE_TEMPERATURE')

@app.route('/maxStats/RELATIVE_HUMIDITY')
def serve_max_stats_relative_humidity():
    maxStatsByMonth = proxy.summarizer.getMaxStatsByMonth('RELATIVE_HUMIDITY')
    df_list = pd.DataFrame({'data': maxStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#8000ff', 'Month', 'Maximum values', 'RELATIVE_HUMIDITY')

@app.route('/minStats/AIR_TEMPERATURE')
def serve_min_stats_air_temp():
    minStatsByMonth = proxy.summarizer.getMinStatsByMonth('AIR_TEMPERATURE')
    minStatsByMonth = [-1 if a == 10000 else a for a in minStatsByMonth]
    df_list = pd.DataFrame({'data': minStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#ffcccc', 'Month', 'Minimum values', 'AIR_TEMPERATURE')

@app.route('/minStats/PRECIPITATION')
def serve_min_stats_prep():
    minStatsByMonth = proxy.summarizer.getMinStatsByMonth('PRECIPITATION')
    minStatsByMonth = [-1 if a == 10000 else a for a in minStatsByMonth]
    df_list = pd.DataFrame({'data': minStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#b3c6ff', 'Month', 'Minimum values', 'PRECIPITATION')

@app.route('/minStats/SOLAR_RADIATION')
def serve_min_stats_solar_radiation():
    minStatsByMonth = proxy.summarizer.getMinStatsByMonth('SOLAR_RADIATION')
    minStatsByMonth = [-1 if a == 10000 else a for a in minStatsByMonth]
    df_list = pd.DataFrame({'data': minStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#b4e4cd', 'Month', 'Minimum values', 'SOLAR_RADIATION')

@app.route('/minStats/SURFACE_TEMPERATURE')
def serve_min_stats_surface_temp():
    minStatsByMonth = proxy.summarizer.getMinStatsByMonth('SURFACE_TEMPERATURE')
    minStatsByMonth = [-1 if a == 10000 else a for a in minStatsByMonth]
    df_list = pd.DataFrame({'data': minStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#ffc299', 'Month', 'Minimum values', 'SURFACE_TEMPERATURE')

@app.route('/minStats/RELATIVE_HUMIDITY')
def serve_min_stats_relative_humidity():
    minStatsByMonth = proxy.summarizer.getMinStatsByMonth('RELATIVE_HUMIDITY')
    minStatsByMonth = [-1 if a == 10000 else a for a in minStatsByMonth]
    df_list = pd.DataFrame({'data': minStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#d9b3ff', 'Month', 'Minimum values', 'RELATIVE_HUMIDITY')


@app.route('/meanStats/AIR_TEMPERATURE')
def serve_mean_stats_air_temp():
    meanStatsByMonth = proxy.summarizer.getMeanStatsByMonth('AIR_TEMPERATURE')
    df_list = pd.DataFrame({'data': meanStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#ff8080', 'Month', 'Mean values', 'AIR_TEMPERATURE')

@app.route('/meanStats/PRECIPITATION')
def serve_mean_stats_prep():
    meanStatsByMonth = proxy.summarizer.getMeanStatsByMonth('PRECIPITATION')
    df_list = pd.DataFrame({'data': meanStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#668cff', 'Month', 'Mean values', 'PRECIPITATION')

@app.route('/meanStats/SOLAR_RADIATION')
def serve_mean_stats_solar_radiation():
    meanStatsByMonth = proxy.summarizer.getMeanStatsByMonth('SOLAR_RADIATION')
    df_list = pd.DataFrame({'data': meanStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#44bb81', 'Month', 'Mean values', 'SOLAR_RADIATION')

@app.route('/meanStats/SURFACE_TEMPERATURE')
def serve_mean_stats_surface_temp():
    meanStatsByMonth = proxy.summarizer.getMeanStatsByMonth('SURFACE_TEMPERATURE')
    df_list = pd.DataFrame({'data': meanStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#ff944d', 'Month', 'Mean values', 'SURFACE_TEMPERATURE')

@app.route('/meanStats/RELATIVE_HUMIDITY')
def serve_mean_stats_relative_humidity():
    meanStatsByMonth = proxy.summarizer.getMeanStatsByMonth('RELATIVE_HUMIDITY')
    df_list = pd.DataFrame({'data': meanStatsByMonth, 'name': month_lst})
    return make_charts(df_list, '#bf80ff', 'Month', 'Mean values', 'RELATIVE_HUMIDITY')

def make_charts(df, color, x_axis_title, y_axis_title, title):
    chart = Chart(data=df, height=height, width=width).mark_bar(color=color).encode(
        X('name', axis=Axis(title= x_axis_title), sort=None),
        Y('data', axis=Axis(title= y_axis_title))
    ).properties(
        title= title
    )
    return chart.to_json()


if __name__ == '__main__':
    app.run()