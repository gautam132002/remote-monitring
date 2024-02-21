import csv
import psutil
import time

import updatedb

output_file = "system_mntr.csv"
update_interval = 2

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_free = 100 - cpu_usage
    cpu_used = cpu_usage

    memory_info = psutil.virtual_memory()
    memory_usage_percentage = memory_info.percent
    memory_used_mb = memory_info.used / (1024 ** 2)
    memory_free_mb = memory_info.available / (1024 ** 2)

    storage_info = psutil.disk_usage('/')
    storage_usage_percentage = storage_info.percent
    storage_used_gb = storage_info.used / (1024 ** 3)
    storage_free_gb = storage_info.free / (1024 ** 3)

    network_info = psutil.net_io_counters()
    network_upload_mb = network_info.bytes_sent / (1024 ** 2)
    network_download_mb = network_info.bytes_recv / (1024 ** 2)

    updatedb.save_server_data(cpu_usage, cpu_free, cpu_used,
            memory_usage_percentage, memory_used_mb, memory_free_mb,
            storage_usage_percentage, storage_free_gb, storage_used_gb,
            network_upload_mb, network_download_mb)

    return [cpu_usage, cpu_free, cpu_used,
            memory_usage_percentage, memory_used_mb, memory_free_mb,
            storage_usage_percentage, storage_free_gb, storage_used_gb,
            network_upload_mb, network_download_mb]


def write_to_csv(data):
    with open(output_file, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        header = ["CPU Usage Percentage", "CPU Free", "CPU Used",
                  "Memory Usage Percentage", "Memory Used (MB)", "Memory Free (MB)",
                  "Storage Usage Percentage", "Storage Free (GB)", "Storage Used (GB)",
                  "Network Upload (MB/s)", "Network Download (MB/s)"]

        csv_writer.writerow(header)
        csv_writer.writerow(data)

if __name__ == "__main__":
    while True:
        system_info = get_system_info()
        write_to_csv(system_info)
        print(f"Updated CSV at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        # time.sleep(update_interval)
