from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from contextlib import contextmanager
from models.cell import Cell
from modules.expression_evaluator import ExpressionEvaluator

class ExcelTable(QTableWidget):
    CELL_ROW_VALUE = 'row_value'
    CELL_CALCULATED_VALUE = 'calculated_value'
    CELL_CONTENTS = [CELL_ROW_VALUE, CELL_CALCULATED_VALUE]

    def __init__(self, state_label=None, cell_text_box=None):
        self.state_label = state_label
        self.cell_text_box = cell_text_box
        self.current_editing_cell = None
        self.__setup_size()
        self.__setup_styles()
        with self.block_signals():
            self.__import_data()
        self.__setup_event_connections()
        self.setCurrentItem(self.item(0, 0))
        cell_text_box.table = self

    def save_data(self):
        list_data = []
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item:
                    address = self.__cell_address(item)
                    data = item.data(Qt.UserRole)
                    calculated_value = None
                    text = ''
                    if data:
                        calculated_value = data[self.CELL_ROW_VALUE]
                        text = data[self.CELL_CALCULATED_VALUE]

                    list_data.append((calculated_value, text, address))
        print(list_data)
        Cell.update_all(list_data)

    def on_item_selection_changed(self):
        self.__change_cell_content(self.CELL_CALCULATED_VALUE, self.current_editing_cell)
        selected_items = self.selectedItems()
        self.current_editing_cell = selected_items[0]
        data = self.current_editing_cell.data(Qt.UserRole)
        text = data and data[self.CELL_ROW_VALUE]
        self.cell_text_box.update_text(text)
        self.state_label.setText(self.__cells_address(selected_items))

    def on_cell_double_clicked(self, row, col):
        selected_item = self.item(row, col)
        self.current_editing_cell = selected_item
        self.__change_cell_content(self.CELL_ROW_VALUE, self.current_editing_cell)

    def on_item_changed(self, item):
        row_value = item.text()
        address = self.__cell_address(item)
        print('on_item_changed')
        if row_value and row_value[0] == '=':
            calculated_value = ExpressionEvaluator(address).evaluate(row_value[1:])
        else:
            calculated_value = row_value

        Cell.update((row_value, calculated_value, address))

        self.__update_cell_content(item, row_value, calculated_value)
        self.__change_cell_content(self.CELL_ROW_VALUE, self.current_editing_cell)
        with self.block_signals():
            self.__import_data()

    def __cells_address(self, cells):
        if cells:
            if len(cells) == 1:
                return self.__cell_address(cells[0])
            else:
                first_address = self.__cell_address(cells[0])
                last_address = self.__cell_address(cells[-1])
                return f'{first_address}:{last_address}'

    def __update_cell_content(self, cell, row_value, calculated_value):
        with self.block_signals():
            data = {
                self.CELL_ROW_VALUE: row_value,
                self.CELL_CALCULATED_VALUE: str(calculated_value)
            }
            cell.setData(Qt.UserRole, data)

    def __change_cell_content(self, content, cell):
        if not cell:
            return None

        if content not in self.CELL_CONTENTS:
            raise ValueError("Invalid value for content")

        data = cell.data(Qt.UserRole)

        if data:
            with self.block_signals():
                cell.setText(data[content])

    def __cell_address(self, cell):
        if cell:
            row = cell.row()
            col = cell.column()
            row_header = self.verticalHeaderItem(row).text()
            col_header = self.horizontalHeaderItem(col).text()
            return f'{col_header}{row_header}'

    @contextmanager
    def block_signals(self):
        """Context manager to block and unblock signals."""
        self.blockSignals(True)
        try:
            yield self
        finally:
            self.blockSignals(False)


    def __setup_event_connections(self):
        self.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.itemChanged.connect(self.on_item_changed)

    def __setup_styles(self):
        self.setStyleSheet("QTableWidget { background-color: #2e2e2e }")
        self.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #2e2e2e; }")
        self.verticalHeader().setStyleSheet("QHeaderView::section { background-color: #2e2e2e; }")

    def __setup_size(self):
        column_names = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        row_names = [str(i) for i in range(1, 101)]
        rows_count = len(row_names)
        columns_count = len(column_names)

        super().__init__(rows_count, columns_count)

        self.setHorizontalHeaderLabels(column_names)
        self.setVerticalHeaderLabels(row_names)

        self.setRowCount(rows_count)
        self.setColumnCount(columns_count)

        # Add data to the table
        for i, row_name in enumerate(row_names):
            for j, column_name in enumerate(column_names):
                self.setItem(i, j, QTableWidgetItem(None))

    def __import_data(self):
        for cell in Cell.all():
            item = self.item(cell['row'], cell['column'])
            item.setText(cell['text'])
            data = {
                self.CELL_ROW_VALUE: cell['data'],
                self.CELL_CALCULATED_VALUE: cell['text']
            }
            item.setData(Qt.UserRole, data)
