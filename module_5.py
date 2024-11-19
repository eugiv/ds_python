import os
import json

dir_ = "ds_python_file_read"

for file in os.listdir(dir_):

    if file.endswith(".txt"):
        file_path = os.path.join(dir_, file)

        with open(file_path, 'r', encoding='utf-8') as f_txt:
            purchases_log = f_txt.readlines()

        purchases = {}
        for record in purchases_log:
            record = record.strip()
            record_json = json.loads(record)
            final_record = {record_json["user_id"]: record_json["category"]}
            purchases.update(final_record)
        print(purchases)
