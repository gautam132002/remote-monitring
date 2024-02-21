import streamlit as st
import plotly.express as px
import threading
import time
from getdatafb import get_all_entries
import plotly.figure_factory as ff
import pandas as pd
import load_processs


st.title("/Remote-monitring")
st.caption(":green[! Connected to Firebase.]")

tab1, tab2, tab3, tab4, tab5, tab6  = st.tabs(["CPU", "Memory", "DIsk", "Network", "Process", "Flag"])



placeholder = tab1.empty()
placeholder2 = tab2.empty()
placeholder3 = tab3.empty()
placeholder5 = tab5.empty()
placeholder4 = tab4.empty()
placeholder6 = tab6.empty()
# placeholder7 = tab7.empty()


#const ================

prev_download = None
prev_upload = None
df = pd.DataFrame(columns=["Process Name", "USER", "PID", "%CPU", "%MEM", "STAT", "TIME"])

#=====================

while True:
    data = get_all_entries()
    latest_data = data[-1]

    print(latest_data)

    cpu_value = latest_data.get("CPU_Usage_Percentage", 0)
    cpu_usage = latest_data.get("CPU_Used", 0)
    cpu_free = round(latest_data.get("CPU_Free",0),2)

    mem_value = latest_data.get("Memory_Usage_Percentage", 0)
    mem_usage = latest_data.get("Memory_Used_MB", 0)
    mem_free = round(latest_data.get("Memory_Free_MB", 0),2)

    storage_value = latest_data.get("Storage_Usage_Percentage", 0)
    storage_usage = latest_data.get("Storage_Used_GB", 0)
    storage_free = round(latest_data.get("Storage_Free_GB", 0),2)

    net_up = round(latest_data.get("Network_Upload_MB_s", 0)/8,1)
    net_dow = round(latest_data.get("Network_Download_MB_s", 0)/8,1)
    
    ############################################################################################

    with placeholder.container():

        h = 220
        with st.container(border=True):
            col1, col2, col3 = st.columns([30,10,60])

            with col1:
                st.subheader("CPU consuption")

                k1,k2= st.columns([30,70])
                with k2:
                    st.metric("CPU Usage", f"{cpu_value}%", cpu_free)
                # st.markdown("---")
                cpu = px.pie(values=[cpu_value, 100 - cpu_value], names=["cpu_usage", 'Unused'], hole=0.7, color_discrete_sequence=["#d4bff9","#7E3FF2"])
                cpu.update_layout(height=h, width=h,showlegend=False)
                st.plotly_chart(cpu)
                
                
            with col2:
                pass
            with col3:
                df = pd.DataFrame(data)[-30:]
                st.subheader("CPU Usage Distribution")
                st.bar_chart(df["CPU_Used"],height=300)
        st.caption(f":red[cpu free => {cpu_free}]")


    #################################################################################

    with placeholder2.container():

        h = 220
        with st.container(border=True):
            col1, col2, col3 = st.columns([30,10,60])

            with col1:
                st.subheader("Memory Usage")

                k1,k2= st.columns([30,70])
                with k2:
                    st.metric("Memory Usage", f"{mem_value}%", mem_free)
                # st.markdown("---")
                mem = px.pie(values=[mem_value, 100 - mem_value], names=["memory used", 'Unused'], hole=0.7, color_discrete_sequence=["#ffe194", "#faa647"])
                mem.update_layout(height=h, width=h,showlegend=False)
                st.plotly_chart(mem)
                
            with col2:
                pass
            with col3:
                df = pd.DataFrame(data)[-30:]
                st.subheader("Memory Usage Distribution")
                st.bar_chart(df["Memory_Used_MB"],height=300)
        st.caption(f":red[Memory free => {mem_free}MB]")
    ############################################################################################

    with placeholder3.container():

        h = 220
        with st.container(border=True):
            col1, col2, col3 = st.columns([30,10,60])

            with col1:
                st.subheader("Disk Usage")

                k1,k2= st.columns([30,70])
                with k2:
                    st.metric("Disk Usage", f"{storage_value}%", storage_free)
                # st.markdown("---")
                storage = px.pie(values=[storage_value, 100 - storage_value], names=["storage used", 'Unused'], hole=0.7, color_discrete_sequence=["#F8BBD0", "#C2185B"])
                storage.update_layout(height=h, width=h,showlegend=False)
                st.plotly_chart(storage)
                
            with col2:
                pass
            with col3:
                df = pd.DataFrame(data)[-30:]
                st.subheader("Memory Usage Distribution")
                st.bar_chart(df["Storage_Used_GB"],height=300)
        st.caption(f":red[Disk free => {storage_free}GB]")

    ##################################################################################

    with placeholder5.container():
        
        
        try:
            process_data = load_processs.get_data_from_firebase()
            if process_data:
                df = load_processs.update_dataframe(process_data)
                load_processs.load_data(df)
            else:
                st.write("No process data available.")
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            st.error(f"Error: {e}")


    ##############################################################################################

    with placeholder4.container():

        # pass

        st.subheader("Network Status")

        # print(net_dow, net_up, "====================")

        if net_up == 0.0 and net_dow == 0.0:
            st.caption(":red[Network is either disconnected or not in use!]")

        else:
            st.caption(":green[network connected!]")
            x1,x2 = st.columns(2)


            with x1:

                if prev_download  == None:

                    st.metric(label="Download", value=f"{net_dow}KB/s", delta="0")
                    prev_download = net_dow
                else:
                    diff = round(net_dow - prev_download, 2)
                    st.metric(label="Download", value=f"{net_dow}KB/s", delta=f"{diff}kb/s")

            with x2:

                if prev_upload  == None:

                    st.metric(label="Upload", value=f"{net_up}KB/s", delta="0")
                    prev_upload = net_up
                else:
                    diff_2 = round(net_up - prev_upload,2)
                    st.metric(label="Upload", value=f"{net_up}KB/s", delta=f"{diff_2}kb/s")


    ########################################################################

    with placeholder6.container():
        st.subheader("/Actions required")

        # Load CSV data
        csv_filename = "result_statistics.csv"
        try:
            csv_data = pd.read_csv(csv_filename)
        except FileNotFoundError:
            st.error(f"CSV file '{csv_filename}' not found.")
            st.stop()

        try:
            process_data = load_processs.get_data_from_firebase()
            if process_data:
                df = load_processs.update_dataframe(process_data)

                flags = []
                processed_pids = set()

                for index, row in df.iterrows():
                    pid = row['PID']
                    process_name = row['Process Name']

                    if (pid, process_name) in processed_pids:
                        continue

                    if any(
                        (csv_data['PID'] == pid) | (csv_data['Process Name'] == process_name)
                    ):
                        matching_rows = csv_data[
                            (csv_data['PID'] == pid) | (csv_data['Process Name'] == process_name)
                        ]

                        is_flagged = False

                        for _, csv_row in matching_rows.iterrows():
                            cpu_mean = csv_row['CPU_MEAN']
                            cpu_std_dev = csv_row['CPU_STD_Deviation']
                            mem_mean = csv_row['MEM_MEAN']
                            mem_std_dev = csv_row['MEM_STD_Deviation']

                            if (
                                row['%CPU'] <= cpu_mean + cpu_std_dev
                                and row['%MEM'] <= mem_mean + mem_std_dev
                            ):
                                processed_pids.add((pid, process_name))
                                is_flagged = False
                                break
                            else:
                                is_flagged = True

                        if is_flagged:
                            flags.append([
                                process_name,
                                pid,
                                row['%CPU'],
                                row['%MEM'],
                                f"Out of resources!",
                                f"http://127.0.0.1:5000/kill_process/{pid}"
                                
                            ])

                    else:
                        flags.append([
                            process_name,
                            pid,
                            row['%CPU'],
                            row['%MEM'],
                            "Unknown process",
                            f"http://127.0.0.1:5000/kill_process/{pid}"
                        ])

                # Create a dataframe with flagged processes
                flags_df = pd.DataFrame(flags, columns=[
                    'Process Name', 'PID', '%CPU', '%MEM', 'Flag Reason', 'Kill URL'
                ]).drop_duplicates()

                # st.write("Flagged Processes:")
                # st.write(flags_df)
                st.dataframe(
                    flags_df,
                    column_config={
                        "Process Name": "App name",
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
                        "Kill URL": st.column_config.LinkColumn("Kill URL")
                    },
                    hide_index=True,
                )

                

                flags_df.to_csv("flagged_processes.csv", index=False)


            else:
                st.write("No process data available.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

