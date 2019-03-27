
if __name__ == "__main__":

    empireGeojson = ""
    with open('territoryBorders.geojson') as f:
        empireGeojson = f.read()
    continentsGeojson = ""
    with open('continents.geojson') as f:
        continentsGeojson = f.read()
    seasGeojson = ""
    with open('seas.geojson') as f:
        seasGeojson = f.read()
    battlesGeojson = ""
    with open('battles.geojson') as f:
        battlesGeojson = f.read()
    citiesGeojson = ""
    with open('cities.geojson') as f:
        citiesGeojson = f.read()


    # The header and beginning text for the map
    #  make sure to cite the leaflet things
    map_start = """<html>
      <head>
       <link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css"
   integrity="sha512-puBpdR0798OZvTTbP4A8Ix/l+A4dHDD0DGqYW6RQ+9jxkRFclaxxQb/SJAWZfWAkuyeQUytO7+7N4QKrDh+drA=="
   crossorigin=""/>
   <link rel="stylesheet" href = "map_style.css"/>
        <script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js"
   integrity="sha512-QVftwZFqvtRNi0ZyCtsznlKSWOStnDORoefr1enyq5mVL4tmKB3S/EnC3rRJcxCPavG10IcrVGSmPh6Qw5lwrg=="
   crossorigin=""></script>
        
        <script type="text/javascript">
          window.onload = function() {
          var map = L.map('map').setView([40, 25], 4.5);
          map.options.minZoom = 4;
          map.options.maxZoom = 6;
          var SW = L.latLng(10, -25);
          var NE = L.latLng(70, 60);
          var bounds = L.latLngBounds(SW, NE);
          map.setMaxBounds(bounds);
          
        map.on('drag', function () {
            map.panInsideBounds(bounds, {animate: false});
        });
          
          
          //setting a background color
          var bColor = '#0077be';
                var el = document.getElementsByClassName('leaflet-container');
                for (var i = 0; i < el.length; i++)
                {
                    el[i].style.backgroundColor = bColor;
                }
          
         baseLayer = L.geoJSON(""" + continentsGeojson + """, {
                style: continentStyle,
                
          }).addTo(map);
          
          function continentStyle(feature)
            {
                return {
                    fillColor: 'green',
                    weight: 1,
                    opacity:1,
                    color: 'green',
                    fillOpacity:1
                };
            }
        
        baseLayer = L.geoJSON(""" + empireGeojson + """, {
                style: empireStyle,
                onEachFeature: onEachFeature
                
          }).addTo(map);
          
          function empireStyle(feature)
            {
                return {
                    fillColor: 'blue',
                    weight: 1,
                    opacity:1,
                    color: 'black',
                    fillOpacity: 0.5
                };
            }
            
            function onEachFeature(feature, layer)
            {
                layer.on({
                    mouseover: highlightFeature,
                    mouseout: resetHighlight,
                });
            }
            
            function highlightFeature (e)
            {
                var layer = e.target;
                layer.setStyle({
                        weight: 5,
                        color: '#666',
                        fillOpacity: 0.7
                });
                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge)
                {
                    layer.bringToFront();
                }
                info.update(layer.feature.properties);
                console.log(layer.feature.properties);
                featureLayers();
            }
            
            function resetHighlight(e)
            {
                var layer = e.target;
               layer.setStyle({
                    weight:1,
                    fillOpacity: 0.5,
                    color: 'black'
               });
            info.update();
            featureLayers();
            }
            
            oceansMarkerOptions = {
            radius: 10,
            fillColor: "#FFFFFF",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 1
        };
            oceansLayer = L.geoJson(""" + seasGeojson +""", {
                pointToLayer: function (feature, latlng) {
                    var marker = L.circleMarker(latlng, oceansMarkerOptions);
                    marker.bindPopup(feature.properties.name);
                    return marker;
                }
            });
            oceansLayer.addTo(map);
            
            battlesMarkerOptions = {
            radius: 7,
            fillColor: "red",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 1
        };
            
            battlesLayer = L.geoJson(""" + battlesGeojson + """, {
                pointToLayer: function (feature, latlng) {
                    var marker = L.circleMarker(latlng, battlesMarkerOptions);
                    marker.bindPopup(feature.properties.name + '<br>' + feature.properties.year + '<br>' + feature.properties.description);
                    return marker;
                }
            });
            battlesLayer.addTo(map);
            battlesLayer.bringToFront();
            
            citiesMarkerOptions = {
            radius: 8,
            fillColor: "purple",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 1
        };
            citiesLayer = L.geoJson(""" + citiesGeojson +""", {
                pointToLayer: function (feature, latlng) {
                    var marker = L.circleMarker(latlng, citiesMarkerOptions);
                    marker.bindPopup(feature.properties.name);
                    return marker;
                }
            });
            citiesLayer.addTo(map);
            
            var info = L.control();

            info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
                this.update();
                return this._div;
            };
            
            var addOnLayers = [oceansLayer, battlesLayer, citiesLayer];
            var addOnLayersOn = [true, true, true];
            var layerNames = ["Seas", "Battles", "Cities"];

        // method that we will use to update the control based on feature properties passed
        info.update = function (props) {
        this._div.innerHTML = (props ?
            '<b>' + props.name + '</b>'
            : 'Hover over a territory');
        };

        info.addTo(map);
        addOnButtons();
        
        function addOnButtons ()
    {
    var addOns = addOnLayers.length;
    var layers = L.control({position: 'bottomleft'});
    layers.onAdd = function(map) {
        var div = L.DomUtil.create("div", "info");
        var boxes = new Array(addOnLayers.length);
        var labels = new Array(addOnLayers.length);
        for (var i = 0; i < addOns; i++)
        {
            boxes[i] = document.createElement('input'); // Create the box
            boxes[i].type = "checkbox";
            boxes[i].id = "id" + i;
            boxes[i].checked = true;

            labels[i] = document.createElement('text'); // Create the label
            labels[i].appendChild(document.createTextNode(' ' + layerNames[i] + ' '));

            div.appendChild(boxes[i]); // Add to map
            div.appendChild(labels[i]);

        }
        for (var x = 0; x < addOns; x++)
        {
            boxes[x].addEventListener('change', function () {

                var numChecked = this.id.charAt(2);
                if (this.checked)
                {
                    addOnLayersOn[numChecked] = true;
                    map.addLayer(addOnLayers[numChecked]);
                }
                else
                {
                    map.removeLayer(addOnLayers[numChecked]);
                    popUpsOn[numChecked] = false;
                }
                featureLayers();
            });
        }
        return div;
    }
    layers.addTo(map);
}
        
        function featureLayers()
        {
            for (var x = 0; x < addOnLayers.length; x++)
            {
                if(addOnLayersOn[x])
                {
                    addOnLayers[x].bringToFront();
                }
            }
        }
        
        var labels = ["Seas", "Battles", "Cities"]
        var colors = ["White", "Red", "Purple"]
        
        
        var legend = L.control({position: 'bottomleft'});   //Where it is
        legend.onAdd = function (map) {                     //Adds the legend
        var div = L.DomUtil.create('div', 'info legend')
        div.innerHTML += '<b>' + 'Legend' + '<br></b>';//Title
        for(var i = 0; i < labels.length; i++){
            div.innerHTML += '<i style="background:' + colors[i] + '"></i> '
                + labels[i] + '<br>';
        }
        return div;
    };
    legend.addTo(map);
    
    
    
        
        
            
            
            }; //end of window.onload


      """

    # The ending text for the map
    map_end = """
        </script>
      </head>

      <body style="border: 0; margin: 0;">
        <div id="map" style="width: 100%; height: 675px;"></div>
      </body>
    </html>"""

    # Opening and writing the file
    myfile = open("mymap.html", "w")
    myfile.write(map_start + map_end)
    myfile.close()