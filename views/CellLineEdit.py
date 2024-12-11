from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QLabel


class CellLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.__table = None  # Private variable to store table
        self.__setup_event_connections()

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, new_table):
        self.__table = new_table

    def update_text(self, text, blockSignals = True):
        if blockSignals:
            self.blockSignals(True)
            self.setText(text)
            self.blockSignals(False)
        else:
            self.setText(text)

    def on_text_changed(self, text):
        self.table.blockSignals(True)
        self.table.currentItem().setText(text)
        self.table.blockSignals(False)

    def on_editing_finished(self):
        self.table.blockSignals(True)
        item = self.table.currentItem()
        item.setText(self.text())
        self.table.on_item_changed(item)
        self.table.blockSignals(False)

    def __setup_event_connections(self):
        self.textChanged.connect(self.on_text_changed)
        self.editingFinished.connect(self.on_editing_finished)
