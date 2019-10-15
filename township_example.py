import geopandas as gpd
import folium
import pandas as pd
from branca.colormap import linear


## https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/GeoJSON_and_choropleth.ipynb?flush_cache=true


gem =  gpd.read_file('maps/townships.geojson')



m = folium.Map(location=[52.9,6.8], zoom_start=10.5, tiles='Stamen terrain')

df = pd.read_csv("data/data.csv", sep=';', encoding = "ISO-8859-1")
df['name'] = df['Regionaam']
df = gem.merge(df, on='name')


colormap = linear.YlGn_09.scale(
    df['Gemiddeld inkomen per inwoner'].min(),
    df['Gemiddeld inkomen per inwoner'].max())



df_dict = df.set_index('name')['Gemiddeld inkomen per inwoner']
color_dict = {key: colormap(df_dict[key]) for key in df_dict.keys()}

folium.GeoJson(
    df,
    tooltip=folium.GeoJsonTooltip(fields=['name', 'Gemiddeld inkomen per inwoner']),
#    style_function=lambda feature: {
#        'fillColor': color_dict[feature['id']],
#        'color': 'black',
#        'weight': 2,
#        'dashArray': '5, 5'
#   }  
).add_to(m)

m.save('GeoJSON_and_choropleth.html')

