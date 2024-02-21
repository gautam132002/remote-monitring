import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://remotemoniter-default-rtdb.firebaseio.com/'
})

def get_all_entries():
    try:
        root_ref = db.reference()
        metrics_ref = root_ref.child('metrics')
        all_entries = metrics_ref.get()

        if all_entries:
            entries_list = list(all_entries.values())
            # print(entries_list)
            return entries_list
        else:
            return None
    except Exception as e:
        return None


# get_all_entries_in_original_order()
