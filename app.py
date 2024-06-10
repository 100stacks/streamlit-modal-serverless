"""
Generative AI application to run text generation inference (TGI) on Mixtral_8x7B
running on Modal's Serverless Platform.

ref: https://docs.streamlit.io/get-started/tutorials/create-an-app
"""

def main():
    import numpy as np
    import pandas as pd
    import streamlit as st

    st.title("Uber pickups in NYC! (Streamlit provided dataset)")

    DATE_COLUMN = "data/time"
    DATA_URL = (
        "https://s3-us-west-2.amazonaws.com"
        "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
    )

    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)

        def lowercase(x):
            return str(x).lower()

        data.rename(lowercase, axis="columns", inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

        return data

    data_load_state = st.text("Loading data...")
    data = load_data(100000)
    data_load_state.text("Done! (using st.cache_data)")

    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(data)

    st.subheader("Number of pickups per hour")
    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24)
    )[0]
    st.bar_chart(hist_values)

    # Some bumer in the range 0-23
    hour_to_filter = st.slider("hour", 0, 23, 17)
    filterd_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader("Map of all pickups at %s:00" % hour_to_filter)
    st.map(filterd_data)

if __name__ == "__main__":
    main()
