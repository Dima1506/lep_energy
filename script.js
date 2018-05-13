ymaps.ready(init);

var myMap;
var kal =true;

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}


function init () {
    // Параметры карты можно задать в конструкторе.
    myMap = new ymaps.Map(
        // ID DOM-элемента, в который будет добавлена карта.
        'map',
        // Параметры карты.
        {
            // Географические координаты центра отображаемой карты.
            center: [56.854602, 35.877191],
            // Масштаб.
            zoom: 7,
            // Тип покрытия карты: "Спутник".
            type: 'yandex#hybrid'
        }

    );

    /*ymaps.regions.load('RU', {
    	lang: 'ru',
    	quality: 3
	}).then(function (result) {
    	var regions = result.geoObjects;
    // Включим возможность перетаскивания регионов.
    	//regions.options.set('draggable', true);
    // Проходим по коллекции регионов и ищем Иркутскую область (osmId = 145454).
    	regions.each(function (reg) {
        	if (reg.properties.get('osmId') == 2095259) {
            // Меняем цвет на красный
            	reg.options.set('fillColor', 'ff000000')
        	}
        	else{

        		reg.options.set('fillColor', 'ff003377');
        	}
    });

    	myMap.geoObjects.add(regions); 
 	}, function () {

	});*/

	/*myMap.events.add(['click', 'contextmenu'], function (e) {
    	var coords = e.get('coords');
    	eType == 'click' ? alert('left button') : alert('right button');
    	alert(coords[0].toPrecision(6))
	});*/
	/*var myButton = new ymaps.control.Button('<b>Я<b>');
	myButton.events
	    .add('click', function () { alert('Щёлк'); })
	    .add('select', function () { 
	    	if (kal == true){
	    		kal = false;
	    	}
	    	else{
	    		kal = true;
	    	}

	     })
	    .add('deselect', function () { alert('Отжата'); });
	myMap.controls.add(myButton);*/


    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
            
        //alert(coords[0].toPrecision(6))
        var x = new XMLHttpRequest();
		x.open("GET", 'http://deltax.pythonanywhere.com/api', true);
		//x.setHeader("Access-Control-Allow-Origin", "*");
		x.onload = function (){
		    alert( x.responseText);
		}
		x.send(null);
    });



    // Обработка события, возникающего при щелчке
    // правой кнопки мыши в любой точке карты.
    // При возникновении такого события покажем всплывающую подсказку
    // в точке щелчка.
    
   

    

	
}
function setCenter () {
    myMap.setCenter([57.767265, 40.925358]);
}

function setBounds () {
    // Bounds - границы видимой области карты.
    // Задаются в географических координатах самой юго-восточной и самой северо-западной точек видимой области.
    myMap.setBounds([[37, 38], [39, 40]]);
}

function setTypeAndPan () {
    // Меняем тип карты на "Гибрид".
    myMap.setType('yandex#hybrid');
    // Плавное перемещение центра карты в точку с новыми координатами.
    myMap.panTo([62.915, 34.461], {
            // Задержка между перемещениями.
            delay: 1500
        });
}
