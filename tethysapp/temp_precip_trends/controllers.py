import logging
from urllib.parse import urlparse, urljoin

from tethys_sdk.layouts import MapLayout

from tethysapp.temp_precip_trends.app import TempPrecipTrendsApp as app

log = logging.getLogger(f'tethys.{__name__}')


class GwscMapLayout(MapLayout):
    app = app
    base_template = 'temp_precip_trends/base.html'
    map_title = 'Trends'
    sds_setting_name = app.THREDDS_SDS_NAME
    default_center = [-98.583, 39.833]  # USA Center
    initial_map_extent = [-65.69, 23.81, -129.17, 49.38]  # USA EPSG:2374
    default_zoom = 5
    max_zoom = 16
    min_zoom = 2
    show_legends = True

    def compose_layers(self, request, map_view, *args, **kwargs):
        # TODO: Get these from App Settings
        THREDDS_WMS_BASE = '/thredds/wms/'
        DATASET_URL_PATH = 'era5/daily-summary.nc'
        MIN_TEMP_LAYER_NAME = 'min_t2m_c'
        MEAN_TEMP_LAYER_NAME = 'mean_t2m_c'
        MAX_TEMP_LAYER_NAME = 'max_t2m_c'
        TOT_PRECIP_LAYER_NAME = 'sum_tp_mm'

        # Get Catalog URL
        thredds_engine = self.sds_setting.get_engine(public=True)
        catalog_url = urlparse(thredds_engine.catalog_url)
        log.debug(f'Catalog: {thredds_engine}')
        log.debug(f'Catalog URL: {catalog_url}')
        log.debug(f'Datasets: {thredds_engine.datasets}')

        # Build WMS URL
        base_wms_url = urljoin(f'{catalog_url.scheme}://{catalog_url.netloc}', THREDDS_WMS_BASE)
        log.debug(f'Base WMS URL: {base_wms_url}')
        dataset_wms_url = urljoin(base_wms_url, DATASET_URL_PATH)
        log.debug(f'Dataset WMS URL: {dataset_wms_url}')

        # Define layers and add to given MapView
        mean_temp_layer = self.build_wms_layer(
            endpoint=dataset_wms_url, layer_name=MEAN_TEMP_LAYER_NAME, layer_title='Mean Temperature',
            layer_variable='temperature', selectable=False, visible=True,
        )
        min_temp_layer = self.build_wms_layer(
            endpoint=dataset_wms_url, layer_name=MIN_TEMP_LAYER_NAME, layer_title='Minimum Temperature',
            layer_variable='temperature', selectable=False, visible=False,
        )
        max_temp_layer = self.build_wms_layer(
            endpoint=dataset_wms_url, layer_name=MAX_TEMP_LAYER_NAME, layer_title='Maximum Temperature',
            layer_variable='temperature', selectable=False, visible=False,
        )
        tot_precip_layer = self.build_wms_layer(
            endpoint=dataset_wms_url, layer_name=TOT_PRECIP_LAYER_NAME, layer_title='Total Precipitation',
            layer_variable='precipitation', selectable=False, visible=False,
        )
        map_view.layers.extend([mean_temp_layer, min_temp_layer, max_temp_layer, tot_precip_layer])

        # Define the layer groups
        layer_groups = [
            self.build_layer_group(
                id='era5-layer-group',
                display_name='ECMWF ERA 5',
                layer_control='radio',
                layers=[mean_temp_layer, min_temp_layer, max_temp_layer, tot_precip_layer],
            ),
        ]

        # TODO: Add legend graphics
        return layer_groups
