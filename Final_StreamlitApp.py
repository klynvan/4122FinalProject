#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[15]:


# Load the data
data = pd.read_csv("combined.csv")

# Set up the Streamlit app
st.title("World Happiness Report 2015")
st.sidebar.title("Filter Countries")
economy_status = st.sidebar.radio("Economy", ["Developed", "Developing", "Both"])
pop_min, pop_max = st.sidebar.slider("Population", 0, int(data["Population_mln"].max()), (0, int(data["Population_mln"].max())))
gen_min, gen_max = st.sidebar.slider("Generosity", 0.0, 1.0, (0.0, 1.0))
trust_min, trust_max = st.sidebar.slider("Government Trust", 0.0, 1.0, (0.0, 1.0))
school_min, school_max = st.sidebar.slider("Schooling", 0, int(data["Schooling"].max()), (0, int(data["Schooling"].max())))
free_min, free_max = st.sidebar.slider("Freedom", 0.0, 1.0, (0.0, 1.0))
gdp_min, gdp_max = st.sidebar.slider("GDP per capita", 0, int(data["GDP_per_capita"].max()), (0, int(data["GDP_per_capita"].max())))

# Filter the data based on the selected economy and population range
if economy_status == 'Developed':
    data = data[data['Economy_status_Developed'] == 1]
elif economy_status == 'Developing':
    data = data[data['Economy_status_Developing'] == 1]

data = data[(data["Population_mln"] >= pop_min) & (data["Population_mln"] <= pop_max)]
data = data[(data["Generosity"] >= gen_min) & (data["Generosity"] <= gen_max)]
data = data[(data["Trust (Government Corruption)"] >= trust_min) & (data["Trust (Government Corruption)"] <= trust_max)]
data = data[(data["Schooling"] >= school_min) & (data["Schooling"] <= school_max)]
data = data[(data["Freedom"] >= free_min) & (data["Freedom"] <= free_max)]
data = data[(data["GDP_per_capita"] >= gdp_min) & (data["GDP_per_capita"] <= gdp_max)]

# Set up the choropleth map
fig = px.choropleth(data,
                    locations="Country",
                    locationmode="country names",
                    color="Happiness Score",
                    hover_name="Country",
                    hover_data=["Generosity", "Population_mln", "Trust (Government Corruption)", "Schooling", "Freedom", "GDP_per_capita"],
                    color_continuous_scale="RdBu",
                    range_color=[0, 10])

# Display the choropleth map
st.plotly_chart(fig)

