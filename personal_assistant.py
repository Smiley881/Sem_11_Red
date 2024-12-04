import os, json

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

    def load_file(self, kind_file, path_import, path_home):
        """ Импорт файла """
        if kind_file == 'json':
            with open(path_import) as f:
                self.data = json.load(f)
        else:
            df = pd.read_csv(path_import)
            self.data = df.to_csv()

        self.save_file('json', path_home)

    def find_data(self, key_dict, key_result):
        """ Поиск данных в хранилище по ключу """
        data_res = [i for i in self.data if i[key_dict] == key_result]
        return data_res

    def delete_data(self, kind_data, key_dict, key_result):
        """ Удаление данных по ключу """
        data_res = self.find_data(key_dict, key_result)
        index_list = [self.data.index(data) for data in data_res]
        test = data_res[0] # для проверки на нахождение

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

    def create_note(self, title, content):
        """ Создание заметки """
        if title in [i['title'] for i in self.manager.data]:
            print('Заметка с таким названием уже существует. Пожалуйста, придумайте новое название.\n')
            return
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # дата создания заметки
        if content == '':
            content = None

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
            print('Список заметок пуст. Создайте новую заметку прямо сейчас!\n')
        else:
            print('Список заметок:')
            for note in self.manager.data:
                print(f'Заметка {note["id"]} — {note["title"]} — {note["timestamp"]}')
            print(' ') # просто отступ

    def print_note(self, title):
        """ Вывод определенной заметки """
        try:
            note_res = self.manager.find_data('title', title)[0]
        except IndexError:
            print('Заметка не была найдена. Проверьте корректность введённого названия.\n')
            return
        else:
            print(f'Заметка {note_res['id']}')
            print(f"\"{note_res['title']}\"")
            print(note_res['content'])
            print('Дата обновления:', note_res['timestamp'])
            print(' ') # просто отступ

    def update_note(self, title, type_change, new_data):
        """ Обновление заметки """
        # Нахождение заметки
        try:
            note = self.manager.find_data('title', title)[0]
        except IndexError:
            print('Заметка не была найдена. Проверьте корректность введённого названия.\n')
            return
        else:
            # Обновление данных
            note[type_change] = new_data
            note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            # Сохранение
            with open(self.path, 'w') as f:
                json.dump(self.manager.data, f)

            print(f'Заметка {title} успешно обновлена!\n')

    def delete_note(self, title):
        """ Удаление заметки """
        try:
            self.manager.delete_data('notes', 'title', title)
        except IndexError:
            print('Заметка не была найдена. Проверьте корректность введённого названия.\n')
            return
        else:
            print(f'Заметка {title} успешна удалена.\n')

    def export_notes(self, kind_file, path=None):
        """ Экспорт заметок """
        if path is None:
            path = self.path
        self.manager.save_file(kind_file, path)
        print(f'Заметки успешно сохранены по пути: {path} \n')

    def import_notes(self, kind_file, path_import, path_home=None):
        """ Импорт заметок """
        if path_home is None:
            path_home = self.path
        self.manager.load_file(kind_file, path_import, path_home)
        print(f'Заметки успешно загружены из следующего файла: {path_import}\n')

