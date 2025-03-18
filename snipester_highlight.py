from PyQt5.QtWidgets import QWidget

def highlight_all(self, event):
    if self.link_input.toPlainText():
        self.link_input.selectAll()
    QWidget.mousePressEvent(self, event)
