import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd

# Page config
st.set_page_config(page_title="Employee Viewer", layout="wide")
st.title("Employee Data")

# Get active Snowflake session (no credentials needed in Snowflake Streamlit)
session = get_active_session()

# Load data
@st.cache_data
def load_employees():
    df = session.sql("SELECT * FROM APP_PULSE.US.EMPLOYEE ORDER BY EMPNO").to_pandas()
    return df

df = load_employees()

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", len(df))
col2.metric("Avg Salary", f"${df['SAL'].mean():,.2f}")
col3.metric("Departments", df['DEPTNO'].nunique())

st.divider()

# Filters
col_f1, col_f2 = st.columns(2)
with col_f1:
    dept_options = ["All"] + sorted(df['DEPTNO'].dropna().astype(int).unique().tolist())
    selected_dept = st.selectbox("Filter by Department", dept_options)
with col_f2:
    job_options = ["All"] + sorted(df['JOB'].dropna().unique().tolist())
    selected_job = st.selectbox("Filter by Job", job_options)

# Apply filters
filtered = df.copy()
if selected_dept != "All":
    filtered = filtered[filtered['DEPTNO'] == selected_dept]
if selected_job != "All":
    filtered = filtered[filtered['JOB'] == selected_job]

st.dataframe(filtered, use_container_width=True)
