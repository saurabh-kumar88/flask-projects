/* This function works as Librarry for icon markers for all types tree species
Every tree icon object have different properties..like iconSize, shdowSize
NOTE: tree specie name stored in db should match here...*/

function tree_icon_object(string)
{
    // common dir for tree icons 
    const icon_path = "static/images/tree_icons/"
    
    if(string == "Maple_tree")
    {
        
        var Maple_tree = L.icon({            
        iconUrl: icon_path + 'Maple_tree.png',
        shadowUrl: icon_path + 'Maple_tree_shadow.png',
        iconSize:     [50, 95],  
        shadowSize:   [50, 95], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [25, 0] 

        });
        
        return (Maple_tree);
    }

    else if(string == "Acacia_tortillis")
    {
        var Acacia_tortillis = L.icon({            
        iconUrl: icon_path + 'Acacia_tortillis.png',
        shadowUrl: icon_path + 'Acacia_tortillis_shadow.png',
        iconSize:     [100, 95],  
        shadowSize:   [100, 95], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [50, 10] 

        });

        return (Acacia_tortillis);
    }

    else if(string == "Birch")
    {
        var Birch = L.icon({            
        iconUrl: icon_path + 'Birch.png',
        shadowUrl: icon_path + 'Birch_shadow.png',
        iconSize:     [60, 95],  
        shadowSize:   [60, 95], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [30, 0]

        });
        
        return (Birch);
    }

    else if(string == "Brachychiton")
    {
        var Brachychiton = L.icon({            
        iconUrl: icon_path + 'Brachychiton.png',
        shadowUrl: icon_path + 'Brachychiton_shadow.png',
        iconSize:     [60, 95],  
        shadowSize:   [60, 95], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [30, 0] 

        });

        return (Brachychiton);
    }

    else if(string == "Cadrus")
    {
        var Cadrus = L.icon({            
        iconUrl: icon_path + 'Cadrus.png',
        shadowUrl: icon_path + 'Cadrus_shadow.png',
        iconSize:     [100, 100],  
        shadowSize:   [100, 100], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [50, 10] 

        });

        return (Cadrus);
    }

    else if(string == "Dracena_draco")
    {
        var Dracena_draco = L.icon({            
        iconUrl: icon_path + 'Dracena_draco.png',
        shadowUrl: icon_path + 'Dracena_draco_shadow.png',
        iconSize:     [100, 80],  
        shadowSize:   [100, 80], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [50, 5] 

        });

        return (Dracena_draco);
    }

    else if(string == "False_Ashoka")
    {
        var False_Ashoka = L.icon({            
        iconUrl: icon_path + 'False_Ashoka.png',
        shadowUrl: icon_path + 'False_Ashoka_shadow.png',
        iconSize:     [40, 90],  
        shadowSize:   [40, 90], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [20, 5] 

        });

        return (False_Ashoka);
    }


    else if(string == "Bargad")
    {
        var Ficus_benghalensis = L.icon({            
        iconUrl: icon_path + 'Ficus_benghalensis.png',
        shadowUrl: icon_path + 'Ficus_benghalensis_shadow.png',
        iconSize:     [100, 70],  
        shadowSize:   [100, 70], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [45, 5] 

        });

        return (Ficus_benghalensis);
    }

    else if(string == "Neem")
    {
        var Azardiricta_indica = L.icon({            
        iconUrl: icon_path + 'Azardiricta_indica.png',
        shadowUrl: icon_path + 'Azardiricta_indica_shadow.png',
        iconSize:     [100, 85],  
        shadowSize:   [100, 85], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [45, 5] 

        });

        return (Azardiricta_indica);
    }


    else if(string == "Gulmohar")
    {
        var Delonix_regia = L.icon({            
        iconUrl: icon_path + 'Delonix_regia.png',
        shadowUrl: icon_path + 'Delonix_regia_shadow.png',
        iconSize:     [60, 100],  
        shadowSize:   [60, 100], 
        iconAnchor:   [0, 0], 
        shadowAnchor: [-5, 25],  
        popupAnchor:  [35, 5] 

        });

        return (Delonix_regia);
    }

    // default return, if no match found
    else
    {
        return NaN;
    }


};


    var Longitude = '{{Lon}}';
    var Latitude = '{{Lat}}';
    var TreeCode = '{{treeCode}}';
    var Specie = '{{specie}}';
    var mymap = L.map('map').setView([Longitude, Latitude], 18);

   /*     
    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 20,
    //id: 'mapbox.dark-v9',
    //id: 'mapbox.mapbox-streets',
    accessToken: 'pk.eyJ1IjoieWtpbmc4OCIsImEiOiJjam9scGdjZGYwYmM4M3ZxYnprcnJlMWJvIn0.Ey_PnhKVVx1BBYC2T2NNjw'
    }).addTo(mymap);
    */    
    
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 20,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoieWtpbmc4OCIsImEiOiJjam9scGdjZGYwYmM4M3ZxYnprcnJlMWJvIn0.Ey_PnhKVVx1BBYC2T2NNjw'
    }).addTo(mymap);
    
                
    // get tree_icon           
    tree_icon = tree_icon_object(Specie);
    
    var Banyan =  L.marker([Longitude, Latitude], {icon: tree_icon}).addTo(mymap);
    Banyan.bindPopup(TreeCode + " <br> Hi, i am " + Specie + " tree! ").openPopup();