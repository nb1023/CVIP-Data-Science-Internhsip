import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot, iplot
import folium
from streamlit_folium import folium_static

st.title('COVID-19 :blue[_Analysis_]')
st.markdown("### **COVID Cases in :orange[_India_] Dataset**")

def load_data():
    df = pd.read_csv("Covid cases in India.csv")
    df['Total Cases'] = df['Total Confirmed cases (Indian National)'] + df['Total Confirmed cases ( Foreign National )']
    return df

df = load_data()
st.write(df)

def get_info(df):
    total_cases = df['Total Cases'].sum()
    st.markdown("#### :orange[Total Cases till 27 march 2020 in India] " + "  " +str(total_cases))
    df['Active Cases'] = df['Total Cases']-(df['Death']+df['Cured'])
    total_active_cases = df.groupby('Name of State / UT')['Active Cases'].sum().sort_values(ascending = False).to_frame()
    st.markdown("### Total Active cases")
    st.write(total_active_cases.style.background_gradient(cmap='Reds'))

def draw_graphs(df):
    st.markdown("### Total Cases in India")
    fig = px.bar(df, x='Name of State / UT', y='Total Cases', color='Total Cases')
    fig.update_yaxes(range=[0, df['Total Cases'].max()])
    st.plotly_chart(fig)

def load_data1():
    df2 = pd.read_csv("Indian Coordinates.csv")
    df1 = pd.merge(df2,df,on='Name of State / UT')
    return df1

df1 = load_data1()
st.markdown("### **After merging with :orange[_Indian_] Coordinates Dataset**")
st.write(df1)

def draw_map(df1):
    st.markdown("#### **Map of India with CircleMarkers representing the total COVID-19 cases for each State**")
    map = folium.Map(location = [20,70], zoom_start = 4, tiles = 'Stamenterrain')
    for lat,long,value,name in zip(df1['Latitude'], df1['Longitude'],df1['Total Cases'],df1['Name of State / UT']):
        folium.CircleMarker([lat,long],radius=value*0.8, popup=('<strong>State</strong>: '+str(name).capitalize()+'<br>''<strong>Total Cases</strong>: '+str(value)+'<br>'),color='red', fill_color='red',fill_opacity=0.3).add_to(map)
    folium_static(map)

def load_data2():
    df_India = pd.read_excel(r"M:\Internshala assignments\CodersCave\Phase 1 Normal task\per_day_cases.xlsx", parse_dates=True,sheet_name = "India")
    df_Italy = pd.read_excel(r"M:\Internshala assignments\CodersCave\Phase 1 Normal task\per_day_cases.xlsx", parse_dates=True,sheet_name = "Italy")
    df_Wuhan = pd.read_excel(r"M:\Internshala assignments\CodersCave\Phase 1 Normal task\per_day_cases.xlsx", parse_dates=True,sheet_name = "Wuhan")
    df_Korea = pd.read_excel(r"M:\Internshala assignments\CodersCave\Phase 1 Normal task\per_day_cases.xlsx", parse_dates=True,sheet_name = "Korea")

    return df_India,df_Italy,df_Wuhan ,df_Korea

df_India, df_Italy, df_Wuhan, df_Korea = load_data2()

st.markdown("### **Cases per day in India, Italy, Wuhan and Korea Dataset**")
st.subheader("India")
st.write(df_India)

st.subheader("Italy")
st.write(df_Italy)

st.subheader("Wuhan")
st.write(df_Wuhan)

st.subheader("Korea")
st.write(df_Korea)

def graph_India(df_India):
    st.markdown("### :blue[_Confirmed_] Cases in India")
    fig = px.bar(df_India, x = "Date", y="Total Cases", color='Total Cases')
    st.plotly_chart(fig)

def graph_Italy(df_Italy):
    st.markdown("### :blue[_Confirmed_] Cases in Italy")
    fig = px.bar(df_Italy, x = "Date", y="Total Cases", color='Total Cases')
    st.plotly_chart(fig)

def graph_Wuhan(df_Wuhan):
    st.markdown("### :blue[_Confirmed_] Cases in Wuhan")
    fig = px.bar(df_Wuhan, x = "Date", y="Total Cases", color='Total Cases')
    st.plotly_chart(fig)

def graph_Korea(df_Korea):
    st.markdown("### :blue[_Confirmed_] Cases in Korea")
    fig = px.bar(df_Korea, x = "Date", y="Total Cases", color='Total Cases')
    st.plotly_chart(fig)

def load_data3():
    df2 = pd.read_csv("covid_19_data.csv", parse_dates = ['Last Update'])
    df2.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country'},inplace=True)
    return df2

def world(df2):
    world_data_on_date = df2.groupby('Date')[['Confirmed', 'Deaths', 'Recovered']].sum()
    st.markdown("### Date Wise Cases")
    st.write(world_data_on_date)
    st.markdown("### Scatter Plot of :blue[_Confirmed_], :red[_Deaths_] and :green[_Recovered_] cases worldwide")
    confirmed = df2.groupby('Date').sum()['Confirmed'].reset_index()
    death = df2.groupby('Date').sum()['Deaths'].reset_index()
    rec = df2.groupby('Date').sum()['Recovered'].reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=confirmed['Date'], y=confirmed['Confirmed'], mode = 'lines+markers', name = 'Confirmed', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=death['Date'], y=death['Deaths'], mode = 'lines+markers', name = 'Deaths', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=rec['Date'], y=rec['Recovered'], mode = 'lines+markers', name = 'Recovered', line=dict(color='green', width=2)))
    st.plotly_chart(fig)

def load_data4():
    df4 = pd.read_csv("time_series_covid_19_confirmed.csv")
    df4.rename(columns={'Country/Region': 'Country'}, inplace=True)

    df2 = pd.read_csv("covid_19_data.csv", parse_dates=['Last Update'])
    df2.rename(columns={'ObservationDate': 'Date', 'Country/Region': 'Country'}, inplace=True)

    df3 = pd.merge(df2, df4, on=['Country', 'Province/State'])
    return df3

def plot(df3):
    st.markdown("### Worldwide :red[_Corona Virus_] Cases")
    fig = px.density_mapbox(df3, lat="Lat", lon="Long", hover_name="Province/State", hover_data=["Confirmed", "Deaths", "Recovered"], animation_frame="Date", color_continuous_scale="Portland", radius=7, zoom=0, height=700)
    fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
    fig.update_layout(margin={"r": 0, "t": 0, "b": 0})
    st.plotly_chart(fig)

def main():
    get_info(df)
    draw_graphs(df)
    draw_map(df1)
    graph_India(df_India)
    graph_Italy(df_Italy)
    graph_Wuhan(df_Wuhan)
    graph_Korea(df_Korea)
    df2 = load_data3()
    st.markdown("### **World COVID-19 Dataset**")
    st.write(df2)
    world(df2)
    df3 = load_data4()
    st.markdown("### **Time-Series Confirmed Dataset**")
    st.write(df3)
    plot(df3)
main()