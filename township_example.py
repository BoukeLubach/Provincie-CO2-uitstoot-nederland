import geopandas as gpd
import folium
import pandas as pd

gem =  gpd.read_file('maps/townships.geojson')



m = folium.Map(location=[52.9,6.8], zoom_start=10.5, tiles='Stamen terrain')

df = pd.read_csv("data/data.csv", sep=';', encoding = "ISO-8859-1")
df['name'] = df['Regionaam']
df = gem.merge(df, on='name')


#m.choropleth(
        
folium.Choropleth(df, 
             data=df, 
             key_on='feature.properties.name', 
             columns=['name', 'Gemiddeld inkomen per inwoner'], 
             fill_color='GnBu',  
             legend_name='Test',
             tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False, sticky=False),
             highlight_function=lambda x: {'weight':3,'fillColor':'grey'}).add_to(m)




#label = '{}: {} euro/inwoner'.format(df['name'], round(df['Gemiddeld inkomen per inwoner'], 1))

folium.Popup(label).add_to(m)

        
        
m.save('choropleth.html')