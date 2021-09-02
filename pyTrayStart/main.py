#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program entry point"""

import json
import os.path
import subprocess
import sys

import icoextract
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def get_styles(filename):
    file = os.path.join(os.path.split(__file__)[0], f"resources/styles/{filename}.stylesheet")
    style = open(file, 'r').read()
    return style


def write_json(data, sections):
    json_dict = {}
    for section in sections:
        json_dict.update({section: {}})
        for item in data:
            # clean dict from None Values
            item = {k: v for k, v in item.items() if v is not None}
            try:
                if section == item["section"]:
                    temp = {
                        item["name"]: {
                            "path": item["path"],
                            "type": item["type"]
                        }
                    }
                    json_dict[section].update(temp)

            except KeyError:
                pass
    with open('resources/json/action.json', 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)


class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1, 4)
        self.setHorizontalHeaderLabels(['Name', 'Pfad', 'Type', 'Label'])
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(250)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setStyleSheet(get_styles("table"))
        self._populate()

    def _addRow(self):
        row_count = self.rowCount()
        self.insertRow(row_count)

    def _save(self):
        sections = []
        action_list = []
        for row in range(self.rowCount()):
            action_dict = {
                "name": None,
                "path": None,
                "type": None,
                "section": None
            }
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is None:
                    continue
                if item.column() == 0:
                    action_dict["name"] = item.text()
                elif item.column() == 1:
                    action_dict["path"] = item.text()
                elif item.column() == 2:
                    action_dict["type"] = item.text()
                elif item.column() == 3:
                    action_dict["section"] = item.text()
                    if item.text() not in sections:
                        sections.append(item.text())

            action_list.append(action_dict)

        write_json(action_list, sections)
        os.execv(sys.executable, ['python'] + sys.argv)

    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount() - 1)

    def _populate(self):
        with open("resources/json/action.json") as actions_file:
            actions_json = json.load(actions_file)

        actions_file.close()
        for label in actions_json:
            for action_items in actions_json[label]:
                row_position = self.rowCount() - 1
                self.insertRow(row_position)
                self.setItem(row_position, 0, QTableWidgetItem(action_items))
                self.setItem(row_position, 1, QTableWidgetItem(actions_json[label][action_items]["path"]))
                self.setItem(row_position, 2, QTableWidgetItem(actions_json[label][action_items]["type"]))
                self.setItem(row_position, 3, QTableWidgetItem(label))


class Options(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1122, 632)
        self.setStyleSheet(get_styles("options"))
        self.setWindowTitle("PyTrayStart")
        self.setWindowIcon(QIcon("resources/icons/icon.ico"))

        main_layout = QHBoxLayout()
        table = TableWidget()
        main_layout.addWidget(table)
        button_layout = QVBoxLayout()

        button_new = QPushButton('New')
        button_new.clicked.connect(table._addRow)
        button_layout.addWidget(button_new)

        button_remove = QPushButton('Remove')
        button_remove.clicked.connect(table._removeRow)
        button_layout.addWidget(button_remove)

        button_save = QPushButton('Save and Quit')
        button_save.clicked.connect(table._save)
        button_layout.addWidget(button_save, alignment=Qt.AlignTop)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)


def create_label(name):
    action_label = QLabel(name)
    action_label.setAlignment(Qt.AlignCenter)
    label_widget = QWidgetAction(action_label)
    label_widget.setDefaultWidget(action_label)
    return label_widget


def create_action(name=None, path=None, action_type=None):
    action_item = QAction(name)
    if action_type == "application":
        action_item.triggered.connect((lambda: launch(path)))
        action_item_icon = icoextract.IconExtractor(path)
        action_item_icon.export_icon("action_icon.ico")
        action_item.setIcon(QIcon("action_icon.ico"))

    return action_item


def getActions():
    with open("resources/json/action.json") as actions_file:
        actions_json = json.load(actions_file)

    actions_file.close()
    action_list = []
    for label in actions_json:
        action_list.append(create_label(
            name=label
        ))
        for action_items in actions_json[label]:
            action_list.append(create_action(
                name=action_items,
                path=actions_json[label][action_items]["path"],
                action_type=actions_json[label][action_items]["type"]
            ))

    return action_list


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)


def openOptions():
    pass


def launch(text):
    subprocess.run(text)


# Create the tray
class Tray(QSystemTrayIcon):
    def __init__(self):
        super(QSystemTrayIcon, self).__init__()
        self.setIcon(QIcon("resources/icons/icon.ico"))
        self.setVisible(True)
        self.tray_menu = menu
        self.opt_item = self.add_options()
        self.ext_item = self.add_exit()
        self.tray_menu.addAction(self.opt_item)
        self.tray_menu.addAction(self.ext_item)
        self.setContextMenu(self.tray_menu)

    @staticmethod
    def add_options():
        opt_item = QAction("Options")
        opt = Options()
        opt_item.triggered.connect((lambda: opt.show()))

        return opt_item

    def add_exit(self):
        ext_item = QAction("Quit")
        ext_item.triggered.connect((lambda: self.quit()))

        return ext_item


# Create the menu
menu = QMenu()
menu.setMinimumWidth(200)
menu.setStyleSheet(get_styles("tray"))

actions = getActions()
for action in actions:
    menu.addAction(action)

if __name__ == "__main__":
    tray = Tray()
    tray.show()
    sys.exit(app.exec_())
