import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QScrollArea, QDockWidget, QStatusBar, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication


class CRUDApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD App")
        self.setGeometry(100, 100, 800, 600)
        self.conn = sqlite3.connect("dat.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS koleksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT,
                kategori TEXT,
                tahun INTEGER
            )
        """)
        self.conn.commit()
        self.selected_id = None
        self.initUI()
        self.load_data()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Input Fields
        self.judul_input = QLineEdit()
        self.judul_input.setPlaceholderText("Judul")

        self.paste_button = QPushButton("Paste from Clipboard")
        self.paste_button.clicked.connect(self.paste_clipboard)

        self.kategori_input = QLineEdit()
        self.kategori_input.setPlaceholderText("Kategori")

        self.tahun_input = QLineEdit()
        self.tahun_input.setPlaceholderText("Tahun")

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.judul_input)
        form_layout.addWidget(self.paste_button)
        form_layout.addWidget(self.kategori_input)
        form_layout.addWidget(self.tahun_input)

        # Buttons
        self.add_button = QPushButton("Add")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")

        self.add_button.clicked.connect(self.add_data)
        self.update_button.clicked.connect(self.update_data)
        self.delete_button.clicked.connect(self.delete_data)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        form_layout.addLayout(button_layout)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)

        scroll_form = QScrollArea()
        scroll_form.setWidgetResizable(True)
        scroll_form.setWidget(form_widget)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Kategori", "Tahun"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellClicked.connect(self.select_row)

        scroll_table = QScrollArea()
        scroll_table.setWidgetResizable(True)
        scroll_table.setWidget(self.table)

        layout.addWidget(scroll_form)
        layout.addWidget(scroll_table)
        central_widget.setLayout(layout)

        # DockWidget
        dock = QDockWidget("Help", self)
        dock_text = QTextEdit()
        dock_text.setReadOnly(True)
        dock_text.setText(
            "Petunjuk Penggunaan:\n"
            "- Gunakan tombol Add untuk menambah data.\n"
            "- Gunakan Update setelah memilih data.\n"
            "- Gunakan Delete untuk menghapus data.\n"
            "- Klik 'Paste from Clipboard' untuk menempelkan teks ke kolom judul."
        )
        dock.setWidget(dock_text)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Nama: M. Bayu Aji | NIM: F1D02310144")

    def paste_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        self.judul_input.setText(clipboard.text())

    def load_data(self):
        self.table.setRowCount(0)
        self.cur.execute("SELECT * FROM koleksi")
        for row_data in self.cur.fetchall():
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_data(self):
        judul = self.judul_input.text()
        kategori = self.kategori_input.text()
        tahun = self.tahun_input.text()
        if judul and kategori and tahun:
            self.cur.execute("INSERT INTO koleksi (judul, kategori, tahun) VALUES (?, ?, ?)",
                             (judul, kategori, tahun))
            self.conn.commit()
            self.load_data()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Warning", "Semua field harus diisi!")

    def update_data(self):
        if self.selected_id:
            judul = self.judul_input.text()
            kategori = self.kategori_input.text()
            tahun = self.tahun_input.text()
            self.cur.execute("UPDATE koleksi SET judul=?, kategori=?, tahun=? WHERE id=?",
                             (judul, kategori, tahun, self.selected_id))
            self.conn.commit()
            self.load_data()
            self.clear_inputs()
            self.selected_id = None
        else:
            QMessageBox.warning(self, "Warning", "Pilih data terlebih dahulu!")

    def delete_data(self):
        if self.selected_id:
            self.cur.execute("DELETE FROM koleksi WHERE id=?", (self.selected_id,))
            self.conn.commit()
            self.load_data()
            self.clear_inputs()
            self.selected_id = None
        else:
            QMessageBox.warning(self, "Warning", "Pilih data terlebih dahulu!")

    def select_row(self, row, _):
        self.selected_id = int(self.table.item(row, 0).text())
        self.judul_input.setText(self.table.item(row, 1).text())
        self.kategori_input.setText(self.table.item(row, 2).text())
        self.tahun_input.setText(self.table.item(row, 3).text())

    def clear_inputs(self):
        self.judul_input.clear()
        self.kategori_input.clear()
        self.tahun_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CRUDApp()
    window.show()
    sys.exit(app.exec_())
