import json
import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .app import TempPrecipTrends as app


def get_data(variable, params):
    """
    Calculate cumulative precipitation over given time.

    Args:
        variable(str): Name of the variable to query.
        params(Python Dict): Python dictionary with request parameters.

    Returns:
        Python Dict: JSON-compatible Python Dict with specified variable data.
    """
    catalog = app.get_spatial_dataset_service(app.THREDDS_SERVICE_NAME, as_engine=True)
    geometry = params['geometry']
    start_time = params.get('start_time', None)
    end_time = params.get('end_time', None)
    vertical_level = params.get('vertical_level', None)

    time_series = extract_time_series_at_location(
        catalog=catalog,
        geometry=geometry,
        variable=variable,
        start_time=start_time,
        end_time=end_time,
        vertical_level=vertical_level
    )

    return jsonify(time_series, variable)


def get_cum_precip_data(params):
    """
    Calculate cumulative precipitation over given time.

    Args:
        params(Python Dict): Python dictionary with request parameters.

    Returns:
        Python Dict: JSON-compatible Python Dict with cummulative precipitation.
    """
    catalog = app.get_spatial_dataset_service(app.THREDDS_SERVICE_NAME, as_engine=True)
    geometry = params['geometry']
    start_time = params.get('start_time', None)
    end_time = params.get('end_time', None)
    vertical_level = params.get('vertical_level', None)

    time_series = extract_time_series_at_location(
        catalog=catalog,
        geometry=geometry,
        variable='sum_tp_mm',
        start_time=start_time,
        end_time=end_time,
        vertical_level=vertical_level
    )

    cum_precip = time_series.sum_tp_mm.cumsum(dim='obs', skipna=True)
    time_series['cum_pr_mm'] = cum_precip

    return jsonify(time_series, 'cum_pr_mm')


def jsonify(dataset, variable):
    """
    Extract a time series from a THREDDS dataset at the given location.

    Args:
        dataset(xarray.Dataset): an xarray dataset.
        variable(str): Name of the variable to query.

    Returns:
        Python Dict: JSON-compatible Python Dict.
    """
    df = pd.DataFrame(data={variable: np.transpose(dataset[variable].data)}, index=dataset.time.data)
    df.index = df.index.strftime('%Y-%m-%dT%H:%M:%SZ')
    df.index.name = 'datetime'

    context = {
        'time_series': {
            'datetime': df.index.tolist(),
            variable: df[variable].to_list()
        }
    }

    context['time_series'].update(df.to_dict(orient='list'))

    return context


def param_check(request):
    """
    Check that required parameters were passed.

    Args:
        request(Django HttpRequest): Django GET request with input parameters.

    Returns:
        Python Dict: Dictionary with success or error key  and a message.
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
        time_series(Python Dict): times_series dict returned by the get_data or get_cum_precip_data functions.

    Returns:

    """
    new_date_list = []
    for date in time_series['time_series']['datetime']:
        new_date = f'{date[:3]}{int(date[3]) + 1}{date[4:]}'  # add one to the year for projected data overlap
        new_date_list.append(new_date)

        time_series['time_series']['datetime'] = new_date_list


def extract_time_series_at_location(catalog, geometry, variable, start_time=None, end_time=None, vertical_level=None):
    """
    Extract a time series from a THREDDS dataset at the given location.

    Args:
        catalog(siphon.catalog.TDSCatalog): a Siphon catalog object bound to a valid THREDDS service.
        geometry(geojson): A geojson object representing the location.
        variable(str): Name of the variable to query.
        start_time(datetime): Start of time range to query. Defaults to 9 months before end_time.
        end_time(datetime): End of time range to query. Defaults to datetime.utcnow().
        vertical_level(number): The vertical level to query. Defaults to 100000.

    Returns:
        xarray.Dataset: The data from the NCSS query.
    """
    try:
        dataset = catalog.datasets['ERA5 Daily Precipitation and Temperatures']
        ncss = dataset.subset()
        query = ncss.query()

        # Filter by location
        coordinates = json.loads(geometry)['coordinates']
        query.lonlat_point(coordinates[0], coordinates[1])

        # Filter by time
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, '%Y%m%d')

        if start_time is None:
            start_time = end_time + relativedelta(months=-9)
        elif isinstance(start_time, str):
            start_time = datetime.strptime(start_time, '%Y%m%d')

        query.time_range(start_time, end_time)

        # Filter by variable
        query.variables(variable).accept('netcdf')

        # Filter by vertical level
        if vertical_level is not None:
            query.vertical_level(vertical_level)
        else:
            query.vertical_level(100000)

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
