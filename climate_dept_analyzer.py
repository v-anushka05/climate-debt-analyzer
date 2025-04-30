import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
def load_data():
    file_path = r"climate_debt_analyzer_top100_10yrs.xlsx"
    df = pd.read_excel(file_path)
    return df

df = load_data()

# Streamlit App
st.set_page_config(page_title='Climate Debt Analyzer', layout='wide')
st.title('🌍 Climate Debt Analyzer - 10 Years Analysis')

# Sidebar
st.sidebar.header('Filter Options')
selected_country = st.sidebar.selectbox('Select a Country', df['Country'].unique())
years = st.sidebar.slider('Select Year Range', int(df['Year'].min()), int(df['Year'].max()), (2015, 2024))

# Filtered Data
filtered_df = df[(df['Country'] == selected_country) & (df['Year'].between(years[0], years[1]))]

# Debt and CO2 Emissions Over Time
col1, col2 = st.columns(2)
with col1:
    st.subheader(f'Debt Trend ({selected_country})')
    fig_debt = px.line(filtered_df, x='Year', y='Debt (Billion USD)', markers=True, title='Debt Over Time')
    st.plotly_chart(fig_debt, use_container_width=True)

with col2:
    st.subheader(f'CO₂ Emissions Trend ({selected_country})')
    fig_co2 = px.line(filtered_df, x='Year', y='CO2 Emissions (Million Tons)', markers=True, title='CO₂ Emissions Over Time')
    st.plotly_chart(fig_co2, use_container_width=True)

# Renewable Investment and SDG Score Comparison
col3, col4 = st.columns(2)
with col3:
    st.subheader(f'Renewable Energy Investment ({selected_country})')
    fig_invest = px.bar(filtered_df, x='Year', y='Renewable Energy Investment (Billion USD)', color='Year', title='Investment in Renewable Energy')
    st.plotly_chart(fig_invest, use_container_width=True)

with col4:
    st.subheader(f'SDG Score Trend ({selected_country})')
    fig_sdg = px.line(filtered_df, x='Year', y='SDG Score', markers=True, title='Sustainable Development Goal Score')
    st.plotly_chart(fig_sdg, use_container_width=True)

# Correlation Heatmap
st.subheader('📊 Correlation Insights')
corr_df = df[['Debt (Billion USD)', 'CO2 Emissions (Million Tons)', 'Renewable Energy Investment (Billion USD)', 'SDG Score']].corr()
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_df, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Policy Recommendations
st.subheader('📌 AI-Powered Policy Recommendations')
if filtered_df['SDG Score'].mean() < 65:
    st.warning(f"{selected_country} should significantly increase renewable energy investments and debt transparency.")
elif filtered_df['SDG Score'].mean() < 75:
    st.info(f"{selected_country} is making progress but should optimize climate debt usage for better impact.")
else:
    st.success(f"{selected_country} is on track with sustainable development goals. Keep up the good work!")

# Dataset Download Option
st.sidebar.subheader('Download Dataset')
st.sidebar.download_button(label='📥 Download Data', data=df.to_csv(index=False), file_name='climate_debt_analyzer_10yrs.csv', mime='text/csv')

# Run command:
# streamlit run climate_debt_analyzer.py
