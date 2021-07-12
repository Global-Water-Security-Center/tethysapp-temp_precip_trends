from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.http import JsonResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .functions import get_data, get_cum_precip_data, param_check, overlap_ts


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_min_temperature(request):
    check_request = param_check(request)
    if 'success' in check_request.keys():
        try:
            params = request.GET
            time_series = get_data('min_t2m_c', params)

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
            params = request.GET
            time_series = get_data('max_t2m_c', params)

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
            params = request.GET
            time_series = get_data('mean_t2m_c', params)

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
            params = request.GET
            time_series = get_data('sum_tp_mm', params)

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
            params = request.GET
            time_series = get_cum_precip_data(params)

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
            params = request.GET.copy()  # create a mutable copy
            params['start_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-21)
            params['end_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-9)
            time_series = get_data('mean_t2m_c', params)

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
            params = request.GET.copy()  # create a mutable copy
            params['start_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-21)
            params['end_time'] = datetime.strptime(params['end_time'], '%Y%m%d') + relativedelta(months=-9)
            time_series = get_cum_precip_data(params)

            overlap_ts(time_series)  # add one year to time-series dates for projected data overlap

            return JsonResponse(time_series)

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
    else:
        return JsonResponse(check_request)
