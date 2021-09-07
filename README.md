# Temperature and Precipitation Trends App

A Tethys App that displays temperature and precipitation at a location anywhere in the world. This app is powered by the [ERA 5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5) dataset, which is produced by the [European Centre for Medium-Range Weather Forecasts (ECMWF)](https://www.ecmwf.int/).

## Tethys Platform

This app uses a new feature of Tethys Platform that is still under development: MapViewLayout. This feature is only available on the [map_view_layout branch](https://github.com/tethysplatform/tethys/tree/map_view_layout) of Tethys Platform (there are no Conda packages available yet). To install this branch of Tethys Platform do the following:

1. Clone the `map_view_layout` branch:

   ```bash
   git clone https://github.com/tethysplatform/tethys.git
   ```

2. Change into the root directory of the Tethys Platform repository and create a new `tethys` conda environment using the `environment.yml` file:

   ```bash
   cd tethys
    conda env create -f environment.yml
   ```

3. Activate the new `tethys` environment and install Tethys Platform packages:

   ```bash
   conda activate tethys
   python setup.py install
   ```

4. Complete the steps 2-4 of the [Getting Started](http://docs.tethysplatform.org/en/stable/installation.html) instructions as usual.

   **Note:** For a production installation, replace the [Install Tethys Platform](http://docs.tethysplatform.org/en/stable/installation/production/installation.html#id1) step with the above instructions and proceed as usual.

## THREDDS Service

1. Create a THREDDS server and populate with ERA5 data using the Docker Compose configuration and `README.md` that are found in the [gwsc-thredds repository](https://github.com/Global-Water-Security-Center/gwsc-thredds).

2. Create a new Spatial Dataset Service in the Tethys Portal where the app is to be installed that points to the `era5Catalog.xml` of the THREDDS server (see step 1 of [Assign Spatial Dataset Service](http://docs.tethysplatform.org/en/stable/tethys_sdk/tethys_services/spatial_dataset_services.html#assign-spatial-dataset-service)):

   * Name: <some_meaningful_name>
   * Engine: THREDDS
   * Endpoint: <protocol>://<host>:<ip>/thredds/era5Catalog.xml
   * Public Endpoint: <protocol>://<host>:<ip>/thredds/era5Catalog.xml
   * Apikey: <leave_blank>
   * Username: <leave_blank>
   * Password: <leave_blank>

   Example Endpoints: 
   * http://192.168.1.1:8080/thredds/era5Catalog.xml
   * https://example.com/thredds/era5Catalog.xml

## Installation

1. Clone the `main` branch of the app repository as follows:

   ```bash
   git clone https://github.com/Global-Water-Security-Center/tethysapp-temp_precip_trends.git
   ```

2. Change into the `tethysapp-temp_precip_trends` directory and run the `tethys install` command to install the app:

   ```bash
   cd tethysapp-temp_precip_trends
   tethys install
   ```

3. When prompted, select the Spatial Dataset Service that you created in the previous section.

## Configuration

If the `era5Catalog.xml` was used to configure the THREDDS server without modification, then no additional configuration should be required. However, if changes were made to this configuration such as changes to the names of datasets, then the settings for the app need to be adjusted as follows.

1. Navigate to the app settings using one of the following methods:
   1. Launch the app and select the gear icon located in the top right, near the exit button.
   2. Navigate to the `Installed Apps` section of the admin pages and click on the link with the name of the app.

2. The `CUSTOM SETTINGS` section contains settings whose values need to match the names of datasets and variables declared in the `era5Catalog.xml`.

   **Note:** All of the custom settings have default values that are consistent with the `era5Catalog.xml` found in the [gwsc-thredds repository](https://github.com/Global-Water-Security-Center/gwsc-thredds). No changes should be required unless the `era5Catalog.xml` is modified.