from unittest import mock

from django.http import JsonResponse
from tethys_sdk.testing import TethysTestCase

from tethysapp.temp_precip_trends.app import TempPrecipTrendsApp as app
from tethysapp.temp_precip_trends.controllers.map_view import GwscMapLayout


class GwscMapLayoutTests(TethysTestCase):

    def test_GwscMapLayout_properties(self):
        self.assertEqual(app, GwscMapLayout.app)
        self.assertEqual('temp_precip_trends/map_view.html',
                         GwscMapLayout.template_name)
        self.assertEqual('temp_precip_trends/base.html',
                         GwscMapLayout.base_template)
        self.assertEqual('', GwscMapLayout.map_title)
        self.assertEqual('', GwscMapLayout.map_subtitle)
        self.assertEqual(app.SET_THREDDS_SDS_NAME,
                         GwscMapLayout.sds_setting_name)
        self.assertEqual([-98.583, 39.833],
                         GwscMapLayout.default_center)
        self.assertEqual([-65.69, 23.81, -129.17, 49.38],
                         GwscMapLayout.initial_map_extent)
        self.assertEqual(5, GwscMapLayout.default_zoom)
        self.assertEqual(16, GwscMapLayout.max_zoom)
        self.assertEqual(2, GwscMapLayout.min_zoom)
        self.assertTrue(GwscMapLayout.show_legends)

    @mock.patch('tethysapp.temp_precip_trends.controllers.map_view.GwscMapLayout.get_dataset_wms_endpoint')
    @mock.patch('tethysapp.temp_precip_trends.controllers.map_view.MapLayout.sds_setting',
                new_callable=mock.PropertyMock)
    @mock.patch('tethysapp.temp_precip_trends.controllers.map_view.app')
    def test_compose_layers(self, mock_app, mock_sds_setting, mock_gdwe):
        mock_app.get_custom_setting.side_effect = [
            'min',  # SET_MIN_TEMP_NAME
            'avg',  # SET_MEAN_TEMP_NAME
            'max',  # SET_MAX_TEMP_NAME
            'sum',  # SET_TOT_PRECIP_NAME
        ]

        mock_sds_setting.return_value = mock.MagicMock(
            get_engine=mock.MagicMock()
        )

        mock_gdwe.return_value = 'http://some.server.com:8585/some/wms/data/dataset.nc'

        mock_map_view = mock.MagicMock(layers=[])
        mock_request = mock.MagicMock()

        ret = GwscMapLayout().compose_layers(
            request=mock_request,
            map_view=mock_map_view,
        )

        self.assertEqual(4, len(mock_map_view.layers))
        self.assertEqual(1, len(ret))

        # Validate layers
        layer1 = mock_map_view.layers[0]
        layer2 = mock_map_view.layers[1]
        layer3 = mock_map_view.layers[2]
        layer4 = mock_map_view.layers[3]

        # Layer 1 checks - mean temp
        self.assertEqual('TileWMS', layer1.source)
        self.assertEqual('http://some.server.com:8585/some/wms/data/dataset.nc',
                         layer1.options['url'])
        self.assertEqual('avg', layer1.options['params']['LAYERS'])
        self.assertEqual('thredds', layer1.options['serverType'])
        self.assertEqual(None, layer1.options['crossOrigin'])
        self.assertEqual('avg', layer1.data['layer_id'])
        self.assertEqual('avg', layer1.data['layer_name'])
        self.assertEqual('Mean Temperature', layer1.legend_title)
        self.assertEqual('temperature', layer1.data['layer_variable'])
        self.assertTrue(layer1.layer_options['visible'])

        # Layer 2 checks - min temp
        self.assertEqual('TileWMS', layer2.source)
        self.assertEqual('http://some.server.com:8585/some/wms/data/dataset.nc',
                         layer2.options['url'])
        self.assertEqual('min', layer2.options['params']['LAYERS'])
        self.assertEqual('thredds', layer2.options['serverType'])
        self.assertEqual(None, layer2.options['crossOrigin'])
        self.assertEqual('min', layer2.data['layer_id'])
        self.assertEqual('min', layer2.data['layer_name'])
        self.assertEqual('Minimum Temperature', layer2.legend_title)
        self.assertEqual('temperature', layer2.data['layer_variable'])
        self.assertFalse(layer2.layer_options['visible'])

        # Layer 3 check - max temp
        self.assertEqual('TileWMS', layer3.source)
        self.assertEqual('http://some.server.com:8585/some/wms/data/dataset.nc',
                         layer3.options['url'])
        self.assertEqual('max', layer3.options['params']['LAYERS'])
        self.assertEqual('thredds', layer3.options['serverType'])
        self.assertEqual(None, layer3.options['crossOrigin'])
        self.assertEqual('max', layer3.data['layer_id'])
        self.assertEqual('max', layer3.data['layer_name'])
        self.assertEqual('Maximum Temperature', layer3.legend_title)
        self.assertEqual('temperature', layer3.data['layer_variable'])
        self.assertFalse(layer3.layer_options['visible'])

        # Layer 4 checks - tot precip
        self.assertEqual('TileWMS', layer4.source)
        self.assertEqual('http://some.server.com:8585/some/wms/data/dataset.nc',
                         layer4.options['url'])
        self.assertEqual('sum', layer4.options['params']['LAYERS'])
        self.assertEqual('thredds', layer4.options['serverType'])
        self.assertEqual(None, layer4.options['crossOrigin'])
        self.assertEqual('sum', layer4.data['layer_id'])
        self.assertEqual('sum', layer4.data['layer_name'])
        self.assertEqual('Total Precipitation', layer4.legend_title)
        self.assertEqual('precipitation', layer4.data['layer_variable'])
        self.assertFalse(layer4.layer_options['visible'])

        # Validate layer group
        layer_group = ret[0]
        self.assertEqual('era5-layer-group', layer_group['id'])
        self.assertEqual('ECMWF ERA 5', layer_group['display_name'])
        self.assertEqual('radio', layer_group['control'])
        self.assertEqual(4, len(layer_group['layers']))

    @mock.patch('tethysapp.temp_precip_trends.controllers.map_view.app')
    def test_get_dataset_wms_endpoint(self, mock_app):
        mock_app.get_custom_setting.side_effect = ['/some/wms/', 'data/dataset.nc']
        mock_catalog = mock.MagicMock(catalog_url='http://some.server.com:8585/thredds/catalog.xml')

        ret = GwscMapLayout.get_dataset_wms_endpoint(mock_catalog)

        self.assertEqual('http://some.server.com:8585/some/wms/data/dataset.nc', ret)

    @mock.patch('tethysapp.temp_precip_trends.controllers.map_view.MapLayout.sds_setting',
                new_callable=mock.PropertyMock)
    @mock.patch('tethysapp.temp_precip_trends.controllers.map_view.app')
    def test_get_valid_time(self, mock_app, mock_sds_setting):
        mock_request = mock.MagicMock()
        mock_ncss = mock.MagicMock(
            metadata=mock.MagicMock(
                time_span={
                    'start': '2015-02-15T01:02:03Z',
                    'end': '2021-07-05T03:17:58Z'
                }
            )
        )
        mock_dataset = mock.MagicMock(
            subset=mock.MagicMock(return_value=mock_ncss)
        )
        mock_catalog = mock.MagicMock(
            datasets={'Some Dataset Name': mock_dataset}
        )
        mock_sds_setting.return_value = mock.MagicMock(
            get_engine=mock.MagicMock(return_value=mock_catalog)
        )
        mock_app.get_custom_setting.return_value = 'Some Dataset Name'

        ret = GwscMapLayout().get_valid_time(request=mock_request)

        self.assertIsInstance(ret, JsonResponse)
        self.assertEqual(ret.content, b'{"valid_time": "5 July 2021"}')
