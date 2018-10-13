from PyQt5.QtWidgets import QPushButton, QLabel

def placeholder():
    pass

class VMenuElement(QPushButton):
    def __init__(self, parent, size, space, name, connection = placeholder):
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
