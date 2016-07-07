var myMap;
var markers = [];
var markersLayer = new L.LayerGroup();

// function initialize_gmap(lat,long_) {
//     var myCenter = new google.maps.LatLng(lat, long_); //new google.maps.LatLng(53.6369, -2.1398);
//     var mapProp = {
//       center:myCenter,
//       zoom:10,
//       scrollwheel:false,
//       draggable:true,
//       mapTypeId:google.maps.MapTypeId.ROADMAP
//       };
//
//     var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
//
//     var marker = new google.maps.Marker({
//       position:myCenter,
//       });
//
//     marker.setMap(map);
// }

function initialize_lmap(lat, long_){
    myMap = L.map('googleMap').setView([lat, long_],13);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'ankitvb.0h4ap8k0',
    accessToken: 'pk.eyJ1IjoiYW5raXR2YiIsImEiOiJjaXB6MWRieG0wMDBhajdtMnV2a240MGg2In0.atqX9KU-PeSqxuDaLpEfbQ'
    }).addTo(myMap);

    var marker = L.marker([lat,long_]).addTo(myMap);

    markersLayer.addTo(myMap);
}

function add_circles(addrList){
   var circle;
   var popup;
   var typeText;

   for(i=0; i<addrList.length; i++){
     switch (addrList[i][3]) {
       case 'F':
       typeText = 'Flat';
       break;
       case 'D':
       typeText = 'Detached';
       break;
       case 'S':
       typeText = 'Semi-Detached';
       break;
       case 'T':
       typeText = 'Terrace';
       break;
     }
     popup = L.popup().setContent('Address: '+addrList[i][6]+', '+addrList[i][8]+', '+addrList[i][9]+' '+addrList[i][2]+'<br>'
                                  +'Price: '+'&pound;&nbsp;'+numeral(addrList[i][0]).format('0,0')+'<br>'
                                  + 'Type: '+typeText);
     circle = L.circle([addrList[i][10], addrList[i][11]],
       100, // radius in m
       {color:'red'}
     ).bindPopup(popup);

     markersLayer.addLayer(circle);

        //console.log(addrList[i][10], addrList[i][11]);
    }
}

function generate_table(addrList){
    var myText = '<thead><tr><th>Date</th><th>Price</th><th>Type</th><th>Address</th></tr></thead>';
    var typeText;

    myText += '<tbody>'
    for(i=0; i<addrList.length; i++){
        if(addrList[i][3] != 'O'){
            switch (addrList[i][3]) {
              case 'F':
                typeText = 'Flat';
                break;
              case 'D':
                typeText = 'Detached';
                break;
              case 'S':
                typeText = 'Semi-Detached';
                break;
              case 'T':
                typeText = 'Terrace';
                break;
            }
            myText += '<tr><td>'+addrList[i][1].slice(0,10)+'</td>'
                    + '<td>'+'&pound;&nbsp;'+numeral(addrList[i][0]).format('0,0')+'</td>'
                    + '<td>'+typeText+'</td>'
                    + '<td>'+addrList[i][6]+', '+addrList[i][8]+', '+addrList[i][9]+' '+addrList[i][2]+'</td></tr>';
        }
    }
    myText += '</tbody>'

    $('#recent-sales').html(myText);
    $('#recent-sales').DataTable({"order": [[0,"desc"]]});
}

$(function(){
    var submit_form = function(e) {
    $("#estimate-modal").show();
    hometype = $('select[name="type"]').val();
    var zipcode = $('input[name="zip"]').val();

    // AJAX call to get estimate: getJSON(url,data,func)
    $.getJSON($SCRIPT_ROOT + '/get_estimate', {
              zip: $('input[name="zip"]').val(),
              type: $('select[name="type"]').val(),
              newbuild: $('select[name="newbuild"]').val(),
              esttype: $('select[name="esttype"]').val()
              }, function(data) {
              //console.log(data);
              if(data.result[8].price > 0){
                  $("#estimate-modal").modal("toggle")
                  $('#dashboard').show()
                  $('#plots').show()
                  $('#myestimate').html("&pound;&nbsp;"+numeral(data.result[8].price).format('0,0'));
                  if(data.result[2][hometype] > 0){
                      $('#fiveyravg').html("&pound;&nbsp;"+numeral(data.result[2][hometype]).format('0,0'));
                  }else{
                      $('#fiveyravg').html("&pound;&nbsp;"+numeral(data.result[3][hometype]).format('0,0'));
                  }
                  var qlat = data.result[8].latitude;
                  var qlong = data.result[8].longitude;
                  // Generate map
                  initialize_lmap(qlat, qlong);
                  add_circles(data.result[6]);
                  plot_histogram(data.result[7], zipcode);
                  // Generate table
                  generate_table(data.result[6]);
                  // Mean price/vol plots
                  plot_yearly_mean(data.result[0], data.result[1], data.result[4], data.result[5], zipcode);
                  plot_typewise_mean(data.result[2], data.result[3], zipcode);
                  // Scroll to dashboard
                  $('html, body').animate({
                      scrollTop: $("#dashboard").offset().top
                      }, 1000);
            }else{
              $('#estimator').html("<p>Invalid Zipcode! Please try again. </p>")
            }
            });
    return false;
    };

    // Bind search button to call above
    $("#dashboard").hide()
    $("#plots").hide()
    $("#estimate-modal").on('shown.bs.modal', submit_form);
    $('[data-toggle="popover"]').popover();
    });

    $(document).ready(function(){
      $('[data-toggle="popover"]').popover();
    });
