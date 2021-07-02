from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class TempPrecipTrends(TethysAppBase):
    """
    Tethys app class for Temperature and Precipitation Trends.
    """

    name = 'Temperature and Precipitation Trends'
    index = 'temp_precip_trends:home'
    icon = 'temp_precip_trends/images/icon.gif'
    package = 'temp_precip_trends'
    root_url = 'temp-precip-trends'
    color = '#c0392b'
    description = 'Look up tool for current and normal temperature and precipitation information at a point.'
    tags = '"Temperature","Precipitation","Trends","ERA5"'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='temp-precip-trends',
                controller='temp_precip_trends.controllers.home'
            ),
            UrlMap(
                name='home',
                url='get-min-temp',
                controller='temp_precip_trends.api.get_min_temperature'
            ),
        )

        return url_maps


    def custom_settings(self):
        custom_settings = (
            CustomSetting(
              name='data_path',
              type=CustomSetting.TYPE_STRING,
              description='Data location',
              required=True
            ),
        )

        return custom_settings
