/*****************************************************************************
 * DATE: 22 July 2021
 * AUTHOR: Nathan Swain
 * COPYRIGHT: (c) Aquaveo 2021
 *****************************************************************************/

/*****************************************************************************
 *                      LIBRARY WRAPPER
 *****************************************************************************/
var TPT_MAP_VIEW = (function() {
	"use strict";
	/************************************************************************
 	*                      MODULE LEVEL / GLOBAL VARIABLES
 	*************************************************************************/
 	const ERA5_LINK = 'https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation#ERA5:datadocumentation-Introduction',
 	      PLOT_SUBTITLE = `(Data derived from the <a href="${ERA5_LINK}" target="_blank">ERA5</a>, 1950-2021)`,
 	      SERIES_ENDPOINTS = {
 	          min_temp: '/apps/temp-precip-trends/api/get-min-temp/',
 	          max_temp: '/apps/temp-precip-trends/api/get-max-temp/',
 	          mean_temp: '/apps/temp-precip-trends/api/get-mean-temp/',
 	          tot_prcp: '/apps/temp-precip-trends/api/get-total-precip/',
 	          cum_prcp: '/apps/temp-precip-trends/api/get-cum-precip/',
 	          prj_mean_temp: '/apps/temp-precip-trends/api/get-proj-mean-temp/',
 	          prj_cum_prcp: '/apps/temp-precip-trends/api/get-proj-cum-precip/',
 	      };

 	var public_interface,				// Object returned by the module
 	    m_auth_token,                   // User's authentication token for the API
 		m_map,				            // MapView object
 		m_plot,                         // Slide Sheet Plotly object/element
 		m_plot_data,                    // Data object of the slide sheet plot
 		m_plot_layout,                  // Data object of the slide sheet plot
 		m_plot_title,                   // Title for the plot
 		m_valid_time,                   // Current valid time
 		m_valid_time_str,               // Current valid time as US locale date string
 		m_valid_time_request_str;       // Valid time formatted for request: YYYYMMDD

	/************************************************************************
 	*                    PRIVATE FUNCTION DECLARATIONS
 	*************************************************************************/
 	var init_members;
 	var init_valid_time;
 	var init_click_n_plot, update_lat_lon, update_plot, update_plot_series,
 	    fetch_time_series;

 	/************************************************************************
 	*                    PRIVATE FUNCTION IMPLEMENTATIONS
 	*************************************************************************/
 	init_members = function() {
 	    let tpt_map_attrs = $('#tpt-map-attributes');
 	    m_map = TETHYS_MAP_VIEW.getMap();
 	    m_plot = MAP_LAYOUT.get_plot();
 	    m_auth_token = tpt_map_attrs.data('auth-token');
 	};

 	init_valid_time = function() {
        let title_elem = document.querySelector('#nav-title .title');
        title_elem.innerHTML = '<img src="/static/temp_precip_trends/images/loading-dots.gif">';

        fetch('?method=get-valid-time')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                // Save for use in other parts of the script
                m_valid_time = new Date(data.valid_time);

                // Human-friendly string format
                let options = {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                };
                m_valid_time_str = m_valid_time.toLocaleDateString('en-US', options);

                // Generate formatted date needed for request: YYYYMMDD
                let date = String(m_valid_time.getUTCDate()).padStart(2, '0');
                let month = String(m_valid_time.getUTCMonth() + 1).padStart(2, '0');
                let year = m_valid_time.getUTCFullYear();
                m_valid_time_request_str = `${year}${month}${date}`;

                // Set nav title
                title_elem.innerHTML = m_valid_time_str;

                // Set plot title
                m_plot_title = 'Temp. + Precip. Trends through ' + m_valid_time_str;
            });
    };

    init_click_n_plot = function() {
        // Set the plot height based on the height of the slide sheet
        const pss_height = $('#plot-slide-sheet').height();


        m_plot_layout = {
            'height': 0.85 * pss_height,
            'margin': {
                't': 0,
            },
            'modebar': {
                'remove': [
                    'lasso',
                    'select2d',
                    'zoomin',
                    'zoomout',
                    'pan'
                ],
                'add': [
                    'hovercompare',
                    'hoverclosest',
                ],
            },
            'hovermode': 'x unified',
            'legend':{
                'orientation': 'h',
                'traceorder': 'grouped',
            },
            'xaxis': {
               'type': 'date',
               'tickformat': '%b%y',
               'dtick': 'M1',
               'showgrid': true,
               'spikemode': 'across',
               'spikethickness': 2,
               'hoverformat': '%B %d, %Y',
            },
            'yaxis': {
                'title': {
                    'text': 'Temperature (\u00B0C)'
                },
            },
            'yaxis2': {
                'title': {
                    'text': 'Precipitation (mm)',
                },
                'overlaying': 'y',
                'side': 'right',
            },
        };

        // Initialize the plot data series
        m_plot_data = [
            // min_temp
            {
                'x': [],
                'y': [],
                'legendgroup': 'temp',
                'hovertemplate': 'Min Temp: %{y:.1f} \u00B0C',
                'hoverlabel': {
                    'namelength': 0,
                },
                'showlegend': false,
                'legendrank': 20,
                'name': 'Temperature Range',
                'type': 'scatter',
                'line': {
                    'color': '#FF9999',
                },
            },
            // max_temp
            {
                'x': [],
                'y': [],
                'legendgroup': 'temp',
                'name': 'Temperature Range',
                'hovertemplate': 'Max Temp: %{y:.1f} \u00B0C',
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 20,
                'type': 'scatter',
                'fill': 'tonexty',
                'fillcolor': '#FF9999',
                'line': {
                    'color': '#FF9999',
                },
            },
            // mean_temp
            {
                'x': [],
                'y': [],
                'legendgroup': 'temp',
                'hovertemplate': 'Mean Temp: %{y:.1f} \u00B0C',
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 10,
                'name': "Current Year's Temperature",
                'type': 'scatter',
                'line': {
                    'color': '#ff0000',
                    'width': 2,
                },
            },
            // tot_prcp
            {
                'x': [],
                'y': [],
                'legendgroup': 'prcpbar',
                'hovertemplate': "Daily. Precip.: %{y:.1f} mm",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 50,
                'name': 'Daily Precip.',
                'type': 'bar',
                'yaxis': 'y2',
                'marker': {
                    'color': '#0E810E',
                },
            },
            // cum_prcp
            {
                'x': [],
                'y': [],
                'legendgroup': 'prcp',
                'hovertemplate': "Cum. Precip.: %{y:.1f} mm",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 60,
                'name': 'Cumulative Precip. this Year',
                'type': 'scatter',
                'yaxis': 'y2',
                'line': {
                    'color': '#00ff00',
                    'width': 2,
                },
            },
            // prj_mean_temp
            {
                'x': [],
                'y': [],
                'legendgroup': 'temp',
                'hovertemplate': "Last Year's Temp: %{y:.1f} \u00B0C",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 30,
                'name': "Last Year's Temperature",
                'type': 'scatter',
                'line': {
                    'color': '#868686',
                    'width': 1.5,
                },
            },
            // prj_cum_prcp
            {
                'x': [],
                'y': [],
                'legendgroup': 'prcp',
                'hovertemplate': "Last Year's Cum. Precip.: %{y:.1f} mm",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 70,
                'name': "Last Year's Cumulative Precip.",
                'type': 'scatter',
                'yaxis': 'y2',
                'line': {
                    'color': '#868686',
                    'dash': 'dot',
                    'width': 1.5,
                },
            },
        ];

        MAP_LAYOUT.update_plot(m_plot_title, m_plot_data, m_plot_layout);

        // Insert subtitle
        $('#plot-slide-sheet .slide-sheet-title').after(
            `<h5 class="slide-sheet-subtitle">${PLOT_SUBTITLE}</h5>`
        );

        // Insert lat and lon fields
        $('#plot-slide-sheet .slide-sheet-title').before(
            '<span class="lat-lon-fields pull-right">Lat: <span id="lat-field">0</span> Lon: <span id="lon-field">0</span></span>'
        );

        // Remove point when slide sheet is closed
        $('.slide-sheet-content .close').on('click', function() {
            TETHYS_MAP_VIEW.clearClickedPoint();
        });

        // Bind to map click event
        TETHYS_MAP_VIEW.mapClicked(function(coordinate, event) {
            let lon_lat = ol.proj.toLonLat(coordinate);
            let lat = lon_lat[1];
            let lon = lon_lat[0];
            update_plot(lat, lon);
            MAP_LAYOUT.show_plot();
        });
    };

    fetch_time_series = async function(series, lat, lon) {
        // Min temperature
        let geometry = {
            type: 'Point',
            coordinates: [lon, lat]
        };
        let params = new URLSearchParams({
            geometry: JSON.stringify(geometry),
            end_time: m_valid_time_request_str,
        });
        let url = `${SERIES_ENDPOINTS[series]}?${params.toString()}`;
        console.log(url);
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${m_auth_token}`
            },
        });
        return response.json();
    };

    update_lat_lon = function(lat, lon) {
        $('#lat-field').text(lat.toFixed(2));
        $('#lon-field').text(lon.toFixed(2));
    };

    update_plot_series = function(series_index, x, y) {
        m_plot_data[series_index].x = x;
        m_plot_data[series_index].y = y;
        m_plot_data[series_index].visible = true;
        MAP_LAYOUT.update_plot(m_plot_title, m_plot_data, m_plot_layout);
    };

    update_plot = function(lat, lon) {
        // Update the latitude and longitude coordinates shown on the plot
        update_lat_lon(lat, lon);

        // Fetch the time series dataset for the given coordinates
        fetch_time_series('min_temp', lat, lon).then((data) => {
            console.log(data);
            update_plot_series(0,  // min_temp
                data.time_series.datetime,
                data.time_series.min_t2m_c
            );
        });
        fetch_time_series('max_temp', lat, lon).then((data) => {
            update_plot_series(1,  // max_temp
                data.time_series.datetime,
                data.time_series.max_t2m_c
            );
        });
        fetch_time_series('mean_temp', lat, lon).then((data) => {
            update_plot_series(2,  // mean_temp
                data.time_series.datetime,
                data.time_series.mean_t2m_c
            );
        });
        fetch_time_series('tot_prcp', lat, lon).then((data) => {
            update_plot_series(3,  // tot_prcp
                data.time_series.datetime,
                data.time_series.sum_tp_mm
            );
        });
        fetch_time_series('cum_prcp', lat, lon).then((data) => {
            update_plot_series(4,  // cum_prcp
                data.time_series.datetime,
                data.time_series.cum_pr_mm
            );
        });
        fetch_time_series('prj_mean_temp', lat, lon).then((data) => {
            update_plot_series(5,  // prj_mean_temp
                data.time_series.datetime,
                data.time_series.mean_t2m_c
            );
        });
        fetch_time_series('prj_cum_prcp', lat, lon).then((data) => {
            update_plot_series(6,  // prj_cum_prcp
                data.time_series.datetime,
                data.time_series.cum_pr_mm
            );
        });
    };

	/************************************************************************
 	*                            PUBLIC INTERFACE
 	*************************************************************************/
	public_interface = {};

	/************************************************************************
 	*                  INITIALIZATION / CONSTRUCTOR
 	*************************************************************************/
	$(function() {
		init_members();
        init_valid_time();
        init_click_n_plot();
	});

	return public_interface;
}()); // End of library wrapper
