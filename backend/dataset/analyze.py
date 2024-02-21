import pandas as pd
import statistics


# csv_file_path = "dataset.csv"


def stats_analysis(csv_file_path):

    data_from_csv = pd.read_csv(csv_file_path)

    # Step 1: Use specified labels
    selected_labels = ['Process Name', 'USER', 'PID', '%CPU', '%MEM', 'STAT']
    data_from_csv = data_from_csv[selected_labels]

    # Step 2: Group by PID
    grouped_data = data_from_csv.groupby('PID')


    # Step 3 and 4: Calculate mean and std deviation for each group
    result_data = []
    for pid, group in grouped_data:
        try:
            cpu_mean = statistics.mean(group['%CPU'])
            cpu_std_deviation = statistics.stdev(group['%CPU'])
            mem_mean = statistics.mean(group['%MEM'])
            mem_std_deviation = statistics.stdev(group['%MEM'])


            result_data.append({
                'Process Name': group['Process Name'].iloc[0],
                'USER': group['USER'].iloc[0],
                'PID': pid,
                'CPU_MEAN': cpu_mean,
                'CPU_STD_Deviation': cpu_std_deviation,
                'MEM_MEAN': mem_mean,
                'MEM_STD_Deviation': mem_std_deviation,
            })
        except:

            print(pid)
            print(group)
            print("==================================================")

    # Step 5: Write result to a new CSV file
    result_csv_file_path = "result_statistics.csv"
    result_df = pd.DataFrame(result_data)
    result_df.to_csv(result_csv_file_path, index=False)

    print("Analysis completed. Results saved in result_statistics.csv")

    return True
