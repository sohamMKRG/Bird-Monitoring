import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bird Observation Dashboard", layout="wide")
st.title("Bird Species Observation Dashboard")

# Load dataset
df = pd.read_csv("Cleaned_Bird_Data.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filters")
habitat_filter = st.sidebar.multiselect(
    "Select Habitat Type",
    options=df['Habitat_Type'].unique(),
    default=df['Habitat_Type'].unique()
)
observer_filter = st.sidebar.multiselect(
    "Select Observer",
    options=df['Observer'].unique(),
    default=df['Observer'].unique()
)

df_filtered = df[df['Habitat_Type'].isin(habitat_filter)]
df_filtered = df_filtered[df_filtered['Observer'].isin(observer_filter)]

# Sidebar download button for filtered dataset
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=df_filtered.to_csv(index=False).encode('utf-8'),
    file_name="filtered_bird_data.csv",
    mime="text/csv"
)

# ==============================
# Chart 1: Temporal Heatmap
# ==============================
st.header("1. Temporal Heatmap")
df_filtered['Year'] = df_filtered['Date'].dt.year
df_filtered['Month'] = df_filtered['Date'].dt.month_name()
heatmap_data = df_filtered.groupby(['Year', 'Month'])['Common_Name'].count().reset_index()
heatmap_pivot = heatmap_data.pivot(index='Month', columns='Year', values='Common_Name').fillna(0)
fig_heatmap = px.imshow(heatmap_pivot, text_auto=True, color_continuous_scale='Viridis',
                        title="Sightings by Month and Year")
st.plotly_chart(fig_heatmap, use_container_width=True)

# ==============================
# Chart 2: Top 15 Species by Sightings
# ==============================
st.header("2. Top 15 Species by Sightings")
species_counts = df_filtered['Scientific_Name'].value_counts().head(15).reset_index()
species_counts.columns = ['Scientific_Name', 'Sightings']
fig_species = px.bar(species_counts, x='Scientific_Name', y='Sightings',
                     title='Top 15 Species by Sightings')
fig_species.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_species, use_container_width=True)

# ==============================
# Chart 3: Sightings by Habitat Type
# ==============================
st.header("3. Sightings by Habitat Type")
habitat_counts = df_filtered['Habitat_Type'].value_counts().reset_index()
habitat_counts.columns = ['Habitat_Type', 'Count']
fig_habitat_pie = px.pie(habitat_counts, names='Habitat_Type', values='Count',
                         title='Sightings by Habitat Type')
st.plotly_chart(fig_habitat_pie, use_container_width=True)

# ==============================
# Chart 4: Sex Distribution
# ==============================
st.header("4. Sex Distribution")
sex_counts = df_filtered['Sex'].value_counts().reset_index()
sex_counts.columns = ['Sex', 'Count']
fig_sex = px.pie(sex_counts, names='Sex', values='Count', title='Sex Distribution')
st.plotly_chart(fig_sex, use_container_width=True)

# ==============================
# Chart 5: Bird Sightings vs Temperature and Humidity
# ==============================
st.header("5. Bird Sightings vs Temperature and Humidity")
env_data = df_filtered.groupby(['Temperature', 'Humidity'])['Common_Name'].count().reset_index()
env_data.columns = ['Temperature', 'Humidity', 'Sightings']
fig_env = px.scatter(env_data, x='Temperature', y='Humidity', size='Sightings', color='Sightings',
                     title='Bird Sightings vs Temperature and Humidity',
                     color_continuous_scale='Plasma')
st.plotly_chart(fig_env, use_container_width=True)

# ==============================
# Chart 6: Sightings by Park Code
# ==============================
st.header("6. Sightings by Park Code")
park_counts = df_filtered.groupby('Admin_Unit_Code')['Common_Name'].count().reset_index()
fig_park = px.bar(park_counts, x='Admin_Unit_Code', y='Common_Name',
                  title='Sightings by Park Code')
st.plotly_chart(fig_park, use_container_width=True)

