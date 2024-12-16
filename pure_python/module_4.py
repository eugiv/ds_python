DOCUMENTS = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
]

DIRECTORIES = {"1": ["2207 876234", "11-2"], "2": ["10006"], "3": []}


def shelve_search(shelves: dict, document_number: str):
    return "".join([key for key, value in shelves.items() if document_number in value])


def documents_search(documents: list, document_number: str):
    return [document for document in documents if document_number in document.values()]


def shelves_order(shelves: dict):
    return ", ".join([shelve for shelve in shelves])


def command_document_owner(document_number: str):
    document = documents_search(DOCUMENTS, document_number)
    if document:
        document_owner = document[0]["name"]
        print(f"\nВладелец документа: {document_owner}")
    else:
        print("\nДокумент не найден в базе")


def command_document_shelve_location(document_number: str):
    shelve = shelve_search(DIRECTORIES, document_number)
    if shelve:
        print(f"\nДокумент хранится на полке: {shelve}")
    else:
        print("\nДокумент не найден в базе")


def command_full_data_info():
    for document in DOCUMENTS:
        full_info = {
            "№: ": list(document.values())[1],
            "тип: ": list(document.values())[0],
            "владелец: ": list(document.values())[2],
            "полка хранения: ": shelve_search(DIRECTORIES, list(document.values())[1]),
        }
        print("; ".join(f"{key}{value}" for key, value in full_info.items()))


def command_shelve_add(shelve_number: str):
    if shelve_number.isdigit():
        if shelve_number not in DIRECTORIES:
            DIRECTORIES[shelve_number] = []
            print(
                f"Полка добавлена. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
            )
        else:
            print(
                f"Такая полка уже существует. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
            )
    else:
        print("Номер полки должен быть целым числом")


def command_shelve_remove(shelve_number: str):
    if shelve_number in DIRECTORIES and DIRECTORIES[shelve_number] == []:
        del DIRECTORIES[shelve_number]
        print(f"Полка удалена. Текущий перечень полок: {shelves_order(DIRECTORIES)}")

    elif DIRECTORIES.get(shelve_number):
        print(
            f"На полке есть документы, удалите их перед удалением полки. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
        )

    else:
        print(
            f"Такой полки не существует. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
        )


def command_document_data_add(
    document_number: str, document_type: str, document_owner: str, shelve_number: str
):
    if shelve_number in DIRECTORIES:
        DOCUMENTS.append(
            {"type": document_type, "number": document_number, "name": document_owner}
        )
        DIRECTORIES[shelve_number].append(document_number)
        print(
            f"\nДокумент добавлен. Текущий список документов: {command_full_data_info()}"
        )
    else:
        print(
            "\nТакой полки не существует. Добавьте полку командой as.\n"
            f"Текущий список документов: {command_full_data_info()}"
        )


def command_document_remove(document_number: str):
    document_to_remove = documents_search(DOCUMENTS, document_number)
    if document_to_remove:
        DOCUMENTS.remove(document_to_remove[0])
        print(
            "\nДокумент удалён.\n"
            f"Текущий список документов: {command_full_data_info()}"
        )
    else:
        print(
            "Документ не найден в базе.\n"
            f"Текущий список документов: {command_full_data_info()}"
        )


def command_document_transfer(document_number: str, new_shelve_number: str):
    document_exists = documents_search(DOCUMENTS, document_number)

    if new_shelve_number in DIRECTORIES and document_exists:
        old_shelve_number = shelve_search(DIRECTORIES, document_number)
        DIRECTORIES[old_shelve_number].remove(document_number)
        DIRECTORIES[new_shelve_number].append(document_number)
        print(
            "\nДокумент перемещён."
            f"Текущий список документов: {command_full_data_info()}"
        )
    elif new_shelve_number not in DIRECTORIES:
        print(f"Такой полки не существует: {shelves_order(DIRECTORIES)}")
    else:
        print(
            "\nДокумент не найден в базе."
            f"Текущий список документов: {command_full_data_info()}"
        )


