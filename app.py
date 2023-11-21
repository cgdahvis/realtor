import streamlit as st
import pandas as pd

# Read the data from the URL
url = r"https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/RDC_Inventory_Core_Metrics_Zip_History.csv"
df = pd.read_csv(url,low_memory=False)

# Extract year and month from the 'month_date_yyyymm' column
df['year'] = df['month_date_yyyymm'].astype(str).str[:4]
df['month'] = df['month_date_yyyymm'].astype(str).str[4:6]

# Convert year and month to numeric values
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['month'] = pd.to_numeric(df['month'], errors='coerce')

# Create a 'date' column
df['date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Streamlit app header
st.title("Saratoga Springs Real Estate Data")

# Sidebar for selecting a location
var = st.sidebar.text_input("Enter location (e.g., Saratoga Springs, NY):")

# Filter data based on the selected location
data = df[df['zip_name'].str.lower() == var.lower()]

if not data.empty:
    # Line chart for median listing price per square foot
    st.subheader("Median Listing Price per Square Foot")
    st.line_chart(data['median_listing_price_per_square_foot'])

    # Line chart for active listing count
    st.subheader("Active Listing Count Over Time")
    st.line_chart(data.query('year > 2016').set_index('date')['active_listing_count'])

    # Line chart for active listing count with linear line shape
    st.subheader("Active Listing Count Over Time (Linear Line Shape)")
    st.line_chart(data.set_index('date')['active_listing_count'])
else:
    st.warning(f"No data found for location: {var}")
