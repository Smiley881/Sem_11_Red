import csv, os, json
import pandas as pd
from datetime import datetime, timedelta

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

class Contact:
    def __init__(self):
        self.path = os.path.join('data', 'contacts.json')
        self.manager = MainManager(self.path)

    def create_contact(self, name, phone=None, email=None):
        """ Создание записи """
        # Установка id
        if len(self.manager.data) == 0:
            id_contact = 1
        else:
            id_contact = self.manager.data[-1]['id'] + 1

        contact = {
            'id': id_contact,
            'name': name,
            'phone': phone,
            'email': email
        }

        # Сохранение
        self.manager.data.append(contact)
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)
        print(f'Контакт {name} успешно создан!\n')

    def print_contact(self, key_dict, key_result):
        """ Вывод данных контакта """
        contact = self.manager.find_data(key_dict, key_result)[0]
        print({contact['name']})
        print('Телефон —', contact['phone'])
        print('Email —', contact['email'])

    def update_contact(self, key_dict, key_result, type_change, new_data):
        """ Обновление данных контакта """
        contact = self.manager.find_data(key_dict, key_result)[0]
        contact[type_change] = new_data

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)
        print(f'Контакт {key_result} успешно изменен!\n')

    def delete_contact(self, key_dict, key_result):
        """ Удаление контакта """
        self.manager.delete_data('contacts', key_dict, key_result)

        print(f'Контакт {key_result} успешно удалён!\n')

    def import_contacts(self, kind_file, path=None):
        """ Импорт данных контактов """
        if path is None:
            path = self.path
        self.manager.load_file(kind_file, path)
        print(f'Контакты успешно загружены из следующего файла: {path}\n')

    def export_contacts(self, kind_file, path=None):
        """ Экспорт данных контактов """
        if path is None:
            path = self.path
        self.manager.load_file(kind_file, path)
        print(f'Контакты успешно сохранены по следующему пути: {path}\n')

class FinanceRecord:
    def __init__(self):
        self.path = os.path.join('data', 'finance.json')
        self.manager = MainManager(self.path)

    def create_record(self, amount: float, category: str, date: str, description=None):
        """ Создание записи о доходе/расходе """
        # Проверка наличия ошибки в поле даты
        try:
            date_check = datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            raise ValueError('Формат даты указан неверно. Правильный: ДД-ММ-ГГГГ')

        # Установка id
        if len(self.manager.data) == 0:
            id_record = 1
        else:
            id_record = self.manager.data[-1]['id'] + 1

        record = {
            'id': id_record,
            'amount': amount,
            'category': category,
            'date': date,
            'description': description
        }

        self.manager.data.append(record)
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Запись {id_record} за {date} успешно создана!\n')

    def show_list_records(self, key_dict, key_result):
        """ Вывод списка записей """
        records_list = self.manager.find_data(key_dict, key_result)
        if records_list:
            revenue_list = [i for i in records_list if i['amount'] > 0]
            cost_list = [i for i in records_list if i['amount'] < 0]
            print('Результаты поиска:')
            print(key_result)
            print('Доходы:')
            if revenue_list:
                for revenue in revenue_list:
                    print(f'{revenue['date']} — {revenue['category']} — {revenue['amount']}')
            else:
                print('Данные отсутствуют')
            if cost_list:
                for cost in cost_list:
                    print(f'{cost['date']} — {cost['category']} — {cost['amount']}')
            else:
                print('Данные отсутствуют')
            print(' ') # просто отступ
        else:
            print('Данные отсутствуют\n')

    def create_report(self, start_date, end_date):
        """ Генерация отчёта """
        # Проверка формата даты
        try:
            start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
            end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError('Формат даты указан неверно. Правильный формат: ДД-ММ-ГГГГ')

        dates_list = [start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)]

        result = []
        for date in dates_list:
            records_list = self.manager.find_data('date', date)
            result.extend(records_list)

        # Сохранение данных
        path = os.path.join('data', f'report_{start_date}_{end_date}.csv')
        self.manager.save_file('csv', path)

        # Ревизия
        sum_rev = sum([i for i in result if i['amount'] > 0])
        sum_cost = sum([i for i in result if i['amount'] < 0])
        balance = sum_rev + sum_cost

        print(f'Финансовый отчет за период с {start_date} по {end_date}:')
        print('Общий доход:', sum_rev)
        print('Общие расходы:', sum_cost)
        print('Баланс:', balance)
        print('Подробная информация сохранена в файле', path)

    def delete_record(self, key_dict, key_result):
        self.manager.delete_data('finance', key_dict, key_result)

        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print('Данные успешно удалены!')

    def import_records(self, path=None):
        if path is None:
            path = self.path
        self.manager.load_file('csv', path)
        print(f'Финансовые записи успешно загружены из следующего файла: {path}\n')

    def export_records(self, path=None):
        if path is None:
            path = self.path
        self.manager.save_file('csv', path)
        print(f'Финансовые записи успешно сохранены по следующему пути: {path}\n')




