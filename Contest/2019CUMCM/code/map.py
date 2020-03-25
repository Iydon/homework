# -*- encode: utf-8 -*-
# https://python-visualization.github.io/folium/quickstart.html
import folium
from folium import plugins

from data import cities, airline
from settings import html_file, translation, language


m = folium.Map(location=translation['location'][language],
	zoom_start=4,
	tiles='Stamen Terrain',)

# City -> Airport -> Aircraft
for city in cities:
    folium.Marker(city.coordinate[::-1],
        popup='<i>{}</i>'.format(city.airports),
        tooltip=city.name
    ).add_to(m)
    for airport in city.airports:
        folium.Marker(airport.coordinate[::-1],
            popup='<i>{}</i>'.format(airport),
            tooltip=airport.name,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

# Airline
attr = {
    'text': '\u2708' + ' '*16,
    'repeat': True,
    'offset': 8,
    'font_size': 8,
}

for path in airline:
    line = folium.PolyLine(
        [path[i].coordinate[::-1] for i in range(len(path))],
        weight=0.5,
    ).add_to(m)

    plugins.PolyLineTextPath(line, **attr).add_to(m)

m.save(html_file)
