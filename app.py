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
    st.subheader("Air pollution is a phenomenon when the atmosphere is contaminated with pollutants such as gases(  Sulphur dioxide (SO2),  Nitrogen dioxide (NO2),etc.), particulates ( respirable suspended particulate matter (RSPM),  etc.), organic matter( Ash, toxins, etc.).  which causes an enormous amount of death per year as well as astronomical amount of economic damage. it causes disease such as respirator diseases,  cardiovascular diseases,  and affect immunity of the body. nowadays air pollution is major issue faced by every country and it is ranked as major cause of death to humans as well as causing adverse effect to the environment.  it can cause and effect like low visibility, respiratory trouble as well as death.")
if menu == options[1]:
    st.image('image/img2.jpeg',width=500)
    st.subheader("Earlier the air we breathe in use to be pure and fresh. But, due to increasing industrialization and concentration of poisonous gases in the environment the air is getting more and more toxic day by day. Also, these gases are the cause of many respiratory and other diseases. Moreover, the rapidly increasing human activities like the burning of fossil fuels, deforestation is the major cause of air pollution.")
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
        st.write("In the above bar plot of Type Wise Count, it can observe that the residential area has the highest count at 265963, followed by industrial at 148071, and sensitive at 15011. residential and industrial are also the major contributor towards air pollution in India.")
    if choice == cols[1]:
        st.subheader("Type Wise SO2 Distribution")
        st.bar_chart(type_df.so2, width=2, height=450,
                     use_container_width=True)
        st.write("In the above bar plot of Type Wise SO2 Distribution we can observe that other at second lowest count at 5393 has the highest amount of SO2 at 16.49, but the second major contributor remains to be industrial at 13.42, rural lowest counter 1304 is the third highest at 10.92 while the residential with the highest count is at 9.5.")
    if choice == cols[2]:
        st.subheader("Type Wise NO2 Distribution")
        st.bar_chart(type_df.no2, width=2, height=450,
                     use_container_width=True)
        st.write("In the above bar plot of Type Wise NO2 Distribution we can observe that rural has highest sound followed by industrial, others and residential at 31.78, 29.5, 27.6 and 24 respectively.")
    if choice == cols[3]:
        st.subheader("Type Wise RSPM Distribution")
        st.bar_chart(type_df.rspm, width=2, height=450,
                     use_container_width=True)
        st.write("In the above bar plot of Type Wise RSPM Distribution we can observe that industrial contributes the highest level of RSPM at 122 followed by rural at 103.6, residential at 102.4 and sensitive at 99.5.")

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
        st.write("In the above bar plot of State Wise SO2 Distribution we can observe that Uttarakhand has the highest level of SO2 at 24.43 followed by Jharkhand at 23.49, Sikkim at 19.8, Bihar at 19.40 and in Maharashtra at 17.4, the lowest level of SO2 can be observe in Nagaland at 2.1.")
    if choice == cols[1]:
        st.subheader("State Wise NO2 Distribution")
        st.bar_chart(state_df.no2, width=2, height=450,
                     use_container_width=True)
        st.write("In the above bar plot of State Wise NO2 Distribution we can observe that West Bengal has highest level of NO2 at 59.1 followed by Delhi at 53.5, Jharkhand at 43.4, Bihar 36.6 and Maharashtra at 32.1, the lowest level of NO2 can be observed in the state of Arunachal Pradesh at 5.5.")
    if choice == cols[2]:
        st.subheader("State Wise RSPM Distribution")
        st.bar_chart(state_df.rspm, width=2, height=450,
                     use_container_width=True)
        st.write("In the above bar plot of State Wise RSPM Distribution we can observe that Delhi has highest level of rspm at 196.7 followed by Uttar Pradesh at 177, Punjab at 173.5, Jharkhand at 168.51 and Haryana at 150, the lowest level of rspm is observed in the state of Sikkim at 32.")
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
        st.write("In the above bar plot of City Wise SO2 Distribution it can observed that among the 20 city with highest level of SO2 is in byrnihat(Meghalaya) at 45.47 followed by gajroula(Uttar Pradesh), Jamshedpur(Jharkhand) 38.18, nanded( Maharashtra) at 38.1 and dharuhera(Haryana) at 37.8, Railways level in Ghaziabad(Uttar Pradesh) at 24.1.")
    if choice == cols[1]:
        st.subheader("City Wise NO2 Distribution")
        f, ax = plt.subplots(figsize=(25, 12))
        ax = sns.barplot(x="location", y="no2",
                         data=no2_location_groupby2, ax=ax)
        st.write(f)
        st.write("In the above bar plot of City Wise NO2 Distribution it can observed that among the 20 city with highest level of NO2 is in Howrah( West Bengal) at 78 followed by badlapur( Maharashtra) at 64.5, Dombivli( Maharashtra) at 60.5, UlhasNagar( Maharashtra) at 59.8, Kolkata( West Bengal) at 59.4, the lowest level is in Jalgaon( Maharashtra) at 45.1.")
    if choice == cols[2]:
        st.subheader("City Wise RSPM Distribution")
        f, ax = plt.subplots(figsize=(25, 12))
        ax = sns.barplot(x="location", y="rspm",
                         data=rspm_location_groupby2, ax=ax)
        st.write(f)
        st.write("In the above bar plot of City Wise RSPM Distribution it can observed that among the 20 city with highest level of rspm is in Ghaziabad( Uttar Pradesh) at 250.5 followed by West singhbhum( Jharkhand) at 246.41, Bareilly( Uttar Pradesh) at 233.1, Allahabad( Uttar Pradesh) at 230.8, Ludhiana( Punjab) at 218.6, the lowest level is in Yamuna Nagar( Haryana) at 177.6.")

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
        st.write("In the above bar plot of Year Wise SO2 Distribution we can observe that the SO2 level highest in year 1995 at 26 followed by year 1994 at 22.5, year 1988 at 22.1, year 1993 at 22, year 1987 at 21.8, the lowest level of SO2 is observed in year 2003 at 6.6.")
    if choice == cols[1]:
        st.subheader("Year Wise NO2 Distribution")
        st.bar_chart(year_df.no2, width=2, height=450,
                     use_container_width=True)
        st.write("In the above bar plot of Year Wise NO2 Distribution we can observe that the highest level of NO2 is observed in year 1995 at 33.1 followed by year 1994 at 31.8, year 1992 at 30.8, year 1988 8 30.6, year 1987 at 30.5, lowest level of NO2 is observed in year 2003 at 21.5.")
    if choice == cols[2]:
        st.subheader("Year Wise RSPM Distribution")
        st.bar_chart(year_df.rspm, width=2, height=450,
                     use_container_width=True)
        st.write("In the above bar plot of Year Wise RSPM Distribution we can observe that the highest level of RSPM is in year 2004 at 121.15 followed by year 2011 at 115.80,year 2009 at 114.33,year 2008 at 112.87,year 2005 at 111.49, the lowest level of RSPM is present in the year 2003 at 88.70.")

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
        st.write("In the above Choropleth of SO2 Distribution we can observe that states like Uttarakhand, Jharkhand have an extreme amount of SO2 present, states like Bihar, Maharashtra, Sikkim have less extreme but still a substantial amount of SO2 present, States like Haryana, Punjab, Delhi, Uttar Pradesh, Gujarat, Karnataka, Tamil Nadu, West Bengal, have more than average amount of SO2 present while states like Himachal Pradesh, Orissa, Kerala, Rajasthan, Andhra Pradesh, Assam, Meghalaya, Arunachal Pradesh, Nagaland, Manipur, Mizoram have below average level of SO2 present.")

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
        st.write("In the above Choropleth of NO2 Distribution we can observe that states like Delhi, West Bengal have extreme amount of NO2 present, where as Jharkhand has less extreme but still a substantial amount of NO2 present, Bihar has average level of NO2 present, states like Uttar Pradesh, Uttarakhand, Punjab, Haryana, Rajasthan, Gujarat, Maharashtra, Chhattisgarh have above average level of NO2 present while states like Madhya Pradesh, Orissa, Andhra Pradesh, Karnataka, Kerala, Tamil Nadu, Himachal Pradesh, Arunachal Pradesh, Assam, Manipur have a below average level of NO2 present.")
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
        st.write("In the above Choropleth of RSPM Distribution we can observe that States like Uttar Pradesh, Delhi, Punjab have an extreme amount of RSPM present, states like Jammu and Kashmir, Uttarakhand, Haryana, Rajasthan, Jharkhand have less extreme but still a substantial amount of RSPM present, where as states like Himachal Pradesh, Madhya Pradesh, Chhattisgarh, Bihar, West Bengal, Assam have average level of RSPM present, while states like Karnataka Kerala, Tamil Nadu, Andhra Pradesh, Orissa have a below average level of RSPM present.")

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
        st.write("In the above heatmap of SO2 Between State & Year we can observe that Goa in year 1995 has the highest recorded value of SO2 present in any state in year between 1987 and 2015, followed by the same in year 1997 and in 1996.")
    if choice == cols[1]:
        st.subheader("Heatmap of NO2 Between State & Year")
        f, ax = plt.subplots(figsize=(25, 12))
        ax.set_title('{} by state and year'.format('no2'))
        sns.heatmap(no2_year_state, annot=True, cmap="YlGnBu", fmt='.3g', mask=no2_year_state.isnull(
        ), linewidths=2, ax=ax, cbar_kws={'label': 'Annual Average'})
        st.write(f)
        st.write("In the above heatmap of NO2 Between State & Year we can observe that Rajasthan in year 1987 has highest amount of NO2 in any of the states between the year 1987 and 2015 followed by West Bengal in year 1994 and year 1995.")
    if choice == cols[2]:
        st.subheader("Heatmap of RSPM Between State & Year")
        f, ax = plt.subplots(figsize=(15, 7))
        ax.set_title('{} by state and year'.format('rspm'))
        sns.heatmap(rspm_year_state, annot=True, cmap="YlGnBu", fmt='.3g', mask=rspm_year_state.isnull(
        ), linewidths=2, ax=ax, cbar_kws={'label': 'Annual Average'})
        st.write(f)
        st.write("In the above heatmap of RSPM Between State & Year we can observe that Haryana recorded level of RSPM in the year of 2009 followed by Delhi in the same year, and in the year of 2012 and Punjab in year 2003 and 2004.")
        
