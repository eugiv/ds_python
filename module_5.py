import os
import json

dir_ = "ds_python_file_read"

for file in os.listdir(dir_):

    file_path_txt = os.path.join(dir_, "purchase_log.txt")
    file_path_csv = os.path.join(dir_, "visit_log.csv")

    purchases = {}
    with open(file_path_txt, "r", encoding="utf-8") as f_txt:
        purchases_log = f_txt.readlines()

    for record in purchases_log:
        record = record.strip()
        record_json = json.loads(record)
        final_record = {record_json["user_id"]: record_json["category"]}
        purchases.update(final_record)

    with open(file_path_csv, "r", encoding="utf-8") as f_csv:
        with open("funnel.csv", "w", encoding="utf-8") as f_write:
            for line in f_csv:
                line = line.strip().split(",")
                if line[0] in purchases.keys() and line[1] != "None":
                    line.append(purchases[line[0]])
                    f_write.write(", ".join(line) + "\n")
