import datetime as dt
from dateutil.relativedelta import relativedelta
import json

import pandas as pd
import xarray as xr


def get_data(variable, dataset, geometry, start_time=None, end_time=None, cum_sum=False,
             return_json=True, offset_dates=None):
    """
    Get available variable data for specified location and time range. Available variables are: min_t2m_c, mean_t2m_c,
        max_t2m_c, and sum_tp_mm.

    Args:
        variable (str): Name of the variable to query.
        dataset (xarray.Dataset): A dataset from a THREDDS catalog.
        geometry (str): GeoJSON string of a Point location at which to retrieve the data.
        start_time (str): Start time of the date range of data to retrieve (e.g.: 'YYYYMMDD').
        end_time (str): End time of the date range of data to retrieve (e.g.: 'YYYYMMDD').
        cum_sum (bool): Sum values accumulatively if True. Defaults to False.
        return_json (bool): Jsonify data before returning when True. Otherwise return xr.DataSet. Defaults to True.
        offset_dates (dateutil.relativedelta): Offset the time dimension by given relativedelta. Defaults to None.
            NOT IMPLEMENTED YET.

    Returns:
        dict: JSON-compatible Python Dict with specified variable data.
    """
    time_series = extract_time_series_at_location(
        dataset=dataset,
        geometry=geometry,
        variable=variable,
        start_time=start_time,
        end_time=end_time,
    )

    if cum_sum:
        original_variable = variable
        variable = 'cumsum_' + variable
        time_series[variable] = time_series[original_variable].cumsum(dim='obs', skipna=True)

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
    str_time_da = dataset.time.dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    json_dict = {
        'time_series': {
            'variable': variable,
            'datetime': str_time_da.data.tolist(),
            'values': dataset[variable].data.tolist(),
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
        dataset(xarray.Dataset): A dataset from a THREDDS catalog.
        geometry(geojson): A geojson object representing the location.
        variable(str): Name of the variable to query.
        start_time(str): Start of time range to query. Defaults to 9 months before end_time.
        end_time(str): End of time range to query. Defaults to datetime.utcnow().
        day_of_year(int): Day of a 366 day year.

    Returns:
        xarray.Dataset: The data from the NCSS query.
    """
    try:
        # Filter by time
        ncss = dataset.subset()
        query = ncss.query()

        # Filter by location
        coordinates = json.loads(geometry)['coordinates']
        query.lonlat_point(coordinates[0], coordinates[1])

        # Filter by time
        if isinstance(end_time, str):
            end_time = dt.datetime.strptime(end_time, '%Y%m%d')

        if start_time is None and isinstance(end_time, dt.datetime):
            start_time = end_time + relativedelta(months=-9)
        elif isinstance(start_time, str):
            start_time = dt.datetime.strptime(start_time, '%Y%m%d')

        if start_time or end_time:
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


def resample_to_weekly_sum(variable, dataset):
    """
    Resample the variable on the given dataset to a weekly sum of values. Returns a new dataset
        with only the reduced variable.

    Args:
        variable (str): Name of the variable to query.
        dataset (xarray.Dataset): A dataset from a THREDDS catalog.

    Returns:
        xarray.Dataset: New dataset with resampled and reduced variable.
    """
    # Create new dataset with simplified structure that resample can operate on
    simplified_ds = xr.Dataset({
        variable: xr.DataArray(
            data=dataset[variable].data.copy(),
            coords={'time': dataset.time.data.copy()},
        )
    })
    # Resample
    weekly_da = simplified_ds[variable] \
        .resample(time='7D', skipna=True) \
        .sum('time')
    # Wrap resampled DataArray in dataset for jsonify to work
    weekly_ds = xr.Dataset({variable: weekly_da})
    return weekly_ds


def realign_normal_dataset(in_variable, out_variable, dataset, curr_datetime):
    """
    Cut given dataset 9-months before the current day-of-year and move first part to end to align
        it with the time window of the other data series.

    Args:
        in_variable (str): Name of variable in the given Dataset.
        out_variable (str): Name to give the variable in returned Dataset.
        dataset (xarray.Dataset): The ERA5 normal dataset from a THREDDS catalog.
        curr_datetime (datetime.datetime): Current date and time.

    Returns:
        xarray.Dataset: New dataset, realigned to match other data series.
    """
    # Compute times: series should start 9 months before given datetime
    given_datetime = dt.datetime.strptime(curr_datetime, '%Y%m%d')
    begin_plot_time = given_datetime + relativedelta(months=-9)
    begin_doy = int(begin_plot_time.strftime('%j'))

    # Move part of array before begin_doy to the end of the array
    da = dataset[in_variable]
    before_beg_doy = da.where(da.time.dt.dayofyear < begin_doy, drop=True)
    after_beg_doy = da.where(da.time.dt.dayofyear >= begin_doy, drop=True)  # inclusive

    # Concat parts into new array
    recombined = xr.concat([after_beg_doy, before_beg_doy], 'obs')

    # Build new time series dataset to return
    realigned_ds = xr.Dataset({
        out_variable: xr.DataArray(
            data=recombined.data.copy(),
            dims=['time'],
            coords={
                'time': pd.date_range(
                    start=begin_plot_time,
                    end=begin_plot_time + relativedelta(months=12),
                    freq='D'
                )
            },
        )
    })

    # Handle precipitation cases
    if 'cumm_prcp' in out_variable:
        realigned_ds[out_variable] = realigned_ds[out_variable]\
            .cumsum(dim='time', skipna=True)
    elif 'normal_prcp' in out_variable:
        realigned_ds = resample_to_weekly_sum(out_variable, realigned_ds)

    return realigned_ds
