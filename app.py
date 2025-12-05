import streamlit as st
import pandas as pd
import plotly.express as px
df=pd.read_csv('/content/pizza_sales.csv')

# 2. Set up the Streamlit page configuration
st.set_page_config(page_title="Pizza Sales Dashboard", layout="wide")

# 3. Add a main title for the dashboard
st.title("Pizza Sales Dashboard")

# 4. Add a subheader for "Data Filtering"
st.subheader("Data Filtering")

# 5. Create multiselect widgets for filtering
pizza_categories = df['pizza_category'].unique()
pizza_sizes = df['pizza_size'].unique()
pizza_names = df['pizza_name'].unique()

selected_categories = st.multiselect(
    "Select Pizza Categories:",
    options=pizza_categories,
    default=pizza_categories
)

selected_sizes = st.multiselect(
    "Select Pizza Sizes:",
    options=pizza_sizes,
    default=pizza_sizes
)

selected_names = st.multiselect(
    "Select Pizza Names:",
    options=pizza_names,
    default=pizza_names
)

# 6. Filter the original df DataFrame based on selections
filtered_df = df[
    df['pizza_category'].isin(selected_categories) &
    df['pizza_size'].isin(selected_sizes) &
    df['pizza_name'].isin(selected_names)
]

# 7. Add a subheader for "Key Metrics"
st.subheader("Key Metrics")

# 8. Display overall key metrics
total_revenue_filtered = filtered_df['total_price'].sum()
total_quantity_filtered = filtered_df['quantity'].sum()
average_order_value_filtered = filtered_df['total_price'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue_filtered:,.2f}")
col2.metric("Total Quantity Sold", f"{total_quantity_filtered:,}")
col3.metric("Average Order Value", f"${average_order_value_filtered:,.2f}")

# 9. Add a subheader for "Visualizations"
st.subheader("Visualizations")

# 10. Create a plotly.express scatter plot for quantity vs total_price
fig_scatter = px.scatter(
    filtered_df,
    x='quantity',
    y='total_price',
    color='pizza_name',
    title='Quantity vs Total Price by Pizza Name',
    labels={'quantity': 'Quantity Sold', 'total_price': 'Total Price ($)'},
    hover_name='pizza_name'
)
st.plotly_chart(fig_scatter, width='stretch')

# 11. Create a plotly.express bar chart for pizza_category distribution
category_counts = filtered_df['pizza_category'].value_counts().reset_index()
category_counts.columns = ['pizza_category', 'count']
fig_bar_category = px.bar(
    category_counts,
    x='pizza_category',
    y='count',
    title='Distribution of Pizza Categories',
    labels={'pizza_category': 'Pizza Category', 'count': 'Number of Orders'},
    color='pizza_category'
)
st.plotly_chart(fig_bar_category, width='stretch')

# 12. Create a plotly.express pie chart for proportion of total_price by pizza_category
pizza_category_revenue = filtered_df.groupby('pizza_category')['total_price'].sum().reset_index()
fig_pie_category = px.pie(
    pizza_category_revenue,
    values='total_price',
    names='pizza_category',
    title='Proportion of Total Revenue by Pizza Category',
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig_pie_category, width='stretch')

# 13. Add a button to show summary report
if st.button("Show Summary Report"):
    st.subheader("Summary Reports")
    st.write("### Sales by Pizza Name")
    st.dataframe(pizza_name_sales)
    st.write("### Sales by Pizza Category")
    st.dataframe(pizza_category_sales)
    st.write("### Sales by Pizza Size")
    st.dataframe(pizza_size_sales)
    st.write("### Monthly Sales")
    st.dataframe(monthly_sales_ordered)
    st.write("### Daily Sales")
    st.dataframe(daily_sales_ordered)

print("Streamlit dashboard code generated. To run, save this code as a .py file and execute 'streamlit run your_file_name.py'")
