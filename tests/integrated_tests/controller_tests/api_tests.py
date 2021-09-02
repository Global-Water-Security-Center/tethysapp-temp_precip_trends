import json
from pathlib import Path
from unittest import TestCase, mock

from rest_framework.test import force_authenticate, APIRequestFactory

from tethysapp.temp_precip_trends.controllers import api

from .api_data import get_normal_data_ds


class ApiTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mock.MagicMock(username='foo')
        self.files_dir = Path(__file__).parent.parent.parent / 'files'

    def tearDown(self):
        pass

    def configure_mock_app(self, mock_app):
        mock_dataset = mock.MagicMock()
        mock_catalog = mock.MagicMock(datasets={'Dataset Name': mock_dataset})
        mock_app.get_spatial_dataset_service.return_value = mock_catalog
        mock_app.get_custom_setting.return_value = 'Dataset Name'

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.jsonify')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_temps_and_precip(self, mock_get_data, mock_param_check, mock_app, mock_jsonify):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request_min = self.factory.get('/get-min-temp/', data=mock_data)
        mock_request_mean = self.factory.get('/get-mean-temp/', data=mock_data)
        mock_request_max = self.factory.get('/get-max-temp/', data=mock_data)
        mock_request_tp = self.factory.get('/get-total-precip/', data=mock_data)

        force_authenticate(mock_request_min, user=self.user)
        force_authenticate(mock_request_mean, user=self.user)
        force_authenticate(mock_request_max, user=self.user)
        force_authenticate(mock_request_tp, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_data.return_value = expected_result
        mock_jsonify.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret_min = api.get_min_temperature(mock_request_min)
        ret_mean = api.get_mean_temperature(mock_request_mean)
        ret_max = api.get_max_temperature(mock_request_max)
        ret_tp = api.get_total_precipitation(mock_request_tp)

        self.assertEqual(expected_result, json.loads(ret_min.content))
        self.assertEqual(expected_result, json.loads(ret_mean.content))
        self.assertEqual(expected_result, json.loads(ret_max.content))
        self.assertEqual(expected_result, json.loads(ret_tp.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.log')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_temps_and_precips_exceptions(self, mock_get_data, mock_param_check, mock_app, mock_log):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request_min = self.factory.get('/get-min-temp/', data=mock_data)
        mock_request_mean = self.factory.get('/get-mean-temp/', data=mock_data)
        mock_request_max = self.factory.get('/get-max-temp/', data=mock_data)
        mock_request_tp = self.factory.get('/get-total-precip/', data=mock_data)

        force_authenticate(mock_request_min, user=self.user)
        force_authenticate(mock_request_mean, user=self.user)
        force_authenticate(mock_request_max, user=self.user)
        force_authenticate(mock_request_tp, user=self.user)

        expected_result = {'error': 'Something went wrong while retrieving the data.'}

        mock_get_data.side_effect = Exception
        mock_param_check.return_value = {'success': 'test'}

        ret_min = api.get_min_temperature(mock_request_min)
        ret_mean = api.get_mean_temperature(mock_request_mean)
        ret_max = api.get_max_temperature(mock_request_max)
        ret_tp = api.get_total_precipitation(mock_request_tp)

        self.assertEqual(expected_result, json.loads(ret_min.content))
        self.assertEqual(expected_result, json.loads(ret_mean.content))
        self.assertEqual(expected_result, json.loads(ret_max.content))
        self.assertEqual(expected_result, json.loads(ret_tp.content))
        mock_log.exception.assert_called()

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_cum_precip(self, mock_get_cpd, mock_param_check, mock_app):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request = self.factory.get('/get-cum-precip/', data=mock_data)

        force_authenticate(mock_request, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_cpd.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.log')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_cum_precip_exceptions(self, mock_get_cpd, mock_param_check, mock_app, mock_log):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request = self.factory.get('/get-cum-precip/', data=mock_data)

        force_authenticate(mock_request, user=self.user)

        expected_result = {'error': 'Something went wrong while retrieving the data.'}

        mock_get_cpd.side_effect = Exception
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))
        mock_log.exception.assert_called()

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.dt')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_proj_mean_temp(self, mock_get_data, mock_param_check, mock_overlap_ts, _, __, mock_app):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request = self.factory.get('/get-proj-mean_temp/', mock_data)

        force_authenticate(mock_request, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_data.return_value = expected_result
        mock_overlap_ts.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_mean_temperature(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.log')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.dt')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_proj_mean_temp_exceptions(self, mock_get_data, mock_param_check, mock_overlap_ts, _, __, mock_app,
                                           mock_log):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request = self.factory.get('/get-proj-mean_temp/', data=mock_data)

        force_authenticate(mock_request, user=self.user)

        expected_result = {'error': 'Something went wrong while retrieving the data.'}

        mock_get_data.return_value = {'test': 'test_data'}
        mock_overlap_ts.side_effect = Exception
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_mean_temperature(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))
        mock_log.exception.assert_called()

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.dt')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_proj_cum_precip(self, mock_get_cpd, mock_param_check, mock_overlap_ts, _, __, mock_app):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request = self.factory.get('/get-proj-cum-precip/', data=mock_data)

        force_authenticate(mock_request, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_cpd.return_value = expected_result
        mock_overlap_ts.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.log')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.dt')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_proj_cum_precip_exceptions(self, mock_get_cpd, mock_param_check, mock_overlap_ts, _, __, mock_log,
                                            mock_app):
        self.configure_mock_app(mock_app)
        mock_data = {'geometry': 'foo', 'start_time': 'bar', 'end_time': 'baz'}
        mock_request = self.factory.get('/get-proj-cum-precip/', data=mock_data)

        force_authenticate(mock_request, user=self.user)

        expected_result = {'error': 'Something went wrong while retrieving the data.'}

        mock_get_cpd.return_value = {'test': 'test_data'}
        mock_overlap_ts.side_effect = Exception
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))
        mock_log.exception.assert_called()

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    def test_bad_params(self, mock_param_check):
        mock_request_min = self.factory.get('/get-min-temp/')
        mock_request_mean = self.factory.get('/get-mean-temp/')
        mock_request_max = self.factory.get('/get-max-temp/')
        mock_request_tp = self.factory.get('/get-total-precip/')
        mock_request_cp = self.factory.get('/get-cum-precip/')
        mock_request_pmt = self.factory.get('/get-proj-mean_temp/')
        mock_request_pcp = self.factory.get('/get-proj-cum-precip/')
        mock_request_nt = self.factory.get('/normal-temp/')

        force_authenticate(mock_request_min, user=self.user)
        force_authenticate(mock_request_mean, user=self.user)
        force_authenticate(mock_request_max, user=self.user)
        force_authenticate(mock_request_tp, user=self.user)
        force_authenticate(mock_request_cp, user=self.user)
        force_authenticate(mock_request_pmt, user=self.user)
        force_authenticate(mock_request_pcp, user=self.user)
        force_authenticate(mock_request_nt, user=self.user)

        expected_result = {'error': 'test'}
        mock_param_check.return_value = expected_result

        ret_min = api.get_min_temperature(mock_request_min)
        ret_mean = api.get_mean_temperature(mock_request_mean)
        ret_max = api.get_max_temperature(mock_request_max)
        ret_tp = api.get_total_precipitation(mock_request_tp)
        ret_cp = api.get_cumulative_precipitation(mock_request_cp)
        ret_pmt = api.get_projected_mean_temperature(mock_request_pmt)
        ret_pcp = api.get_projected_cumulative_precipitation(mock_request_pcp)
        ret_nt = api.get_normal_data(mock_request_nt, 'normal-temp')

        self.assertEqual(expected_result, json.loads(ret_min.content))
        self.assertEqual(expected_result, json.loads(ret_mean.content))
        self.assertEqual(expected_result, json.loads(ret_max.content))
        self.assertEqual(expected_result, json.loads(ret_tp.content))
        self.assertEqual(expected_result, json.loads(ret_cp.content))
        self.assertEqual(expected_result, json.loads(ret_pmt.content))
        self.assertEqual(expected_result, json.loads(ret_pcp.content))
        self.assertEqual(expected_result, json.loads(ret_nt.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_normal_data_temperature(self, mock_get_data, mock_param_check, mock_app):
        self.configure_mock_app(mock_app)
        mock_app.get_custom_setting.side_effect = ('Dataset Name', 'normal_mean_t2m_c')
        mock_data = {'geometry': 'fake_geometry', 'end_time': '20210831'}
        mock_request_nrml_temp = self.factory.get('/normal-temp/', data=mock_data)

        force_authenticate(mock_request_nrml_temp, user=self.user)

        mock_get_data.return_value = get_normal_data_ds
        mock_param_check.return_value = {'success': 'test'}

        ret_nrml_temp = api.get_normal_data(mock_request_nrml_temp, 'normal-temp')

        # Dates are hard-coded to the year 2000
        mock_get_data.assert_called_with(
            variable=mock.ANY,
            dataset=mock.ANY,
            geometry='fake_geometry',
            start_time='20000101',
            end_time='20001231',
            return_json=False
        )

        res_file = self.files_dir / 'test_get_normal_data' / 'normal_temp.json'
        with open(res_file) as f:
            expected_json = json.load(f)
        self.assertEqual(expected_json, json.loads(ret_nrml_temp.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_normal_data_precipitation(self, mock_get_data, mock_param_check, mock_app):
        self.configure_mock_app(mock_app)
        mock_app.get_custom_setting.side_effect = ('Dataset Name', 'normal_sum_tp_mm')
        mock_data = {'geometry': 'fake_geometry', 'end_time': '20210831'}
        mock_request_nrml_temp = self.factory.get('/normal-prcp/', data=mock_data)

        force_authenticate(mock_request_nrml_temp, user=self.user)

        mock_get_data.return_value = get_normal_data_ds
        mock_param_check.return_value = {'success': 'test'}

        ret_nrml_temp = api.get_normal_data(mock_request_nrml_temp, 'normal-prcp')

        # Dates are hard-coded to the year 2000
        mock_get_data.assert_called_with(
            variable=mock.ANY,
            dataset=mock.ANY,
            geometry='fake_geometry',
            start_time='20000101',
            end_time='20001231',
            return_json=False
        )

        res_file = self.files_dir / 'test_get_normal_data' / 'normal_prcp.json'
        with open(res_file) as f:
            expected_json = json.load(f)
        self.assertEqual(expected_json, json.loads(ret_nrml_temp.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_normal_data_cumm_precipitation(self, mock_get_data, mock_param_check, mock_app):
        self.configure_mock_app(mock_app)
        mock_app.get_custom_setting.side_effect = ('Dataset Name', 'normal_sum_tp_mm')
        mock_data = {'geometry': 'fake_geometry', 'end_time': '20210831'}
        mock_request_nrml_temp = self.factory.get('/normal-cumm-prcp/', data=mock_data)

        force_authenticate(mock_request_nrml_temp, user=self.user)

        mock_get_data.return_value = get_normal_data_ds
        mock_param_check.return_value = {'success': 'test'}

        ret_nrml_temp = api.get_normal_data(mock_request_nrml_temp, 'normal-cumm-prcp')

        # Dates are hard-coded to the year 2000
        mock_get_data.assert_called_with(
            variable=mock.ANY,
            dataset=mock.ANY,
            geometry='fake_geometry',
            start_time='20000101',
            end_time='20001231',
            return_json=False
        )

        res_file = self.files_dir / 'test_get_normal_data' / 'normal_cumm_prcp.json'
        with open(res_file) as f:
            expected_json = json.load(f)
        self.assertEqual(expected_json, json.loads(ret_nrml_temp.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.log')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.app')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_normal_data_exception(self, mock_get_data, mock_param_check, mock_app, mock_log):
        self.configure_mock_app(mock_app)
        mock_app.get_custom_setting.side_effect = ('Dataset Name', 'normal_mean_t2m_c')
        mock_data = {'geometry': 'fake_geometry', 'end_time': '20210831'}
        mock_request_nrml_temp = self.factory.get('/normal-temp/', data=mock_data)

        force_authenticate(mock_request_nrml_temp, user=self.user)

        mock_get_data.side_effect = RuntimeError
        mock_param_check.return_value = {'success': 'test'}

        ret_nrml_temp = api.get_normal_data(mock_request_nrml_temp, 'normal-temp')

        # Dates are hard-coded to the year 2000
        mock_get_data.assert_called_with(
            variable=mock.ANY,
            dataset=mock.ANY,
            geometry='fake_geometry',
            start_time='20000101',
            end_time='20001231',
            return_json=False
        )
        expected_json = {'error': 'Something went wrong while retrieving the normals data.'}
        self.assertEqual(expected_json, json.loads(ret_nrml_temp.content))
        mock_log.exception.assert_called()
