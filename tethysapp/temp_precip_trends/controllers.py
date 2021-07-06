import logging

from tethys_sdk.layouts import MapLayout

from tethysapp.temp_precip_trends.app import TempPrecipTrendsApp as app

log = logging.getLogger(f'tethys.{__name__}')


class GwscMapLayout(MapLayout):
    app = app
    base_template = 'temp_precip_trends/base.html'
    map_title = 'Trends Map'
    map_subtitle = 'Temperature and Precipitation'
    sds_setting_name = app.THREDDS_SDS_NAME
    default_center = [-98.583, 39.833]  # USA Center
    initial_map_extent = [-65.69, 23.81, -129.17, 49.38]  # USA EPSG:2374
    default_zoom = 5
    max_zoom = 16
    min_zoom = 4

    def compose_layers(self, request, map_view, *args, **kwargs):
        thredds_engine = self.sds_setting.get_engine(public=True)
        log.debug(f'Catalog: {thredds_engine}')
        log.debug(f'Datasets: {thredds_engine.datasets}')

        if not len(thredds_engine.datasets):
            log.error(f'The "{thredds_engine}" catalog assigned to the app contains no datasets. Please verify '
                      f'that the "{app.THREDDS_SDS_NAME}" Spatial Dataset Service Setting is set to the correct '
                      f'THREDDS server and catalog.')
            return []

        tp_dataset = None
        for dataset_name, dataset_obj in thredds_engine.datasets.items():
            log.debug(f'Current Dataset Name: "{dataset_name}", Current Dataset OBJECT: {dataset_obj.__dict__}')
            if dataset_obj.id == app.get_custom_setting(app.DATASET_ID_SETTING_NAME):
                tp_dataset = dataset_obj
                break

        if not tp_dataset:
            log.error(f'Unable to find dataset with id: "{app.get_custom_setting(app.DATASET_ID_SETTING_NAME)}"')
            return []

        log.debug(f'Dataset Selected: {tp_dataset.__dict__}')

        try:
            log.debug(f'Access URLs: {tp_dataset.access_urls}')
            tp_dataset.make_access_urls(thredds_engine.base_tds_url, thredds_engine.services, thredds_engine.metadata)
            wms_endpoint = tp_dataset.access_urls['wms']
        except KeyError:
            log.error(f'No WMS endpoint found for dataset "{tp_dataset.name}"')
            return []

        log.debug(f'WMS Endpoint: {wms_endpoint}')
        return []
