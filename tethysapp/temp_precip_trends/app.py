from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting, SpatialDatasetServiceSetting


class TempPrecipTrendsApp(TethysAppBase):
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

    SET_THREDDS_SDS_NAME = 'primary_thredds'
    SET_THREDDS_DATASET_NAME = 'primary_dataset'
    DATASET_ID_SETTING_NAME = 'temp_precip_dataset_id'

    def url_maps(self):
        """
        Add controllers
        """
        from .controllers import GwscMapLayout
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='temp-precip-trends',
                controller=GwscMapLayout.as_controller(app=TempPrecipTrendsApp)
            ),
            UrlMap(
                name='min_temp',
                url='api/get-min-temp',
                controller='temp_precip_trends.api.get_min_temperature'
            ),
            UrlMap(
                name='max_temp',
                url='api/get-max-temp',
                controller='temp_precip_trends.api.get_max_temperature'
            ),
            UrlMap(
                name='mean_temp',
                url='api/get-mean-temp',
                controller='temp_precip_trends.api.get_mean_temperature'
            ),
            UrlMap(
                name='total_precip',
                url='api/get-total-precip',
                controller='temp_precip_trends.api.get_total_precipitation'
            ),
            UrlMap(
                name='cum_precip',
                url='api/get-cum-precip',
                controller='temp_precip_trends.api.get_cumulative_precipitation'
            ),
            UrlMap(
                name='proj_mean_temp',
                url='api/get-proj-mean_temp',
                controller='temp_precip_trends.api.get_projected_mean_temperature'
            ),
            UrlMap(
                name='proj_cum_precip',
                url='api/get-proj-cum-precip',
                controller='temp_precip_trends.api.get_projected_cumulative_precipitation'
            ),
        )

        return url_maps

    def custom_settings(self):
        custom_settings = (
            CustomSetting(
                name='primary_dataset',
                type=CustomSetting.TYPE_STRING,
                description='Default THREDDS dataset.',
                required=True,
                default='ERA5 Daily Precipitation and Temperatures',
            ),
        )

        return custom_settings

    def spatial_dataset_service_settings(self):
        """
        Define Spatial Dataset Service Settings for the app.
        """
        return (
            SpatialDatasetServiceSetting(
                name=self.THREDDS_SDS_NAME,
                description='THREDDS server hosting WMS services of ERA 5 daily summary dataset.',
                engine=SpatialDatasetServiceSetting.THREDDS,
                required=True
            ),
        )
