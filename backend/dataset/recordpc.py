import csv
import psutil
import time
import statistics
from analyze import stats_analysis

# File to store data
csv_file_path = "dataset.csv"

def get_process_data():
    process_data = []
    for process in psutil.process_iter(['name', 'username', 'pid', 'cpu_percent', 'memory_percent', 'memory_info', 'terminal', 'status', 'create_time', 'cpu_times', 'cmdline']):
        process_data.append({
            "Process Name": process.info['name'],
            "USER": process.info['username'],
            "PID": process.info['pid'],
            "%CPU": process.info['cpu_percent'],
            "%MEM": process.info['memory_percent'],
            "VSZ": process.info['memory_info'].vms,
            "RSS": process.info['memory_info'].rss,
            "TTY": process.info['terminal'],
            "STAT": process.info['status'],
            "START": process.info['create_time'],
            "TIME": process.info['cpu_times'].user + process.info['cpu_times'].system,
            "COMMAND": ' '.join(process.info['cmdline']) if process.info['cmdline'] else ''
        })
    return process_data

def record_data_to_csv(data):
    with open(csv_file_path, 'a', newline='') as csv_file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerows(data)



if __name__ == "__main__":
    data_collection_time = 10
    start_time = time.time()
    while (time.time() - start_time) < data_collection_time:
        print(time.time() - start_time)
        try:
            process_data = get_process_data()
            record_data_to_csv(process_data)
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    if stats_analysis(csv_file_path):
        print("================++done++==========================")
    else:
        print("================++fail++==========================")