class Task:
    def __init__(self):
        self.path = os.path.join('data', 'tasks.json')
        self.manager = MainManager(self.path)

    def create_task(self, title: str, priority: str, due_date: str, description=None, done=False):
        """ Создание задачи """
        # Проверка уникальности названия
        if title in [i['title'] for i in self.manager.data]:
            print('Заметка с таким названием уже существует. Пожалуйста, придумайте новое название.\n')
            return
        if description == '':
            description = None

        # Проверка наличия ошибок в поле приоритет
        priority_list = ['высокий', 'средний', 'низкий']
        if priority.lower() not in priority_list:
            print('Укажите один из следующих вариантов приоритета: высокий, средний, низкий')
            return
        else:
            priority = priority.capitalize()

        # Установка id
        if len(self.manager.data) == 0:
            id_task = 1
        else:
            id_task = self.manager.data[-1]['id'] + 1

        # Проверка наличия ошибки в поле даты
        try:
            date_check = datetime.strptime(due_date, '%d-%m-%Y')
        except ValueError:
            print('Формат даты указан неверно. Правильный: ДД-ММ-ГГГГ')
            return

        # Создание таска
        task = {
            'id': id_task,
            'title': str(title),
            'description': str(description),
            'done': done,
            'priority': str(priority),
            'due_date': str(due_date)
        }
        self.manager.data.append(task)

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Задача {id_task} успешно добавлена!\n')

    def print_task(self, title):
        """ Вывод определенной заметки """
        try:
            task_res = self.manager.find_data('title', title)[0]
        except IndexError:
            print('Задача не была найдена. Проверьте корректность введённого названия.\n')
            return
        else:
            print(f'Задача {task_res['id']}')
            print(f"\"{task_res['title']}\"")
            print(task_res['description'])
            print('Приоритет:', task_res['priority'])
            print('Крайний срок:', task_res['due_date'])
            print(' ') # просто отступ

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

    def mark_done(self, title):
        """ Отметка выполнения задачи """
        task = self.manager.find_data('title', title)[0]
        task['done'] = True

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Задача \"{title}\" успешно отмечена как выполненная!\n')

    def update_task(self, title, kind_change, new_data):
        """ Обновление данных задачи """
        task = self.manager.find_data('title', title)[0]
        if kind_change == 'priority' and new_data.lower() not in ['высокий', 'средний', 'низкий']:
            print('Укажите один из следующих вариантов приоритета: высокий, средний, низкий')
            return
        elif kind_change == 'due_date':
            # Проверка наличия ошибки в поле даты
            try:
                date_check = datetime.strptime(new_data, '%d-%m-%Y')
            except ValueError:
                print('Формат даты указан неверно. Правильный: ДД-ММ-ГГГГ')
                return

        task[kind_change] = new_data

        # Сохранение
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Задача \"{title}\" успешно обновлена!\n')

    def delete_task(self, title):
        """ Удаление задачи """
        try:
            self.manager.delete_data('tasks', 'title', title)
        except IndexError:
            print('Задача не была найдена. Проверьте корректность введённого названия.\n')
            return
        else:
            print(f'Задача {title} успешна удалена.\n')

    def import_tasks(self, kind_file, path_import, path_home=None):
        """ Импорт задач """
        if path_home is None:
            path_home = self.path

        self.manager.load_file(kind_file, path_import, path_home)
        print(f'Задачи успешно загружены из следующего файла: {path_import}\n')

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

        if phone == '':
            phone = None
        if email == '':
            email = None

        contact = {
            'id': id_contact,
            'name': name,
            'phone': str(phone),
            'email': str(email)
        }

        # Сохранение
        self.manager.data.append(contact)
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)
        print(f'Контакт {name} успешно создан!\n')

    def print_contact(self, key_dict, key_result):
        """ Вывод данных контакта """
        try:
            contact = self.manager.find_data(key_dict, key_result)[0]
        except IndexError:
            print('Контакт не был найден. Проверьте корректность введённого названия.\n')
            return
        else:
            print('Телефон —', contact['phone'])
            print('Email —', contact['email'])
            print(' ')

    def update_contact(self, key_dict, key_result, type_change, new_data):
        """ Обновление данных контакта """
        try:
            contact = self.manager.find_data(key_dict, key_result)[0]
        except IndexError:
            print('Контакт не был найден. Проверьте корректность введённого названия.\n')
            return
        else:
            contact[type_change] = new_data

            # Сохранение
            with open(self.path, 'w') as f:
                json.dump(self.manager.data, f)
            print(f'Контакт {key_result} успешно изменен!\n')

    def delete_contact(self, key_dict, key_result):
        """ Удаление контакта """
        try:
            self.manager.delete_data('contacts', key_dict, key_result)
        except IndexError:
            print('Задача не была найдена. Проверьте корректность введённого названия.\n')
            return
        else:
            print(f'Контакт {key_result} успешно удалён.\n')

    def import_contacts(self, kind_file, path_import, path_home=None):
        """ Импорт данных контактов """
        if path_home is None:
            path_home = self.path
        self.manager.load_file(kind_file, path_import, path_home)
        print(f'Контакты успешно загружены из следующего файла: {path_import}\n')

    def export_contacts(self, kind_file, path=None):
        """ Экспорт данных контактов """
        if path is None:
            path = self.path
        self.manager.save_file(kind_file, path)
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
            print('Формат даты указан неверно. Правильный: ДД-ММ-ГГГГ')
            return

        # Установка id
        if len(self.manager.data) == 0:
            id_record = 1
        else:
            id_record = self.manager.data[-1]['id'] + 1

        # Исправление description
        if description == '':
            description = None

        record = {
            'id': id_record,
            'amount': amount,
            'category': str(category),
            'date': date,
            'description': str(description)
        }

        self.manager.data.append(record)
        with open(self.path, 'w') as f:
            json.dump(self.manager.data, f)

        print(f'Запись {id_record} за {date} успешно создана!\n')

    def show_list_records(self, key_dict, key_result):
        """ Вывод списка записей """
        if key_dict is None:
            records_list = self.manager.data
        else:
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

    def import_records(self, path_import, path_home=None):
        if path_home is None:
            path_home = self.path
        self.manager.load_file('csv', path_import, path_home)
        print(f'Финансовые записи успешно загружены из следующего файла: {path_import}\n')

    def export_records(self, path=None):
        if path is None:
            path = self.path
        self.manager.save_file('csv', path)
        print(f'Финансовые записи успешно сохранены по следующему пути: {path}\n')

