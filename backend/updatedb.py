import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://remotemoniter-default-rtdb.firebaseio.com/'
})

def save_server_data(cpu_usage_percent, cpu_free, cpu_used, memory_usage_percent, memory_used_mb,
                     memory_free_mb, storage_usage_percent, storage_free_gb, storage_used_gb,
                     network_upload_mb_s, network_download_mb_s):
    try:
        root_ref = db.reference()
        metrics_ref = root_ref.child('metrics')

        data = {
            "CPU_Usage_Percentage": cpu_usage_percent,
            "CPU_Free": cpu_free,
            "CPU_Used": cpu_used,
            "Memory_Usage_Percentage": memory_usage_percent,
            "Memory_Used_MB": memory_used_mb,
            "Memory_Free_MB": memory_free_mb,
            "Storage_Usage_Percentage": storage_usage_percent,
            "Storage_Free_GB": storage_free_gb,
            "Storage_Used_GB": storage_used_gb,
            "Network_Upload_MB_s": network_upload_mb_s,
            "Network_Download_MB_s": network_download_mb_s
        }
        metrics_ref.push(data)

        print("Data successfully saved to Firebase Realtime Database.")
    except Exception as e:
        print("Error saving data to Firebase Realtime Database:", e)

# cpu_usage_percent = 20.5
# cpu_free = 80.0
# cpu_used = 19.5
# memory_usage_percent = 30.0
# memory_used_mb = 2048
# memory_free_mb = 4096
# storage_usage_percent = 50.0
# storage_free_gb = 100.0
# storage_used_gb = 100.0
# network_upload_mb_s = 5.0
# network_download_mb_s = 10.0
# save_server_data(cpu_usage_percent, cpu_free, cpu_used, memory_usage_percent,
#                  memory_used_mb, memory_free_mb, storage_usage_percent,
#                  storage_free_gb, storage_used_gb, network_upload_mb_s, network_download_mb_s)
