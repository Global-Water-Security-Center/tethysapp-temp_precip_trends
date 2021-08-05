from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

import numpy as np
import pandas as pd
import xarray as xr


def get_data(variable, dataset, params, cum_sum=False, offset_dates=None, return_json=True):
    """
    Get available variable data for specified location and time range. Available variables are: min_t2m_c, mean_t2m_c,
    max_t2m_c, and sum_tp_mm.

    Args:
        variable (str): Name of the variable to query.
        dataset (siphon.catalog.Dataset): A THREDDS dataset from a catalog.
        params (dict): Python dictionary with request parameters.
        cum_sum (bool): Sum values accumulatively if True. Defaults to False.
        offset_dates (dateutil.relativedelta): Offset the time dimension by given relativedelta. Defaults to None.
        return_json (bool): Jsonify data before returning when True. Otherwise return xr.DataSet. Defaults to True.

    Returns:
        dict: JSON-compatible Python Dict with specified variable data.
    """
    geometry = params['geometry']
    start_time = params.get('start_time', None)
    end_time = params.get('end_time', None)

    time_series = extract_time_series_at_location(
        dataset=dataset,
        geometry=geometry,
        variable=variable,
        start_time=start_time,
        end_time=end_time,
    )

    if cum_sum:
        variable = 'cumsum_' + variable
        time_series[variable] = time_series.sum_tp_mm.cumsum(dim='obs', skipna=True)

    if offset_dates:
        # TODO: Implment offset_dates capability
        pass

    if not return_json:
        return time_series

    return jsonify(time_series, variable)


def jsonify(dataset, variable):
    """
    Extract a time series from a THREDDS dataset at the given location.

    Args:
        dataset(xarray.Dataset): an xarray dataset.
        variable(str): Name of the variable to query.

    Returns:
        dict: JSON-compatible Python Dict.
    """
    df = pd.DataFrame(data={variable: np.transpose(dataset[variable].data)}, index=dataset.time.data)
    df.index = df.index.strftime('%Y-%m-%dT%H:%M:%SZ')
    df.index.name = 'datetime'

    json_dict = {
        'time_series': {
            'variable': variable,
            'datetime': df.index.tolist(),
            'values': df[variable].to_list(),
        }
    }

    return json_dict


def param_check(request):
    """
    Check that required parameters were passed.

    Args:
        request(rest_framework.request.Request): GET request with input parameters.

    Returns:
        dict: Dictionary with success or error key  and a message.
    """
    if request.method != "GET":
        return {"error": "only GET requests are allowed."}
    elif not request.GET.get("geometry", None):
        return {"error": "'geometry' is a required parameter."}
    elif not request.GET.get("end_time", None):
        return {"error": "'end_time' (YYYYMMDD) is a required parameter."}
    else:
        return {"success": "required parameters provided."}


def overlap_ts(time_series):
    """
    Updates time series by adding one year to time-series dates

    Args:
        time_series(dict): times_series dict returned by the get_data or get_cum_precip_data functions.
    """
    new_date_list = []
    for date in time_series['time_series']['datetime']:
        new_date = f'{int(date[:4]) + 1}{date[4:]}'  # add one to the year for projected data overlap
        new_date_list.append(new_date)

    time_series['time_series']['datetime'] = new_date_list


def extract_time_series_at_location(dataset, geometry, variable, start_time=None, end_time=None):
    """
    Extract a time series from a THREDDS dataset at the given location.

    Args:
        dataset(siphon.catalog.Dataset): a THREDDS dataset from a catalog.
        geometry(geojson): A geojson object representing the location.
        variable(str): Name of the variable to query.
        start_time(datetime): Start of time range to query. Defaults to 9 months before end_time.
        end_time(datetime): End of time range to query. Defaults to datetime.utcnow().

    Returns:
        xarray.Dataset: The data from the NCSS query.
    """
    try:
        # Filter by time
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, '%Y%m%d')

        if start_time is None:
            start_time = end_time + relativedelta(months=-9)
        elif isinstance(start_time, str):
            start_time = datetime.strptime(start_time, '%Y%m%d')

        ncss = dataset.subset()
        query = ncss.query()

        # Filter by location
        coordinates = json.loads(geometry)['coordinates']
        query.lonlat_point(coordinates[0], coordinates[1])

        query.time_range(start_time, end_time)

        # Filter by variable
        query.variables(variable).accept('netcdf')

        # Get the data
        data = ncss.get_data(query)

        ds = xr.open_dataset(xr.backends.NetCDF4DataStore(data))

        return ds

    except OSError as e:
        if 'NetCDF: Unknown file format' in str(e):
            raise ValueError("We are sorry, but we don't support querying this type of dataset at this time. "
                             "Please try another dataset.")
        else:
            raise e
