#!/usr/bin/env python3

from PyQt5.QtWidgets import (QMainWindow, QApplication, qApp, QWidget,\
 QFileDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit)
from PyQt5.QtGui import (QIcon, QImage, QPixmap)
from sys import argv, exit
import sqlite3

class address_book_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.db_connect()
    def init_ui(self):
        main_layout = QWidget()
        grid = QGridLayout()
        main_layout.setLayout(grid)

        label_name = QLabel('Name', main_layout)
        label_id = QLabel('ID#', main_layout)
        label_notes = QLabel('Notes', main_layout)

        self.avatar_path = './assets/icon.png'
        self.photo = QLabel('Photo',main_layout)
        self.set_photo()

        self.edit_name = QLineEdit(main_layout)
        self.edit_id = QLineEdit(main_layout)
        self.edit_data = QTextEdit(main_layout)
        self.edit_search = QLineEdit(main_layout)

        button_find_next = QPushButton('Next', main_layout)
        button_find_next.clicked[bool].connect(self.db_fetch_next)
        button_search = QPushButton('Search', main_layout)
        button_search.clicked[bool].connect(self.db_query)

        button_delete = QPushButton('Delete', main_layout)
        button_delete.clicked[bool].connect(self.db_delete)

        button_add = QPushButton('Add', main_layout)
        button_add.clicked[bool].connect(self.db_insert)

        button_quit = QPushButton('Save & Exit', main_layout)
        button_quit.clicked[bool].connect(self.db_close)

        button_find_file = QPushButton('Find photo', main_layout)
        button_find_file.clicked[bool].connect(self.find_file)

        grid.addWidget(label_name, 0, 0)
        grid.addWidget(label_id, 1, 0)
        grid.addWidget(label_notes, 2, 0)

        grid.addWidget(self.photo, 0, 3, 4, 1)
        grid.addWidget(self.edit_name, 0, 1)
        grid.addWidget(self.edit_id, 1, 1)
        grid.addWidget(self.edit_data, 2, 1, 4, 1)
        grid.addWidget(self.edit_search, 6, 1)

        grid.addWidget(button_find_next, 3, 0)
        grid.addWidget(button_add, 4, 0)
        grid.addWidget(button_delete, 5,0)
        grid.addWidget(button_quit, 6, 0)
        grid.addWidget(button_find_file, 5, 3)
        grid.addWidget(button_search, 6, 3)

        self.setCentralWidget(main_layout)
        self.setWindowTitle('Address book')
        self.statusBar().showMessage('Ready')
        self.setWindowIcon(QIcon('./assets/icon.png'))
        self.setGeometry(100, 100, 640, 240)
        self.show()

    def db_connect(self):
        try:
            self.db_conn = sqlite3.connect('./assets/address_book.db')
            self.db_curs = self.db_conn.cursor()
            try:
                self.db_curs.execute('''CREATE TABLE contacts (name TEXT NOT NULL,\
                 tel TEXT NOT NULL, data TEXT NOT NULL, photo TEXT NOT NULL)''')
                self.statusBar().showMessage('Created new database')
            except:
                self.statusBar().showMessage('Connected to database')
        except:
            self.statusBar().showMessage('Unable to connect to database')
    def db_fetch_next(self):
        self.statusBar().showMessage('Searching...')
        try:
            result = self.db_curs.fetchone()
            self.edit_name.setText(result[0])
            self.edit_id.setText(result[1])
            self.edit_data.setText(result[2])
            self.avatar_path = result[3]
            self.set_photo()
            self.statusBar().showMessage('Searching... Done.')
        except:
            self.statusBar().showMessage('Searching... Error.')
    def db_query(self):
        self.statusBar().showMessage('Searching...')
        try:
            self.db_curs.execute('''SELECT name, tel, data, photo FROM contacts \
            WHERE (name LIKE (?) or tel LIKE (?) or data LIKE (?))''',\
             (3*("%{}%".format(self.edit_search.text()),)))
            self.statusBar().showMessage('Searching... Done.')
            result = self.db_curs.fetchone()
            self.edit_name.setText(result[0])
            self.edit_id.setText(result[1])
            self.edit_data.setText(result[2])
            self.avatar_path = result[3]
            self.set_photo()
        except:
            self.statusBar().showMessage('Searching... Error.')
    def db_delete(self):
        self.statusBar().showMessage('Deleting...')
        try:
            self.db_curs.execute('''DELETE FROM contacts \
            WHERE (name = (?) AND tel = (?) AND data = (?))''',\
             (self.edit_name.text(), self.edit_id.text(),\
              self.edit_data.toPlainText()))
            self.statusBar().showMessage('Deleting... Done.')
        except:
            self.statusBar().showMessage('Deleting... Error.')
    def db_insert(self):
        self.statusBar().showMessage('Adding...')
        try:
            self.db_curs.execute('''INSERT INTO contacts VALUES (?, ?, ?, ?)''',\
             (self.edit_name.text(), self.edit_id.text(),\
              self.edit_data.toPlainText(), self.avatar_path))
            self.statusBar().showMessage('Adding... Done.')
        except:
            self.statusBar().showMessage('Adding... Error.')
    def db_close(self):
        self.statusBar().showMessage('Commiting to database')
        self.db_conn.commit()
        self.db_conn.close()
        qApp.exit()
    def find_file(self):
        self.avatar_path = QFileDialog.getOpenFileName(self, 'Open photo',\
         './assets', 'Image Files (*.png *.jpg *.bmp)')[0]
        self.set_photo()
    def set_photo(self):
        self.statusBar().showMessage('Loading Photo...')
        try:
            picture = QImage()
            picture.load(self.avatar_path)
            self.photo.setPixmap(QPixmap.fromImage(picture))
            self.statusBar().showMessage('Loading Photo... Done.')
        except:
            self.statusBar().showMessage('Loading Photo... Error.')
if "__main__" == __name__:
    app = QApplication(argv)
    ex = address_book_window()
    exit(app.exec_())
