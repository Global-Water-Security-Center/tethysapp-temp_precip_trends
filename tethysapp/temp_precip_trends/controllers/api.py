import datetime as dt
from dateutil.relativedelta import relativedelta
import logging

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes

from tethysapp.temp_precip_trends.api_helpers import get_data, param_check, overlap_ts, jsonify
from tethysapp.temp_precip_trends.app import TempPrecipTrendsApp as app

log = logging.getLogger(f'tethys.{__name__}')


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_min_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_DATASET_NAME)]
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
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_DATASET_NAME)]
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
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_DATASET_NAME)]
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
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_DATASET_NAME)]
            params = request.GET
            geometry = params['geometry']
            start_time = params.get('start_time', None)
            end_time = params.get('end_time', None)
            ds = get_data(variable, dataset, geometry, start_time, end_time, return_json=False)

            # TODO: Weekly total precipitation
            # ds = time_series.resample(datetime='7D').sum()
            time_series = jsonify(ds, variable)

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
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_DATASET_NAME)]
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
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_DATASET_NAME)]
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
            dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_DATASET_NAME)]
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
