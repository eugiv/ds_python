DOCUMENTS = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
]

DIRECTORIES = {"1": ["2207 876234", "11-2"], "2": ["10006"], "3": []}


def data_search(cmd: str):
    select_cmd = {"doc": "p", "shelve": "s", "quit": "q"}
    full_cmd = {
        "full": "/",
    }

    while True:
        if not cmd:
            cmd = input("Выбери команду 'p', 's', '/' или 'q': ")

        elif cmd == select_cmd["quit"]:
            print("сессия окончена, пока")
            break

        else:
            shelve = lambda param: "".join(
                [k for k, v in DIRECTORIES.items() if param in v]
            )

            if cmd in select_cmd.values():
                doc_num = input("Введите номер документа: ")
                doc = [x for x in DOCUMENTS if doc_num in x.values()]

                if cmd == select_cmd["doc"]:
                    if doc:
                        doc_owner = doc[0]["name"]
                        print(f"\nВладелец документа: {doc_owner}")
                        return doc_owner

                elif cmd == select_cmd["shelve"]:
                    if shelve(doc_num):
                        print(f"\nДокумент хранится на полке: {shelve(doc_num)}")
                        return shelve(doc_num)

                return print("\nДокумент не найден в базе")

            if cmd in full_cmd.values():
                if cmd == full_cmd["full"]:

                    cnt = 0
                    for i in DOCUMENTS:
                        res = {
                            "№: ": list(i.values())[1],
                            "тип: ": list(i.values())[0],
                            "владелец: ": list(i.values())[2],
                            "полка хранения: ": shelve(list(i.values())[1]),
                        }
                        res = "; ".join(f"{key}{value}" for key, value in res.items())
                        print(res)
                        cnt += 1
                        if cnt == len(DOCUMENTS):
                            return


data_search(input("Введите команду: "))