import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache
def load_data():
    df = pd.read_csv('data/data.csv', encoding='cp1252', low_memory=False)

    cols_to_rmv = ['stn_code', 'sampling_date', 'spm','pm2_5', 'agency', 'location_monitoring_station']
    df.drop(cols_to_rmv, axis=1, inplace=True)
    df['type'] = df['type'].fillna('Others')
    df['location'].fillna(df.location.mode()[0], inplace=True)
    df['date'].fillna(df.date.mode()[0], inplace=True)
    df['type'].replace('Residential, Rural and other Areas','Residential', inplace=True)
    df['type'].replace('Residential and others', 'Residential', inplace=True)
    df['type'].replace('Industrial Areas', 'Industrial', inplace=True)
    df['type'].replace('Industrial Area', 'Industrial', inplace=True)
    df['type'].replace('Sensitive Area', 'Sensitive', inplace=True)
    df['type'].replace('Sensitive Areas', 'Sensitive', inplace=True)
    df['type'].replace('RIRUO', 'Rural', inplace=True)

    df.replace(to_replace='Visakhapatnam',value='Vishakhapatnam', inplace=True)
    df.replace(to_replace='Silcher', value='Silchar', inplace=True)
    df.replace(to_replace='Kotttayam', value='Kottayam', inplace=True)
    df.replace(to_replace='Bhubaneswar', value='Bhubaneshwar', inplace=True)
    df.replace(to_replace='Pondichery', value='Pondicherry', inplace=True)
    df.replace(to_replace='Noida, Ghaziabad', value='Noida', inplace=True)
    df.replace(to_replace='Calcutta', value='Kolkata', inplace=True)
    df.replace(to_replace='Greater Mumbai', value='Mumbai', inplace=True)
    df.replace(to_replace='Navi Mumbai', value='Mumbai', inplace=True)
    df.replace(to_replace='Bombay', value='Mumbai', inplace=True)
    df.replace(to_replace='andaman-and-nicobar-islands',value='Andaman & Nicobar Islands', inplace=True)
    df.replace(to_replace='Uttaranchal',value='Uttarakhand', inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df.drop('date', axis=1, inplace=True)

    return df

df = load_data()
limit = 100
states = list(df['state'].unique())
states.sort()
cities = list(df['location'].unique())
cities.sort()
years = list(df['year'].unique())
years.sort()

type_groupby = df['type'].value_counts()
so2_type_groupby = df.groupby('type')['so2'].mean()
no2_type_groupby = df.groupby('type')['no2'].mean()
rspm_type_groupby = df.groupby('type')['rspm'].mean()

so2_state_groupby = df.groupby('state')['so2'].mean()
no2_state_groupby = df.groupby('state')['no2'].mean()
rspm_state_groupby = df.groupby('state')['rspm'].mean()

so2_location_groupby = df.groupby('location')['so2'].mean()
no2_location_groupby = df.groupby('location')['no2'].mean()
rspm_location_groupby = df.groupby('location')['rspm'].mean()

so2_year_groupby = df.groupby('year')['so2'].mean()
no2_year_groupby = df.groupby('year')['no2'].mean()
rspm_year_groupby = df.groupby('year')['rspm'].mean()

st.sidebar.title("Air Pollution data Analysis")
options = [
    'Introduction',
    'About',
    'View Raw Data',
    'Analysis - Type Wise',
    'Analysis - State Wise',
    'Analysis - City Wise',
    'Analysis - Year Wise',
    'Analysis - Geo Visualization',
    'Statistical Analysis',
    'Conclusion'
]
menu = st.sidebar.radio("Select an Option", options)

if menu == options[0]:
    st.title("Air Pollution Data Analysis")
    st.image('image/img1.jpeg',use_column_width=True)
    st.write("Air pollution is a phenomenon when the atmosphere is contaminated with pollutants such as gases(  Sulphur dioxide (SO2),  Nitrogen dioxide (NO2),etc.), particulates ( respirable suspended particulate matter (RSPM),  etc.), organic matter( Ash, toxins, etc.).  which causes an enormous amount of death per year as well as astronomical amount of economic damage. it causes disease such as respirator diseases,  cardiovascular diseases,  and affect immunity of the body. nowadays air pollution is major issue faced by every country and it is ranked as major cause of death to humans as well as causing adverse effect to the environment.  it can cause and effect like low visibility, respiratory trouble as well as death.")
if menu == options[1]:
    st.image('image/img2.jpeg',width=500)
    st.write("Earlier the air we breathe in use to be pure and fresh. But, due to increasing industrialization and concentration of poisonous gases in the environment the air is getting more and more toxic day by day. Also, these gases are the cause of many respiratory and other diseases. Moreover, the rapidly increasing human activities like the burning of fossil fuels, deforestation is the major cause of air pollution.")
    st.write("The fossil fuel, firewood, and other things that we burn produce oxides of carbons which got released into the atmosphere. Earlier there happens to be a large number of trees which can easily filter the air we breathe in. But with the increase in demand for land, the people started cutting down of trees which caused deforestation. That ultimately reduced the filtering capacity of the tree.Moreover, during the last few decades, the numbers of fossil fuel burning vehicle increased rapidly which increased the number of pollutants in the air.")

if menu == options[2]:
    st.header("Data Source")
    if st.checkbox("Show Cleaned Data"):
        st.write(df)
    if st.checkbox("Show List of States & Union Territories"):
        st.text('List of States & Union Territories')
        st.write(states)
    if st.checkbox("Show List of Cities"):
        st.text('List of Cities')
        st.write(cities)
    if st.checkbox("Show Range of Years"):
        st.text('List of Years')
        st.write(years)

if menu == options[3]:
    st.header("Area Type Wise Data Representation")
    df1 = pd.DataFrame(type_groupby)
    df2 = pd.DataFrame(so2_type_groupby)
    df3 = pd.DataFrame(no2_type_groupby)
    df4 = pd.DataFrame(rspm_type_groupby)
    type_df = df1.merge(df2, left_index=True, right_index=True).merge(
        df3, left_index=True, right_index=True).merge(df4, left_index=True, right_index=True)
    if st.checkbox("Show Type Wise Data"):
        st.write(type_df)

    cols = ['Type Count', 'SO2', 'NO2', 'RSPM']
    choice = st.selectbox("select a columns", cols)

    if choice == cols[0]:
        st.subheader("Type Wise Count")
        st.bar_chart(df1, width=2, height=450, use_container_width=True)
    if choice == cols[1]:
        st.subheader("Type Wise SO2 Distribution")
        st.bar_chart(type_df.so2, width=2, height=450,
                     use_container_width=True)
    if choice == cols[2]:
        st.subheader("Type Wise NO2 Distribution")
        st.bar_chart(type_df.no2, width=2, height=450,
                     use_container_width=True)
    if choice == cols[3]:
        st.subheader("Type Wise RSPM Distribution")
        st.bar_chart(type_df.rspm, width=2, height=450,
                     use_container_width=True)

if menu == options[4]:
    st.header("State Wise Data Representation")
    df1 = pd.DataFrame(so2_state_groupby)
    df2 = pd.DataFrame(no2_state_groupby)
    df3 = pd.DataFrame(rspm_state_groupby)
    state_df = df1.merge(df2, left_index=True, right_index=True).merge(
        df3, left_index=True, right_index=True)
    df.replace(to_replace='NaN', value='na', inplace=True)
    state_df.dropna(axis=0, how='all', inplace=True)
    if st.checkbox("Show State Wise Data"):
        st.write(state_df)

    cols = ['SO2', 'NO2', 'RSPM']
    choice = st.selectbox("select a columns", cols)

    if choice == cols[0]:
        st.subheader("State Wise SO2 Distribution")
        st.bar_chart(state_df.so2, width=2, height=450,
                     use_container_width=True)
    if choice == cols[1]:
        st.subheader("State Wise NO2 Distribution")
        st.bar_chart(state_df.no2, width=2, height=450,
                     use_container_width=True)
    if choice == cols[2]:
        st.subheader("State Wise RSPM Distribution")
        st.bar_chart(state_df.rspm, width=2, height=450,
                     use_container_width=True)
if menu == options[5]:
    st.header("City Wise Data Representation")
    df1 = pd.DataFrame(so2_location_groupby)
    df2 = pd.DataFrame(no2_location_groupby)
    df3 = pd.DataFrame(rspm_location_groupby)
    location_df = df1.merge(df2, left_index=True, right_index=True).merge(
        df3, left_index=True, right_index=True)
    df.replace(to_replace='NaN', value='na', inplace=True)
    location_df.dropna(axis=0, how='all', inplace=True)
    location_df.index = location_df.index.str.lower()
    so2_location_groupby1 = df.groupby([df['location']])[
        'so2'].mean().sort_values(ascending=False)
    so2_location_groupby.index = so2_location_groupby.index.str.lower()
    no2_location_groupby1 = df.groupby([df['location']])[
        'no2'].mean().sort_values(ascending=False)
    no2_location_groupby.index = no2_location_groupby.index.str.lower()
    rspm_location_groupby1 = df.groupby([df['location']])[
        'rspm'].mean().sort_values(ascending=False)
    rspm_location_groupby.index = rspm_location_groupby.index.str.lower()
    if st.checkbox("Show City Wise data"):
        st.write(location_df)

    f = st.form(key="f1")
    limit = f.slider("Limit of records", min_value=20, max_value=294)
    if f.form_submit_button("update"):
        st.info(f"limit changed to {limit}")
    so2_location_groupby2 = pd.DataFrame(so2_location_groupby1.head(limit))
    so2_location_groupby2['index'] = so2_location_groupby2.reset_index(
        level=0, inplace=True)
    no2_location_groupby2 = pd.DataFrame(no2_location_groupby1.head(limit))
    no2_location_groupby2['index'] = no2_location_groupby2.reset_index(
        level=0, inplace=True)
    rspm_location_groupby2 = pd.DataFrame(rspm_location_groupby1.head(limit))
    rspm_location_groupby2['index'] = rspm_location_groupby2.reset_index(
        level=0, inplace=True)

    cols = ['SO2', 'NO2', 'RSPM']
    choice = st.selectbox("select a columns", cols)

    if choice == cols[0]:
        st.subheader("City Wise SO2 Distribution")
        f, ax = plt.subplots(figsize=(25, 12))
        ax = sns.barplot(x="location", y="so2",
                         data=so2_location_groupby2, ax=ax)
        st.write(f)
    if choice == cols[1]:
        st.subheader("City Wise NO2 Distribution")
        f, ax = plt.subplots(figsize=(25, 12))
        ax = sns.barplot(x="location", y="no2",
                         data=no2_location_groupby2, ax=ax)
        st.write(f)
    if choice == cols[2]:
        st.subheader("City Wise RSPM Distribution")
        f, ax = plt.subplots(figsize=(25, 12))
        ax = sns.barplot(x="location", y="rspm",
                         data=rspm_location_groupby2, ax=ax)
        st.write(f)

if menu == options[6]:
    st.header("Year Wise Data Representation")
    df1 = pd.DataFrame(so2_year_groupby)
    df2 = pd.DataFrame(no2_year_groupby)
    df3 = pd.DataFrame(rspm_year_groupby)
    year_df = df1.merge(df2, left_index=True, right_index=True).merge(
        df3, left_index=True, right_index=True)
    if st.checkbox("Show Year Wise Data"):
        st.write(year_df)

    cols = ['SO2', 'NO2', 'RSPM']
    choice = st.selectbox("select a columns", cols)

    if choice == cols[0]:
        st.subheader("Year Wise SO2 Distribution")
        st.bar_chart(year_df.so2, width=2, height=450,
                     use_container_width=True)
    if choice == cols[1]:
        st.subheader("Year Wise NO2 Distribution")
        st.bar_chart(year_df.no2, width=2, height=450,
                     use_container_width=True)
    if choice == cols[2]:
        st.subheader("Year Wise RSPM Distribution")
        st.bar_chart(year_df.rspm, width=2, height=450,
                     use_container_width=True)

if menu == options[7]:
    st.header("Geo Visualization Data Representation")
    df1 = pd.DataFrame(so2_state_groupby)
    df2 = pd.DataFrame(no2_state_groupby)
    df3 = pd.DataFrame(rspm_state_groupby)
    state_df = df1.merge(df2, left_index=True, right_index=True).merge(
        df3, left_index=True, right_index=True)
    sloc = state_df
    sloc['index'] = sloc.index.tolist()
    if st.checkbox("Show Data"):
        st.write(sloc)

    cols = ['SO2', 'NO2', 'RSPM']
    choice = st.selectbox("select a columns", cols)

    if choice == cols[0]:
        st.subheader("Geo Visualization SO2 Distribution")
        wmap = folium.Map(location=[25, 80], zoom_start=4)
        folium.Choropleth(
            geo_data='india_states.json',
            name='choropleth',
            data=sloc,
            columns=['index', 'so2'],
            key_on='feature.properties.NAME_1',
            fill_color='YlOrRd',
            fill_opacity=0.75,
            line_opacity=0.3,
            legend_name='so2 Distribution Across India'
        ).add_to(wmap)
        folium_static(wmap)

    if choice == cols[1]:
        st.subheader("Geo Visualization NO2 Distribution")
        wmap = folium.Map(location=[25, 80], zoom_start=4)
        folium.Choropleth(
            geo_data='india_states.json',
            name='choropleth',
            data=sloc,
            columns=['index', 'no2'],
            key_on='feature.properties.NAME_1',
            fill_color='YlOrRd',
            fill_opacity=0.75,
            line_opacity=0.3,
            legend_name='no2 Distribution Across India'
        ).add_to(wmap)
        folium_static(wmap)
    if choice == cols[2]:
        st.subheader("Geo Visualization RSPM Distribution")
        wmap = folium.Map(location=[25, 80], zoom_start=4)
        folium.Choropleth(
            geo_data='india_states.json',
            name='choropleth',
            data=sloc,
            columns=['index', 'rspm'],
            key_on='feature.properties.NAME_1',
            fill_color='YlOrRd',
            fill_opacity=0.75,
            line_opacity=0.3,
            legend_name='RSPM Distribution Across India'
        ).add_to(wmap)
        folium_static(wmap)

if menu == options[8]:
    st.header("Relation Between State & Year")
    cols = ['SO2', 'NO2', 'RSPM']
    choice = st.selectbox("select a columns", cols)
    so2_year_state = df.pivot_table('so2', index='state', columns=[
                                    'year'], aggfunc='mean', fill_value=0, margins=True)
    so2_year_state.fillna(0, inplace=True)
    no2_year_state = df.pivot_table('no2', index='state', columns=[
                                    'year'], aggfunc='mean', fill_value=0, margins=True)
    no2_year_state.fillna(0, inplace=True)
    rspm_year_state = df.pivot_table('rspm', index='state', columns=[
                                     'year'], aggfunc='mean', fill_value=0, margins=True)
    rspm_year_state.fillna(0, inplace=True)
    if choice == cols[0]:
        st.subheader("Heatmap of SO2 Between State & Year")
        f, ax = plt.subplots(figsize=(25,12))
        ax.set_title('{} by state and year'.format('so2'))
        sns.heatmap(so2_year_state, annot=True, cmap="YlGnBu", fmt='.3g', mask=so2_year_state.isnull(
        ), linewidths=2, ax=ax, cbar_kws={'label': 'Annual Average'})
        st.write(f)
    if choice == cols[1]:
        st.subheader("Heatmap of NO2 Between State & Year")
        f, ax = plt.subplots(figsize=(25, 12))
        ax.set_title('{} by state and year'.format('no2'))
        sns.heatmap(no2_year_state, annot=True, cmap="YlGnBu", fmt='.3g', mask=no2_year_state.isnull(
        ), linewidths=2, ax=ax, cbar_kws={'label': 'Annual Average'})
        st.write(f)
    if choice == cols[2]:
        st.subheader("Heatmap of RSPM Between State & Year")
        f, ax = plt.subplots(figsize=(15, 7))
        ax.set_title('{} by state and year'.format('rspm'))
        sns.heatmap(rspm_year_state, annot=True, cmap="YlGnBu", fmt='.3g', mask=rspm_year_state.isnull(
        ), linewidths=2, ax=ax, cbar_kws={'label': 'Annual Average'})
        st.write(f)
        
if menu == options[9]:
    st.write("There has been a gradual increase and then gradual decrease in level of SO2, NO2, RSPM in various states while few states have either maintained above average level or increse in the level of SO2, NO2, RSPM.")

