import datetime as dt
from dateutil.relativedelta import relativedelta
import logging

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes

from tethysapp.temp_precip_trends.api_helpers import get_data, param_check, overlap_ts, jsonify, \
    resample_to_weekly_sum, realign_normal_dataset
from tethysapp.temp_precip_trends.app import TempPrecipTrendsApp as app

log = logging.getLogger(f'tethys.{__name__}')


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_min_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = params.get('start_time', None)
            end_time = params.get('end_time', None)
            time_series = get_data('min_t2m_c', dataset, geometry, start_time, end_time)
            return JsonResponse(time_series)

        except Exception:
            error_msg = 'Something went wrong while retrieving the data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_max_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = params.get('start_time', None)
            end_time = params.get('end_time', None)
            time_series = get_data('max_t2m_c', dataset, geometry, start_time, end_time)
            return JsonResponse(time_series)

        except Exception:
            error_msg = 'Something went wrong while retrieving the data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_mean_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = params.get('start_time', None)
            end_time = params.get('end_time', None)
            time_series = get_data('mean_t2m_c', dataset, geometry, start_time, end_time)
            return JsonResponse(time_series)

        except Exception:
            error_msg = 'Something went wrong while retrieving the data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_total_precipitation(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            variable = 'sum_tp_mm'
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = params.get('start_time', None)
            end_time = params.get('end_time', None)
            ds = get_data(variable, dataset, geometry, start_time, end_time, return_json=False)
            resampled_ds = resample_to_weekly_sum(variable, ds)
            time_series = jsonify(resampled_ds, variable)
            return JsonResponse(time_series)

        except Exception:
            error_msg = 'Something went wrong while retrieving the data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_cumulative_precipitation(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = params.get('start_time', None)
            end_time = params.get('end_time', None)
            time_series = get_data('sum_tp_mm', dataset, geometry, start_time, end_time, cum_sum=True)
            return JsonResponse(time_series)

        except Exception:
            error_msg = 'Something went wrong while retrieving the data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_projected_mean_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = dt.datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-21)
            end_time = dt.datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-9)
            time_series = get_data('mean_t2m_c', dataset, geometry, start_time, end_time)
            overlap_ts(time_series)  # add one year to time-series dates for projected data overlap
            return JsonResponse(time_series)

        except Exception:
            error_msg = 'Something went wrong while retrieving the data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_projected_cumulative_precipitation(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = dt.datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-21)
            end_time = dt.datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-9)
            time_series = get_data('sum_tp_mm', dataset, geometry, start_time, end_time, cum_sum=True)
            overlap_ts(time_series)  # add one year to time-series dates for projected data overlap
            return JsonResponse(time_series)

        except Exception:
            error_msg = 'Something went wrong while retrieving the data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_normal_data(request, variable):
    check_request = param_check(request)

    if 'success' in check_request.keys():
        try:
            params = request.GET
            geometry = params['geometry']
            end_time = params.get('end_time')
            variable = variable.replace('-', '_')

            # Get data at location
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_NORMAL_DATASET_NAME)]
            if 'temp' in variable:
                query_variable = app.get_custom_setting(app.SET_NORMAL_TEMP_NAME)
            else:
                query_variable = app.get_custom_setting(app.SET_NORMAL_PRECIP_NAME)

            # Note: Dates for normal dataset are arbitrarily set for the year 2000
            ds = get_data(
                variable=query_variable,
                dataset=dataset,
                geometry=geometry,
                start_time='20000101',
                end_time='20001231',
                return_json=False,
            )
            realigned_ds = realign_normal_dataset(query_variable, variable, ds, end_time)

            time_series = jsonify(realigned_ds, variable)
            return JsonResponse(time_series)
        except Exception:
            error_msg = 'Something went wrong while retrieving the normals data.'
            log.exception(error_msg)
            return JsonResponse({'error': error_msg})
    else:
        return JsonResponse(check_request)
