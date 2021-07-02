from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .app import TempPrecipTrends as app


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def get_min_temperature(request):
    # lat = request.GET['geometry']['coordinates'][0]
    # lon = request.GET['geometry']['coordinates'][1]
    #
    # data_dir = app.get_custom_setting('data_path')
    pass
