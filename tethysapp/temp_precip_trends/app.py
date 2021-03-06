from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting, SpatialDatasetServiceSetting
from django.contrib.auth.decorators import login_required


class TempPrecipTrendsApp(TethysAppBase):
    """
    Tethys app class for Temperature and Precipitation Trends.
    """

    name = 'Temperature and Precipitation Trends'
    index = 'temp_precip_trends:home'
    icon = 'temp_precip_trends/images/icon.jpg'
    package = 'temp_precip_trends'
    root_url = 'temp-precip-trends'
    color = '#c0392b'
    description = 'Look up tool for current and normal temperature and precipitation information at a point.'
    tags = '"Temperature","Precipitation","Trends","ERA5"'
    enable_feedback = False
    feedback_emails = []

    SET_THREDDS_SDS_NAME = 'primary_thredds'
    SET_THREDDS_PRIMARY_DATASET_NAME = 'primary_dataset'
    SET_THREDDS_NORMAL_DATASET_NAME = 'normal_dataset'
    SET_THREDDS_WMS_BASE = 'thredds_wms_base'
    SET_DATASET_URL_PATH = 'dataset_url_path'
    SET_MIN_TEMP_NAME = 'min_temp_name'
    SET_MEAN_TEMP_NAME = 'mean_temp_name'
    SET_MAX_TEMP_NAME = 'max_temp_name'
    SET_TOT_PRECIP_NAME = 'tot_precip_name'
    SET_NORMAL_TEMP_NAME = 'normal_temp_name'
    SET_NORMAL_PRECIP_NAME = 'normal_precip_name'

    def url_maps(self):
        """
        Add controllers
        """
        from .controllers.map_view import GwscMapLayout
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='temp-precip-trends',
                controller=login_required(GwscMapLayout.as_controller())
            ),
            UrlMap(
                name='min_temp',
                url='api/get-min-temp',
                controller='temp_precip_trends.controllers.api.get_min_temperature'
            ),
            UrlMap(
                name='max_temp',
                url='api/get-max-temp',
                controller='temp_precip_trends.controllers.api.get_max_temperature'
            ),
            UrlMap(
                name='mean_temp',
                url='api/get-mean-temp',
                controller='temp_precip_trends.controllers.api.get_mean_temperature'
            ),
            UrlMap(
                name='total_precip',
                url='api/get-total-precip',
                controller='temp_precip_trends.controllers.api.get_total_precipitation'
            ),
            UrlMap(
                name='cum_precip',
                url='api/get-cum-precip',
                controller='temp_precip_trends.controllers.api.get_cumulative_precipitation'
            ),
            UrlMap(
                name='proj_mean_temp',
                url='api/get-proj-mean-temp',
                controller='temp_precip_trends.controllers.api.get_projected_mean_temperature'
            ),
            UrlMap(
                name='proj_cum_precip',
                url='api/get-proj-cum-precip',
                controller='temp_precip_trends.controllers.api.get_projected_cumulative_precipitation'
            ),
            UrlMap(
                name='get_normal_data',
                url='api/get-normal-data/{variable}/',
                controller='temp_precip_trends.controllers.api.get_normal_data'
            )
        )

        return url_maps

    def custom_settings(self):
        """
        Define custom settings for the app.
        """
        return (
            CustomSetting(
                name=self.SET_THREDDS_PRIMARY_DATASET_NAME,
                type=CustomSetting.TYPE_STRING,
                description='Name of primary THREDDS dataset.',
                default='ERA5 Daily Precipitation and Temperatures',
                required=True,
            ),
            CustomSetting(
                name=self.SET_THREDDS_NORMAL_DATASET_NAME,
                type=CustomSetting.TYPE_STRING,
                description='Name of normal THREDDS dataset.',
                default='ERA5 Normal Precipitation and Temperature (1950-2021)',
                required=True,
            ),
            CustomSetting(
                name=self.SET_THREDDS_WMS_BASE,
                description=f'Base path for WMS services on the "{self.SET_THREDDS_SDS_NAME}" '
                            f'THREDDS server (e.g.: /thredds/wms/).',
                type=CustomSetting.TYPE_STRING,
                default='/thredds/wms/',
                required=True,
            ),
            CustomSetting(
                name=self.SET_DATASET_URL_PATH,
                description=f'The "urlPath" of the ERA 5 daily summary dataset on the '
                            f'"{self.SET_THREDDS_SDS_NAME}" THREDDS server (e.g.: era5/daily-summary.nc).',
                type=CustomSetting.TYPE_STRING,
                default='era5/daily-summary.nc',
                required=True,
            ),
            CustomSetting(
                name=self.SET_MIN_TEMP_NAME,
                description='Name of the Minimum Temperature WMS layer/THREDDS dataset.',
                type=CustomSetting.TYPE_STRING,
                default='min_t2m_c',
                required=True,
            ),
            CustomSetting(
                name=self.SET_MEAN_TEMP_NAME,
                description='Name of the Mean Temperature WMS layer/THREDDS dataset.',
                type=CustomSetting.TYPE_STRING,
                default='mean_t2m_c',
                required=True,
            ),
            CustomSetting(
                name=self.SET_MAX_TEMP_NAME,
                description='Name of the Maximum Temperature WMS layer/THREDDS dataset.',
                type=CustomSetting.TYPE_STRING,
                default='max_t2m_c',
                required=True,
            ),
            CustomSetting(
                name=self.SET_TOT_PRECIP_NAME,
                description='Name of the Total Precipitation WMS layer/THREDDS dataset.',
                type=CustomSetting.TYPE_STRING,
                default='sum_tp_mm',
                required=True,
            ),
            CustomSetting(
                name=self.SET_NORMAL_TEMP_NAME,
                description='Name of the Normal Temperature WMS layer/THREDDS dataset.',
                type=CustomSetting.TYPE_STRING,
                default='normal_mean_t2m_c',
                required=True,
            ),
            CustomSetting(
                name=self.SET_NORMAL_PRECIP_NAME,
                description='Name of the Normal Precipitation WMS layer/THREDDS dataset.',
                type=CustomSetting.TYPE_STRING,
                default='normal_sum_tp_mm',
                required=True,
            ),
        )

    def spatial_dataset_service_settings(self):
        """
        Define Spatial Dataset Service Settings for the app.
        """
        return (
            SpatialDatasetServiceSetting(
                name=self.SET_THREDDS_SDS_NAME,
                description='THREDDS server hosting ERA 5 daily summary dataset.',
                engine=SpatialDatasetServiceSetting.THREDDS,
                required=True
            ),
        )
