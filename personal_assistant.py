import csv, os, json
import pandas as pd
from datetime import datetime

class MainManager:
    def __init__(self):
        notes = []
        task_data = []
        phonebook_data = []
        finance_data = []

        self.data = {'notes': notes}

    def save_file(self, kind_data, kind_file, path=None):
        """ Экспорт файла """
        if path is None:
            path = os.path.join('data', f'{kind_data}.{kind_file}')

        if kind_file == 'json':
            with open(path, 'w') as f:
                json.dump(self.data[kind_data], f)
        elif kind_file == 'csv':
            df = pd.DataFrame(self.data[kind_data])
            df.to_csv(path)
        else:
            raise Exception('Недоступный формат вывода файла. Выберите пожалуйста json или csv.')

    def load_file(self, kind_data, path=None):
        """ Импорт файла """
        if path is None:
            path = os.path.join('data', f'{kind_data}.json')
        with open(path) as f:
            self.data[kind_data] = json.load(f)

    def find_data(self, kind_data, key_dict, key_result):
        """ Поиск данных в хранилище по ключу """
        try:
            data_res = [i for i in self.data[kind_data] if i[key_dict] == key_result]
            data_res = data_res
            return data_res
        except IndexError:
            raise ValueError(f'Ничего не удалось найти по указанному параметру {key_dict}.')

    def delete_data(self, kind_data, key_dict, key_result):
        """ Удаление данных по ключу """
        data_res = self.find_data(kind_data, key_dict, key_result)
        index_list = [self.data[kind_data].index(data) for data in data_res]

        for i in index_list:
            self.data[kind_data].pop(i)

        self.save_file(kind_data, self.data[kind_data])


class Note:
    def __init__(self):
        self.manager = MainManager()
        self.log = []

    def create_note(self, title, content=None):
        """ Создание заметки """
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # дата создания заметки

        # Установка id
        if len(self.manager.data['notes']) == 0:
            id_note = 1
        else:
            id_note = self.manager.data['notes'][-1]['id'] + 1

        # Заполнение данных
        note = {
            'id': id_note,
            'title': str(title),
            'content': str(content),
            'timestamp': str(timestamp)
        }
        self.manager.data['notes'].append(note) # Сохранение в базе

    def show_list_note(self):
        """ Вывод списка """
        if len(self.manager.data['notes']) == 0:
            print('Список заметок пуст. Создайте новую заметку прямо сейчас!')
        else:
            print('Список заметок:')
            for note in self.manager.data['notes']:
                print(f'Заметка {note["id"]} — {note["title"]} — {note["timestamp"]}')
            print(' ') # просто отступ

    def print_note(self, id_note):
        """ Вывод определенной заметки """
        note_res = self.manager.find_data('notes', 'id', id_note)[0]

        print(f'Заметка {id_note}')
        print(f"\"{note_res['title']}\"")
        print(note_res['content'])
        print('Дата обновления:', note_res['timestamp'])

    def update_note(self, id_note, type_change, new_data):
        """ Обновление заметки """
        # Нахождение заметки
        note = self.manager.find_data('notes', 'id', id_note)[0]

        # Обновление данных
        note[type_change] = new_data
        note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def delete_note(self, id_note):
        """ Удаление заметки """
        self.manager.delete_data('notes', 'id', id_note)
        print(f'Заметка {id_note} успешна удалена.\n')

    def export_notes(self, kind_file, path=None):
        """ Экспорт заметок """
        self.manager.save_file('notes', kind_file, path)
        print('Заметки успешно сохранены!')

    def import_notes(self, path=None):
        """ Импорт заметок """
        self.manager.load_file('notes', path)
        print('Заметки успешно загружены!')

