import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image


st.set_page_config(
    layout="wide",
    page_title="F1 2025 Season Analysis",
    page_icon="🏎️"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Titillium Web', sans-serif; }
    .main { background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%); }
    h1 { background: linear-gradient(90deg, #E10600 0%, #FF1801 50%, #E10600 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; letter-spacing: 3px; text-transform: uppercase; text-align: center; padding: 20px 0; }
    h3 { color: #FFFFFF; font-weight: 600; text-align: center; letter-spacing: 1px; margin-bottom: 30px; }
    [data-testid="column"] { background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%); padding: 25px; border-radius: 15px; border: 2px solid #E10600; border-left: 8px solid #E10600; box-shadow: 0 8px 16px rgba(225, 6, 0, 0.2); transition: all 0.3s ease; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    [data-testid="column"]:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(225, 6, 0, 0.4); border-left-width: 12px; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%); border-right: 3px solid #E10600; }
    [data-testid="stSidebar"] h2 { color: #E10600; text-transform: uppercase; letter-spacing: 2px; font-weight: 900; }
    hr { border: none; height: 3px; background: linear-gradient(90deg, transparent 0%, #E10600 20%, #E10600 80%, transparent 100%); margin: 30px 0; }
    .insight-box { background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%); border-left: 6px solid #E10600; padding: 25px; border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(225, 6, 0, 0.2); }
    .insight-box h4 { color: #E10600; font-weight: 700; margin-bottom: 15px; }
    .insight-box p { color: #CCCCCC; line-height: 2.0; font-size: 15px; }
    .insight-box strong { color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

try:
    banner_img = Image.open("banner.png")
    st.image(banner_img, use_container_width=True)
except FileNotFoundError:
    st.warning("Banner image not found.")

st.markdown(
    "<div style='text-align: center; padding: 20px 0;'><h1>🏎️ FORMULA 1 2025 SEASON</h1><h3 style='color: #888;'>DRIVER PERFORMANCE ANALYSIS DASHBOARD</h3></div>",
    unsafe_allow_html=True)

df = pd.read_csv("final_f1_data.csv")
if "DriverNumber" in df.columns:
    df = df.set_index("DriverNumber")
df_analysis = df.copy()

COLOR_MAPPING = {
    "McLaren": "#FF8000", "Ferrari": "#E8002D", "Mercedes": "#00D2BE", "Kick Sauber": "#52E252",
    "Racing Bulls": "#6692FF", "Alpine": "#0090FF", "Aston Martin": "#006F62", "Red Bull Racing": "#0600EF",
    "Williams": "#005AFF", "Haas F1 Team": "#FFFFFF"
}

st.sidebar.markdown("## 🎛️ CONTROL PANEL\n---")
page = st.sidebar.selectbox("📊 Select Analysis", [
    "Insight 1: Race Pace vs Points Efficiency", "Insight 2: Race Consistency vs Reliability",
    "Insight 3: Team Dominance Hierarchy", "Insight 4: DNF Risk Profile",
    "Insight 5: Saturday vs Sunday Pace", "Insight 6: Sprint vs Race Masters"
])
st.sidebar.markdown("---")
show_all_drivers = st.sidebar.toggle("🏁 Show All Drivers", value=False)
full_season_only = st.sidebar.toggle("📅 Full Season (22+ Races)", value=False)
st.sidebar.markdown("---")
selected_teams = st.sidebar.multiselect("🏁 Filter by Team", options=sorted(df["TeamName"].unique()))
selected_drivers = st.sidebar.multiselect("👤 Filter by Driver", options=sorted(df["Driver"].unique()))
st.sidebar.markdown("---")
st.sidebar.info("💡 **Pro Tip:** Hover over data points for detailed statistics")

filtered_df = df_analysis.copy()
if not show_all_drivers:
    filtered_df = filtered_df[filtered_df["RacesEntered"] >= (22 if full_season_only else 16)]
    st.sidebar.success("✅ " + ("Full Season Drivers" if full_season_only else "Regular Drivers (16+)"))
else:
    st.sidebar.success("✅ All Drivers Active")
if selected_teams:
    filtered_df = filtered_df[filtered_df["TeamName"].isin(selected_teams)]
if selected_drivers:
    filtered_df = filtered_df[filtered_df["Driver"].isin(selected_drivers)]

filtered_df["efficiency"] = np.where(filtered_df["MedianRacePace"] > 0,
                                     filtered_df["PointsPerRace"] / filtered_df["MedianRacePace"], 0.0)


def kpi_card_text(value, label, caption, value_color="#E10600"):
    return f"""<div style="text-align: center; padding-top: 10px;"><h1 style="color: {value_color}; margin: 0; font-size: 3.5em;">{value}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{label}</p><p style="color: #888888; font-size: 14px; margin: 0;">{caption}</p></div>"""


def kpi_image_placeholder():
    st.markdown(
        '<div style="height:150px;background:linear-gradient(135deg,#1a1a1a,#2a2a2a);border:2px solid #E10600;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#E10600;font-size:48px;width:150px;margin:0 auto;">🏎️</div>',
        unsafe_allow_html=True)


# INSIGHT 1
if page == "Insight 1: Race Pace vs Points Efficiency":
    st.markdown("---")
    if filtered_df.empty:
        st.error("⚠️ **NO DATA AVAILABLE** - Adjust filters")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_image_placeholder()
            st.markdown(kpi_card_text(filtered_df['Driver'].nunique(), "Total Drivers", "in current filter"),
                        unsafe_allow_html=True)
        with col2:
            fastest = filtered_df.nsmallest(1, "MedianRacePace").iloc[0]
            try:
                st.image(Image.open(fastest["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{fastest['MedianRacePace']:.2f}s</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{fastest['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">quickest avg lap</p></div>""",
                unsafe_allow_html=True)
        with col3:
            best_pts = filtered_df.nlargest(1, "PointsPerRace").iloc[0]
            try:
                st.image(Image.open(best_pts["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{best_pts['PointsPerRace']:.2f}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{best_pts['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">highest points/race</p></div>""",
                unsafe_allow_html=True)
        with col4:
            kpi_image_placeholder()
            corr = filtered_df["MedianRacePace"].corr(filtered_df["PointsPerRace"])
            corr_color = "#00D2BE" if abs(corr) > 0.7 else "#FFD700" if abs(corr) > 0.4 else "#FF1801"
            strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.4 else "Weak"
            st.markdown(kpi_card_text(f"{corr:.2f}", "Pace-Points Link", f"{strength} relationship", corr_color),
                        unsafe_allow_html=True)

        st.markdown("---")
        filtered_df['PaceRank'] = filtered_df['MedianRacePace'].rank(ascending=True, method='min').astype(int)
        filtered_df['PointsRank'] = filtered_df['PointsPerRace'].rank(ascending=False, method='min').astype(int)
        filtered_df['DNF_%'] = (filtered_df['DNF_Rate'] * 100).round(1)

        fig = px.scatter(filtered_df, x="MedianRacePace", y="PointsPerRace", color="TeamName",
                         color_discrete_map=COLOR_MAPPING, size="RacesEntered", size_max=20, hover_name="Driver",
                         hover_data={'TeamName': True, 'RacesEntered': True, 'PaceRank': True, 'PointsRank': True,
                                     'DNF_%': True, 'efficiency': ':.4f'})
        fig.update_traces(marker=dict(line=dict(width=2, color='white'), opacity=0.9))
        fig.update_xaxes(autorange="reversed", showgrid=True, gridcolor='rgba(225,6,0,0.1)',
                         title_font=dict(size=14, color='white'), tickfont=dict(color='white'))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(225,6,0,0.1)', title_font=dict(size=14, color='white'),
                         tickfont=dict(color='white'))
        fig.add_vline(x=filtered_df["MedianRacePace"].mean(), line_dash="dash", line_color="#E10600", opacity=0.7,
                      line_width=2, annotation_text="AVG PACE", annotation_position="top",
                      annotation_font_color="white")
        fig.add_hline(y=filtered_df["PointsPerRace"].mean(), line_dash="dash", line_color="#E10600", opacity=0.7,
                      line_width=2, annotation_text="AVG POINTS", annotation_position="right",
                      annotation_font_color="white")
        fig.update_layout(title={'text': "<b>RACE PACE vs POINTS PERFORMANCE</b>", 'x': 0.5, 'xanchor': 'center',
                                 'font': {'size': 22, 'color': '#E10600'}}, height=600,
                          legend=dict(bgcolor="rgba(10,10,10,0.9)", bordercolor="#E10600", borderwidth=2,
                                      font=dict(color='white', size=11)),
                          plot_bgcolor='rgba(26,26,26,0.8)', paper_bgcolor='rgba(10,10,10,0)', font=dict(color='white'),
                          hoverlabel=dict(bgcolor="rgba(26,26,26,0.95)", font_size=13, font_color="white",
                                          bordercolor="white"))

        col_chart, col_rankings = st.columns([3, 1])
        with col_chart:
            st.plotly_chart(fig, use_container_width=True)
        with col_rankings:
            st.markdown("### 🏆 TOP 5 EFFICIENCY")
            top5 = filtered_df.nlargest(5, 'efficiency')[['Driver', 'efficiency', 'TeamName']].copy()
            top5['efficiency'] = top5['efficiency'].round(4)
            top5.columns = ['Driver', 'Score', 'Team']
            st.dataframe(top5, hide_index=True, use_container_width=True, height=220)
            st.markdown("---")
            st.markdown("### 📉 BOTTOM 5 EFFICIENCY")
            bottom5 = filtered_df.nsmallest(5, 'efficiency')[['Driver', 'efficiency', 'TeamName']].copy()
            bottom5['efficiency'] = bottom5['efficiency'].round(4)
            bottom5.columns = ['Driver', 'Score', 'Team']
            st.dataframe(bottom5, hide_index=True, use_container_width=True, height=220)

        st.markdown("---")
        top_driver = filtered_df.nlargest(1, 'efficiency').iloc[0]
        second_driver = filtered_df.nlargest(2, 'efficiency').iloc[1]
        worst_driver = filtered_df.nsmallest(1, 'efficiency').iloc[0]
        mclaren_top5 = len(
            filtered_df.nlargest(5, 'efficiency')[filtered_df.nlargest(5, 'efficiency')['TeamName'] == 'McLaren'])
        eff_ratio = top_driver['efficiency'] / filtered_df.nsmallest(5, 'efficiency')['efficiency'].mean()

        st.markdown(f"""<div class='insight-box'><h4>🏁 Raw Speed Doesn't Win Championships—Smart Racing Does</h4>
<p><strong>{top_driver['Driver']}</strong> leads with an efficiency of <strong>{top_driver['efficiency']:.4f}</strong>, which is <strong>{eff_ratio:.1f}x better</strong> than the bottom 5. This shows that converting pace into points is what wins championships, not just being fast.</p>
<p>Notice that <strong>{mclaren_top5}/5 of the top efficient drivers</strong> are from McLaren. Having two elite drivers scoring consistently gives them a massive advantage in the constructors' standings.</p>
<p>The correlation of <strong>{corr:.2f}</strong> tells us that while faster lap times help, they don't guarantee points. Drivers who finish cleanly and avoid crashes score more than those who are fast but make mistakes.</p>
<p><strong>Championship prediction:</strong> Based on current efficiency, <strong>{top_driver['Driver']}</strong> or <strong>{second_driver['Driver']}</strong> are strong favorites if they maintain reliability.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown(f"""<div class='insight-box'><h4>🎯 McLaren's Winning Formula: Two Strong Drivers Beat One Superstar</h4>
<p><strong>{top_driver['Driver']}</strong> (efficiency: <strong>{top_driver['efficiency']:.4f}</strong>) and <strong>{second_driver['Driver']}</strong> (efficiency: <strong>{second_driver['efficiency']:.4f}</strong>) form a deadly driver pairing.</p>
<p>While Red Bull relies on Max Verstappen alone, McLaren has <strong>two elite drivers</strong> who can fight for podiums every race. This means they collect points from both cars consistently, giving them strategic flexibility.</p>
<p><strong>Key takeaway:</strong> In modern F1, team depth beats individual genius. Two drivers scoring 15-20 points each is more valuable than one scoring 25 and the other scoring 2.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown(f"""<div class='insight-box'><h4>⚡ The Pace Paradox: Fastest Lap Doesn't Mean Most Points</h4>
<p><strong>{fastest['Driver']}</strong> has the fastest race pace at <strong>{fastest['MedianRacePace']:.2f}s</strong>, but <strong>{best_pts['Driver']}</strong> scores the most points per race with <strong>{best_pts['PointsPerRace']:.2f} PPR</strong>.</p>
<p>This proves a critical truth: <strong>raw speed alone doesn't win championships</strong>. Consistency, racecraft, tire management, and avoiding incidents matter just as much as pace. You can set the fastest lap but if you crash out, you score zero.</p>
<p><strong>Championship reality:</strong> Races are won on Sundays with smart execution, not Saturdays with qualifying speed. Finishing in the points beats setting purple sectors from the gravel trap.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown(f"""<div class='insight-box'><h4>⚠️ Bottom 5: When Unreliability Destroys Championship Dreams</h4>
<p><strong>{worst_driver['Driver']}</strong> has the lowest efficiency at <strong>{worst_driver['efficiency']:.4f}</strong> with a DNF rate of <strong>{worst_driver['DNF_%']:.1f}%</strong>. Every retirement costs 4-8 championship points.</p>
<p>The bottom drivers struggle with inconsistent performance—sometimes fast, sometimes crashing, often dealing with mechanical failures. This creates a "point drought" where even when they have pace, they can't convert it.</p>
<p><strong>Hard truth:</strong> You can't score points from the garage. Reliability—both mechanical and error-free driving—is the foundation of success. Speed means nothing if you don't finish races.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown("---\n### 📋 COMPLETE DRIVER STATISTICS")
        st.dataframe(filtered_df.drop(columns=['HeadshotUrl'], errors='ignore').round(3).sort_values('efficiency',
                                                                                                     ascending=False),
                     use_container_width=True, height=400)

# INSIGHT 2
elif page == "Insight 2: Race Consistency vs Reliability":
    st.markdown("---")
    if filtered_df.empty:
        st.error("⚠️ **NO DATA AVAILABLE** - Adjust filters")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_image_placeholder()
            st.markdown(kpi_card_text(filtered_df["Driver"].nunique(), "Total Drivers", "in current filter"),
                        unsafe_allow_html=True)
        with col2:
            best_cons = filtered_df.nsmallest(1, "MedianRaceIQR").iloc[0]
            try:
                st.image(Image.open(best_cons["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{best_cons['MedianRaceIQR']:.2f}s</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{best_cons['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">lowest lap variation</p></div>""",
                unsafe_allow_html=True)
        with col3:
            best_rel = filtered_df.nlargest(1, "FinishRate").iloc[0]
            try:
                st.image(Image.open(best_rel["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{best_rel['FinishRate']:.0%}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{best_rel['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">best finish rate</p></div>""",
                unsafe_allow_html=True)
        with col4:
            kpi_image_placeholder()
            avg_iqr = filtered_df["MedianRaceIQR"].mean()
            st.markdown(kpi_card_text(f"{avg_iqr:.2f}s", "Avg Lap Variance", "grid baseline IQR"),
                        unsafe_allow_html=True)

        st.markdown("---")


        filtered_df['FinishRate_%'] = (filtered_df['FinishRate'] * 100).round(1)
        filtered_df['DNF_Rate_%'] = (filtered_df['DNF_Rate'] * 100).round(1)

        fig2 = px.scatter(filtered_df, x="MedianRaceIQR", y="FinishRate", color="TeamName",
                          color_discrete_map=COLOR_MAPPING, size="TotalPoints", hover_name="Driver")
        fig2.update_traces(marker=dict(line=dict(width=1, color="Black")))
        fig2.update_xaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig2.update_yaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig2.update_layout(
            title={"text": "<b>CONSISTENCY vs RELIABILITY</b>", "x": 0.5, "font": {"size": 22, "color": "#E10600"}},
            height=600, legend=dict(bgcolor="rgba(10,10,10,0.9)", bordercolor="#E10600", borderwidth=2,
                                    font=dict(color="white", size=11)),
            plot_bgcolor="rgba(26,26,26,0.8)", paper_bgcolor="rgba(10,10,10,0)", font=dict(color="white"),
            hoverlabel=dict(bgcolor="rgba(26,26,26,0.95)", font_size=13, font_color="white", bordercolor="white"))

        col_chart, col_rankings = st.columns([3, 1])
        with col_chart:
            st.plotly_chart(fig2, use_container_width=True)
        with col_rankings:
            st.markdown("### 🏹 Top 5 Consistent")
            top5_consistent = filtered_df.nsmallest(5, 'MedianRaceIQR')[
                ['Driver', 'MedianRaceIQR', 'FinishRate_%', 'PointsPerRace']].copy()
            top5_consistent.columns = ['Driver', 'Lap IQR (s)', 'Finish %', 'Pts/Race']
            top5_consistent['Lap IQR (s)'] = top5_consistent['Lap IQR (s)'].round(2)
            top5_consistent['Pts/Race'] = top5_consistent['Pts/Race'].round(2)
            st.dataframe(top5_consistent, hide_index=True, use_container_width=True, height=220)

            st.markdown("---")

            st.markdown("### 🛡️ Top 5 Reliable")
            top5_reliable = filtered_df.nlargest(5, 'FinishRate')[
                ['Driver', 'FinishRate_%', 'DNF_Rate_%', 'TotalPoints']].copy()
            top5_reliable.columns = ['Driver', 'Finish %', 'DNF %', 'Total Pts']
            top5_reliable['Total Pts'] = top5_reliable['Total Pts'].round(0).astype(int)
            st.dataframe(top5_reliable, hide_index=True, use_container_width=True, height=220)

        st.markdown("---")
        st.markdown(f"""<div class='insight-box'><h4>📏 Low Lap Variation = Championship Material</h4>
<p><strong>{best_cons['Driver']}</strong> has the most consistent lap times with an IQR of <strong>{best_cons['MedianRaceIQR']:.2f}s</strong>, meaning their lap times vary very little throughout a race. This shows incredible mental toughness and car control under pressure.</p>
<p><strong>{best_rel['Driver']}</strong> has the best finish rate at <strong>{best_rel['FinishRate']:.0%}</strong>, meaning they almost always finish races. Combining low variance (IQR &lt; 1.5s) with high finish rate (&gt; 90%) is the championship profile.</p>
<p><strong>Key insight:</strong> Drivers who can deliver consistent lap times lap after lap, while also finishing races reliably, are the ones who win titles. Variance kills championships.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown(f"""<div class='insight-box'><h4>🎯 What Separates Champions from Mid-Pack Drivers</h4>
<p>Machine-like drivers have IQR under 1.5s and finish rates above 90%. They're predictable, reliable, and always there to collect points.</p>
<p>Volatile drivers show IQR over 1.8s and DNF rates above 20%. Some laps they're fast, other laps they're slow or in the wall. This inconsistency means they can't be relied upon for championship points.</p>
<p><strong>Championship formula:</strong> IQR &lt; 1.5s + Finish Rate &gt; 90% = guaranteed podium contender.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown("---\n### 📋 COMPLETE DRIVER STATISTICS")
        st.dataframe(filtered_df.drop(columns=["HeadshotUrl"], errors="ignore").round(3).sort_values("MedianRaceIQR",
                                                                                                     ascending=True),
                     use_container_width=True, height=400)

# INSIGHT 3
elif page == "Insight 3: Team Dominance Hierarchy":
    st.markdown("---")
    if filtered_df.empty:
        st.error("⚠️ **NO DATA AVAILABLE** - Adjust filters")
    else:
        team_perf = filtered_df.groupby("TeamName").agg(
            TotalPoints=("TotalPoints", "sum"),
            PointsPerRace=("PointsPerRace", "mean"),
            efficiency=("efficiency", "mean"),
            Drivers=("Driver", "count")
        ).reset_index().sort_values("TotalPoints", ascending=False)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_image_placeholder()
            st.markdown(kpi_card_text(filtered_df["Driver"].nunique(), "Total Drivers", "in current filter"),
                        unsafe_allow_html=True)
        with col2:
            leader = team_perf.iloc[0]
            lead_driver = filtered_df[filtered_df["TeamName"] == leader["TeamName"]].nlargest(1, "TotalPoints").iloc[0]
            try:
                st.image(Image.open(lead_driver["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{leader['TotalPoints']:.0f}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{leader['TeamName']}</p><p style="color: #888888; font-size: 14px; margin: 0;">leading team points</p></div>""",
                unsafe_allow_html=True)
        with col3:
            best_team = leader["TeamName"]
            team_drivers = filtered_df[filtered_df["TeamName"] == best_team].nlargest(2, "TotalPoints")
            if len(team_drivers) >= 2:
                second_best_driver = team_drivers.iloc[1]
                try:
                    st.image(Image.open(second_best_driver["HeadshotUrl"]), width=150)
                except:
                    kpi_image_placeholder()
                st.markdown(
                    f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{second_best_driver['TotalPoints']:.0f}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{second_best_driver['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">teammate contribution</p></div>""",
                    unsafe_allow_html=True)
            else:
                kpi_image_placeholder()
                st.markdown(kpi_card_text("—", "Teammate", "single driver team"), unsafe_allow_html=True)
        with col4:
            kpi_image_placeholder()
            spread = team_perf["TotalPoints"].std()
            st.markdown(kpi_card_text(f"{spread:.0f} pts", "Team Spread", "points disparity measure"),
                        unsafe_allow_html=True)

        st.markdown("---")

        fig3 = px.bar(team_perf, x="TeamName", y="TotalPoints", color="TeamName", color_discrete_map=COLOR_MAPPING)
        fig3.update_traces(hovertemplate="<b>%{x}</b><br>Points: %{y}<br><extra></extra>")
        fig3.update_xaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig3.update_yaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig3.update_layout(
            title={"text": "<b>TEAM DOMINANCE HIERARCHY</b>", "x": 0.5, "font": {"size": 22, "color": "#E10600"}},
            height=600, legend=dict(bgcolor="rgba(10,10,10,0.9)", bordercolor="#E10600", borderwidth=2,
                                    font=dict(color="white", size=11)),
            plot_bgcolor="rgba(26,26,26,0.8)", paper_bgcolor="rgba(10,10,10,0)", font=dict(color="white"),
            hoverlabel=dict(bgcolor="rgba(26,26,26,0.95)", font_size=13, font_color="white", bordercolor="white"))

        col_chart, col_rankings = st.columns([3, 1])
        with col_chart:
            st.plotly_chart(fig3, use_container_width=True)
        with col_rankings:
            st.markdown("### 🏆 Top 10 Teams")
            top10_teams = team_perf.head(10)[
                ['TeamName', 'TotalPoints', 'PointsPerRace', 'efficiency', 'Drivers']].copy()
            top10_teams['TotalPoints'] = top10_teams['TotalPoints'].round(0).astype(int)
            top10_teams['PointsPerRace'] = top10_teams['PointsPerRace'].round(2)
            top10_teams['efficiency'] = top10_teams['efficiency'].round(4)
            top10_teams.columns = ['Team', 'Total Pts', 'Avg PPR', 'Avg Eff', 'Drivers']
            st.dataframe(top10_teams, hide_index=True, use_container_width=True, height=220)

            st.markdown("---")

            st.markdown("### 📉 Bottom 10 Teams")
            bottom10_teams = team_perf.tail(10).sort_values("TotalPoints", ascending=True)[
                ['TeamName', 'TotalPoints', 'PointsPerRace', 'efficiency', 'Drivers']].copy()
            bottom10_teams['TotalPoints'] = bottom10_teams['TotalPoints'].round(0).astype(int)
            bottom10_teams['PointsPerRace'] = bottom10_teams['PointsPerRace'].round(2)
            bottom10_teams['efficiency'] = bottom10_teams['efficiency'].round(4)
            bottom10_teams.columns = ['Team', 'Total Pts', 'Avg PPR', 'Avg Eff', 'Drivers']
            st.dataframe(bottom10_teams, hide_index=True, use_container_width=True, height=220)

        st.markdown("---")
        st.markdown(f"""<div class='insight-box'><h4>🏆 Two Elite Drivers Beat One Superstar</h4>
<p><strong>{leader['TeamName']}</strong> leads the constructors' championship with <strong>{leader['TotalPoints']:.0f} points</strong>. Their success comes from having two drivers who can both score big points consistently.</p>
<p>While some teams rely on one superstar driver carrying the load, the top teams benefit from dual-driver strength. This means they can use team strategy better, protect positions, and always have a backup if one driver has a bad day.</p>
<p><strong>Strategic insight:</strong> In modern F1, having two competitive drivers is worth more than one world-class driver and one average teammate.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown(f"""<div class='insight-box'><h4>📊 Mid-Field Battle: Car Performance Sets the Ceiling</h4>
<p>The team points spread of <strong>{spread:.0f} points</strong> shows the massive gap between top teams and mid-field/backmarker teams. This disparity is mostly due to car performance.</p>
<p>Even the best driver in the world can't score 300 points in a mid-field car. The performance ceiling is set by the machinery, and driver skill can only maximize within that limit.</p>
<p><strong>Reality check:</strong> The top 3 teams have the best cars AND the best drivers. Mid-field teams need major upgrades to compete for podiums consistently.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown("---\n### 📋 TEAM STATISTICS")
        st.dataframe(team_perf.round(3), use_container_width=True, height=400)

# INSIGHT 4
elif page == "Insight 4: DNF Risk Profile":
    st.markdown("---")
    if filtered_df.empty:
        st.error("⚠️ **NO DATA AVAILABLE** - Adjust filters")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_image_placeholder()
            st.markdown(kpi_card_text(filtered_df["Driver"].nunique(), "Total Drivers", "in current filter"),
                        unsafe_allow_html=True)
        with col2:
            worst_dnf = filtered_df.nlargest(1, "DNF_Rate").iloc[0]
            try:
                st.image(Image.open(worst_dnf["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{worst_dnf['DNF_Rate']:.1%}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{worst_dnf['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">highest DNF rate</p></div>""",
                unsafe_allow_html=True)
        with col3:
            perfect = filtered_df[filtered_df["DNF_Rate"] == 0]
            if not perfect.empty:
                best_rel = perfect.iloc[0]
                val, cap = "0%", "perfect reliability"
            else:
                best_rel = filtered_df.nsmallest(1, "DNF_Rate").iloc[0]
                val, cap = f"{best_rel['DNF_Rate']:.1%}", "best reliability"
            try:
                st.image(Image.open(best_rel["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{val}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{best_rel['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">{cap}</p></div>""",
                unsafe_allow_html=True)
        with col4:
            kpi_image_placeholder()
            dnf_cost = (filtered_df["TotalPoints"].max() / 24) * 0.15
            st.markdown(kpi_card_text(f"-{dnf_cost:.0f}", "Avg DNF Cost", "lost points per retirement", "#FF1801"),
                        unsafe_allow_html=True)

        st.markdown("---")


        filtered_df['DNF_Rate_%'] = (filtered_df['DNF_Rate'] * 100).round(1)
        filtered_df['FinishRate_%'] = (filtered_df['FinishRate'] * 100).round(1)

        fig4 = px.scatter(filtered_df, x="DNF_Rate", y="TotalPoints", color="TeamName",
                          color_discrete_map=COLOR_MAPPING, size="RacesEntered", hover_name="Driver")
        fig4.update_traces(marker=dict(line=dict(width=1, color="Black")))
        z = np.polyfit(filtered_df["DNF_Rate"], filtered_df["TotalPoints"], 1)
        p = np.poly1d(z)
        fig4.add_trace(go.Scatter(x=filtered_df["DNF_Rate"], y=p(filtered_df["DNF_Rate"]), mode="lines",
                                  name="Trend", line=dict(dash="dash", color="rgba(255,255,255,0.5)")))
        fig4.update_xaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig4.update_yaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig4.update_layout(title={"text": "<b>DNF RISK vs CHAMPIONSHIP POINTS</b>", "x": 0.5,
                                  "font": {"size": 22, "color": "#E10600"}}, height=600,
                           legend=dict(bgcolor="rgba(10,10,10,0.9)", bordercolor="#E10600", borderwidth=2,
                                       font=dict(color="white", size=11)),
                           plot_bgcolor="rgba(26,26,26,0.8)", paper_bgcolor="rgba(10,10,10,0)",
                           font=dict(color="white"),
                           hoverlabel=dict(bgcolor="rgba(26,26,26,0.95)", font_size=13, font_color="white",
                                           bordercolor="white"))

        col_chart, col_rankings = st.columns([3, 1])
        with col_chart:
            st.plotly_chart(fig4, use_container_width=True)
        with col_rankings:
            st.markdown("### ⚠️ High-Risk Drivers")
            high_dnf = filtered_df.nlargest(5, 'DNF_Rate')[
                ['Driver', 'DNF_Rate_%', 'DNFs', 'RacesEntered', 'TotalPoints']].copy()
            high_dnf['DNFs'] = high_dnf['DNFs'].astype(int)
            high_dnf['RacesEntered'] = high_dnf['RacesEntered'].astype(int)
            high_dnf['TotalPoints'] = high_dnf['TotalPoints'].round(0).astype(int)
            high_dnf.columns = ['Driver', 'DNF %', 'DNFs', 'Races', 'Total Pts']
            st.dataframe(high_dnf, hide_index=True, use_container_width=True, height=220)

            st.markdown("---")

            st.markdown("### ✅ Most Reliable")
            most_reliable = filtered_df.nsmallest(5, 'DNF_Rate')[
                ['Driver', 'DNF_Rate_%', 'FinishRate_%', 'TotalPoints', 'PointsPerRace']].copy()
            most_reliable['TotalPoints'] = most_reliable['TotalPoints'].round(0).astype(int)
            most_reliable['PointsPerRace'] = most_reliable['PointsPerRace'].round(2)
            most_reliable.columns = ['Driver', 'DNF %', 'Finish %', 'Total Pts', 'Pts/Race']
            st.dataframe(most_reliable, hide_index=True, use_container_width=True, height=220)

        st.markdown("---")
        st.markdown(f"""<div class='insight-box'><h4>🚫 Reliability Is Non-Negotiable for Championships</h4>
<p>Drivers with <strong>0% DNF rate</strong> like <strong>{best_rel['Driver']}</strong> finish every race they start. This perfect reliability is championship-level performance.</p>
<p>On the other extreme, <strong>{worst_dnf['Driver']}</strong> has a DNF rate of <strong>{worst_dnf['DNF_Rate']:.1%}</strong>. Every retirement costs an estimated <strong>{dnf_cost:.0f} points</strong> on average. Over a season, high DNF rates can cost 50-100+ points.</p>
<p><strong>Championship math:</strong> A 20% DNF rate means you DNF roughly 5 races out of 24. If you score 8 points per race average, that's 40 points lost just from not finishing. That's often the difference between 2nd and 5th in the championship.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown(f"""<div class='insight-box'><h4>🔧 DNF Sources: Mechanical vs Driver Error</h4>
<p>DNFs come from two sources: mechanical failures (car breaks down) and driver errors (crashes, incidents). The best drivers minimize their own mistakes while their teams provide reliable cars.</p>
<p>The negative trend line shows a clear inverse relationship: <strong>as DNF rate increases, total points decrease dramatically</strong>. This is why reliability testing and driver consistency training are so critical.</p>
<p><strong>Hard truth:</strong> You can have the fastest car and the most skilled driver, but if you can't finish races, you won't win championships. Pace is 60% of the equation, reliability is 40%.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown("---\n### 📋 COMPLETE DRIVER STATISTICS")
        st.dataframe(
            filtered_df.drop(columns=["HeadshotUrl"], errors="ignore").round(3).sort_values("DNF_Rate", ascending=True),
            use_container_width=True, height=400)

# INSIGHT 5
elif page == "Insight 5: Saturday vs Sunday Pace":
    st.markdown("---")
    if filtered_df.empty:
        st.error("⚠️ **NO DATA AVAILABLE** - Adjust filters")
    else:
        filtered_df["QualVsRace_Gap"] = filtered_df["MedianQualifyingPace"] - filtered_df["MedianRacePace"]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_image_placeholder()
            st.markdown(kpi_card_text(filtered_df["Driver"].nunique(), "Total Drivers", "in current filter"),
                        unsafe_allow_html=True)
        with col2:
            quali_fade = filtered_df.nlargest(1, "QualVsRace_Gap").iloc[0]
            try:
                st.image(Image.open(quali_fade["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">+{quali_fade['QualVsRace_Gap']:.2f}s</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{quali_fade['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">qualifying specialist</p></div>""",
                unsafe_allow_html=True)
        with col3:
            race_improver = filtered_df.nsmallest(1, "QualVsRace_Gap").iloc[0]
            try:
                st.image(Image.open(race_improver["HeadshotUrl"]), width=150)
            except:
                kpi_image_placeholder()
            st.markdown(
                f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{abs(race_improver['QualVsRace_Gap']):.2f}s</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{race_improver['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">race day warrior</p></div>""",
                unsafe_allow_html=True)
        with col4:
            kpi_image_placeholder()
            corr_qs = filtered_df["MedianQualifyingPace"].corr(filtered_df["MedianRacePace"])
            c = "#00D2BE" if abs(corr_qs) > 0.7 else "#FFD700" if abs(corr_qs) > 0.4 else "#FF1801"
            strength_qs = "Strong" if abs(corr_qs) > 0.7 else "Moderate" if abs(corr_qs) > 0.4 else "Weak"
            st.markdown(kpi_card_text(f"{corr_qs:.2f}", "Quali-Race Link", f"{strength_qs} correlation", c),
                        unsafe_allow_html=True)

        st.markdown("---")

        fig5 = px.scatter(filtered_df, x="MedianQualifyingPace", y="MedianRacePace", color="TeamName",
                          color_discrete_map=COLOR_MAPPING, size="TotalPoints", hover_name="Driver")
        min_pace = min(filtered_df["MedianQualifyingPace"].min(), filtered_df["MedianRacePace"].min())
        max_pace = max(filtered_df["MedianQualifyingPace"].max(), filtered_df["MedianRacePace"].max())
        fig5.add_shape(type="line", x0=min_pace, y0=min_pace, x1=max_pace, y1=max_pace,
                       line=dict(dash="dash", color="rgba(255,255,255,0.7)", width=2))
        fig5.update_traces(marker=dict(line=dict(width=1, color="Black")))
        fig5.update_xaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig5.update_yaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                          tickfont=dict(color="white"))
        fig5.update_layout(
            title={"text": "<b>SATURDAY vs SUNDAY PERFORMANCE</b>", "x": 0.5, "font": {"size": 22, "color": "#E10600"}},
            height=600, legend=dict(bgcolor="rgba(10,10,10,0.9)", bordercolor="#E10600", borderwidth=2,
                                    font=dict(color="white", size=11)),
            plot_bgcolor="rgba(26,26,26,0.8)", paper_bgcolor="rgba(10,10,10,0)", font=dict(color="white"),
            hoverlabel=dict(bgcolor="rgba(26,26,26,0.95)", font_size=13, font_color="white", bordercolor="white"))

        col_chart, col_rankings = st.columns([3, 1])
        with col_chart:
            st.plotly_chart(fig5, use_container_width=True)
        with col_rankings:
            st.markdown("### 🏎️ Saturday Stars")
            quali_stars = filtered_df.nsmallest(5, 'MedianQualifyingPace')[
                ['Driver', 'MedianQualifyingPace', 'MedianRacePace', 'QualVsRace_Gap', 'TotalPoints']].copy()
            quali_stars['MedianQualifyingPace'] = quali_stars['MedianQualifyingPace'].round(2)
            quali_stars['MedianRacePace'] = quali_stars['MedianRacePace'].round(2)
            quali_stars['QualVsRace_Gap'] = quali_stars['QualVsRace_Gap'].round(2)
            quali_stars['TotalPoints'] = quali_stars['TotalPoints'].round(0).astype(int)
            quali_stars.columns = ['Driver', 'Qual Pace (s)', 'Race Pace (s)', 'Race Drop (s)', 'Total Pts']
            st.dataframe(quali_stars, hide_index=True, use_container_width=True, height=220)

            st.markdown("---")

            st.markdown("### 🏁 Sunday Specialists")
            race_improvers = filtered_df.nsmallest(5, 'QualVsRace_Gap')[
                ['Driver', 'MedianQualifyingPace', 'MedianRacePace', 'QualVsRace_Gap', 'PointsPerRace']].copy()
            race_improvers['MedianQualifyingPace'] = race_improvers['MedianQualifyingPace'].round(2)
            race_improvers['MedianRacePace'] = race_improvers['MedianRacePace'].round(2)
            race_improvers['QualVsRace_Gap'] = race_improvers['QualVsRace_Gap'].round(2)
            race_improvers['PointsPerRace'] = race_improvers['PointsPerRace'].round(2)
            race_improvers.columns = ['Driver', 'Qual Pace (s)', 'Race Pace (s)', 'Race Gain (s)', 'Pts/Race']
            st.dataframe(race_improvers, hide_index=True, use_container_width=True, height=220)

        st.markdown("---")
        st.markdown(f"""<div class='insight-box'><h4>🏁 Saturday Speed Doesn't Guarantee Sunday Success</h4>
<p>The correlation between qualifying and race pace is <strong>{corr_qs:.2f}</strong>. While being fast on Saturday helps you start near the front, it doesn't automatically mean you'll be fast on Sunday with a full fuel load, managing tires, and racing in traffic.</p>
<p><strong>{quali_fade['Driver']}</strong> shows a gap of <strong>+{quali_fade['QualVsRace_Gap']:.2f}s</strong>, meaning they're faster in qualifying than in races. This could be due to struggling with tire management or race pace setup.</p>
<p>On the flip side, <strong>{race_improver['Driver']}</strong> actually improves in race conditions, being <strong>{abs(race_improver['QualVsRace_Gap']):.2f}s</strong> better on Sunday. These are the "race day warriors" who come alive when the lights go out.</p>
<p><strong>Championship insight:</strong> Qualifying in the top 5 gives you a chance to win, but race pace and tire management on Sunday is what actually delivers the 25 points.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown(f"""<div class='insight-box'><h4>⏱️ Why the Gap Exists: Fuel, Tires, and Traffic</h4>
<p>In qualifying, drivers run low fuel, fresh tires, and clear track. In races, they manage heavy fuel loads at the start, degrading tires throughout stints, and battle in dirty air behind other cars.</p>
<p>The drivers above the diagonal line (on the chart) are slower in races than qualifying. The drivers below the line are actually faster or similar in race trim. This shows who has strong race craft and tire management.</p>
<p><strong>Strategic reality:</strong> Qualifying P1 but fading to P5 in the race scores fewer points than qualifying P3 and finishing P2. Sunday performance is what counts for championships.</p></div>""",
                    unsafe_allow_html=True)

        st.markdown("---\n### 📋 COMPLETE DRIVER STATISTICS")
        st.dataframe(filtered_df.drop(columns=["HeadshotUrl"], errors="ignore").round(3).sort_values("QualVsRace_Gap",
                                                                                                     ascending=True),
                     use_container_width=True, height=400)

# INSIGHT 6
elif page == "Insight 6: Sprint vs Race Masters":
    st.markdown("---")
    if filtered_df.empty:
        st.error("⚠️ **NO DATA AVAILABLE** - Adjust filters")
    else:
        filtered_df_sprint = filtered_df[filtered_df["SprintPointsPerSprint"] > 0].copy()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_image_placeholder()
            st.markdown(kpi_card_text(filtered_df["Driver"].nunique(), "Total Drivers", "in current filter"),
                        unsafe_allow_html=True)
        with col2:
            if filtered_df_sprint.empty:
                kpi_image_placeholder()
                st.markdown(
                    """<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">—</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">Sprint Specialist</p><p style="color: #888888; font-size: 14px; margin: 0;">no sprint data</p></div>""",
                    unsafe_allow_html=True)
            else:
                sprint_best = filtered_df_sprint.nlargest(1, "SprintPointsPerSprint").iloc[0]
                try:
                    st.image(Image.open(sprint_best["HeadshotUrl"]), width=150)
                except:
                    kpi_image_placeholder()
                st.markdown(
                    f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{sprint_best['SprintPointsPerSprint']:.1f}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{sprint_best['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">best sprint scorer</p></div>""",
                    unsafe_allow_html=True)
        with col3:
            if filtered_df_sprint.empty:
                kpi_image_placeholder()
                st.markdown(
                    """<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">—</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">Race Master</p><p style="color: #888888; font-size: 14px; margin: 0;">no sprint data</p></div>""",
                    unsafe_allow_html=True)
            else:
                race_best = filtered_df_sprint.nlargest(1, "PointsPerRace").iloc[0]
                try:
                    st.image(Image.open(race_best["HeadshotUrl"]), width=150)
                except:
                    kpi_image_placeholder()
                st.markdown(
                    f"""<div style="text-align: center;"><h1 style="color: #E10600; margin: 0; font-size: 3.5em;">{race_best['PointsPerRace']:.1f}</h1><p style="color: #FFFFFF; font-weight: 700; font-size: 18px; margin: 5px 0 0 0;">{race_best['Driver']}</p><p style="color: #888888; font-size: 14px; margin: 0;">best race scorer</p></div>""",
                    unsafe_allow_html=True)
        with col4:
            kpi_image_placeholder()
            corr_sr = filtered_df_sprint["SprintPointsPerSprint"].corr(filtered_df_sprint["PointsPerRace"]) if len(
                filtered_df_sprint) > 1 else 0.0
            strength_sr = "Strong" if abs(corr_sr) > 0.7 else "Moderate" if abs(corr_sr) > 0.4 else "Weak"
            st.markdown(kpi_card_text(f"{corr_sr:.2f}", "Sprint-Race Link", f"{strength_sr} relationship"),
                        unsafe_allow_html=True)

        st.markdown("---")

        if filtered_df_sprint.empty:
            st.warning(
                "⚠️ No drivers with sprint points in the filtered dataset. Adjust your filters to view sprint analysis.")
        else:
            fig6 = px.scatter(filtered_df_sprint, x="SprintPointsPerSprint", y="PointsPerRace", color="TeamName",
                              color_discrete_map=COLOR_MAPPING, size="TotalPoints", hover_name="Driver")
            fig6.update_traces(marker=dict(line=dict(width=1, color="Black")))
            fig6.update_xaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                              tickfont=dict(color="white"))
            fig6.update_yaxes(showgrid=True, gridcolor="rgba(225,6,0,0.1)", title_font=dict(size=14, color="white"),
                              tickfont=dict(color="white"))
            fig6.update_layout(
                title={"text": "<b>SPRINT vs RACE PERFORMANCE</b>", "x": 0.5, "font": {"size": 22, "color": "#E10600"}},
                height=600, legend=dict(bgcolor="rgba(10,10,10,0.9)", bordercolor="#E10600", borderwidth=2,
                                        font=dict(color="white", size=11)),
                plot_bgcolor="rgba(26,26,26,0.8)", paper_bgcolor="rgba(10,10,10,0)", font=dict(color="white"),
                hoverlabel=dict(bgcolor="rgba(26,26,26,0.95)", font_size=13, font_color="white", bordercolor="white"))

            col_chart, col_rankings = st.columns([3, 1])
            with col_chart:
                st.plotly_chart(fig6, use_container_width=True)
            with col_rankings:
                st.markdown("### ⚡ Sprint Specialists")
                sprint_specialists = filtered_df_sprint.nlargest(5, 'SprintPointsPerSprint')[
                    ['Driver', 'SprintPointsPerSprint', 'TotalSprintPoints', 'PointsPerRace', 'TotalPoints']].copy()
                sprint_specialists['SprintPointsPerSprint'] = sprint_specialists['SprintPointsPerSprint'].round(2)
                sprint_specialists['TotalSprintPoints'] = sprint_specialists['TotalSprintPoints'].round(0).astype(int)
                sprint_specialists['PointsPerRace'] = sprint_specialists['PointsPerRace'].round(2)
                sprint_specialists['TotalPoints'] = sprint_specialists['TotalPoints'].round(0).astype(int)
                sprint_specialists.columns = ['Driver', 'Sprint PPR', 'Sprint Pts', 'Race PPR', 'Total Pts']
                st.dataframe(sprint_specialists, hide_index=True, use_container_width=True, height=220)

                st.markdown("---")

                st.markdown("### 🏁 Race Points Masters")
                race_masters = filtered_df_sprint.nlargest(5, 'PointsPerRace')[
                    ['Driver', 'PointsPerRace', 'TotalRacePoints', 'SprintPointsPerSprint', 'TotalPoints']].copy()
                race_masters['PointsPerRace'] = race_masters['PointsPerRace'].round(2)
                race_masters['TotalRacePoints'] = race_masters['TotalRacePoints'].round(0).astype(int)
                race_masters['SprintPointsPerSprint'] = race_masters['SprintPointsPerSprint'].round(2)
                race_masters['TotalPoints'] = race_masters['TotalPoints'].round(0).astype(int)
                race_masters.columns = ['Driver', 'Race PPR', 'Race Pts', 'Sprint PPR', 'Total Pts']
                st.dataframe(race_masters, hide_index=True, use_container_width=True, height=220)

            st.markdown("---")
            st.markdown(f"""<div class='insight-box'><h4>🏃 Sprints vs Races: Different Tactics, Different Winners</h4>
<p>The correlation between sprint and race performance is <strong>{corr_sr:.2f}</strong>. Sprint races are only 19-24 laps with no pit stops, while full races are 50-70 laps with tire strategy and multiple pit stops.</p>
<p><strong>{sprint_best['Driver'] if not filtered_df_sprint.empty else 'N/A'}</strong> excels in sprints with <strong>{sprint_best['SprintPointsPerSprint']:.1f}</strong> points per sprint. Sprint races reward aggressive attacking and one-lap pace since there's no time for strategy.</p>
<p><strong>{race_best['Driver'] if not filtered_df_sprint.empty else 'N/A'}</strong> dominates full races with <strong>{race_best['PointsPerRace']:.1f}</strong> points per race. Full races reward tire management, fuel strategy, and consistent pace over many laps.</p>
<p><strong>Championship insight:</strong> Sprints make up about 10% of total season points, but they reveal which drivers are pure attackers versus strategic thinkers.</p></div>""",
                        unsafe_allow_html=True)

            st.markdown(f"""<div class='insight-box'><h4>🎯 The Complete Package: Excel at Both</h4>
<p>Drivers who score well in both sprints AND races are the complete package. They can attack aggressively in short formats and manage strategy in long formats.</p>
<p>Some drivers are sprint specialists—fast and aggressive but struggle with tire management over long races. Others are race masters—excellent at strategy and consistency but don't have the one-lap attacking speed for sprints.</p>
<p><strong>Elite driver profile:</strong> High sprint points + high race points = championship contender who can win in any format.</p></div>""",
                        unsafe_allow_html=True)

            st.markdown("---\n### 📋 COMPLETE DRIVER STATISTICS (Sprint Participants)")
            st.dataframe(filtered_df_sprint.drop(columns=["HeadshotUrl"], errors="ignore").round(3).sort_values(
                "SprintPointsPerSprint", ascending=False), use_container_width=True, height=400)

else:
    st.info(f"🚧 **{page}** - Page not found. Please select a valid insight from the sidebar.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'><p style='font-size: 12px; letter-spacing: 2px;'>FORMULA 1 © 2025 | PERFORMANCE ANALYTICS DASHBOARD</p></div>",
    unsafe_allow_html=True)