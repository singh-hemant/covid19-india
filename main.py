import requests
import streamlit as st
import pandas as pd
import csv


@st.cache
def load_data(url):
    try:
        res = requests.get(url)
        return res, True
    except:
        return -1, False


def daily_cases(df):
    st.header("Today's Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Confirmed", int(df['Daily Confirmed'][-1]),
                (int(df['Daily Confirmed'][-1]) - int(df['Daily Confirmed'][-2])))
    col2.metric("Deceased", int(df['Daily Deceased'][-1]),
                (int(df['Daily Deceased'][-1]) - int(df['Daily Deceased'][-2])))
    col3.metric("Recovered", int(df['Daily Recovered'][-1]),
                (int(df['Daily Recovered'][-1]) - int(df['Daily Recovered'][-2])))

    st.header("Daily confirmed cases -:")
    st.line_chart(df['Daily Confirmed'].rolling(7).mean())

    st.header("Daily Deceased cases -:")
    st.line_chart(df['Daily Deceased'].rolling(7).mean())

    st.header("Daily Recovered cases -:")
    st.line_chart(df['Daily Recovered'].rolling(7).mean())


def total_cases(df):
    st.header("Total Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Confirmed", int(df['Total Confirmed'][-1]))
    col2.metric("Deceased", int(df['Total Deceased'][-1]))
    col3.metric("Recovered", int(df['Total Recovered'][-1]))

    st.header("Total confirmed cases -:")
    st.bar_chart(df['Total Confirmed'].rolling(7).mean())

    st.header("Total Deceased cases -:")
    st.bar_chart(df['Total Deceased'].rolling(7).mean())

    st.header("Total Recovered cases -:")
    st.bar_chart(df['Total Recovered'].rolling(7).mean())


def plot_data():
    df1 = pd.DataFrame(data)
    df = df1.copy()
    # -------------------- Data cleaning ----------------
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])
    df['Date_YMD'] = pd.to_datetime(df['Date_YMD'])
    df['Daily Confirmed'] = pd.to_numeric(df['Daily Confirmed'])
    df['Total Confirmed'] = pd.to_numeric(df['Total Confirmed'])
    df['Daily Recovered'] = pd.to_numeric(df['Daily Recovered'])
    df['Total Recovered'] = pd.to_numeric(df['Total Recovered'])
    df['Daily Deceased'] = pd.to_numeric(df['Daily Deceased'])
    df['Total Deceased'] = pd.to_numeric(df['Total Deceased'])

    df.index = df['Date']
    # --------------------------------------------------------

    # ------------------- side bar ---------------------------
    st.sidebar.title("Covid-19 in India")
    show_data = st.sidebar.checkbox("ShowData")
    if show_data:
        st.subheader("Dataset")
        st.write(df)

    select_cases = st.sidebar.selectbox("Select cases", ['Daily', 'Total'])
    if select_cases == "Daily":
        daily_cases(df)
    if select_cases == "Total":
        total_cases(df)


# ----------------------- Main code --------------------------------
url = 'https://data.covid19india.org/csv/latest/case_time_series.csv'
url2 = 'https://data.covid19india.org/v4/min/data.min.json'
st.title("Covid cases in India")
st.write("Fetching data...")
res, success = load_data(url)
data = csv.reader(res.text.strip().split('\n'))
if success:
    st.write("Fetching data...complete")
    plot_data()
else:
    st.write("Fetching data...failed,\n refresh page")
