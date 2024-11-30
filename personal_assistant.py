import csv, os, json
import pandas as pd
from datetime import datetime

class MainManager:
    def __init__(self, path):
        if os.path.exists(path):
            with open(path) as f:
                self.data = json.load(f)
        else:
            self.data = []

    def save_file(self, kind_file, path):
        """ Экспорт файла """

        if kind_file == 'json':
            with open(path, 'w') as f:
                json.dump(self.data, f)
        else:
            df = pd.DataFrame(self.data)
            df.to_csv(path)

    def load_file(self, kind_file, path):
        """ Импорт файла """
        if kind_file == 'json':
            with open(path) as f:
                self.data = json.load(f)
        else:
            df = pd.read_csv(path)
            self.data = df.to_csv()

    def find_data(self, key_dict, key_result):
        """ Поиск данных в хранилище по ключу """
        try:
            data_res = [i for i in self.data if i[key_dict] == key_result]
            data_res = data_res
            return data_res
        except IndexError:
            raise ValueError(f'Ничего не удалось найти по указанному параметру {key_dict}.')

    def delete_data(self, kind_data, key_dict, key_result):
        """ Удаление данных по ключу """
        data_res = self.find_data(key_dict, key_result)
        index_list = [self.data.index(data) for data in data_res]

        for i in index_list:
            self.data.pop(i)

        # Сохранение
        path = os.path.join('data', f'{kind_data}.json')
        with open(path, 'w') as f:
            json.dump(self.data, f)


class Note:
    def __init__(self):
        self.path = os.path.join('data', 'notes.json')
        self.manager = MainManager(self.path)

    def create_note(self, title, content=None):
        """ Создание заметки """
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # дата создания заметки

        # Установка id
        if len(self.manager.data) == 0:
            id_note = 1
        else:
            id_note = self.manager.data[-1]['id'] + 1

        # Заполнение данных
        note = {
            'id': id_note,
            'title': str(title),
            'content': str(content),
            'timestamp': str(timestamp)
        }
        self.manager.data.append(note) # Сохранение в базе

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Заметка {id_note} успешно создана!\n')

    def show_list_notes(self):
        """ Вывод списка заметок """
        if len(self.manager.data) == 0:
            print('Список заметок пуст. Создайте новую заметку прямо сейчас!')
        else:
            print('Список заметок:')
            for note in self.manager.data:
                print(f'Заметка {note["id"]} — {note["title"]} — {note["timestamp"]}')
            print(' ') # просто отступ

    def print_note(self, id_note):
        """ Вывод определенной заметки """
        note_res = self.manager.find_data('id', id_note)[0]

        print(f'Заметка {id_note}')
        print(f"\"{note_res['title']}\"")
        print(note_res['content'])
        print('Дата обновления:', note_res['timestamp'])

    def update_note(self, id_note, type_change, new_data):
        """ Обновление заметки """
        # Нахождение заметки
        note = self.manager.find_data('id', id_note)[0]

        # Обновление данных
        note[type_change] = new_data
        note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Заметка {id_note} успешно обновлена!\n')

    def delete_note(self, id_note):
        """ Удаление заметки """
        self.manager.delete_data('notes', 'id', id_note)
        print(f'Заметка {id_note} успешна удалена.\n')

    def export_notes(self, kind_file, path=None):
        """ Экспорт заметок """
        if path is None:
            path = self.path
        self.manager.save_file(kind_file, path)
        print(f'Заметки успешно сохранены по пути: {path} !\n')

    def import_notes(self, kind_file, path=None):
        """ Импорт заметок """
        if path is None:
            path = self.path
        self.manager.load_file(kind_file, path)
        print(f'Заметки успешно загружены из следующего файла: {path}\n')

class Task:
    def __init__(self):
        self.path = os.path.join('data', 'tasks.json')
        self.manager = MainManager(self.path)

    def create_task(self, title: str, priority: str, due_date: str, description=None, done=False):
        """ Создание задачи """
        # Проверка наличия ошибок в поле приоритет
        priority_list = ['высокий', 'средний', 'низкий']
        if priority.lower() not in priority_list:
            raise ValueError('Укажите один из следующих вариантов приоритета: высокий, средний, низкий')
        else:
            priority = priority.capitalize()

        # Проверка наличия ошибки в поле срока
        try:
            date_check = datetime.strptime(due_date, '%d-%m-%Y')
        except ValueError:
            raise ValueError('Формат даты указан неверно. Правильный: ДД-ММ-ГГГГ')

        # Установка id
        if len(self.manager.data) == 0:
            id_task = 1
        else:
            id_task = self.manager.data[-1]['id'] + 1

        # Создание таска
        task = {
            'id': id_task,
            'title': title,
            'description': description,
            'done': done,
            'priority': priority,
            'due_date': due_date
        }
        self.manager.data.append(task)

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Задача {id_task} успешно добавлена!\n')

    def show_list_tasks(self):
        """ Вывод списка задач """
        if self.manager.data:
            print('Список поставленных задач:')
            for i, task in enumerate(self.manager.data):
                print('Задача', task['id'])
                print(f'\"{task['title']}\"')
                print('Срок:' , task['due_date'])
                if i < len(self.manager.data) - 1:
                    print('===============================')
            print('\n')
        else:
            print('Список задач пуст.\n')

    def mark_done(self, id_task):
        """ Отметка выполнения задачи """
        task = self.manager.find_data('id', id_task)[0]
        task['done'] = True

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Задача {id_task} успешно отмечена как выполненная!\n')

    def update_task(self, id_task, kind_change, new_data):
        """ Обновление данных задачи """
        task = self.manager.find_data('id', id_task)[0]
        task[kind_change] = new_data

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Задача {id_task} успешно обновлена!\n')

    def delete_task(self, id_task):
        """ Удаление задачи """
        self.manager.delete_data('tasks', 'id', id_task)

        print(f'Задача {id_task} успешно удалена!\n')

    def import_tasks(self, kind_file, path=None):
        """ Импорт задач """
        if path is None:
            path = self.path

        self.manager.load_file(kind_file, path)
        print(f'Задачи успешно загружены из следующего файла: {path}\n')

    def export_tasks(self, kind_file, path=None):
        """ Экспорт задач """
        if path is None:
            path = self.path

        self.manager.save_file(kind_file, path)
        print(f'Задачи успешно сохранены по следующем пути: {path}\n')



# Надо переделать импорт и сохранение, чтоб по умолчанию сохранял в json

