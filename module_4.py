

DOCUMENTS = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

DIRECTORIES = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def docs_search(cmd: str):
    valid_comm = {'doc': 'p', 'shelf': 's', 'quit': 'q'}
    while True:
        if not cmd:
            cmd = input("Выбери команду 'p', 's', или 'q': ")

        elif cmd == valid_comm['quit']:
            print('сессия окончена, пока')
            break

        else:
            doc_num = input('Введите номер документа: ')
            if cmd == valid_comm['doc']:
                doc = [x for x in DOCUMENTS if doc_num in x.values()]
                if doc:
                    doc_owner = doc[0]['name']
                    print(f"\nВладелец документа: {doc_owner}")
                    return doc_owner

            elif cmd == valid_comm['shelf']:
                shelf = ''.join([k for k, v in DIRECTORIES.items() if doc_num in v])
                if shelf:
                    print(f"\nДокумент хранится на полке: {shelf}")
                    return shelf

            return print("\nДокумент не найден в базе")


docs_search(input("Введите команду: "))

