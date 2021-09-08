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
 	      SERIES_ENDPOINTS = {
 	          min_temp: '/apps/temp-precip-trends/api/get-min-temp/',
 	          max_temp: '/apps/temp-precip-trends/api/get-max-temp/',
 	          mean_temp: '/apps/temp-precip-trends/api/get-mean-temp/',
 	          tot_prcp: '/apps/temp-precip-trends/api/get-total-precip/',
 	          cum_prcp: '/apps/temp-precip-trends/api/get-cum-precip/',
 	          prj_mean_temp: '/apps/temp-precip-trends/api/get-proj-mean-temp/',
 	          prj_cum_prcp: '/apps/temp-precip-trends/api/get-proj-cum-precip/',
 	          normal_temp: '/apps/temp-precip-trends/api/get-normal-data/normal-temp/',
 	          normal_prcp: '/apps/temp-precip-trends/api/get-normal-data/normal-prcp/',
 	          normal_cumm_prcp: '/apps/temp-precip-trends/api/get-normal-data/normal-cumm-prcp/',
 	      };

 	var public_interface,				// Object returned by the module
 	    m_auth_token,                   // User's authentication token for the API
 		m_map,				            // MapView object
 		m_plot,                         // Slide Sheet Plotly object/element
 		m_plot_data,                    // Data object of the slide sheet plot
 		m_plot_layout,                  // Layout object of the slide sheet plot
 		m_plot_subtitle,                // Subtitle for the slide sheet plot
 		m_plot_title,                   // Title for the slide sheet plot
 		m_valid_time,                   // Current valid time
 		m_valid_time_str,               // Current valid time as US locale date string
 		m_valid_time_request_str;       // Valid time formatted for request: YYYYMMDD

	/************************************************************************
 	*                    PRIVATE FUNCTION DECLARATIONS
 	*************************************************************************/
 	var init_members;
 	var init_valid_time;
 	var init_click_n_plot, update_lat_lon, update_depart_norms, update_plot,
 	    update_plot_series, update_plot_title, reset_plot, fetch_time_series;

 	/************************************************************************
 	*                    PRIVATE FUNCTION IMPLEMENTATIONS
 	*************************************************************************/
 	init_members = function() {
 	    let tpt_map_attrs = $('#tpt-map-attributes');
 	    m_map = TETHYS_MAP_VIEW.getMap();
 	    m_plot = MAP_LAYOUT.get_plot();
 	    m_auth_token = tpt_map_attrs.data('auth-token');
 	    m_plot_title = `Temp. + Precip. Trends`;
 	    m_plot_subtitle = `Data source: <a href="${ERA5_LINK}" target="_blank">ERA5</a>`;
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
                m_plot_title = `${m_plot_title} through ${m_valid_time_str}`;
                m_plot_subtitle = `${m_plot_subtitle}, 1950-${year}`;
            });
    };

    init_click_n_plot = function() {
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
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Token ${m_auth_token}`
            },
        });
        return response.json();
    };

    reset_plot = function() {
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
                'xanchor': 'center',
                'x': 0.5,
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
            'annotations': [
                // Plot title annotation
                {
                    'align': 'center',
                    'xref': 'paper',
                    'yref': 'paper',
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'x': 0.5,
                    'y': 1,
                    'text': m_plot_title,
                    'showarrow': false,
                    'bgcolor': "rgba(255, 255, 255, 0.5)",
                    'font': {
                        'size': 18,
                    },
                },
                // Plot subtitle annotation
                {
                    'align': 'center',
                    'xref': 'paper',
                    'yref': 'paper',
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'x': 0.5,
                    'y': 0.95,
                    'text': m_plot_subtitle,
                    'showarrow': false,
                    'bgcolor': "rgba(255, 255, 255, 0.5)",
                    'font': {
                        'size': 15,
                        'color': '#888888',
                    },
                },
                // Lat/lon annotation
                {
                    'align': 'center',
                    'xref': 'paper',
                    'yref': 'paper',
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'x': 0.5,
                    'y': 0.90,
                    'text': 'Lat: 0 Lon: 0',
                    'showarrow': false,
                    'bgcolor': "rgba(255, 255, 255, 0.5)",
                    'font': {
                        'size': 15,
                        'color': '#888888',
                    },
                },
                // 9-Month Departures from Normal
                {
                    'align': 'left',
                    'xref': 'paper',
                    'yref': 'paper',
                    'xanchor': 'right',
                    'yanchor': 'bottom',
                    'x': 0.98,
                    'y': 0.1,
                    'text': '9-Month Depatures from Normal:<br>Cum. Precip.: -<br>Mean Temp.: -',
                    'showarrow': false,
                    'bgcolor': "rgba(255, 255, 255, 0.75)",
                    'font': {
                        'size': 15,
                        'color': '#888888',
                    },
                },
            ]
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
                'hovertemplate': "Weekly. Precip.: %{y:.1f} mm",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 50,
                'name': 'Weekly Precip.',
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
            // normal_temp
            {
                'x': [],
                'y': [],
                'legendgroup': 'temp',
                'hovertemplate': "Normal Temp: %{y:.1f} \u00B0C",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 40,
                'name': "Normal Temperature",
                'type': 'scatter',
                'line': {
                    'color': '#000000',
                    'width': 1,
                },
            },
            // normal_cumm_prcp
            {
                'x': [],
                'y': [],
                'legendgroup': 'prcp',
                'hovertemplate': "Normal Cum. Precip.: %{y:.1f} mm",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 80,
                'name': "Normal Cumulative Precip.",
                'type': 'scatter',
                'yaxis': 'y2',
                'line': {
                    'color': '#01ff01',
                    'dash': 'dot',
                    'width': 1.5,
                },
            },
            // normal_tot_prcp
            {
                'x': [],
                'y': [],
                'legendgroup': 'prcpbar',
                'hovertemplate': "Normal Weekly. Precip.: %{y:.1f} mm",
                'hoverlabel': {
                    'namelength': 0,
                },
                'legendrank': 55,
                'name': 'Normal Weekly Precip.',
                'type': 'bar',
                'yaxis': 'y2',
                'marker': {
                    'color': '#0c0cfc',
                },
            },
        ];

        MAP_LAYOUT.update_plot('', m_plot_data, m_plot_layout);
    };

    update_lat_lon = function(lat, lon) {
        // Lat/lon is the 3rd annotation
        m_plot_layout.annotations[2].text = `Lat: ${lat.toFixed(2)} Lon: ${lon.toFixed(2)}`;
    };

    update_depart_norms = function(temp_series, prcp_series, normal_temp_series, normal_prcp_series) {
        // Compute the departures from normal for temperature
        let temp_loc = temp_series.time_series.values.length - 1;
        let curr_temp = temp_series.time_series.values[temp_loc];
        let normal_temp = normal_temp_series.time_series.values[temp_loc];
        let temp_diff = curr_temp - normal_temp;
        let temp_percent = (temp_diff / normal_temp) * 100;

        // Compute the departures from normal for precipitation
        let prcp_loc = prcp_series.time_series.values.length - 1;
        let curr_prcp = prcp_series.time_series.values[prcp_loc];
        let normal_prcp = normal_prcp_series.time_series.values[prcp_loc];
        let prcp_diff = curr_prcp - normal_prcp;
        let prcp_percent = (prcp_diff / normal_prcp) * 100;

        // Departures from normal is the 4th annotation
        m_plot_layout.annotations[3].text = `9-Month Depatures from Normal:<br>` +
            `Cum. Precip.: ${prcp_diff.toFixed(1)} mm / ${prcp_percent.toFixed(1)}%<br>` +
            `Mean Temp.: ${temp_diff.toFixed(1)} \u00B0C / ${temp_percent.toFixed(1)}%`;
    };

    update_plot_series = function(series_index, x, y) {
        m_plot_data[series_index].x = x;
        m_plot_data[series_index].y = y;
        m_plot_data[series_index].visible = true;
        MAP_LAYOUT.update_plot('', m_plot_data, m_plot_layout);
    };

    update_plot_title = function(title, subtitle) {
        // Plot title is the 1st annotation
        m_plot_layout.annotations[0].text = title;
        // Plot subtitle is the 2nd annotation
        m_plot_layout.annotations[1].text = subtitle;
    };

    update_plot = function(lat, lon) {
        reset_plot();

        // Update the latitude and longitude coordinates shown on the plot
        update_lat_lon(lat, lon);

        // Fetch the time series dataset for the given coordinates
        fetch_time_series('min_temp', lat, lon).then((data) => {
            console.log(data);
            update_plot_series(0,  // min_temp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        fetch_time_series('max_temp', lat, lon).then((data) => {
            update_plot_series(1,  // max_temp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        let mt_promise = fetch_time_series('mean_temp', lat, lon);
        mt_promise.then((data) => {
            update_plot_series(2,  // mean_temp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        fetch_time_series('tot_prcp', lat, lon).then((data) => {
            update_plot_series(3,  // tot_prcp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        let cp_promise = fetch_time_series('cum_prcp', lat, lon)
        cp_promise.then((data) => {
            update_plot_series(4,  // cum_prcp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        fetch_time_series('prj_mean_temp', lat, lon).then((data) => {
            update_plot_series(5,  // prj_mean_temp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        fetch_time_series('prj_cum_prcp', lat, lon).then((data) => {
            update_plot_series(6,  // prj_cum_prcp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        let nt_promise = fetch_time_series('normal_temp', lat, lon);
        nt_promise.then((data) => {
            update_plot_series(7,  // normal_temp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        let ncp_promise = fetch_time_series('normal_cumm_prcp', lat, lon);
        ncp_promise.then((data) => {
            update_plot_series(8,  // normal_cumm_prcp
                data.time_series.datetime,
                data.time_series.values,
            );
        });
        fetch_time_series('normal_prcp', lat, lon).then((data) => {
            update_plot_series(9,  // normal_prcp
                data.time_series.datetime,
                data.time_series.values,
            );
        });

        update_plot_title(m_plot_title, m_plot_subtitle);

        // Update the departure from normal stats when the four series needed have been retrieved
        Promise.all([mt_promise, cp_promise, nt_promise, ncp_promise]).then((values) =>{
            update_depart_norms(values[0], values[1], values[2], values[3]);
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
