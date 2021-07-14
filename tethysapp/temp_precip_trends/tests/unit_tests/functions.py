from unittest import TestCase, mock
import numpy as np
import pandas as pd
import xarray as xr

from django.test import RequestFactory
from tethysapp.temp_precip_trends import functions


class FunctionsTests(TestCase):
    @mock.patch('tethysapp.temp_precip_trends.functions.app')
    @mock.patch('tethysapp.temp_precip_trends.functions.jsonify')
    @mock.patch('tethysapp.temp_precip_trends.functions.extract_time_series_at_location')
    def test_get_data(self, mock_extract_ts, mock_jsonify, mock_app):
        mock_params = {'geometry': 'test_geom', 'end_time': 'test_end_time', 'start_time': 'test_start_time',
                       'vertical_level': 'test_vertical_level'}
        mock_variable = 'test_variable'
        mock_catalog = 'test_spatial_ds'

        expected_result = {'test': 'test data'}

        mock_app.get_spatial_dataset_service.return_value = mock_catalog
        mock_jsonify.return_value = expected_result

        ret = functions.get_data(mock_variable, mock_params)

        mock_extract_ts.assert_called_with(
            catalog=mock_catalog,
            geometry=mock_params['geometry'],
            variable=mock_variable,
            start_time=mock_params['start_time'],
            end_time=mock_params['end_time'],
            vertical_level=mock_params['vertical_level']
        )

        self.assertEqual(expected_result, ret)

    @mock.patch('tethysapp.temp_precip_trends.functions.app')
    @mock.patch('tethysapp.temp_precip_trends.functions.jsonify')
    @mock.patch('tethysapp.temp_precip_trends.functions.extract_time_series_at_location')
    def test_get_cum_precip_data(self, mock_extract_ts, mock_jsonify, mock_app):
        mock_params = {'geometry': 'test_geom', 'end_time': 'test_end_time', 'start_time': 'test_start_time',
                       'vertical_level': 'test_vertical_level'}
        mock_variable = 'sum_tp_mm'
        mock_catalog = 'test_spatial_ds'
        mock_precip_data = np.array([1, 2, 3])
        mock_cum_precip_data = np.array([1, 3, 6])
        mock_time_series = xr.Dataset(data_vars={mock_variable: (['obs'], mock_precip_data)})

        expected_result = {'test': 'test data'}

        mock_app.get_spatial_dataset_service.return_value = mock_catalog
        mock_extract_ts.return_value = mock_time_series
        mock_jsonify.return_value = expected_result

        ret = functions.get_cum_precip_data(mock_params)

        mock_extract_ts.assert_called_with(
            catalog=mock_catalog,
            geometry=mock_params['geometry'],
            variable=mock_variable,
            start_time=mock_params['start_time'],
            end_time=mock_params['end_time'],
            vertical_level=mock_params['vertical_level']
        )

        self.assertTrue(np.array_equal(mock_time_series['cum_pr_mm'].data, mock_cum_precip_data))
        self.assertEqual(expected_result, ret)

    @mock.patch('tethysapp.temp_precip_trends.functions.pd')
    @mock.patch('tethysapp.temp_precip_trends.functions.xr.Dataset', spec=xr.Dataset)
    def test_jsonify(self, mock_xr, mock_pd):
        mock_variable = 'test_variable'
        mock_dates = mock.MagicMock(return_value=[1, 2])
        mock_values = mock.MagicMock(return_value=[3, 4])

        mock_xr.time = mock.PropertyMock()
        mock_df = mock.MagicMock(spec=pd.DataFrame)
        mock_pd.DataFrame.return_value = mock_df
        mock_pd.DataFrame().index.strftime.return_value = mock.MagicMock(tolist=mock_dates)
        mock_df.__getitem__.side_effect = {mock_variable: mock.MagicMock(to_list=mock_values)}.__getitem__

        expected_result = {
            'time_series': {
                'datetime': mock_dates(),
                mock_variable: mock_values()
            }
        }
        ret = functions.jsonify(mock_xr, mock_variable)

        self.assertEqual(ret, expected_result)

    def test_check_params(self):
        mock_request = RequestFactory().get('test', {'geometry': 'test_geom', 'end_time': 'test_end_time'})

        ret = functions.param_check(mock_request)

        self.assertEqual(ret, {"success": "required parameters provided."})

    def test_check_params_method_get(self):
        mock_request = RequestFactory().post('test', {})

        ret = functions.param_check(mock_request)

        self.assertEqual(ret, {"error": "only GET requests are allowed."})

    def test_check_params_missing_required_params(self):
        mock_request1 = RequestFactory().get('test', {'end_time': 'test_end_time'})
        mock_request2 = RequestFactory().get('test', {'geometry': 'test_geom'})

        ret1 = functions.param_check(mock_request1)
        ret2 = functions.param_check(mock_request2)

        self.assertEqual(ret1, {"error": "'geometry' is a required parameter."})
        self.assertEqual(ret2, {"error": "'end_time' (YYYYMMDD) is a required parameter."})

    def test_overlap_ts(self):
        mock_ts = {
            'time_series': {
                'datetime': ['2020-09-09T00:00:00Z', '2020-09-10T00:00:00Z'],
                'test_variable': [1, 2]
            }
        }

        expected_result = ['2021-09-09T00:00:00Z', '2021-09-10T00:00:00Z']

        functions.overlap_ts(mock_ts)

        self.assertEqual(mock_ts['time_series']['datetime'], expected_result)

    @mock.patch('tethysapp.temp_precip_trends.functions.app')
    def test_extract_time_series_at_location(self, mock_app):
        mock_params = {'geometry': '{"type": "Point",  "coordinates": [40.23, -111.66]}',
                       'end_time': 'test_end_time', 'start_time': 'test_start_time',
                       'vertical_level': 'test_vertical_level'}
        mock_variable = 'test_variable'
        mock_catalog = 'test_spatial_ds'

        expected_result = {'test': 'test data'}

        mock_app.get_spatial_dataset_service.return_value = mock_catalog

        ret = functions.extract_time_series_at_location(
            catalog=mock_catalog,
            geometry=mock_params['geometry'],
            variable=mock_variable,
            start_time=mock_params['start_time'],
            end_time=mock_params['end_time'],
            vertical_level=mock_params['vertical_level']
        )