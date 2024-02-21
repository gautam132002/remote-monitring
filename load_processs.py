import streamlit as st
from firebase_admin import credentials, db, initialize_app
import time
import pandas as pd


def get_data_from_firebase():
    ref = db.reference('/process')
    process_data = ref.get()
    return process_data

def update_dataframe(process_data):
    data_to_write = []

    for pid, process_info in sorted(process_data.items(), key=lambda x: x[1]['%CPU'], reverse=True):
        data_to_write.append({
            "Process Name": process_info['Process Name'],
            "USER": process_info['USER'],
            "PID": process_info['PID'],
            "%CPU": process_info['%CPU'],
            "%MEM": process_info['%MEM'],
            "STAT": process_info['STAT'],
            "TIME": process_info['TIME']
        })

    return pd.DataFrame(data_to_write)

def load_data(df):
    st.subheader("Ongoing Process")

    unique_df = df.drop_duplicates(subset="PID")
    st.dataframe(
        unique_df,
        column_config={
            "Process Name": "App name",
            "USER": "User",
            "PID": st.column_config.NumberColumn("Process ID"),
            "%CPU": st.column_config.ProgressColumn(
                "CPU usage",
                help="cpu usage percentage",
                format="%f %%",
                min_value=0,
                max_value=100,
            ),
            "%MEM": st.column_config.ProgressColumn(
                "Memory usage",
                help="memory usage percentage",
                format="%0.2f %%",
                min_value=0,
                max_value=100,
            ),
            "STAT": "Status",
            "TIME": "Time",
        },
        hide_index=True,
    )


# def main():
#     st.title("Process Monitoring Dashboard")

#     while True:
#         try:
#             load_data()
#             time.sleep(1)
#         except KeyboardInterrupt:
#             break
#         except Exception as e:
#             st.error(f"Error: {e}")

# if __name__ == "__main__":
#     main()