# ==============================
# Chart 7: Monthly Sightings Trend
# ==============================
st.header("7. Monthly Sightings Trend")
monthly_counts = df_filtered.groupby(df_filtered['Date'].dt.month)['Common_Name'].count().reset_index()
monthly_counts.columns = ['Month', 'Sightings']
fig_monthly = px.line(monthly_counts, x='Month', y='Sightings', markers=True,
                      title='Monthly Sightings Trend')
st.plotly_chart(fig_monthly, use_container_width=True)

# ==============================
# Chart 8: Observation Methods Used
# ==============================
st.header("8. Observation Methods Used")
id_counts = df_filtered['ID_Method'].value_counts().reset_index()
id_counts.columns = ['ID_Method', 'Count']
fig_id_method = px.bar(id_counts, x='ID_Method', y='Count', title='Observation Methods Used')
st.plotly_chart(fig_id_method, use_container_width=True)

# ==============================
# Chart 9: Flyover vs Non-Flyover
# ==============================
st.header("9. Flyover vs Non-Flyover")
fly_counts = df_filtered['Flyover_Observed'].value_counts().reset_index()
fly_counts.columns = ['Flyover_Observed', 'Count']
fig_fly = px.pie(fly_counts, names='Flyover_Observed', values='Count',
                 title='Flyover vs Non-Flyover Sightings')
st.plotly_chart(fig_fly, use_container_width=True)

# ==============================
# Chart 10: Disturbance Impact on Sightings
# ==============================
st.header("10. Disturbance Impact on Sightings")
disturbance_counts = df_filtered['Disturbance'].value_counts().reset_index()
disturbance_counts.columns = ['Disturbance', 'Count']
fig_disturb = px.bar(disturbance_counts, x='Disturbance', y='Count',
                     title='Impact of Disturbance on Sightings')
st.plotly_chart(fig_disturb, use_container_width=True)

# ==============================
# Chart 11: Top Observers by Sightings
# ==============================
st.header("11. Top Observers by Sightings")
observer_counts = df_filtered['Observer'].value_counts().reset_index().head(10)
observer_counts.columns = ['Observer', 'Sightings']
fig_observer = px.bar(observer_counts, x='Sightings', y='Observer', orientation='h',
                      title='Top 10 Observers by Total Sightings')
st.plotly_chart(fig_observer, use_container_width=True)

# ==============================
# Chart 12: Top Plots by Species Diversity
# ==============================
st.header("12. Top Plots by Species Diversity")
plot_species = df_filtered.groupby('Plot_Name')['Scientific_Name'].nunique().reset_index()
plot_species = plot_species.sort_values(by='Scientific_Name', ascending=False).head(10)
fig_plot_species = px.bar(plot_species, x='Scientific_Name', y='Plot_Name', orientation='h',
                          title='Top 10 Plots by Species Diversity')
st.plotly_chart(fig_plot_species, use_container_width=True)

# ==============================
# Chart 13: Bird Sightings by Temperature
# ==============================
st.header("13. Bird Sightings by Temperature")
temp_counts = df_filtered.groupby('Temperature')['Common_Name'].count().reset_index()
temp_counts.columns = ['Temperature', 'Sightings']
fig_temp = px.line(temp_counts.sort_values('Temperature'), x='Temperature', y='Sightings', markers=True,
                   title='Bird Sightings by Temperature')
st.plotly_chart(fig_temp, use_container_width=True)

# ==============================
# Chart 14: Bird Sightings by Humidity
# ==============================
st.header("14. Bird Sightings by Humidity")
humidity_counts = df_filtered.groupby('Humidity')['Common_Name'].count().reset_index()
humidity_counts.columns = ['Humidity', 'Sightings']
fig_humidity = px.line(humidity_counts.sort_values('Humidity'), x='Humidity', y='Sightings', markers=True,
                       title='Bird Sightings by Humidity')
st.plotly_chart(fig_humidity, use_container_width=True)