def main():
    while True:
        command = input("\nВведите команду (p, s, l, ads, ds, ad, d, m, q): ")
        if command == "p":
            command_document_owner(input("Введите номер документа: "))
        elif command == "s":
            command_document_shelve_location(input("Введите номер документа: "))
        elif command == "l":
            command_full_data_info()
        elif command == "ads":
            command_shelve_add(input("Введите номер полки: "))
        elif command == "ds":
            command_shelve_remove(input("Введите номер полки: "))
        elif command == "ad":
            command_document_data_add(
                input("Введите номер документа: "),
                input("Введите тип документа: "),
                input("Введите владельца документа: "),
                input("Введите полку для хранения: "),
            )
        elif command == "d":
            command_document_remove(input("Введите номер документа: "))
        elif command == "m":
            command_document_transfer(
                input("Введите номер документа: "), input("Введите номер полки: ")
            )
        elif command == "q":
            print("сессия окончена, пока")
            break
        else:
            print("Неизвестная команда. Пожалуйста, попробуйте снова.")


main()


# СТАРОЕ РЕШЕНИЕ, ОСТАВИЛ ДЛЯ СЕБЯ
# def data_search(cmd: str):
#     select_cmd = {"doc": "p", "shelve": "s", "quit": "q"}
#     full_cmd = {
#         "full": "/",
#     }
#     action_cmd = {"add_shelve": "ads", "remove_shelve": "ds"}
#
#     while True:
#         if (
#             cmd not in select_cmd.values()
#             and cmd not in full_cmd.values()
#             and cmd not in action_cmd.values()
#         ):
#             cmd = input("Выбери команду 'p', 's', '/', 'ads', 'ds' или 'q': ")
#
#         elif cmd == select_cmd["quit"]:
#             print("сессия окончена, пока")
#             break
#
#         else:
#             shelve = lambda param: "".join(
#                 [k for k, v in DIRECTORIES.items() if param in v]
#             )
#
#             if cmd in select_cmd.values():
#                 doc_num = input("Введите номер документа: ")
#                 doc = [x for x in DOCUMENTS if doc_num in x.values()]
#
#                 if cmd == select_cmd["doc"]:
#                     if doc:
#                         doc_owner = doc[0]["name"]
#                         print(f"\nВладелец документа: {doc_owner}")
#                         return doc_owner
#
#                 elif cmd == select_cmd["shelve"]:
#                     if shelve(doc_num):
#                         print(f"\nДокумент хранится на полке: {shelve(doc_num)}")
#                         return shelve(doc_num)
#
#                 return print("\nДокумент не найден в базе")
#
#             if cmd in full_cmd.values():
#                 if cmd == full_cmd["full"]:
#                     cnt = 0
#                     for i in DOCUMENTS:
#                         res = {
#                             "№: ": list(i.values())[1],
#                             "тип: ": list(i.values())[0],
#                             "владелец: ": list(i.values())[2],
#                             "полка хранения: ": shelve(list(i.values())[1]),
#                         }
#                         res = "; ".join(f"{key}{value}" for key, value in res.items())
#                         print(res)
#                         cnt += 1
#                         if cnt == len(DOCUMENTS):
#                             return
#
#             if cmd in action_cmd.values():
#                 shelve_num = str(int(input("Введите номер полки: ")))
#                 shelves_order = lambda dirs: ",".join([x for x in dirs])
#
#                 if cmd == action_cmd["add_shelve"]:
#                     if shelve_num not in DIRECTORIES:
#                         DIRECTORIES[shelve_num] = []
#                         return print(
#                             f"Полка добавлена. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
#                         )
#                     else:
#                         return print(
#                             f"Такая полка уже существует. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
#                         )
#
#                 if cmd == action_cmd["remove_shelve"]:
#                     if shelve_num in DIRECTORIES and DIRECTORIES[shelve_num] == []:
#                         del DIRECTORIES[shelve_num]
#                         return print(
#                             f"Полка удалена. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
#                         )
#
#                     elif DIRECTORIES.get("shelve_num"):
#                         return print(
#                             f"На полке есть документа, удалите их перед удалением полки. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
#                         )
#
#                     else:
#                         return print(
#                             f"Такой полки не существует. Текущий перечень полок: {shelves_order(DIRECTORIES)}"
#                         )
#
#
# # data_search(input("Введите команду: "))
