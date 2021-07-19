from unittest import TestCase, mock
import json

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from tethysapp.temp_precip_trends.controllers import api


class ApiTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mock.MagicMock(username='foo')

    def tearDown(self):
        pass

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_stats_temp_and_total_precip(self, mock_get_data, mock_param_check):
        mock_request_min = self.factory.get('/get-min-temp/')
        mock_request_mean = self.factory.get('/get-mean-temp/')
        mock_request_max = self.factory.get('/get-max-temp/')
        mock_request_tp = self.factory.get('get-total-precip')

        force_authenticate(mock_request_min, user=self.user)
        force_authenticate(mock_request_mean, user=self.user)
        force_authenticate(mock_request_max, user=self.user)
        force_authenticate(mock_request_tp, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_data.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret_min = api.get_min_temperature(mock_request_min)
        ret_mean = api.get_mean_temperature(mock_request_mean)
        ret_max = api.get_max_temperature(mock_request_max)
        ret_tp = api.get_total_precipitation(mock_request_tp)

        self.assertEqual(expected_result, json.loads(ret_min.content))
        self.assertEqual(expected_result, json.loads(ret_mean.content))
        self.assertEqual(expected_result, json.loads(ret_max.content))
        self.assertEqual(expected_result, json.loads(ret_tp.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_stats_temp_and_total_precip_exceptions(self, mock_get_data, mock_param_check):
        mock_request_min = self.factory.get('/get-min-temp/')
        mock_request_mean = self.factory.get('/get-mean-temp/')
        mock_request_max = self.factory.get('/get-max-temp/')
        mock_request_tp = self.factory.get('get-total-precip')

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

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_cum_precip_data')
    def test_get_cum_precip(self, mock_get_cpd, mock_param_check):
        mock_request = self.factory.get('/get-cum-precip/')

        force_authenticate(mock_request, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_cpd.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_cum_precip_data')
    def test_get_cum_precip_exceptions(self, mock_get_cpd, mock_param_check):
        mock_request = self.factory.get('/get-cum-precip/')

        force_authenticate(mock_request, user=self.user)

        expected_result = {'error': 'Something went wrong while retrieving the data.'}

        mock_get_cpd.side_effect = Exception
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.datetime')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_proj_mean_temp(self, mock_get_data, mock_param_check, mock_overlap_ts, _, __):
        mock_request = self.factory.get('/get-proj-mean_temp/', {'end_time': 'test'})

        force_authenticate(mock_request, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_data.return_value = expected_result
        mock_overlap_ts.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_mean_temperature(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.datetime')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_data')
    def test_get_proj_mean_temp_exceptions(self, mock_get_data, mock_param_check, mock_overlap_ts, _, __):
        mock_request = self.factory.get('/get-proj-mean_temp/', {'end_time': 'test'})

        force_authenticate(mock_request, user=self.user)

        expected_result = {'error': 'Something went wrong while retrieving the data.'}

        mock_get_data.return_value = {'test': 'test_data'}
        mock_overlap_ts.side_effect = Exception
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_mean_temperature(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.datetime')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_cum_precip_data')
    def test_get_proj_cum_precip(self, mock_get_cpd, mock_param_check, mock_overlap_ts, _, __):
        mock_request = self.factory.get('/get-proj-cum-precip/', {'end_time': 'test'})

        force_authenticate(mock_request, user=self.user)

        expected_result = {'test': 'test data'}

        mock_get_cpd.return_value = expected_result
        mock_overlap_ts.return_value = expected_result
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.log')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.relativedelta')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.datetime')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.overlap_ts')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    @mock.patch('tethysapp.temp_precip_trends.controllers.api.get_cum_precip_data')
    def test_get_proj_cum_precip_exceptions(self, mock_get_cpd, mock_param_check, mock_overlap_ts, _, __, ___):
        mock_request = self.factory.get('/get-proj-cum-precip/', {'end_time': 'test'})

        force_authenticate(mock_request, user=self.user)

        expected_result = {'error': 'Something went wrong while retrieving the data.'}

        mock_get_cpd.return_value = {'test': 'test_data'}
        mock_overlap_ts.side_effect = Exception
        mock_param_check.return_value = {'success': 'test'}

        ret = api.get_projected_cumulative_precipitation(mock_request)

        self.assertEqual(expected_result, json.loads(ret.content))

    @mock.patch('tethysapp.temp_precip_trends.controllers.api.param_check')
    def test_bad_params(self, mock_param_check):
        mock_request_min = self.factory.get('/get-min-temp/')
        mock_request_mean = self.factory.get('/get-mean-temp/')
        mock_request_max = self.factory.get('/get-max-temp/')
        mock_request_tp = self.factory.get('/get-total-precip/')
        mock_request_cp = self.factory.get('/get-cum-precip/')
        mock_request_pmt = self.factory.get('/get-proj-mean_temp/')
        mock_request_pcp = self.factory.get('/get-proj-cum-precip/')

        force_authenticate(mock_request_min, user=self.user)
        force_authenticate(mock_request_mean, user=self.user)
        force_authenticate(mock_request_max, user=self.user)
        force_authenticate(mock_request_tp, user=self.user)
        force_authenticate(mock_request_cp, user=self.user)
        force_authenticate(mock_request_pmt, user=self.user)
        force_authenticate(mock_request_pcp, user=self.user)

        expected_result = {'error': 'test'}
        mock_param_check.return_value = expected_result

        ret_min = api.get_min_temperature(mock_request_min)
        ret_mean = api.get_mean_temperature(mock_request_mean)
        ret_max = api.get_max_temperature(mock_request_max)
        ret_tp = api.get_total_precipitation(mock_request_tp)
        ret_cp = api.get_cumulative_precipitation(mock_request_cp)
        ret_pmt = api.get_projected_mean_temperature(mock_request_pmt)
        ret_pcp = api.get_projected_cumulative_precipitation(mock_request_pcp)

        self.assertEqual(expected_result, json.loads(ret_min.content))
        self.assertEqual(expected_result, json.loads(ret_mean.content))
        self.assertEqual(expected_result, json.loads(ret_max.content))
        self.assertEqual(expected_result, json.loads(ret_tp.content))
        self.assertEqual(expected_result, json.loads(ret_cp.content))
        self.assertEqual(expected_result, json.loads(ret_pmt.content))
        self.assertEqual(expected_result, json.loads(ret_pcp.content))