# ==============================
# Chart 15: Species Count by Conservation Status
# ==============================
st.header("15. Species Count by Conservation Status")
df_filtered['Conservation_Status'] = df_filtered['PIF_Watchlist_Status'].apply(
    lambda x: 'Watchlist' if x else 'Not Watchlist')
status_counts = df_filtered.groupby('Conservation_Status')['Scientific_Name'].nunique().reset_index()
fig_cons = px.bar(status_counts, x='Conservation_Status', y='Scientific_Name',
                  title='Species Count by Conservation Status')
st.plotly_chart(fig_cons, use_container_width=True)

# ==============================
# Chart 16: Observation Interval Lengths
# ==============================
st.header("16. Observation Interval Lengths")
interval_counts = df_filtered['Interval_Length'].value_counts().reset_index()
interval_counts.columns = ['Interval_Length', 'Count']
fig_interval = px.bar(interval_counts, x='Interval_Length', y='Count',
                      title='Observation Intervals Used')
st.plotly_chart(fig_interval, use_container_width=True)

# ==============================
# Chart 17: Distribution of Bird Distances
# ==============================
st.header("17. Distribution of Bird Distances")
fig_distance = px.histogram(df_filtered, x='Distance', nbins=20,
                            title='Distribution of Bird Observation Distances')
st.plotly_chart(fig_distance, use_container_width=True)

# ==============================
# Chart 18: Correlation Heatmap of Numerical Features
# ==============================
st.header("18. Correlation Heatmap of Numerical Features")
numeric_df = df_filtered.select_dtypes(include=['float64', 'int64'])
fig_corr = px.imshow(numeric_df.corr(), text_auto=True, color_continuous_scale='RdBu',
                     title='Correlation Heatmap of Numerical Features')
st.plotly_chart(fig_corr, use_container_width=True)

# ==============================
# Chart 19: Pair Plot of Key Numerical Variables
# ==============================
st.header("19. Pair Plot of Key Numerical Variables")
pair_cols = ['Temperature', 'Humidity', 'Distance', 'Initial_Three_Min_Cnt']
if all(col in df_filtered.columns for col in pair_cols):
    sns.pairplot(df_filtered[pair_cols], diag_kind='kde')
    st.pyplot(plt)

# ==============================
# Species Search Tool with Download
# ==============================
st.header("Species Search Tool")

species_list = sorted(df_filtered['Scientific_Name'].unique())
selected_species = st.selectbox("Select a Species", species_list)

if selected_species:
    species_data = df_filtered[df_filtered['Scientific_Name'] == selected_species]
    
    # Basic info
    st.subheader(f"Details for {selected_species}")
    st.write(f"Total Sightings: {species_data.shape[0]}")
    st.write(f"Average Distance: {species_data['Distance'].mean():.2f} meters")
    
    # Download species-specific data
    st.download_button(
        label=f"Download Data for {selected_species}",
        data=species_data.to_csv(index=False).encode('utf-8'),
        file_name=f"{selected_species.replace(' ', '_')}_data.csv",
        mime="text/csv"
    )
    
    # Habitat distribution for this species
    habitat_counts = species_data['Habitat_Type'].value_counts().reset_index()
    habitat_counts.columns = ['Habitat_Type', 'Count']
    fig_habitat_species = px.bar(habitat_counts, x='Habitat_Type', y='Count',
                                 title="Habitat Distribution for Species")
    st.plotly_chart(fig_habitat_species, use_container_width=True)
    
    # Observers who reported this species
    observer_species = species_data['Observer'].value_counts().reset_index()
    observer_species.columns = ['Observer', 'Count']
    fig_observer_species = px.bar(observer_species, x='Observer', y='Count',
                                  title="Observers Reporting This Species")
    st.plotly_chart(fig_observer_species, use_container_width=True)
    
    # Conservation status
    watchlist_status = "Yes" if species_data['PIF_Watchlist_Status'].any() else "No"
    st.write(f"PIF Watchlist Status: {watchlist_status}")