import geopandas as gpd
import folium
import pandas as pd
from branca.colormap import linear


## https://nbviewer.jupyter.org/github/python-visualization/folium/blob/master/examples/GeoJSON_and_choropleth.ipynb?flush_cache=true


prov =  gpd.read_file('maps/provinces.geojson')

m = folium.Map(location=[52.5,6.9], zoom_start=8, tiles='Stamen terrain')

groningen = pd.read_csv("data/CO2-Uitstoot-Groningen.csv", sep = ';')
drenthe = pd.read_csv("data/CO2-Uitstoot-Drenthe.csv", sep = ';')
friesland = pd.read_csv("data/CO2-Uitstoot-Friesland.csv", sep = ';')
noord_holland = pd.read_csv("data/CO2-Uitstoot-Noord-Holland.csv", sep = ';')
zuid_holland = pd.read_csv("data/CO2-Uitstoot-Zuid-Holland.csv", sep = ';')
overijssel = pd.read_csv("data/CO2-Uitstoot-Overijssel.csv", sep = ';') 
flevoland = pd.read_csv("data/CO2-Uitstoot-Flevoland.csv", sep = ';')
zeeland = pd.read_csv("data/CO2-Uitstoot-Zeeland.csv", sep = ';')
gelderland = pd.read_csv("data/CO2-Uitstoot-Gelderland.csv", sep = ';')
noord_brabant = pd.read_csv("data/CO2-Uitstoot-Noord-Brabant.csv", sep = ';')
limburg = pd.read_csv("data/CO2-Uitstoot-Limburg.csv", sep = ';')
utrecht = pd.read_csv("data/CO2-Uitstoot-Utrecht.csv", sep = ';')

gebouwen = 'CO2-uitstoot Gebouwde Omgeving (gas, elektr. en warmte, tier 3/tier 2)'
industrie = 'CO2-uitstoot Industrie, Energie, Afval en Water (gas en elektr., tier 3)'
verkeer = 'CO2-uitstoot Verkeer en vervoer incl. auto(snel)wegen, excl. elektr. railverkeer (scope 1, tier 1)'
landbouw = 'CO2-uitstoot Landbouw, bosbouw en visserij, SBI A (gas, elektr., tier 3)'


def selectYearandSector(df, year, sector):

    df = df[df['Tegel'] == 'CO2-uitstoot per hoofdsector'] 
    df = df[df['Periode'] == year]
    df = df[df['Indicator'] == sector]
    df = df.drop(['Dashboard', 'Tegel', 'Bron', 'Omschrijving'], axis = 1)
    df['name'] = df[['regio / dimensie']]
    df = df.set_index('name')
    
    return df.Waarde.astype(int, errors='ignore')

industrie2017 = pd.DataFrame()
industrie2017 = selectYearandSector(groningen, 2017, industrie)
industrie2017 = industrie2017.append(selectYearandSector(friesland, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(drenthe, 2016, industrie))             #unknown value for 2017
industrie2017 = industrie2017.append(selectYearandSector(noord_holland, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(zuid_holland, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(overijssel, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(flevoland, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(zeeland, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(gelderland, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(noord_brabant, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(limburg, 2017, industrie))
industrie2017 = industrie2017.append(selectYearandSector(utrecht, 2017, industrie))

dff = prov.merge(industrie2017, on='name')


dff['CO2 uitstoot industrie'] = 1
for i in range(12):
    dff['CO2 uitstoot industrie'].iloc[i] = format(dff.Waarde.iloc[i],",") + " ton"



colormap = linear.OrRd_09.scale(
    industrie2017.min(),
    industrie2017.max())

color_dict = {key: colormap(industrie2017[key]) for key in industrie2017.keys()}
#
#
folium.GeoJson(
    dff,
    tooltip=folium.GeoJsonTooltip(fields=['name', 'CO2 uitstoot industrie']),
    style_function=lambda feature: {
        'fillColor': color_dict[feature['properties']['name']],
        'color': 'grey',
        'weight': 2,
        "fillOpacity":  0.7
#        'dashArray': '5, 5'
    }
).add_to(m)

folium.LayerControl().add_to(m)

m.save('Provincie-CO2-uitstoot-industrie.html')



