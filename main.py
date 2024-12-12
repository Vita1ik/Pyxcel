#  source myenv/bin/activate

from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout
from collections import defaultdict
from PyQt5.QtCore import Qt

from views import ExcelTable, CellLineEdit

# Create the application
app = QApplication([])

# Create the main window
window = QWidget()
layout = QVBoxLayout(window)
label = QLabel()
textbox = CellLineEdit()
table = ExcelTable(state_label=label, cell_text_box=textbox)

h_layout = QHBoxLayout()
h_layout.addWidget(textbox)
h_layout.addWidget(label)
layout.addLayout(h_layout)
layout.addWidget(table)



# Set up the window and show it
window.setLayout(layout)
window.setWindowTitle('Pyxcel')
window.resize(800, 600)
window.show()

app.aboutToQuit.connect(table.save_data)

# Execute the application
app.exec_()
