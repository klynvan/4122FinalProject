#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[2]:


# Load the data
data = pd.read_csv("combined.csv")

#sets up tabs
tab1, tab2 = st.tabs(["Choropleth","Graphs"])
# Set up the Streamlit app
with tab1:
    col1, col2 = st.columns(2)
    st.title("World Happiness Report 2015")
    with col1:
        st.title("Filters")
        economy_status = st.radio("Economy", ["Developed", "Developing", "Both"])
        pop_min, pop_max = st.slider("Population(In Millions)", 0, int(data["Population_mln"].max()), (0, int(data["Population_mln"].max())))
        gen_min, gen_max = st.slider("Generosity", 0.0, 1.0, (0.0, 1.0))
        trust_min, trust_max = st.slider("Government Trust", 0.0, 1.0, (0.0, 1.0))
        school_min, school_max = st.slider("Schooling(Average years of age 25+ spent in formal education)", 0, int(data["Schooling"].max()), (0, int(data["Schooling"].max())))
        free_min, free_max = st.slider("Freedom", 0.0, 1.0, (0.0, 1.0))
        gdp_min, gdp_max = st.slider("GDP per capita(In USD)", 0, int(data["GDP_per_capita"].max()), (0, int(data["GDP_per_capita"].max())))

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
    with col2:
        # Set up the choropleth map
        fig = px.choropleth(data,
                            locations="Country",
                            locationmode="country names",
                            color="Happiness Score",
                            hover_name="Country",
                            hover_data=["Generosity", "Population_mln", "Trust (Government Corruption)", "Schooling", "Freedom", "GDP_per_capita"],
                            color_continuous_scale=["red", "green"],
                            range_color=[0, 10])

        # Display the choropleth map
        st.plotly_chart(fig)

with tab2:
    st.title("Graphs")
    col3, col4 = st.columns(2)
    df_removed_year = data.copy()
    df_removed_year = df_removed_year.drop(['Year'], axis=1)
    df_removed_string = df_removed_year.copy()
    df_removed_string = df_removed_string.drop(['Country', 'Region'], axis=1)
    with col3:
        st.title("Options")
        xoption = st.selectbox(
            "Pick the value that will be ploted on the X axis",
            (df_removed_string.columns)
        )
        yoption = st.selectbox(
            "Pick the value that will be ploted on the Y axis",
            (df_removed_string.columns)
        )
        hueoption = st.selectbox(
            "Pick the value that will be the hue of the data points",
            (df_removed_year.columns)
        )

    with col4:
        fig = px.scatter(data, x=xoption, y=yoption, color=hueoption, hover_data=['Country'])
        st.plotly_chart(fig)
