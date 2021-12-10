#!/usr/bin/env python
# coding: utf-8

# In[51]:


import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# In[52]:


df = pd.read_csv(r"C:\Users\HP\Downloads\datafile.csv")


# In[53]:


get_ipython().system('jupyter nbextension enable --py widgetsnbextension --sys-prefix')
get_ipython().system('jupyter serverextension enable voila --sys-prefix')


# In[54]:


import ipywidgets as widgets
from IPython.display import display, clear_output


# In[55]:


grand = widgets.ToggleButtons(
            options=['grandson', 'granddaughter']
        )


# In[56]:


df.head()


# In[57]:


shp_gdf = gpd.read_file(r'C:\Users\HP\Downloads\IND_adm\IND_adm3.shp')
shp_gdf.head()


# In[58]:


shp_gdf.shape


# In[59]:


new_map = shp_gdf[['NAME_3','geometry']]
new_map.head()


# In[60]:


merged = new_map.set_index("NAME_3").join(df.set_index("district"))
merged.head(20)


# In[61]:


merged.isna().sum()


# In[62]:


m1 = merged.dropna()


# In[63]:


import folium


# In[64]:


m1.head()


# In[65]:


m1.plot(figsize=(6,6))
plt.show()


# In[66]:


m1.crs


# In[67]:


m1 = m1.to_crs(epsg=2263)

# Access the centroid attribute of each polygon
m1['centroid'] = m1.centroid


# In[68]:


m1 = m1.to_crs(epsg=4326)

# Centroid column
m1['centroid'] = m1['centroid'].to_crs(epsg=4326)

m1.head()


# In[69]:


grd = m1.groupby('market').apply(lambda x : x.sort_values(by = 'modal_price', ascending = False).head(1).reset_index(drop = True))
print(grd)


# In[70]:


plt.scatter(grd['modal_price'],grd['market'], color='maroon',s=40,marker='*')
plt.xlabel("Modal Price")
plt.ylabel("Market")
plt.title("Maximum modal price per market")
plt.xlim([1500,3500])
plt.show()


# In[71]:


india = folium.Map(location = [20.5937,78.9629],zoom_start=4.5)


# ## Plotting the Maximum modal price with more detailing on India map 

# In[72]:


for _,r in grd.iterrows():
    lat = r['centroid'].y
    lon = r['centroid'].x
    folium.Marker(location=[lat, lon],
                  popup='<b>State:</b>{} <br> <b>Market:</b>{} <br> <b>Commodity:</b>{} <br> <b>Variety:</b>{} <br> <b>Date:</b>{} <br><b>Minimum price:</b>{} <br> <b>Maximum Price:</b>{} <br> <b>Modal price:</b>{}'.format(r['state'], r['market'], r['commodity'], r['variety'], r['arrival_date'], r['min_price'], r['max_price'], r['modal_price'])).add_to(india)

india


# In[73]:


plt.barh(m1['market'],m1['modal_price'])
plt.show()


# In[74]:


plt.scatter(m1['market'],m1['modal_price'])
plt.show()


# In[75]:


import plotly.express as px
dataf = px.data.gapminder().query("year == 2007")
fig = px.treemap(df, path=[px.Constant("world"), 'continent', 'country'], values='pop',
                  color='lifeExp', hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.show()

