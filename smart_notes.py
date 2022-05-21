# Файл умных заметок
# Разработан на курсе python Start
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
#something that i can change.
import json

app = QApplication([])
main_win = QWidget()

main_win.setWindowTitle("Умные Заметки")
main_win.resize(900, 600)

main_h_layout = QHBoxLayout()
text_field = QTextEdit()

second_col = QVBoxLayout()
list_notes_label = QLabel()
list_notes_label.setText("Список заметок")
second_col.addWidget(list_notes_label)
list_notes = QListWidget()
second_col.addWidget(list_notes)

buttons_row_1 = QHBoxLayout()
create_note = QPushButton("Создать заметку")
delete_note = QPushButton("Удалить заметку")
save_note = QPushButton("Сохранить заметку")
buttons_row_1.addWidget(create_note)
buttons_row_1.addWidget(delete_note)

second_col.addLayout(buttons_row_1)
second_col.addWidget(save_note)

list_tag_label = QLabel("Список тегов")
list_tag = QListWidget()
new_tag_line = QLineEdit()
new_tag_line.setPlaceholderText("Введите тег...")
second_col.addWidget(list_tag_label)
second_col.addWidget(list_tag)
second_col.addWidget(new_tag_line)

buttons_row_2 = QHBoxLayout()
add_tag = QPushButton("Добавить к заметки")
remove_tag = QPushButton("Открепить от заметки")
search_tag = QPushButton("Искать заметки по тегу")
buttons_row_2.addWidget(add_tag)
buttons_row_2.addWidget(remove_tag)

second_col.addLayout(buttons_row_2)
second_col.addWidget(search_tag)

# Функционал приложения

# notes = {
#     "Моя первая заметка":{
#         "текст": "Это текст моей первой заметки",
#         "теги": ["Первая", "программа"]
#     }
# }

# with open("data.json", "w") as f:
#     json.dump(notes, f)

def show_note():
    key = list_notes.selectedItems()[0].text()
    text_field.setText(
        notes[key]["текст"]
    )
    list_tag.clear()
    list_tag.addItems(
        notes[key]["теги"]
        )

def add_note():
    note_name, ok = QInputDialog.getText(main_win, "Добавить заметку", "Название заметки:")
    if ok and note_name != "":
        list_notes.addItem(note_name)
        notes[note_name] = {"текст": "", "теги": []}

def del_note():
    key = list_notes.selectedItems()[0].text()
    if key != "":
        del notes[key]
        list_notes.clear()
        text_field.clear()
        list_tag.clear()
        list_notes.addItems(notes)

def s_note():
    if text_field.toPlainText() != "":
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = text_field.toPlainText()
        i = 0
        for note in notes:
            with open(f"notes/{i}.txt", 'w') as f:
                json.dump(notes, f)
                i += 1
                

    # with open("data.json", "w") as f:
        # TBD сохранение 1 заметка - 1 файл
        # json.dump(notes, f)
    print("Заметки сохранены!")

# Работа с тэгами
def add_tag_fun():
    key = list_notes.selectedItems()[0].text()
    if key != "":
        new_tag = new_tag_line.text()
        list_tag.addItem(new_tag)
        notes[key]["теги"].append(new_tag)
        new_tag_line.clear()

def remove_tag_fun():
    key = list_notes.selectedItems()[0].text()
    tag_key = list_tag.selectedItems()[0].text()
    if key and tag_key:
        list_tag.clear()
        notes[key]["теги"].remove(tag_key)
        list_tag.addItems(notes[key]["теги"])


def search_tag_fun():
    search_tag_text = new_tag_line.text()
    filtred_notes = {}
    if search_tag.text() == "Искать заметки по тегу":
        if search_tag_text:
            for key, data in notes.items():
                if search_tag_text in data["теги"]:
                    filtred_notes[key] = data
            if filtred_notes:
                list_notes.clear()
                list_tag.clear()
                list_notes.addItems(filtred_notes)
            search_tag.setText("Cбросить поиск")
    elif search_tag.text() == "Cбросить поиск":
        list_notes.clear()
        new_tag_line.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        search_tag.setText("Искать заметки по тегу")


# with open("data.json", "r") as f:
#     notes = json.load(f)

notes = {}
i = 0
while True:
    try:
        with open(f"notes/{i}.txt", 'r') as note_file:
            record = json.load(note_file)
            for idx, value in record.items():
                print(record)
                notes[idx] = value
        i += 1
    except IOError:
        break

list_notes.addItems(notes)

# Назначение кнопок и выбора из списка
list_notes.itemClicked.connect(show_note)
create_note.clicked.connect(add_note)
delete_note.clicked.connect(del_note)
save_note.clicked.connect(s_note)
# Кнопки по тэгам
add_tag.clicked.connect(add_tag_fun)
remove_tag.clicked.connect(remove_tag_fun)
search_tag.clicked.connect(search_tag_fun)

main_h_layout.addWidget(text_field, stretch=3)
main_h_layout.addLayout(second_col, stretch=2)

main_win.setLayout(main_h_layout)
# Запуск программы
main_win.show()
app.exec_()
