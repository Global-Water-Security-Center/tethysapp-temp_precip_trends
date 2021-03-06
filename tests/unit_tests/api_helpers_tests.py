from unittest import TestCase, mock
import numpy as np
import pandas as pd
import xarray as xr

from tethysapp.temp_precip_trends.api_helpers import (get_data, jsonify, overlap_ts, param_check,
                                                      extract_time_series_at_location)


class APIHelpersTests(TestCase):
    @mock.patch('tethysapp.temp_precip_trends.api_helpers.jsonify')
    @mock.patch('tethysapp.temp_precip_trends.api_helpers.extract_time_series_at_location')
    def test_get_data(self, mock_extract_ts, mock_jsonify):
        mock_geometry = 'test_geom'
        mock_start_time = 'test_start_time'
        mock_end_time = 'test_end_time'
        mock_variable = 'test_variable'
        mock_dataset = 'test_spatial_ds'

        expected_result = {'test': 'test data'}

        mock_jsonify.return_value = expected_result

        ret = get_data(mock_variable, mock_dataset, mock_geometry, mock_start_time, mock_end_time)

        mock_extract_ts.assert_called_with(
            dataset=mock_dataset,
            geometry=mock_geometry,
            variable=mock_variable,
            start_time=mock_start_time,
            end_time=mock_end_time,
        )

        self.assertEqual(expected_result, ret)

    @mock.patch('tethysapp.temp_precip_trends.api_helpers.jsonify')
    @mock.patch('tethysapp.temp_precip_trends.api_helpers.extract_time_series_at_location')
    def test_get_data_not_json(self, mock_extract_ts, mock_jsonify):
        mock_geometry = 'test_geom'
        mock_start_time = 'test_start_time'
        mock_end_time = 'test_end_time'
        mock_variable = 'test_variable'
        mock_dataset = 'test_spatial_ds'

        expected_result = {'test': 'test data'}

        mock_jsonify.return_value = expected_result

        ret = get_data(mock_variable, mock_dataset, mock_geometry, mock_start_time, mock_end_time, return_json=False)

        mock_extract_ts.assert_called_with(
            dataset=mock_dataset,
            geometry=mock_geometry,
            variable=mock_variable,
            start_time=mock_start_time,
            end_time=mock_end_time,
        )

        self.assertNotEqual(expected_result, ret)
        self.assertEqual(mock_extract_ts(), ret)

    @mock.patch('tethysapp.temp_precip_trends.api_helpers.jsonify')
    @mock.patch('tethysapp.temp_precip_trends.api_helpers.extract_time_series_at_location')
    def test_get_data_cum_sum(self, mock_extract_ts, mock_jsonify):
        mock_geometry = 'test_geom'
        mock_start_time = 'test_start_time'
        mock_end_time = 'test_end_time'
        mock_variable = 'sum_tp_mm'
        mock_dataset = 'test_spatial_ds'
        mock_precip_data = np.array([1, 2, 3])
        mock_cum_precip_data = np.array([1, 3, 6])
        mock_time_series = xr.Dataset(data_vars={mock_variable: (['obs'], mock_precip_data)})

        expected_result = {'test': 'test data'}

        mock_extract_ts.return_value = mock_time_series
        mock_jsonify.return_value = expected_result

        ret = get_data(mock_variable, mock_dataset, mock_geometry, mock_start_time, mock_end_time, cum_sum=True)

        mock_extract_ts.assert_called_with(
            dataset=mock_dataset,
            geometry=mock_geometry,
            variable=mock_variable,
            start_time=mock_start_time,
            end_time=mock_end_time,
        )

        self.assertTrue(np.array_equal(mock_time_series['cumsum_sum_tp_mm'].data, mock_cum_precip_data))
        self.assertEqual(expected_result, ret)

    def test_jsonify(self):
        variable = 'foo'
        data = np.array([28.0532, 19.1715,  5.1637])
        times = pd.date_range('2021-09-07', periods=3, freq='D')
        ds = xr.Dataset(
            data_vars={
                variable: xr.DataArray(
                    data=data,
                    coords={'time': times},
                    dims=['time'],
                )
            }
        )
        expected_result = {
            'time_series': {
                'variable': variable,
                'datetime': ['2021-09-07T00:00:00Z', '2021-09-08T00:00:00Z', '2021-09-09T00:00:00Z'],
                'values': [28.0532, 19.1715,  5.1637],
            }
        }

        ret = jsonify(ds, variable)

        self.assertEqual(ret, expected_result)

    def test_check_params(self):
        mock_request = mock.MagicMock()
        mock_request.method = "GET"
        mock_request.GET = {'geometry': 'test_geom', 'end_time': 'test_end_time'}

        ret = param_check(mock_request)

        self.assertEqual(ret, {"success": "required parameters provided."})

    def test_check_params_method_get(self):
        mock_request = mock.MagicMock()
        mock_request.method = "POST"
        mock_request.GET = {}

        ret = param_check(mock_request)

        self.assertEqual(ret, {"error": "only GET requests are allowed."})

    def test_check_params_missing_required_params(self):
        mock_request1 = mock.MagicMock()
        mock_request1.method = "GET"
        mock_request1.GET = {'end_time': 'test_end_time'}

        mock_request2 = mock.MagicMock()
        mock_request2.method = "GET"
        mock_request2.GET = {'geometry': 'test_geom'}

        ret1 = param_check(mock_request1)
        ret2 = param_check(mock_request2)

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

        overlap_ts(mock_ts)

        self.assertEqual(mock_ts['time_series']['datetime'], expected_result)

    @mock.patch('tethysapp.temp_precip_trends.api_helpers.xr')
    def test_extract_time_series_at_location(self, mock_xr):
        mock_geometry = '{"type": "Point",  "coordinates": [40.23, -111.66]}'
        mock_start_time = '20200601'
        mock_end_time = '20200602'
        mock_variable = 'min_t2m_c'
        mock_dataset = mock.MagicMock()
        mock_query = mock_dataset.subset().query()

        expected_result = {'test': 'test data'}
        mock_xr.open_dataset.return_value = expected_result
        mock_xr.backends.NetCDF4DataStore = mock.MagicMock()

        ret = extract_time_series_at_location(
            dataset=mock_dataset,
            geometry=mock_geometry,
            variable=mock_variable,
            start_time=mock_start_time,
            end_time=mock_end_time,
        )

        mock_query.time_range.assert_called()

        self.assertEqual(ret, expected_result)

    @mock.patch('tethysapp.temp_precip_trends.api_helpers.xr')
    def test_extract_time_series_at_location_no_start_time(self, mock_xr):
        mock_geometry = '{"type": "Point",  "coordinates": [40.23, -111.66]}'
        mock_end_time = '20200602'
        mock_variable = 'min_t2m_c'
        mock_dataset = mock.MagicMock()
        mock_query = mock_dataset.subset().query()

        expected_result = {'test': 'test data'}
        mock_xr.open_dataset.return_value = expected_result
        mock_xr.backends.NetCDF4DataStore = mock.MagicMock()

        ret = extract_time_series_at_location(
            dataset=mock_dataset,
            geometry=mock_geometry,
            variable=mock_variable,
            end_time=mock_end_time,
        )

        mock_query.time_range.assert_called()

        self.assertEqual(ret, expected_result)

    @mock.patch('tethysapp.temp_precip_trends.api_helpers.xr')
    def test_extract_time_series_at_location_no_dates(self, mock_xr):
        mock_geometry = '{"type": "Point",  "coordinates": [40.23, -111.66]}'
        mock_variable = 'min_t2m_c'
        mock_dataset = mock.MagicMock()
        mock_query = mock_dataset.subset().query()

        expected_result = {'test': 'test data'}
        mock_xr.open_dataset.return_value = expected_result
        mock_xr.backends.NetCDF4DataStore = mock.MagicMock()

        ret = extract_time_series_at_location(
            dataset=mock_dataset,
            geometry=mock_geometry,
            variable=mock_variable,
        )

        mock_query.time_range.assert_not_called()

        self.assertEqual(ret, expected_result)

    def test_extract_time_series_at_location_netcdf_file_format_exception(self):
        mock_geometry = '{"type": "Point",  "coordinates": [40.23, -111.66]}'
        mock_end_time = '20200602'
        mock_variable = 'min_t2m_c'
        mock_dataset = mock.MagicMock(
            subset=mock.MagicMock(side_effect=OSError('NetCDF: Unknown file format'))
        )

        expected_result = ("We are sorry, but we don't support querying this type of dataset at this time. "
                           "Please try another dataset.")

        with self.assertRaises(ValueError) as ret:
            extract_time_series_at_location(
                dataset=mock_dataset,
                geometry=mock_geometry,
                variable=mock_variable,
                end_time=mock_end_time,
            )

        self.assertEqual(str(ret.exception), expected_result)

    def test_extract_time_series_at_location_other_exception(self):
        mock_geometry = '{"type": "Point",  "coordinates": [40.23, -111.66]}'
        mock_start_time = '20200601'
        mock_end_time = '20200602'
        mock_variable = 'min_t2m_c'
        mock_dataset = mock.MagicMock(
            subset=mock.MagicMock(side_effect=OSError('Another OSError.'))
        )

        expected_result = "Another OSError."

        with self.assertRaises(OSError) as ret:
            extract_time_series_at_location(
                dataset=mock_dataset,
                geometry=mock_geometry,
                variable=mock_variable,
                start_time=mock_start_time,
                end_time=mock_end_time,
            )

        self.assertEqual(str(ret.exception), expected_result)
