from datetime import date, datetime
from abc import ABC, abstractmethod
import re
from notebook import *
from address_book import *
from sorting import *
from flask import Flask

app = Flask(__name__)


@app.route('/')
class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass


    @abstractmethod
    def display_notes(self, notes):
        pass

    @abstractmethod
    def display_help(self, commands):
        pass


class ConsoleInterface(UserInterface):
    def display_contacts(self, contacts):
        print("=== Contacts ===")
        for contact in contacts:
            print(f"Name: {contact['name']}, Phone: {contact['phone']}")
        print()

    def display_notes(self, notes):
        print("=== Notes ===")
        for note in notes:
            print(f"Title: {note['title']}")
            print(note['content'])
            print()
        print()

    def display_help(self, commands):
        print("=== Available Commands ===")
        for command, description in commands.items():
            print(f"{command}: {description}")
        print()


class Name:
    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


class Phone:
    def __init__(self):
        while True:
            self.values = []
            self.value = input("Enter phones with code: +38 plus 10 numbers after:")
            try:
                for number in self.value.split(' '):
                    if re.match('^\\+38\\d{10}$', number):
                        self.values.append(number)
                    else:
                        raise ValueError
            except ValueError:
                print('Incorrect phone number!')
            else:
                break

    def __getitem__(self):
        return self.values


class Address:
    def __init__(self, value=""):
        self.value = value

    def __getitem__(self):
        return self.value


class Birthday:
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Birthday date in format (dd/mm/yyyy) : ")
            try:
                if re.match('^\\d{2}/\\d{2}/\\d{4}$', self.value):
                    self.value = datetime.strptime(self.value, "%d/%m/%Y")
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect date! Please provide correct date format.')

    def __getitem__(self):
        return self.value


class Email:
    def __init__(self, value=''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                if re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', self.value):
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect email! Please enter right email.')

    def __getitem__(self):
        return self.value


class Record:
    def __init__(self, name="", phones='', address='', birthday='', email=''):
        self.name = name
        self.phones = phones
        self.address = address
        self.birthday = birthday
        self.email = email

    def __str__(self):
        return (f"Contact name: {self.name},\nphones: {self.phones},\n"
                f"email: {self.email},\nbirthday: {self.birthday},\naddress: {self.address}")


class Bot:
    def __init__(self):
        self.book = AddressBook()
        self.notebook = Notes()

    def handle(self, action):
        if action == 'add':
            name = Name(input("Name: ")).value.strip()
            phones = Phone().value
            birthday = Birthday().value
            email = Email().value.strip()
            address = Address(input("Address: ")).value.strip()
            record = Record(name, phones, address, birthday, email)
            print(record)
            return self.book.add(record)
        elif action == 'search':
            pattern = input('Enter Search keyword: ')
            result = self.book.search_by_match(pattern)
            if result:
                for item in result:
                    print(item)
            else:
                print("There is no such Contact name!")
        elif action == 'edit':
            contact_name = input('Contact name: ')
            parameter = input('Which parameter to edit(name, phones, birthday, address, email): ').strip()
            return self.book.editing_contact(contact_name, parameter)
        elif action == 'remove':
            self.book.delete()
        elif action == 'save':
            file_name = input("File name: ")
            self.book.save(file_name)
        elif action == 'load':
            self.book.load()
        elif action == 'birthdays':
            days = input("Enter the number of days until Birthday: ")
            self.book.list_contacts_with_day_of_birthday(days)
        elif action == 'view':
            if self.book:
                print(self.book)
            else:
                print("Address book is empty")
        elif action == 'sorting':
            folder_path = input("Input path to folder where you want to sort files: ")
            print(folder_path)
            file_sorter = FileSorter(folder_path)
            file_sorter.sort_files()
        elif action == 'notes':
            note_action = input('Which action for Notes(add, find, edit, delete, sort, save): ').strip()
            if note_action == "add":
                text = input("Enter Note text: ")
                tags = input("Enter Note tags: ").split()
                new_note = (Note(text))
                new_note.add_tag(tags)
                print(new_note)
                self.notebook.add(new_note)
            elif note_action == "find":
                search_parameter = input("Search by tags(Y) or text(N): ")
                search_parameter = True if search_parameter == "Y" else False
                find_text = input("Enter Search pattern: ")
                self.notebook.find(find_text, search_parameter)
            elif note_action == "edit":
                edit_text = input("Enter pattern for note: ")
                edit_note = self.notebook.find(edit_text, False)[0]
                self.notebook.edit_note(edit_note)
            elif note_action == "delete":
                edit_text = input("Enter pattern for note: ")
                edit_note = self.notebook.find(edit_text, False)
                if edit_note:
                    self.notebook.delete(edit_note)
                else:
                    pass
            elif note_action == "sort":
                self.notebook.sort_notes()
            elif note_action == "save":
                file_name = input("File name: ")
                return self.notebook.save(file_name)
            elif note_action == "load":
                file_name = input("File name: ")
                return self.notebook.load(file_name)
            else:
                print("There is no such command for notes!")
            if note_action in ['add', 'delete', 'edit']:
                self.notebook.save("auto_save_notes")
        elif action == 'exit':
            pass
        else:
            print("There is no such command!")


def main():
    bot = Bot()
    commands_help = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Birthdays', 'View', 'Notes', 'Sorting', 'Exit']
    while True:
        command = input("Enter your command or the command Help to see a list of commands: ").lower()
        if command == 'help':
            format_str = str('{:%s%d}' % ('^', 20))
            for command in commands_help:
                print(format_str.format(command))
            command = input("Enter chose command: ").strip().lower()
            bot.handle(command)
            if command in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        else:
            bot.handle(command)
            if command in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        if command == 'exit':
            print("Good bye!")
            break


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