class Calculator:
    def __init__(self):
        self.data = 0

    def operations(self, first_num, op, second_num):
        """ Операции """
        # Проверка операции
        try:
            if op == '+':
                self.data = float(first_num) + float(second_num)
                print(self.data)
            elif op == '-':
                self.data = float(first_num) - float(second_num)
                print(self.data)
            elif op == '/':
                self.data = float(first_num) / float(second_num)
                print(self.data)
            elif op == '*':
                self.data = float(first_num) * float(second_num)
            else:
                raise ValueError('Пожалуйста введите одно из действий: +, -, /, *')
        except ValueError:
            raise ValueError('Пожалуйста введите числа в корректном формате. Если хотите ввести дробное число, то пишите в виде 0.00')

    def clear_calc(self):
        self.data = 0

class Menu:
    def check_choice(self, console, end_choice):
        if console in [i for i in range(1, end_choice + 1)]:
            return console
        else:
            return 0

    def hello(self):
        print('Добро пожаловать в Персональный помощник!')
        print('Список возможных программ:')
        print('1. Управление заметками')
        print('2. Управление задачами')
        print('3. Управление контактами')
        print('4. Управление финансовыми записями')
        print('5. Калькулятор')
        print('6. Выход')

        console = int(input('Выберите действие: '))
        print(' ') # просто отступ
        return console

    def notes(self):
        note = Note()
        print('Список функций:')
        print('1. Создание новой заметки')
        print('2. Вывод списка заметок')
        print('3. Найти заметку по названию')
        print('4. Редактирование заметки')
        print('5. Удаление заметки')
        print('6. Импорт заметок')
        print('7. Экспорт заметок')
        print('8. Вернуться в главное меню')

        console = int(input('Выберите действие: '))
        while self.check_choice(console, 8) == 0:
            console = int(input('Пожалуйста введите число от 1 до 8: '))
        print(' ') # просто отступ

        if console == 1:
            print('СОЗДАНИЕ ЗАМЕТКИ')
            print('Название заметки:')
            title = input()
            print('Описание заметки:')
            print('P.s. Если вы не хотите добавлять описание, просто нажмите ENTER на клавиатуре.')
            content = input()

            note.create_note(title, content)
            return True

        elif console == 2:
            print('ВЫВОД СПИСКА ЗАМЕТОК')
            note.show_list_notes()
            return True

        elif console == 3:
            print('ПОИСК ЗАМЕТКИ')
            print('Название искомой заметки:')
            title = input()
            note.print_note(title)
            return True

        elif console == 4:
            print('РЕДАКТИРОВАНИЕ ЗАМЕТКИ')
            print('Название искомой заметки:')
            title = input()

            print('Выберите вариант данных для редактирования:')
            print('1. Название')
            print('2. Описание')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                type_change = 'title'
            else:
                type_change = 'content'

            print('Введите новое название/описание:')
            new_data = input()

            note.update_note(title, type_change, new_data)
            return True

        elif console == 5:
            print('УДАЛЕНИЕ ЗАМЕТКИ')
            print('Название искомой заметки:')
            title = input()

            note.delete_note(title)
            return True

        elif console == 6:
            print('ИМПОРТ ЗАМЕТОК')
            print('Выберите формат файла:')
            print('1. JSON')
            print('2. CSV')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                kind_file = 'json'
            else:
                kind_file = 'csv'

            print('Введите путь к файлу:')
            path_import = input()
            note.import_notes(kind_file, path_import, note.path)
            return True

        elif console == 7:
            print('ЭКСПОРТ ЗАМЕТОК')
            print('Выберите формат файла:')
            print('1. JSON')
            print('2. CSV')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                kind_file = 'json'
            else:
                kind_file = 'csv'
            print('Введите путь к файлу:')
            path = input()
            note.export_notes(kind_file, path)
            return True

        else:
            return False

    def tasks(self):
        task = Task()
        print('Список функций:')
        print('1. Добавление новой задачи')
        print('2. Вывод списка задач')
        print('3. Найти задачу по названию')
        print('4. Отметить задачу как выполненную')
        print('5. Редактирование задачи')
        print('6. Удаление задачи')
        print('7. Импорт задач')
        print('8. Экспорт задач')
        print('9. Вернуться в главное меню')

        console = int(input('Выберите действие: '))
        while self.check_choice(console, 9) == 0:
            console = int(input('Пожалуйста введите число от 1 до 9: '))
        print(' ')  # просто отступ

        if console == 1:
            print('ДОБАВЛЕНИЕ ЗАДАЧИ')
            print('Название задачи:')
            title = input()
            print('Описание заметки:')
            print('P.s. Если вы не хотите добавлять описание, просто нажмите ENTER на клавиатуре.')
            description = input()
            print('Приоритет:')
            print('P.s. Возможные варианты: высокий, средний, низкий')
            priority = input()
            print('Срок выполнения:')
            print('P.s. Допустимый формат: ДД-ММ-ГГГГ')
            due_date = input()

            task.create_task(title, priority, due_date, description)
            return True

        elif console == 2:
            print('ВЫВОД СПИСКА ЗАДАЧ')
            task.show_list_tasks()
            return True

        elif console == 3:
            print('ПОИСК ЗАДАЧИ')
            print('Название искомой задачи:')
            title = input()
            task.print_task(title)
            return True

        elif console == 4:
            print('ПОМЕТКА ВЫПОЛНЕНИЯ ЗАДАЧИ')
            print('Название задачи:')
            title = input()
            task.mark_done(title)
            print(f'Задача \"{title}\" помечена как выполнена!')

        elif console == 5:
            print('РЕДАКТИРОВАНИЕ ЗАДАЧИ')
            print('Название искомой задачи:')
            title = input()

            print('Что изменить в задаче?')
            print('1. Название')
            print('2. Описание')
            print('3. Приоритет')
            print('4. Срок выполнения')
            console_1 = int(input())
            while self.check_choice(console_1, 4) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 4: '))
            if console_1 == 1:
                kind_change = 'title'
            elif console_1 == 2:
                kind_change = 'description'
            elif console_1 == 3:
                kind_change = 'priority'
            else:
                kind_change = 'due_date'

            print('Введите новые данные:')
            new_data = input()
            task.update_task(title, kind_change, new_data)
            return True

        elif console == 6:
            print('УДАЛЕНИЕ ЗАДАЧИ')
            print('Название искомой задачи:')
            title = input()

            task.delete_task(title)
            return True

        elif console == 7:
            print('ИМПОРТ ЗАДАЧ')
            print('Выберите формат файла:')
            print('1. JSON')
            print('2. CSV')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                kind_file = 'json'
            else:
                kind_file = 'csv'

            print('Введите путь к файлу:')
            path_import = input()
            task.import_tasks(kind_file, path_import, task.path)
            return True

        elif console == 8:
            print('ЭКСПОРТ ЗАДАЧ')
            print('Выберите формат файла:')
            print('1. JSON')
            print('2. CSV')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                kind_file = 'json'
            else:
                kind_file = 'csv'
            print('Введите путь к файлу:')
            path = input()
            task.export_tasks(kind_file, path)
            return True

        else:
            return False

    def contacts(self):
        contact = Contact()
        print('Список функций:')
        print('1. Добавление нового контакта')
        print('2. Поиск контакта по имени или номеру телефона')
        print('3. Редактирование контакта')
        print('4. Удаление контакта')
        print('5. Импорт контактов')
        print('6. Экспорт контактов')
        print('7. Выход в главное меню')
        console = int(input('Выберите действие: '))
        while self.check_choice(console, 7) == 0:
            console = int(input('Пожалуйста введите число от 1 до 7: '))
        print(' ')  # просто отступ

        if console == 1:
            print('ДОБАВЛЕНИЕ КОНТАКТА')
            print('Имя контакта:')
            name = input()
            print('Номер телефона контакта:')
            print('P.s. Если вы не хотите добавлять номер телефона, просто нажмите ENTER на клавиатуре.')
            phone = input()
            print('Email контакта:')
            print('P.s. Если вы не хотите добавлять email, просто нажмите ENTER на клавиатуре.')
            email = input()

            contact.create_contact(name, phone, email)
            return True

        elif console == 2:
            print('ПОИСК КОНТАКТА')
            print('Выберите вариант поиска контакта:')
            print('1. По имени')
            print('2. По номеру телефона')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                key_dict = 'name'
                print('Введите имя:')
            else:
                key_dict = 'phone'
                print('Введите номер телефона:')
            key_result = input()

            contact.print_contact(key_dict, key_result)
            return True

        elif console == 3:
            print('РЕДАКТИРОВАНИЕ КОНТАКТА')
            print('Выберите вариант поиска контакта:')
            print('1. По имени')
            print('2. По номеру телефона')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                key_dict = 'name'
                print('Введите имя:')
            else:
                key_dict = 'phone'
                print('Введите номер телефона:')
            key_result = input()

            print('Выберите вариант данных для редактирования:')
            print('1. Имя')
            print('2. Номер телефона')
            print('3. Email')
            console_2 = int(input())
            while self.check_choice(console_1, 3) == 0:
                console_2 = int(input('Пожалуйста введите число от 1 до 3: '))
            if console_2 == 1:
                type_change = 'name'
            elif console_2 == 2:
                type_change = 'phone'
            else:
                type_change = 'email'
            print('Введите новые данные:')
            new_data = input()
            contact.update_contact(key_dict, key_result, type_change, new_data)
            return True

        elif console == 4:
            print('УДАЛЕНИЕ КОНТАКТА')
            print('Выберите вариант поиска контакта:')
            print('1. По имени')
            print('2. По номеру телефона')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                key_dict = 'name'
                print('Введите имя:')
            else:
                key_dict = 'phone'
                print('Введите номер телефона:')
            key_result = input()

            contact.delete_contact(key_dict, key_result)
            return True

        elif console == 5:
            print('ИМПОРТ КОНТАКОВ')
            print('Выберите формат файла:')
            print('1. JSON')
            print('2. CSV')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                kind_file = 'json'
            else:
                kind_file = 'csv'

            print('Введите путь к файлу:')
            path_import = input()
            contact.import_contacts(kind_file, path_import, contact.path)
            return True

        elif console == 6:
            print('ЭКСПОРТ ЗАДАЧ')
            print('Выберите формат файла:')
            print('1. JSON')
            print('2. CSV')
            console_1 = int(input())
            while self.check_choice(console_1, 2) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 2: '))
            if console_1 == 1:
                kind_file = 'json'
            else:
                kind_file = 'csv'
            print('Введите путь к файлу:')
            path = input()
            contact.export_contacts(kind_file, path)
            return True

        else:
            return False

    def finances(self):
        finance = FinanceRecord()
        print('Список функций:')
        print('1. Добавление новой финансовой записи')
        print('2. Просмотр всех записей с использованием фильтрации')
        print('3. Генерация отчёта с определенный периода')
        print('4. Импорт записей')
        print('5. Экспорт записей')
        print('6. Выйти в главное меню')
        console = int(input('Выберите действие: '))
        while self.check_choice(console, 6) == 0:
            console = int(input('Пожалуйста введите число от 1 до 6: '))
        print(' ')  # просто отступ

        if console == 1:
            print('ДОБАВЛЕНИЕ ФИНАНСОВОЙ ЗАПИСИ')
            print('Введите размер операции:')
            print('P.s. Больше 0 — доход, ниже 0 — расход.')
            amount = int(input())
            print('Введите категорию:')
            print('P.s. Например, Еда, Такси или др.')
            cat = input()
            print('Введите описание операции:')
            print('P.s. Если вы не хотите добавлять номер телефона, просто нажмите ENTER на клавиатуре.')
            description = input()
            print('Введите дату операции')
            print('P.s. Допустимый формат: ДД-ММ-ГГГГ')
            date = input()
            finance.create_record(amount, cat, date, description)
            return True

        elif console == 2:
            print('ВЫВОД ВСЕХ ЗАПИСЕЙ')
            print('Отфильтровать данные по:')
            print('1. По дате')
            print('2. По категории')
            print('3. Не использовать фильтр')
            console_1 = int(input())
            while self.check_choice(console, 3) == 0:
                console_1 = int(input('Пожалуйста введите число от 1 до 3: '))
            if console_1 == 1:
                key_dict = 'date'
                print('Введите дату:')
                print('P.s. Допустимый формат: ДД-ММ-ГГГГ')
                key_result = input()
            elif console_1 == 2:
                key_dict = 'category'
                print('Введите категорию:')
                key_result = input()
            else:
                key_dict = None
                key_result = None

            finance.show_list_records(key_dict, key_result)




def main():
    menu = Menu()
    run_menu = True
    while run_menu:
        console = menu.hello()
        while menu.check_choice(console, 6) == 0:
            console = int(input('Пожалуйста введите число от 1 до 6: '))
        if console == 1:
            run_note = True
            while run_note:
                run_note = menu.notes()
        elif console == 2:
            run_task = True
            while run_task:
                run_task = menu.tasks()
        elif console == 3:
            run_contact = True
            while run_contact:
                run_contact = menu.contacts()
        elif console == 4:
            run_finance = True
            while run_finance:
                run_finance = menu.finances()
        else:
            run_menu = False

if __name__ == '__main__':
    main()

"""
Вы меня простите, но я устал. Я несколько дней пишу этот код уже. Задача была разобраться с Гитом.
Я разобрался. Для чего нужно придумывать настолько огромную задачу? Я из-за этого кучу времени потратил
и теперь не успеваю сделать остальные домашки. Прошу меня простить еще раз, надеюсь на понимание....
"""



