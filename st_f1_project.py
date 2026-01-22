import streamlit as st
import pandas as pd
import plotly as px

st.title("F1 2025 SEASON DRIVER ANALYSIS")
st.header("1. Race Pace vs Race Points ")
df=pd.read_csv("final_f1_data.csv")
df2=df.drop(columns={"HeadshotUrl"})
side_bar_title=st.sidebar.title("Filters")
# race_slider=st.sidebar.slider("Minimum Races Entered",16,24,20)
toggle_1=st.sidebar.toggle("Full Season Drivers Only")
toggle_2=st.sidebar.toggle("Keep All Drivers")
select_teams=st.sidebar.multiselect("Select Team",options=df["TeamName"].unique(),placeholder="Select Teams")
selected_driver=st.sidebar.selectbox("Highlight Driver",df["Driver"].unique(),index=None,placeholder="Select a Driver")
if toggle_1 :
    st.write("Full Season Drivers Selected")
    filtered_df=df2[df2["RacesEntered"] >= 22]

else:
    filtered_df=df2[df2["RacesEntered"]>=16]
if toggle_2:
    st.write("All Drivers are Selected")
    filtered_df=df2
else:
    pass

if select_teams:
    filtered_df=filtered_df[filtered_df["TeamName"].isin(select_teams)]
else:
    pass


if selected_driver:
    filtered_df=filtered_df[filtered_df["Driver"]==selected_driver]
else:
    pass

col_1_1,col_1_2,col_1_3,col_1_4,col_1_5=st.columns(5)
with col_1_1:
    st.write("#Total Drivers")
    number_driver=filtered_df["Driver"].nunique()
    st.write(f"{number_driver} number of drivers")

with col_1_2:
    min_lap_time=df["MedianRacePace"].min()
    fastest_pace=df[df["MedianRacePace"]==min_lap_time]
    fastest_driver=fastest_pace["Driver"].iloc[0]
    image=fastest_pace["HeadshotUrl"].iloc[0]
    # st.metric("Fastest Driver",fastest_driver,f"{round(min_lap_time,2)}seconds")
    st.write("Fastest Pace")
    st.image(image,width=93)
    st.write(f" {fastest_driver} - {round(min_lap_time,2)} Sec ")
with col_1_3:
    max_points_per_race=df["PointsPerRace"].max()
    max_pts=df[df["PointsPerRace"]==max_points_per_race]
    max_pts_driver=max_pts["Driver"].iloc[0]
    image_max_pts=max_pts["HeadshotUrl"].iloc[0]
    st.write("Best Points/Race")
    st.image(image_max_pts)
    st.write(f" {max_pts_driver} - {round(max_points_per_race,2)} ")
with col_1_4:
    corr=df2["MedianRacePace"].corr(df2["PointsPerRace"])
    st.write("Correlation")
    st.write(f" between MedianRacePace vs PointsPerRace is {round(corr,2)}")
    # col_1_1=filtered_df[filtered_df["Driver"]]
st.dataframe(filtered_df)

