from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.http import JsonResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .app import TempPrecipTrends as app
from .api_helpers import get_data, get_cum_precip_data, param_check, overlap_ts

import logging
log = logging.getLogger(f'tethys.{__name__}')


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_min_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.SET_THREDDS_DATASET_NAME]
            params = request.GET
            time_series = get_data('min_t2m_c', dataset, params)

            return JsonResponse(time_series)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_max_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.SET_THREDDS_DATASET_NAME]
            params = request.GET
            time_series = get_data('max_t2m_c', dataset, params)

            return JsonResponse(time_series)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_mean_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.SET_THREDDS_DATASET_NAME]
            params = request.GET
            time_series = get_data('mean_t2m_c', dataset, params)

            return JsonResponse(time_series)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_total_precipitation(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.SET_THREDDS_DATASET_NAME]
            params = request.GET
            time_series = get_data('sum_tp_mm', dataset, params)

            return JsonResponse(time_series)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_cumulative_precipitation(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.SET_THREDDS_DATASET_NAME]
            params = request.GET
            time_series = get_cum_precip_data(dataset, params)

            return JsonResponse(time_series)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_projected_mean_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.SET_THREDDS_DATASET_NAME]
            params = request.GET.copy()  # create a mutable copy
            params['start_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-21)
            params['end_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-9)
            time_series = get_data('mean_t2m_c', dataset, params)

            overlap_ts(time_series)  # add one year to time-series dates for projected data overlap

            return JsonResponse(time_series)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_projected_cumulative_precipitation(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            catalog = app.get_spatial_dataset_service(app.SET_THREDDS_SDS_NAME, as_engine=True)
            dataset = catalog.datasets[app.SET_THREDDS_DATASET_NAME]
            params = request.GET.copy()  # create a mutable copy
            params['start_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-21)
            params['end_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-9)
            time_series = get_cum_precip_data(dataset, params)

            overlap_ts(time_series)  # add one year to time-series dates for projected data overlap

            return JsonResponse(time_series)

        except Exception as e:
            log.exception(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)
