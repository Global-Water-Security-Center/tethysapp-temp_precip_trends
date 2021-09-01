import json
import logging
from pathlib import Path
from urllib.parse import urlparse, urljoin

from django.http import JsonResponse
from rest_framework.authtoken.models import Token


from tethys_sdk.layouts import MapLayout
from tethys_sdk.workspaces import app_workspace

from tethysapp.temp_precip_trends.app import TempPrecipTrendsApp as app

log = logging.getLogger(f'tethys.{__name__}')


@app_workspace
def get_app_workspace(request, app_workspace):  # pragma: no cover - simple return
    """
    The app_workspace decorator doesn't work on class-based views. This is a workaround.
    """
    return app_workspace


class GwscMapLayout(MapLayout):
    app = app
    template_name = 'temp_precip_trends/map_view.html'
    base_template = 'temp_precip_trends/base.html'
    sds_setting_name = app.SET_THREDDS_SDS_NAME
    map_title = ''  # Map title set dynamically to valid time
    map_subtitle = ''
    default_center = [-98.583, 39.833]  # USA Center
    initial_map_extent = [-65.69, 23.81, -129.17, 49.38]  # USA EPSG:2374
    default_zoom = 5
    max_zoom = 16
    min_zoom = 2
    plot_slide_sheet = True
    show_legends = True
    show_map_clicks = True
    show_map_click_popup = False
    show_properties_popup = False

    def compose_layers(self, request, map_view, *args, **kwargs):
        """
        Add layers to the given MapView and create associated layer group objects.
        """
        min_temp_layer_name = app.get_custom_setting(app.SET_MIN_TEMP_NAME)
        mean_temp_layer_name = app.get_custom_setting(app.SET_MEAN_TEMP_NAME)
        max_temp_layer_name = app.get_custom_setting(app.SET_MAX_TEMP_NAME)
        tot_precip_layer_name = app.get_custom_setting(app.SET_TOT_PRECIP_NAME)
        app_workspace = get_app_workspace(request)

        # Get Catalog URL
        catalog = self.sds_setting.get_engine(public=True)
        log.debug(f'Catalog: {catalog}')
        log.debug(f'Datasets: {catalog.datasets}')
        # Get WMS URL
        dataset_wms_url = self.get_dataset_wms_endpoint(catalog)

        # Define data layers
        mean_temp_layer = self.build_wms_layer(
            endpoint=dataset_wms_url,
            layer_name=mean_temp_layer_name,
            layer_title='Mean Temperature',
            layer_variable='temperature',
            selectable=False,
            visible=True,
            server_type='thredds',
        )
        min_temp_layer = self.build_wms_layer(
            endpoint=dataset_wms_url,
            layer_name=min_temp_layer_name,
            layer_title='Minimum Temperature',
            layer_variable='temperature',
            selectable=False,
            visible=False,
            server_type='thredds',
        )
        max_temp_layer = self.build_wms_layer(
            endpoint=dataset_wms_url,
            layer_name=max_temp_layer_name,
            layer_title='Maximum Temperature',
            layer_variable='temperature',
            selectable=False,
            visible=False,
            server_type='thredds',
        )
        tot_precip_layer = self.build_wms_layer(
            endpoint=dataset_wms_url,
            layer_name=tot_precip_layer_name,
            layer_title='Total Precipitation',
            layer_variable='precipitation',
            selectable=False,
            visible=False,
            server_type='thredds',
        )

        # Load GeoJSON for reference layers
        us_states_path = Path(app_workspace.path) / 'data' / 'us-states.geojson'
        with open(us_states_path) as gj:
            us_states_geojson = json.loads(gj.read())

        countries_path = Path(app_workspace.path) / 'data' / 'countries.geojson'
        with open(countries_path) as gj:
            countries_geojson = json.loads(gj.read())

        # Define reference layers
        us_states_layer = self.build_geojson_layer(
            geojson=us_states_geojson,
            layer_name='us-states',
            layer_title='U.S. States',
            layer_variable='reference',
            visible=True,
        )

        countries_layer = self.build_geojson_layer(
            geojson=countries_geojson,
            layer_name='countries',
            layer_title='Countries',
            layer_variable='reference',
            visible=True,
        )

        # Add layers to map
        map_view.layers.extend([
            us_states_layer, countries_layer,
            mean_temp_layer, min_temp_layer, max_temp_layer, tot_precip_layer
        ])

        # Define the layer groups
        layer_groups = [
            self.build_layer_group(
                id='era5-layer-group',
                display_name='ECMWF ERA 5',
                layer_control='radio',
                layers=[mean_temp_layer, min_temp_layer, max_temp_layer, tot_precip_layer],
            ),
            self.build_layer_group(
                id='reference-group',
                display_name='Reference',
                layer_control='checkbox',
                layers=[us_states_layer, countries_layer],
            )
        ]

        # Layer for testing
        if False:
            self.geoserver_workspace = 'topp'
            usa_states = self.build_wms_layer(
                endpoint='http://192.168.1.26:8181/geoserver/wms',
                layer_name='topp:states',
                layer_title="USA States",
                layer_variable='population',
                geometry_attribute='the_geom',
                visible=True,
                selectable=True,
            )
            map_view.layers.insert(0, usa_states)
            layer_groups.insert(
                0,
                self.build_layer_group(
                    id='test-layer-group',
                    display_name='USA States',
                    layer_control='checkbox',
                    layers=[usa_states],
                ),
            )

        return layer_groups

    @classmethod
    def get_vector_style_map(cls):
        return {
            'MultiPolygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'black',
                    'width': 2
                }}
            }},
            'Polygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'black',
                    'width': 2
                }}
            }},
        }

    def get_context(self, request, context, *args, **kwargs):
        # Make sure to call super get_context or everything will break!
        super().get_context(request, context, *args, **kwargs)

        # Get auth token for user and pass to context
        auth_token, _ = Token.objects.get_or_create(user=request.user)
        context.update({
            'auth_token': auth_token.key
        })
        return context

    @staticmethod
    def get_dataset_wms_endpoint(catalog):
        """
        Derive the URL for the WMS endpoint of the dataset.

        Args:
            catalog (siphon.TDSCatalog): The Catalog object bound to public endpoint of the THREDDS server.

        Returns:
            str: The WMS URL.
        """
        thredds_wms_base = app.get_custom_setting(app.SET_THREDDS_WMS_BASE)
        dataset_url_path = app.get_custom_setting(app.SET_DATASET_URL_PATH)
        catalog_url = urlparse(catalog.catalog_url)
        log.debug(f'Catalog URL: {catalog_url}')
        # Build WMS URL
        base_wms_url = urljoin(f'{catalog_url.scheme}://{catalog_url.netloc}', thredds_wms_base)
        log.debug(f'Base WMS URL: {base_wms_url}')
        dataset_wms_url = urljoin(base_wms_url, dataset_url_path)
        log.debug(f'Dataset WMS URL: {dataset_wms_url}')
        return dataset_wms_url

    # Custom AJAX Endpoints
    def get_valid_time(self, request, *args, **kwargs):
        """
        Get the last time step to use as the valid time. This method is called via AJAX.

        Args:
            request (django.HttpRequest): The Django request.
        """
        catalog = self.sds_setting.get_engine(public=True)
        dataset = catalog.datasets[app.get_custom_setting(app.SET_THREDDS_PRIMARY_DATASET_NAME)]
        ncss = dataset.subset()
        log.debug(f'Dataset Time Span: {ncss.metadata.time_span}')
        last_time_step = ncss.metadata.time_span.get('end')
        log.debug(f'End of Time Span: {last_time_step}')
        return JsonResponse({'valid_time': last_time_step})
