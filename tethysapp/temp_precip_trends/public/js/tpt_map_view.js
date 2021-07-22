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
 	var public_interface,				// Object returned by the module
 		m_map;					        // MapView object

	/************************************************************************
 	*                    PRIVATE FUNCTION DECLARATIONS
 	*************************************************************************/
 	var get_valid_time;


 	/************************************************************************
 	*                    PRIVATE FUNCTION IMPLEMENTATIONS
 	*************************************************************************/
 	get_valid_time = function() {
      let title_elem = document.querySelector('#nav-title .title');
      title_elem.innerHTML = '<img src="/static/temp_precip_trends/images/loading-dots.gif">';

      fetch('?method=get-valid-time')
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          title_elem.innerHTML = data.valid_time;
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
		var m_map = TETHYS_MAP_VIEW.getMap();
        get_valid_time();
	});

	return public_interface;

}()); // End of library wrapper
