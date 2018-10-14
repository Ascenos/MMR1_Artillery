from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

styleSheet = \
"""
VMenuElement {
    background-color: #aaa;
    border: 5px outset #777;
    color: black;
    font: 40px \"Montserrat\";
}
VMenuElement:hover {
    background-color: #a9a9a9;
    border-color: #696969;
}
VMenuElement:pressed {
    background-color: #999;
    border-color: #888;
    border-style: inset;
}
VMenu {
    background-color: #ccc;
    border: 5px double #aaa;
}
"""

def placeholer():
    pass

class VMenuElement(QPushButton):
    def __init__(self, parent, size, space, name, connection = placeholer):
        super().__init__(parent)
        self.block = size
        self.space = space
        self.old_size = None
        self.setText(name)
        self.clicked.connect(connection)

class VMenu(QLabel):
    def __init__(self, parent,  end_block = 1):
        super().__init__(parent)
        self.end_block = end_block
        self.elements = []

    def resize(self, *arguments):
        super().resize(*arguments)
        button_width = self.width() // 1.1
        block_number = self.end_block
        for e in self.elements:
            block_number += e.block + e.space
        button_height = self.height() // block_number
        button_position = 0
        button_x = (self.width() - button_width) // 2
        for e in self.elements:
            button_position += e.space
            e.resize(button_width, button_height*e.block)
            e.move(button_x, button_position*button_height)
            button_position += e.block

    def show(self):
        super().show()
        for e in self.elements:
            e.show()

    def add_element(self, *arguments):
        self.elements.append(VMenuElement(self, *arguments))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    main = QMainWindow()
    main.resize(600, 800)
    menu = VMenu(main, 2)
    menu.add_element(4, 2, "New Game")
    menu.add_element(4, 2, "Profiles")
    menu.add_element(4, 2, "Options")
    menu.add_element(3, 2, "Credits")
    menu.add_element(3, 0, "Exit", main.close)
    menu.resize(main.size())
    
    main.show()
    sys.exit(app.exec_())
