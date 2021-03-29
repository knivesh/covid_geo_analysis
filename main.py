import pandas as pd
import pycountry

df=pd.read_csv(r"dataset/time_series_covid19_confirmed_global.csv")

###Preprocessing
df_confirm=df.drop(['Province/State','Lat','Long'], axis=1)

#Repeating countries
vc=df_confirm['Country/Region'].value_counts().to_dict()
repeat_countries=[v for v in list(vc.items()) if v[1]>1]

df_confirm=df_confirm.groupby('Country/Region').agg('sum')
date_list=list(df_confirm.columns)

#Three letter country code
def country_code(country):
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return None

df_confirm['country']=df_confirm.index
df_confirm['iso_alpha_3']=df_confirm.country.apply(lambda x: country_code(x))

#Long form dataset
df_long=pd.melt(df_confirm, id_vars=['country', 'iso_alpha_3'])

###Plotting
import plotly.express as px

fig=px.choropleth(df_long,
              locations='iso_alpha_3',
              color='value',
              hover_name='country',
              animation_frame='variable',
              projection='natural earth',
              )
fig.show()
fig.write_html('covid_cased_worldwide.html')