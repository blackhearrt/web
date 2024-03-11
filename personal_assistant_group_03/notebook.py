from collections import UserList
from tkinter import messagebox
from tkinter import *
import pickle
import os
from datetime import datetime



class Note:
    def __init__(self, text):
        self.text = text
        self.tags = []
        self.create_date = datetime.now()

    def __str__(self):
        return f"Note: {self.text}, has tags: {'; '.join(p for p in self.tags)}, " \
               f"date of creation: {self.create_date.strftime('%Y-%m-%d %H:%M:%S')}"

    def add_tag(self, tags):
        for tag in tags:
            for ch in tag:
                if ch.isspace():
                    raise ValueError("Tag may be one long word without space")
            self.tags.append(tag)


class Notes(UserList):
    def __init__(self):
        self.data = []
        self.counter = -1

    def __iter__(self):
        return iter(self.data)

    def pr_notes(self, lst_notes):
        if lst_notes:
            for note in lst_notes:
                print(f"Note creation date: {note['create_date'].strftime('%d/%m/%Y %H:%M:%S')}, Text: {note['text']},"
                      f" Tags: {note['tags']}")
        else:
            print("List of notes is empty")

    def add(self, note: Note):
        note_info = {'text': note.text,
                     'tags': note.tags,
                     'create_date': note.create_date}
        self.data.append(note_info)
        print(f"Yours note has been added to NoteBook.")

    def find(self, find_text, find_by_tag=True):
        result = []
        for notes in self.data:
            for key, value in notes.items():
                if find_by_tag and key == "tags":
                    for tag in value:
                        if find_text in tag:
                            result.append(notes)
                else:
                    if key == "text" and find_text in value and not find_by_tag:
                        result.append(notes)
        if result:
            sorted_list = sorted(result, key=lambda x: x['create_date'])
            self.pr_notes(sorted_list)
        else:
            print("No such notes found")
        return result

    def delete(self, notes):
        for note in notes:
            self.data.remove(note)

    def sort_notes(self):
        sorted_list = sorted(self.data, key=lambda x: x['create_date'])
        self.pr_notes(sorted_list)

    def save(self, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(self.data, file)

    def load(self, file_name):
        emptyness = os.stat(file_name + '.bin')
        if emptyness.st_size != 0:
            with open(file_name + '.bin', 'rb') as file:
                self.data = pickle.load(file)
        else:
            pass
        return self.data

    def edit_note(self, note):
        root = Tk()
        text = Text(root, width=200, height=200)
        text.pack()

        root.title = "Notes"
        root.geometry("200x200")

        def edit_text():
            text.delete('1.0', END)
            text.insert('1.0', note['text'])

        def save_text():
            note['text'] = text.get('1.0', END)

        def edit_tags():
            text.delete('1.0', END)
            text.insert('1.0', '\n'.join(p for p in note['tags']))

        def save_tags():
            edit_tags = text.get('1.0', END)
            edit_tags = edit_tags.split("\n")
            note['tags'].clear()
            flag_ok = True
            for tag in edit_tags:
                for ch in tag:
                    if ch.isspace():
                        messagebox.showerror(None, f'Tag "{tag}" consist space')
                        flag_ok = False
                        break

            if flag_ok:
                note['tags'].extend(edit_tags)

        main_menu = Menu()
        text_menu = Menu()
        text_menu.add_command(label="Edit", command=edit_text)
        text_menu.add_command(label="Save", command=save_text)
        tag_menu = Menu()
        tag_menu.add_command(label="Edit", command=edit_tags)
        tag_menu.add_command(label="Save", command=save_tags)
        main_menu.add_cascade(label="Text", menu=text_menu)
        main_menu.add_cascade(label="Tags", menu=tag_menu)

        root.config(menu=main_menu)
        root.mainloop()


