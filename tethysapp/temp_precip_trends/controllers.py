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

    def compose_layers(self, request, map_view, *args, **kwargs):
        thredds_engine = self.sds_setting.get_engine(public=True)
        print(thredds_engine.datasets)
        return []
