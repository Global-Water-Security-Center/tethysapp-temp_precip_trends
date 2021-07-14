#!/usr/bin/env bash
mkdir -p coverage
rm -f .coverage
echo "Running Tests..."
coverage run -a --rcfile coverage.ini $1 test tethysapp.temp_precip_trends.tests.unit_tests
coverage run -a --rcfile coverage.ini $1 test tethysapp.temp_precip_trends.tests.integrated_tests
echo "Combined Coverage Report..."
coverage report --rcfile=coverage.ini
echo "Linting..."
flake8
echo "Testing Complete"
