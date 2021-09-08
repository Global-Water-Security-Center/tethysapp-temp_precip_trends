import datetime

import xarray as xr

get_normal_data_dict = {
    'coords': {
        'latitude': {
            'dims': ('station',),
            'attrs': {'units': 'degrees_north', 'long_name': 'station latitude'},
            'data': [50.66687232181073]
        },
        'longitude': {
            'dims': ('station',),
            'attrs': {'units': 'degrees_east', 'long_name': 'station longitude'},
            'data': [-118.95996093749999]
        },
        'time': {
            'dims': ('obs',),
            'attrs': {'standard_name': 'time', 'long_name': 'time coordinate'},
            'data': [datetime.datetime(2000, 1, 1, 0, 0), datetime.datetime(2000, 1, 2, 0, 0),
                     datetime.datetime(2000, 1, 3, 0, 0), datetime.datetime(2000, 1, 4, 0, 0),
                     datetime.datetime(2000, 1, 5, 0, 0), datetime.datetime(2000, 1, 6, 0, 0),
                     datetime.datetime(2000, 1, 7, 0, 0), datetime.datetime(2000, 1, 8, 0, 0),
                     datetime.datetime(2000, 1, 9, 0, 0), datetime.datetime(2000, 1, 10, 0, 0),
                     datetime.datetime(2000, 1, 11, 0, 0), datetime.datetime(2000, 1, 12, 0, 0),
                     datetime.datetime(2000, 1, 13, 0, 0), datetime.datetime(2000, 1, 14, 0, 0),
                     datetime.datetime(2000, 1, 15, 0, 0), datetime.datetime(2000, 1, 16, 0, 0),
                     datetime.datetime(2000, 1, 17, 0, 0), datetime.datetime(2000, 1, 18, 0, 0),
                     datetime.datetime(2000, 1, 19, 0, 0), datetime.datetime(2000, 1, 20, 0, 0),
                     datetime.datetime(2000, 1, 21, 0, 0), datetime.datetime(2000, 1, 22, 0, 0),
                     datetime.datetime(2000, 1, 23, 0, 0), datetime.datetime(2000, 1, 24, 0, 0),
                     datetime.datetime(2000, 1, 25, 0, 0), datetime.datetime(2000, 1, 26, 0, 0),
                     datetime.datetime(2000, 1, 27, 0, 0), datetime.datetime(2000, 1, 28, 0, 0),
                     datetime.datetime(2000, 1, 29, 0, 0), datetime.datetime(2000, 1, 30, 0, 0),
                     datetime.datetime(2000, 1, 31, 0, 0), datetime.datetime(2000, 2, 1, 0, 0),
                     datetime.datetime(2000, 2, 2, 0, 0), datetime.datetime(2000, 2, 3, 0, 0),
                     datetime.datetime(2000, 2, 4, 0, 0), datetime.datetime(2000, 2, 5, 0, 0),
                     datetime.datetime(2000, 2, 6, 0, 0), datetime.datetime(2000, 2, 7, 0, 0),
                     datetime.datetime(2000, 2, 8, 0, 0), datetime.datetime(2000, 2, 9, 0, 0),
                     datetime.datetime(2000, 2, 10, 0, 0), datetime.datetime(2000, 2, 11, 0, 0),
                     datetime.datetime(2000, 2, 12, 0, 0), datetime.datetime(2000, 2, 13, 0, 0),
                     datetime.datetime(2000, 2, 14, 0, 0), datetime.datetime(2000, 2, 15, 0, 0),
                     datetime.datetime(2000, 2, 16, 0, 0), datetime.datetime(2000, 2, 17, 0, 0),
                     datetime.datetime(2000, 2, 18, 0, 0), datetime.datetime(2000, 2, 19, 0, 0),
                     datetime.datetime(2000, 2, 20, 0, 0), datetime.datetime(2000, 2, 21, 0, 0),
                     datetime.datetime(2000, 2, 22, 0, 0), datetime.datetime(2000, 2, 23, 0, 0),
                     datetime.datetime(2000, 2, 24, 0, 0), datetime.datetime(2000, 2, 25, 0, 0),
                     datetime.datetime(2000, 2, 26, 0, 0), datetime.datetime(2000, 2, 27, 0, 0),
                     datetime.datetime(2000, 2, 28, 0, 0), datetime.datetime(2000, 2, 29, 0, 0),
                     datetime.datetime(2000, 3, 1, 0, 0), datetime.datetime(2000, 3, 2, 0, 0),
                     datetime.datetime(2000, 3, 3, 0, 0), datetime.datetime(2000, 3, 4, 0, 0),
                     datetime.datetime(2000, 3, 5, 0, 0), datetime.datetime(2000, 3, 6, 0, 0),
                     datetime.datetime(2000, 3, 7, 0, 0), datetime.datetime(2000, 3, 8, 0, 0),
                     datetime.datetime(2000, 3, 9, 0, 0), datetime.datetime(2000, 3, 10, 0, 0),
                     datetime.datetime(2000, 3, 11, 0, 0), datetime.datetime(2000, 3, 12, 0, 0),
                     datetime.datetime(2000, 3, 13, 0, 0), datetime.datetime(2000, 3, 14, 0, 0),
                     datetime.datetime(2000, 3, 15, 0, 0), datetime.datetime(2000, 3, 16, 0, 0),
                     datetime.datetime(2000, 3, 17, 0, 0), datetime.datetime(2000, 3, 18, 0, 0),
                     datetime.datetime(2000, 3, 19, 0, 0), datetime.datetime(2000, 3, 20, 0, 0),
                     datetime.datetime(2000, 3, 21, 0, 0), datetime.datetime(2000, 3, 22, 0, 0),
                     datetime.datetime(2000, 3, 23, 0, 0), datetime.datetime(2000, 3, 24, 0, 0),
                     datetime.datetime(2000, 3, 25, 0, 0), datetime.datetime(2000, 3, 26, 0, 0),
                     datetime.datetime(2000, 3, 27, 0, 0), datetime.datetime(2000, 3, 28, 0, 0),
                     datetime.datetime(2000, 3, 29, 0, 0), datetime.datetime(2000, 3, 30, 0, 0),
                     datetime.datetime(2000, 3, 31, 0, 0), datetime.datetime(2000, 4, 1, 0, 0),
                     datetime.datetime(2000, 4, 2, 0, 0), datetime.datetime(2000, 4, 3, 0, 0),
                     datetime.datetime(2000, 4, 4, 0, 0), datetime.datetime(2000, 4, 5, 0, 0),
                     datetime.datetime(2000, 4, 6, 0, 0), datetime.datetime(2000, 4, 7, 0, 0),
                     datetime.datetime(2000, 4, 8, 0, 0), datetime.datetime(2000, 4, 9, 0, 0),
                     datetime.datetime(2000, 4, 10, 0, 0), datetime.datetime(2000, 4, 11, 0, 0),
                     datetime.datetime(2000, 4, 12, 0, 0), datetime.datetime(2000, 4, 13, 0, 0),
                     datetime.datetime(2000, 4, 14, 0, 0), datetime.datetime(2000, 4, 15, 0, 0),
                     datetime.datetime(2000, 4, 16, 0, 0), datetime.datetime(2000, 4, 17, 0, 0),
                     datetime.datetime(2000, 4, 18, 0, 0), datetime.datetime(2000, 4, 19, 0, 0),
                     datetime.datetime(2000, 4, 20, 0, 0), datetime.datetime(2000, 4, 21, 0, 0),
                     datetime.datetime(2000, 4, 22, 0, 0), datetime.datetime(2000, 4, 23, 0, 0),
                     datetime.datetime(2000, 4, 24, 0, 0), datetime.datetime(2000, 4, 25, 0, 0),
                     datetime.datetime(2000, 4, 26, 0, 0), datetime.datetime(2000, 4, 27, 0, 0),
                     datetime.datetime(2000, 4, 28, 0, 0), datetime.datetime(2000, 4, 29, 0, 0),
                     datetime.datetime(2000, 4, 30, 0, 0), datetime.datetime(2000, 5, 1, 0, 0),
                     datetime.datetime(2000, 5, 2, 0, 0), datetime.datetime(2000, 5, 3, 0, 0),
                     datetime.datetime(2000, 5, 4, 0, 0), datetime.datetime(2000, 5, 5, 0, 0),
                     datetime.datetime(2000, 5, 6, 0, 0), datetime.datetime(2000, 5, 7, 0, 0),
                     datetime.datetime(2000, 5, 8, 0, 0), datetime.datetime(2000, 5, 9, 0, 0),
                     datetime.datetime(2000, 5, 10, 0, 0), datetime.datetime(2000, 5, 11, 0, 0),
                     datetime.datetime(2000, 5, 12, 0, 0), datetime.datetime(2000, 5, 13, 0, 0),
                     datetime.datetime(2000, 5, 14, 0, 0), datetime.datetime(2000, 5, 15, 0, 0),
                     datetime.datetime(2000, 5, 16, 0, 0), datetime.datetime(2000, 5, 17, 0, 0),
                     datetime.datetime(2000, 5, 18, 0, 0), datetime.datetime(2000, 5, 19, 0, 0),
                     datetime.datetime(2000, 5, 20, 0, 0), datetime.datetime(2000, 5, 21, 0, 0),
                     datetime.datetime(2000, 5, 22, 0, 0), datetime.datetime(2000, 5, 23, 0, 0),
                     datetime.datetime(2000, 5, 24, 0, 0), datetime.datetime(2000, 5, 25, 0, 0),
                     datetime.datetime(2000, 5, 26, 0, 0), datetime.datetime(2000, 5, 27, 0, 0),
                     datetime.datetime(2000, 5, 28, 0, 0), datetime.datetime(2000, 5, 29, 0, 0),
                     datetime.datetime(2000, 5, 30, 0, 0), datetime.datetime(2000, 5, 31, 0, 0),
                     datetime.datetime(2000, 6, 1, 0, 0), datetime.datetime(2000, 6, 2, 0, 0),
                     datetime.datetime(2000, 6, 3, 0, 0), datetime.datetime(2000, 6, 4, 0, 0),
                     datetime.datetime(2000, 6, 5, 0, 0), datetime.datetime(2000, 6, 6, 0, 0),
                     datetime.datetime(2000, 6, 7, 0, 0), datetime.datetime(2000, 6, 8, 0, 0),
                     datetime.datetime(2000, 6, 9, 0, 0), datetime.datetime(2000, 6, 10, 0, 0),
                     datetime.datetime(2000, 6, 11, 0, 0), datetime.datetime(2000, 6, 12, 0, 0),
                     datetime.datetime(2000, 6, 13, 0, 0), datetime.datetime(2000, 6, 14, 0, 0),
                     datetime.datetime(2000, 6, 15, 0, 0), datetime.datetime(2000, 6, 16, 0, 0),
                     datetime.datetime(2000, 6, 17, 0, 0), datetime.datetime(2000, 6, 18, 0, 0),
                     datetime.datetime(2000, 6, 19, 0, 0), datetime.datetime(2000, 6, 20, 0, 0),
                     datetime.datetime(2000, 6, 21, 0, 0), datetime.datetime(2000, 6, 22, 0, 0),
                     datetime.datetime(2000, 6, 23, 0, 0), datetime.datetime(2000, 6, 24, 0, 0),
                     datetime.datetime(2000, 6, 25, 0, 0), datetime.datetime(2000, 6, 26, 0, 0),
                     datetime.datetime(2000, 6, 27, 0, 0), datetime.datetime(2000, 6, 28, 0, 0),
                     datetime.datetime(2000, 6, 29, 0, 0), datetime.datetime(2000, 6, 30, 0, 0),
                     datetime.datetime(2000, 7, 1, 0, 0), datetime.datetime(2000, 7, 2, 0, 0),
                     datetime.datetime(2000, 7, 3, 0, 0), datetime.datetime(2000, 7, 4, 0, 0),
                     datetime.datetime(2000, 7, 5, 0, 0), datetime.datetime(2000, 7, 6, 0, 0),
                     datetime.datetime(2000, 7, 7, 0, 0), datetime.datetime(2000, 7, 8, 0, 0),
                     datetime.datetime(2000, 7, 9, 0, 0), datetime.datetime(2000, 7, 10, 0, 0),
                     datetime.datetime(2000, 7, 11, 0, 0), datetime.datetime(2000, 7, 12, 0, 0),
                     datetime.datetime(2000, 7, 13, 0, 0), datetime.datetime(2000, 7, 14, 0, 0),
                     datetime.datetime(2000, 7, 15, 0, 0), datetime.datetime(2000, 7, 16, 0, 0),
                     datetime.datetime(2000, 7, 17, 0, 0), datetime.datetime(2000, 7, 18, 0, 0),
                     datetime.datetime(2000, 7, 19, 0, 0), datetime.datetime(2000, 7, 20, 0, 0),
                     datetime.datetime(2000, 7, 21, 0, 0), datetime.datetime(2000, 7, 22, 0, 0),
                     datetime.datetime(2000, 7, 23, 0, 0), datetime.datetime(2000, 7, 24, 0, 0),
                     datetime.datetime(2000, 7, 25, 0, 0), datetime.datetime(2000, 7, 26, 0, 0),
                     datetime.datetime(2000, 7, 27, 0, 0), datetime.datetime(2000, 7, 28, 0, 0),
                     datetime.datetime(2000, 7, 29, 0, 0), datetime.datetime(2000, 7, 30, 0, 0),
                     datetime.datetime(2000, 7, 31, 0, 0), datetime.datetime(2000, 8, 1, 0, 0),
                     datetime.datetime(2000, 8, 2, 0, 0), datetime.datetime(2000, 8, 3, 0, 0),
                     datetime.datetime(2000, 8, 4, 0, 0), datetime.datetime(2000, 8, 5, 0, 0),
                     datetime.datetime(2000, 8, 6, 0, 0), datetime.datetime(2000, 8, 7, 0, 0),
                     datetime.datetime(2000, 8, 8, 0, 0), datetime.datetime(2000, 8, 9, 0, 0),
                     datetime.datetime(2000, 8, 10, 0, 0), datetime.datetime(2000, 8, 11, 0, 0),
                     datetime.datetime(2000, 8, 12, 0, 0), datetime.datetime(2000, 8, 13, 0, 0),
                     datetime.datetime(2000, 8, 14, 0, 0), datetime.datetime(2000, 8, 15, 0, 0),
                     datetime.datetime(2000, 8, 16, 0, 0), datetime.datetime(2000, 8, 17, 0, 0),
                     datetime.datetime(2000, 8, 18, 0, 0), datetime.datetime(2000, 8, 19, 0, 0),
                     datetime.datetime(2000, 8, 20, 0, 0), datetime.datetime(2000, 8, 21, 0, 0),
                     datetime.datetime(2000, 8, 22, 0, 0), datetime.datetime(2000, 8, 23, 0, 0),
                     datetime.datetime(2000, 8, 24, 0, 0), datetime.datetime(2000, 8, 25, 0, 0),
                     datetime.datetime(2000, 8, 26, 0, 0), datetime.datetime(2000, 8, 27, 0, 0),
                     datetime.datetime(2000, 8, 28, 0, 0), datetime.datetime(2000, 8, 29, 0, 0),
                     datetime.datetime(2000, 8, 30, 0, 0), datetime.datetime(2000, 8, 31, 0, 0),
                     datetime.datetime(2000, 9, 1, 0, 0), datetime.datetime(2000, 9, 2, 0, 0),
                     datetime.datetime(2000, 9, 3, 0, 0), datetime.datetime(2000, 9, 4, 0, 0),
                     datetime.datetime(2000, 9, 5, 0, 0), datetime.datetime(2000, 9, 6, 0, 0),
                     datetime.datetime(2000, 9, 7, 0, 0), datetime.datetime(2000, 9, 8, 0, 0),
                     datetime.datetime(2000, 9, 9, 0, 0), datetime.datetime(2000, 9, 10, 0, 0),
                     datetime.datetime(2000, 9, 11, 0, 0), datetime.datetime(2000, 9, 12, 0, 0),
                     datetime.datetime(2000, 9, 13, 0, 0), datetime.datetime(2000, 9, 14, 0, 0),
                     datetime.datetime(2000, 9, 15, 0, 0), datetime.datetime(2000, 9, 16, 0, 0),
                     datetime.datetime(2000, 9, 17, 0, 0), datetime.datetime(2000, 9, 18, 0, 0),
                     datetime.datetime(2000, 9, 19, 0, 0), datetime.datetime(2000, 9, 20, 0, 0),
                     datetime.datetime(2000, 9, 21, 0, 0), datetime.datetime(2000, 9, 22, 0, 0),
                     datetime.datetime(2000, 9, 23, 0, 0), datetime.datetime(2000, 9, 24, 0, 0),
                     datetime.datetime(2000, 9, 25, 0, 0), datetime.datetime(2000, 9, 26, 0, 0),
                     datetime.datetime(2000, 9, 27, 0, 0), datetime.datetime(2000, 9, 28, 0, 0),
                     datetime.datetime(2000, 9, 29, 0, 0), datetime.datetime(2000, 9, 30, 0, 0),
                     datetime.datetime(2000, 10, 1, 0, 0), datetime.datetime(2000, 10, 2, 0, 0),
                     datetime.datetime(2000, 10, 3, 0, 0), datetime.datetime(2000, 10, 4, 0, 0),
                     datetime.datetime(2000, 10, 5, 0, 0), datetime.datetime(2000, 10, 6, 0, 0),
                     datetime.datetime(2000, 10, 7, 0, 0), datetime.datetime(2000, 10, 8, 0, 0),
                     datetime.datetime(2000, 10, 9, 0, 0), datetime.datetime(2000, 10, 10, 0, 0),
                     datetime.datetime(2000, 10, 11, 0, 0), datetime.datetime(2000, 10, 12, 0, 0),
                     datetime.datetime(2000, 10, 13, 0, 0), datetime.datetime(2000, 10, 14, 0, 0),
                     datetime.datetime(2000, 10, 15, 0, 0), datetime.datetime(2000, 10, 16, 0, 0),
                     datetime.datetime(2000, 10, 17, 0, 0), datetime.datetime(2000, 10, 18, 0, 0),
                     datetime.datetime(2000, 10, 19, 0, 0), datetime.datetime(2000, 10, 20, 0, 0),
                     datetime.datetime(2000, 10, 21, 0, 0), datetime.datetime(2000, 10, 22, 0, 0),
                     datetime.datetime(2000, 10, 23, 0, 0), datetime.datetime(2000, 10, 24, 0, 0),
                     datetime.datetime(2000, 10, 25, 0, 0), datetime.datetime(2000, 10, 26, 0, 0),
                     datetime.datetime(2000, 10, 27, 0, 0), datetime.datetime(2000, 10, 28, 0, 0),
                     datetime.datetime(2000, 10, 29, 0, 0), datetime.datetime(2000, 10, 30, 0, 0),
                     datetime.datetime(2000, 10, 31, 0, 0), datetime.datetime(2000, 11, 1, 0, 0),
                     datetime.datetime(2000, 11, 2, 0, 0), datetime.datetime(2000, 11, 3, 0, 0),
                     datetime.datetime(2000, 11, 4, 0, 0), datetime.datetime(2000, 11, 5, 0, 0),
                     datetime.datetime(2000, 11, 6, 0, 0), datetime.datetime(2000, 11, 7, 0, 0),
                     datetime.datetime(2000, 11, 8, 0, 0), datetime.datetime(2000, 11, 9, 0, 0),
                     datetime.datetime(2000, 11, 10, 0, 0), datetime.datetime(2000, 11, 11, 0, 0),
                     datetime.datetime(2000, 11, 12, 0, 0), datetime.datetime(2000, 11, 13, 0, 0),
                     datetime.datetime(2000, 11, 14, 0, 0), datetime.datetime(2000, 11, 15, 0, 0),
                     datetime.datetime(2000, 11, 16, 0, 0), datetime.datetime(2000, 11, 17, 0, 0),
                     datetime.datetime(2000, 11, 18, 0, 0), datetime.datetime(2000, 11, 19, 0, 0),
                     datetime.datetime(2000, 11, 20, 0, 0), datetime.datetime(2000, 11, 21, 0, 0),
                     datetime.datetime(2000, 11, 22, 0, 0), datetime.datetime(2000, 11, 23, 0, 0),
                     datetime.datetime(2000, 11, 24, 0, 0), datetime.datetime(2000, 11, 25, 0, 0),
                     datetime.datetime(2000, 11, 26, 0, 0), datetime.datetime(2000, 11, 27, 0, 0),
                     datetime.datetime(2000, 11, 28, 0, 0), datetime.datetime(2000, 11, 29, 0, 0),
                     datetime.datetime(2000, 11, 30, 0, 0), datetime.datetime(2000, 12, 1, 0, 0),
                     datetime.datetime(2000, 12, 2, 0, 0), datetime.datetime(2000, 12, 3, 0, 0),
                     datetime.datetime(2000, 12, 4, 0, 0), datetime.datetime(2000, 12, 5, 0, 0),
                     datetime.datetime(2000, 12, 6, 0, 0), datetime.datetime(2000, 12, 7, 0, 0),
                     datetime.datetime(2000, 12, 8, 0, 0), datetime.datetime(2000, 12, 9, 0, 0),
                     datetime.datetime(2000, 12, 10, 0, 0), datetime.datetime(2000, 12, 11, 0, 0),
                     datetime.datetime(2000, 12, 12, 0, 0), datetime.datetime(2000, 12, 13, 0, 0),
                     datetime.datetime(2000, 12, 14, 0, 0), datetime.datetime(2000, 12, 15, 0, 0),
                     datetime.datetime(2000, 12, 16, 0, 0), datetime.datetime(2000, 12, 17, 0, 0),
                     datetime.datetime(2000, 12, 18, 0, 0), datetime.datetime(2000, 12, 19, 0, 0),
                     datetime.datetime(2000, 12, 20, 0, 0), datetime.datetime(2000, 12, 21, 0, 0),
                     datetime.datetime(2000, 12, 22, 0, 0), datetime.datetime(2000, 12, 23, 0, 0),
                     datetime.datetime(2000, 12, 24, 0, 0), datetime.datetime(2000, 12, 25, 0, 0),
                     datetime.datetime(2000, 12, 26, 0, 0), datetime.datetime(2000, 12, 27, 0, 0),
                     datetime.datetime(2000, 12, 28, 0, 0), datetime.datetime(2000, 12, 29, 0, 0),
                     datetime.datetime(2000, 12, 30, 0, 0), datetime.datetime(2000, 12, 31, 0, 0)]}},
    'attrs': {'Conventions': 'CF-1.6', 'history': 'Written by CFPointWriter',
              'title': 'Extract Points data from Grid file era5/normal-prcp-temp.nc',
              'time_coverage_start': '2000-01-01T00:00:00Z', 'time_coverage_end': '2000-12-31T00:00:00Z',
              'geospatial_lat_min': 50.66637232181073, 'geospatial_lat_max': 50.66737232181073,
              'geospatial_lon_min': -118.96046093749999, 'geospatial_lon_max': -118.95946093749998,
              'featureType': 'timeSeries'},
    'dims': {'station': 1, 'obs': 366},
    'data_vars': {
        'station_id': {
            'dims': ('station',),
            'attrs': {'long_name': 'station identifier', 'cf_role': 'timeseries_id'},
            'data': [b'GridPoint']
        },
        'station_description': {
            'dims': ('station',),
            'attrs': {'long_name': 'station description', 'standard_name': 'platform_name'},
            'data': [b'Grid Point at lat/lon=50.66687232181073,-118.95996093749999']},
        'stationIndex': {
            'dims': ('obs',),
            'attrs': {'long_name': 'station index for this observation record', 'instance_dimension': 'station'},
            'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
        'normal_sum_tp_mm': {
            'dims': ('obs',),
            'attrs': {'units': 'mm', 'long_name': 'normal_sum_tp_mm'},
            'data': [0.8834426999092102, 1.3021093606948853, 1.1562389135360718, 0.8248133659362793,
                     1.798572063446045, 1.3793971538543701, 1.2030701637268066, 1.1913764476776123,
                     1.2515772581100464, 1.0604006052017212, 1.8307009935379028, 1.48170804977417,
                     1.2496330738067627, 1.5318950414657593, 1.5637784004211426, 1.2010200023651123,
                     1.5231218338012695, 1.6995210647583008, 2.162895917892456, 1.2869563102722168,
                     1.8743332624435425, 0.9908745288848877, 1.5489219427108765, 1.581710696220398,
                     1.961148977279663, 1.2416434288024902, 1.528881549835205, 1.5275287628173828,
                     0.8183361887931824, 1.226246953010559, 1.3908181190490723, 1.0632354021072388,
                     1.3949836492538452, 1.3787846565246582, 0.8567322492599487, 1.168095588684082,
                     1.4707516431808472, 1.3659700155258179, 1.5206345319747925, 1.4796028137207031,
                     1.650949478149414, 1.5863250494003296, 1.6451796293258667, 1.8885279893875122,
                     2.186436414718628, 1.1827868223190308, 1.693828821182251, 1.8354460000991821,
                     1.714165210723877, 1.71063232421875, 1.8213582038879395, 1.0077660083770752,
                     1.3383160829544067, 1.2038049697875977, 1.3633239269256592, 1.525235652923584,
                     1.4616467952728271, 1.5408953428268433, 1.3432376384735107, 1.2029389142990112,
                     2.2797062397003174, 2.3430862426757812, 1.3669581413269043, 1.199586272239685,
                     1.8089160919189453, 1.3724892139434814, 1.2016230821609497, 1.276761770248413,
                     1.5096659660339355, 1.4939243793487549, 1.5549923181533813, 1.747247576713562,
                     1.505157232284546, 1.7772021293640137, 1.261400580406189, 1.5287494659423828,
                     1.8091517686843872, 1.4209846258163452, 1.6252535581588745, 1.6775915622711182,
                     1.6486022472381592, 2.2244577407836914, 2.275409698486328, 2.0881080627441406,
                     2.343050241470337, 2.3212435245513916, 2.0646538734436035, 1.9205926656723022,
                     1.9545141458511353, 1.7579981088638306, 2.031564950942993, 2.4745090007781982,
                     2.1894338130950928, 0.9640341997146606, 1.2698101997375488, 1.830962061882019,
                     2.282038688659668, 2.5597074031829834, 2.4718453884124756, 1.965211272239685,
                     1.5550609827041626, 1.3692219257354736, 1.5507014989852905, 1.7219972610473633,
                     2.441770553588867, 1.5695720911026, 1.8834463357925415, 2.3848602771759033, 2.5298783779144287,
                     1.9352457523345947, 2.381423234939575, 1.628350853919983, 2.232306480407715, 2.1783852577209473,
                     2.9692740440368652, 3.1663997173309326, 2.4279026985168457, 2.9107983112335205,
                     2.3972251415252686, 1.6603813171386719, 1.7918652296066284, 2.2359437942504883,
                     1.9860801696777344, 1.499435305595398, 1.3621306419372559, 1.715454339981079,
                     2.4152932167053223, 2.7238144874572754, 2.6880733966827393, 2.5776426792144775,
                     2.295908212661743, 2.2023143768310547, 1.640908122062683, 1.141812801361084, 1.929598093032837,
                     1.6458096504211426, 2.032334089279175, 2.0523288249969482, 1.9653491973876953,
                     2.138004779815674, 2.1410470008850098, 2.123279333114624, 1.815234899520874, 2.366981029510498,
                     1.8158220052719116, 1.3353005647659302, 1.6131131649017334, 1.6094799041748047,
                     1.5894203186035156, 2.0360054969787598, 1.6139346361160278, 1.395927906036377,
                     1.7033904790878296, 1.34810209274292, 1.2454057931900024, 1.177462100982666, 1.9934461116790771,
                     1.9025219678878784, 2.200354814529419, 1.7789111137390137, 1.96018385887146, 1.2090449333190918,
                     1.5157487392425537, 1.5439081192016602, 1.2337677478790283, 0.741601288318634,
                     1.0612107515335083, 0.939987063407898, 1.437804937362671, 0.6825867295265198,
                     0.79891037940979, 0.5087683200836182, 0.5294633507728577, 0.5745163559913635,
                     0.9021593928337097, 1.101211667060852, 0.5204489827156067, 0.6877403855323792,
                     0.5301146507263184, 0.44296571612358093, 0.3506855070590973, 0.2556487023830414,
                     0.4965434968471527, 0.753333568572998, 0.4674091041088104, 0.6149564385414124,
                     0.3647845387458801, 0.48924851417541504, 0.6616204977035522, 0.6228722333908081,
                     0.8653138279914856, 0.6499698162078857, 0.39976009726524353, 0.8354206085205078,
                     0.278477281332016, 0.4611504375934601, 0.442935049533844, 0.8036360740661621,
                     0.7155183553695679, 0.967709481716156, 0.6407402753829956, 1.157958745956421,
                     0.9609462022781372, 1.5663853883743286, 1.2866252660751343, 1.0731655359268188,
                     0.8698267340660095, 0.5974782705307007, 0.7699467539787292, 0.8529271483421326,
                     0.5704760551452637, 0.6283690333366394, 0.8212069272994995, 0.960478663444519,
                     1.0596126317977905, 0.9070025086402893, 0.686007559299469, 0.4113451838493347,
                     0.48043474555015564, 0.8938892483711243, 0.560368001461029, 0.5407335162162781,
                     0.6254276037216187, 0.6254969239234924, 0.6967834830284119, 0.6899245381355286,
                     0.9658114910125732, 0.9513427019119263, 1.1082504987716675, 1.307520866394043,
                     0.8898847103118896, 0.8354983329772949, 0.8510369062423706, 0.6974314451217651,
                     1.07254159450531, 1.254237413406372, 0.6583480834960938, 0.8654849529266357,
                     0.38800013065338135, 0.4628647267818451, 0.6055052280426025, 0.5806525945663452,
                     0.8875892758369446, 1.2411737442016602, 1.5671762228012085, 0.987095832824707,
                     0.5294453501701355, 0.8810698390007019, 1.1075851917266846, 1.021200180053711,
                     1.0575288534164429, 0.8986237049102783, 0.9002524614334106, 1.297292947769165,
                     0.6887224316596985, 0.6416473984718323, 0.835347592830658, 1.3780194520950317,
                     1.0198431015014648, 1.1403956413269043, 2.2606499195098877, 1.452678918838501,
                     1.8098238706588745, 1.0828064680099487, 0.9121608734130859, 1.357546329498291,
                     1.5341484546661377, 1.2310378551483154, 0.6990559697151184, 1.107377290725708,
                     1.1593800783157349, 1.3545572757720947, 1.5984468460083008, 1.0520001649856567,
                     1.3387537002563477, 1.529124140739441, 1.9044039249420166, 1.176877737045288,
                     1.6105128526687622, 1.1759352684020996, 0.9380065202713013, 0.8471258878707886,
                     1.170287013053894, 0.9754530191421509, 1.0241769552230835, 1.4051814079284668,
                     1.1402519941329956, 1.1900064945220947, 1.4688630104064941, 0.9087821245193481,
                     0.7702696919441223, 0.8686906695365906, 1.5078027248382568, 0.9730537533760071,
                     1.0832339525222778, 0.797973096370697, 1.28693425655365, 1.5172497034072876,
                     1.41233491897583, 1.3815284967422485, 1.5621962547302246, 1.5236899852752686,
                     1.6638134717941284, 1.335996150970459, 1.4201205968856812, 1.094778060913086,
                     1.3002033233642578, 0.4449969232082367, 0.8437274098396301, 1.0260411500930786,
                     1.0966663360595703, 1.3884490728378296, 1.1555198431015015, 1.295694351196289,
                     1.611579179763794, 1.8055989742279053, 1.3211901187896729, 1.7335383892059326,
                     1.6134235858917236, 1.825661301612854, 1.4123567342758179, 1.6149585247039795,
                     1.323391079902649, 1.0603140592575073, 2.023615598678589, 1.2035374641418457,
                     1.202082633972168, 1.1336508989334106, 1.8235406875610352, 1.7096539735794067,
                     1.2003086805343628, 1.3896968364715576, 1.56449294090271, 1.388467788696289,
                     1.062124490737915, 1.5804845094680786, 1.4296361207962036, 1.5387300252914429,
                     1.0059388875961304, 1.4111888408660889, 1.7641384601593018, 1.5388598442077637,
                     0.925401508808136, 0.8885897397994995, 0.6793142557144165, 1.3874375820159912,
                     1.8582894802093506, 1.128667950630188, 1.1958938837051392, 0.9549193978309631,
                     1.2529207468032837, 0.8961138129234314, 1.7126818895339966, 1.063652515411377,
                     1.3065701723098755, 2.0049045085906982, 1.1558587551116943, 1.2830554246902466,
                     1.9482011795043945, 2.2377853393554688, 1.6186059713363647, 0.9888063669204712,
                     1.3371821641921997, 1.7315620183944702, 1.5298973321914673, 0.6932955980300903]},
        'normal_mean_t2m_c': {
            'dims': ('obs',),
            'attrs': {'units': 'C', 'long_name': 'normal_mean_t2m_c'},
            'data': [-5.9043869972229, -6.154875755310059, -6.36901330947876, -6.223363876342773,
                     -6.224058151245117, -6.157113075256348, -5.835471153259277, -5.304920196533203,
                     -5.289257049560547, -5.433412075042725, -5.909013748168945, -5.509378433227539,
                     -5.468820571899414, -5.430135250091553, -5.34483528137207, -5.280201435089111,
                     -5.109807968139648, -5.212963104248047, -5.296824932098389, -5.116939544677734,
                     -5.109266757965088, -5.190035820007324, -4.982577800750732, -5.175635814666748,
                     -5.198580265045166, -5.483608245849609, -5.719851970672607, -5.705008506774902,
                     -5.566929817199707, -5.371611595153809, -5.361683368682861, -5.470567226409912,
                     -5.04860782623291, -4.471526145935059, -4.1591715812683105, -4.161170482635498,
                     -4.110952377319336, -4.0438714027404785, -3.914303779602051, -4.027000904083252,
                     -3.626755952835083, -3.2280654907226562, -2.8569204807281494,
                     -2.5622806549072266, -3.0596094131469727, -2.9355220794677734,
                     -2.604161262512207, -2.6532866954803467, -2.9033966064453125, -2.600445508956909,
                     -2.24904727935791, -1.9957575798034668, -1.8795666694641113, -2.240882396697998,
                     -2.572990894317627, -2.5104122161865234, -2.4496846199035645, -2.28778338432312,
                     -1.9791229963302612, -2.119953155517578, -2.0299415588378906, -1.986243724822998,
                     -1.9986226558685303, -1.7518796920776367, -1.3654736280441284,
                     -0.9680007100105286, -0.8220723867416382, -0.3386751413345337,
                     0.07078942656517029, 0.21289291977882385, 0.3281913995742798,
                     0.47245538234710693, 0.5967400074005127, 0.7734147906303406, 0.8983818888664246,
                     0.8721537590026855, 1.0913033485412598, 1.411351203918457, 1.5870270729064941,
                     1.6770544052124023, 1.6225918531417847, 1.5367120504379272, 1.5719897747039795,
                     1.6062418222427368, 1.516923189163208, 1.8487581014633179, 2.0474958419799805,
                     2.0738940238952637, 2.633638381958008, 2.7773287296295166, 2.8269002437591553,
                     2.5854616165161133, 2.7389659881591797, 3.012990951538086, 3.557328224182129,
                     3.6569442749023438, 3.744394302368164, 3.888522148132324, 3.9155023097991943,
                     3.901024341583252, 4.079677104949951, 4.0756072998046875, 4.144546031951904,
                     4.10671329498291, 4.419687271118164, 4.662324905395508, 4.766635417938232,
                     4.788877487182617, 4.888323783874512, 5.277775287628174, 5.849178791046143,
                     5.721066474914551, 5.633642673492432, 5.591697692871094, 5.556856155395508,
                     5.600313663482666, 5.938451766967773, 6.103938102722168, 6.291979789733887,
                     6.467320442199707, 6.547372341156006, 6.8063812255859375, 6.687685489654541,
                     6.85529088973999, 7.4009528160095215, 7.704842567443848, 7.79671049118042,
                     8.146780014038086, 8.361692428588867, 8.418232917785645, 8.676843643188477,
                     8.66254711151123, 8.740693092346191, 9.087305068969727, 9.28481674194336,
                     9.848186492919922, 9.872262001037598, 9.8571138381958, 10.018067359924316,
                     10.102875709533691, 10.297975540161133, 10.4019193649292, 10.680313110351562,
                     10.56679916381836, 10.71957778930664, 10.976236343383789, 11.228572845458984,
                     11.169629096984863, 11.530396461486816, 11.793600082397461, 12.190803527832031,
                     12.658432960510254, 12.612640380859375, 12.68177604675293, 12.785806655883789,
                     12.736165046691895, 12.514242172241211, 12.320117950439453, 12.577031135559082,
                     12.522165298461914, 12.626039505004883, 13.001517295837402, 12.94879150390625,
                     13.043244361877441, 12.94790267944336, 13.057631492614746, 13.268044471740723,
                     13.741864204406738, 13.912015914916992, 13.958046913146973, 14.044785499572754,
                     14.04466724395752, 14.357145309448242, 14.276517868041992, 14.297982215881348,
                     14.264583587646484, 14.701995849609375, 14.746363639831543, 14.726926803588867,
                     14.913325309753418, 14.806255340576172, 14.686019897460938, 14.757694244384766,
                     15.049372673034668, 15.46359920501709, 15.433564186096191, 15.2009859085083,
                     15.36970329284668, 15.900191307067871, 16.425153732299805, 16.704927444458008,
                     16.376689910888672, 16.717445373535156, 16.94956398010254, 16.696128845214844,
                     16.62811279296875, 16.574392318725586, 16.746492385864258, 17.16143226623535,
                     17.3922119140625, 17.32009506225586, 17.361968994140625, 17.676881790161133,
                     18.07240867614746, 17.52664566040039, 17.570268630981445, 17.967573165893555,
                     18.51763916015625, 18.474515914916992, 18.237295150756836, 18.338924407958984,
                     18.53882598876953, 18.658979415893555, 18.597551345825195, 18.22317123413086,
                     17.799001693725586, 17.775163650512695, 17.70589828491211, 17.760984420776367,
                     17.901552200317383, 17.999324798583984, 18.1193904876709, 17.814315795898438,
                     17.705020904541016, 17.448379516601562, 17.718660354614258, 17.15749740600586,
                     17.1372127532959, 16.73740005493164, 17.02794075012207, 17.045127868652344,
                     16.971649169921875, 16.72532081604004, 16.498476028442383, 15.946175575256348,
                     15.604265213012695, 15.408574104309082, 15.238673210144043, 15.154642105102539,
                     15.496383666992188, 15.354741096496582, 15.032661437988281, 14.782695770263672,
                     14.550566673278809, 14.43631362915039, 14.121342658996582, 14.104408264160156,
                     14.294004440307617, 14.258176803588867, 13.702880859375, 13.639184951782227,
                     13.460232734680176, 13.298090934753418, 13.158102989196777, 13.350930213928223,
                     13.33679485321045, 12.993199348449707, 12.949899673461914, 12.762267112731934,
                     12.072270393371582, 12.122547149658203, 11.858808517456055, 11.325733184814453,
                     11.0779390335083, 11.358360290527344, 11.27800178527832, 11.23840045928955,
                     11.204880714416504, 10.906600952148438, 10.306915283203125, 9.991739273071289,
                     10.073695182800293, 9.988078117370605, 9.67359447479248, 8.988075256347656,
                     8.701506614685059, 8.49998950958252, 8.494869232177734, 8.36901569366455,
                     8.281622886657715, 8.067739486694336, 7.633188247680664, 7.5952982902526855,
                     7.003319263458252, 6.776061058044434, 6.96942663192749, 6.529757976531982,
                     6.212710380554199, 6.140221118927002, 5.809778690338135, 5.570686340332031,
                     5.61319637298584, 5.2297210693359375, 5.2048659324646, 4.943162441253662,
                     4.707910060882568, 4.565158367156982, 4.447474479675293, 4.2482428550720215,
                     3.6902518272399902, 3.3085641860961914, 2.895129919052124, 2.852085590362549,
                     2.940829277038574, 2.266979694366455, 2.056224822998047, 2.2010176181793213,
                     2.443751335144043, 1.8764128684997559, 1.9034576416015625, 1.7194502353668213,
                     1.4202146530151367, 1.2705928087234497, 1.3224244117736816, 0.9055443406105042,
                     0.6384443640708923, 0.49434104561805725, 0.4102574586868286, 0.2485962212085724,
                     0.018324634060263634, -0.3310288190841675, -0.42527905106544495,
                     -0.46363136172294617, -0.6704278588294983, -1.1460516452789307,
                     -1.6702779531478882, -1.70479416847229, -1.3791024684906006, -1.2045906782150269,
                     -1.7596502304077148, -2.0746490955352783, -1.9355111122131348,
                     -2.2893788814544678, -2.0893890857696533, -1.698102355003357,
                     -1.4944452047348022, -1.6303166151046753, -1.8431224822998047,
                     -2.6454083919525146, -2.8874497413635254, -3.2703826427459717,
                     -3.5307695865631104, -3.0090668201446533, -2.632096529006958,
                     -2.4058916568756104, -2.2440409660339355, -2.7209482192993164,
                     -2.8247828483581543, -2.5324881076812744, -2.7612006664276123,
                     -3.005298137664795, -3.1607916355133057, -3.648972988128662, -3.488800287246704,
                     -3.4853813648223877, -3.8754022121429443, -3.907853364944458, -3.744891881942749,
                     -3.771865129470825, -4.002835750579834, -4.160407543182373, -4.415798664093018,
                     -4.958073616027832, -5.214082717895508, -5.471161842346191,
                     -6.724740982055664]}
    }
}

get_normal_data_ds = xr.Dataset.from_dict(get_normal_data_dict)