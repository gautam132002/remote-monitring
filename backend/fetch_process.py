import psutil
import firebase_admin
from firebase_admin import credentials, db
import time

cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://remotemoniter-default-rtdb.firebaseio.com/'
})


def get_process_data():
    process_data = {}
    for process in psutil.process_iter(['name', 'username', 'pid', 'cpu_percent', 'memory_percent', 'memory_info', 'terminal', 'status', 'create_time', 'cpu_times', 'cmdline']):
        process_data[process.info['pid']] = {
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
        }
    return process_data

def update_firebase(data):
    ref = db.reference('/process') 
    ref.set(data)


def print_process_count():
    ref = db.reference('/process')
    process_data = ref.get()
    if process_data:
        print(f"no of process in bd : {len(process_data)}")
    else:
        print("no process present")

while True:
    try:
        process_data = get_process_data()
        update_firebase(process_data)
        print_process_count()
        time.sleep(1) 
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")