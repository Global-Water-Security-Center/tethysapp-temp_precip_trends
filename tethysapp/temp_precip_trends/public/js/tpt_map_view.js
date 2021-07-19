$(function() {
    var map = TETHYS_MAP_VIEW.getMap();
    console.log(map);
    get_valid_time();
});

function get_valid_time() {
  let title_elem = document.querySelector('#nav-title .title');
  title_elem.innerHTML = '<img src="/static/temp_precip_trends/images/loading-dots.gif">';

  fetch('?method=get-valid-time')
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      title_elem.innerHTML = data.valid_time;
    });
}