if menu == options[9]:
    st.title("Conclusion")
    st.write("Using the above observations, we can conclude that there has been a gradual increase in the level of SO2 in states like Bihar, Haryana, Karnataka, Rajasthan and West Bengal between the year 1987 and 2000 after which there has been a gradual decline and constant below average level in levels of SO2 concentration in the New Century from 2000. It is can also be observed that between year 1987 and 1995 there has been a gradual increase and the level of SO2 which then has gradual decline and are at below average level of concentration. Bihar, Maharashtra, and West Bengal have seen a gradual increase in the level of NO2 between the year 1987 and 2000 and then gradual declination following the new century below average level, while Delhi has only seen a gradual increase in the amount of NO2 to an extreme level, the same in the years between 1987 and 1995 which has seen gradual rise and then gradual fall to below average level following the new century. States like Punjab, Haryana, Chhattisgarh are following the same tendency in RSPM with a gradual rise and then gradual fall between the years 2003 and 2015, while states like Delhi Jharkhand have seen a gradual increase in the level of RSPM. states like Uttar Pradesh, Uttarakhand, West Bengal, Gujarat, Maharashtra maintained above average level of RSPM. the reason for decline in the level of various air pollutants in various states are due to the policies enforced by the government to protect environment. It has been a wonderful experience doing the Summer Internship and making the project based on the guidelines. It has provided me a very useful experience for my future as well as make me understand and learn various new concepts and techniques which were very helpful.")

