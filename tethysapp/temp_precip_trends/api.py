from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.http import HttpResponseNotAllowed, JsonResponse

from .functions import get_data, get_cum_precip_data


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_min_temperature(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        params = request.GET
        time_series = get_data('min_t2m_c', params)

        return JsonResponse(time_series)

    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something went wrong while retrieving the data.'})


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_max_temperature(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        params = request.GET
        time_series = get_data('max_t2m_c', params)

        return JsonResponse(time_series)

    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something went wrong while retrieving the data.'})


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_mean_temperature(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        params = request.GET
        time_series = get_data('mean_t2m_c', params)

        return JsonResponse(time_series)

    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something went wrong while retrieving the data.'})


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_total_precipitation(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        params = request.GET
        time_series = get_data('sum_tp_mm', params)

        return JsonResponse(time_series)

    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something went wrong while retrieving the data.'})


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_cumulative_precipitation(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        params = request.GET
        time_series = get_cum_precip_data(params)

        return JsonResponse(time_series)

    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something went wrong while retrieving the data.'})
