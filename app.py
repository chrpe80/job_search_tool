from PySide6 import QtWidgets, QtCore, QtGui
import pandas as pd
import sys
import os


class Model(QtGui.QStandardItemModel):
    """The model to be used together with the QTableView"""

    def __init__(self, header_labels: list):
        super().__init__()
        self.setHorizontalHeaderLabels(header_labels)


class Table(QtWidgets.QTableView):
    """A class that inherits and adds more functionality to the QTableView"""

    def __init__(self):
        super().__init__()
        self.model = Model(['Name of company', 'Name of contact', 'Contact phone nr', 'Contact email', 'Note'])
        self.setModel(self.model)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.populate_table()

    def populate_table(self):
        try:
            df = pd.read_csv("entries.csv")
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    item = QtGui.QStandardItem(str(df.iloc[i, j]))
                    item.setToolTip(str(df.iloc[i, j]))
                    self.model.setItem(i, j, item)
        except pd.errors.EmptyDataError:
            pass

    def add_entry(self, company, contact, phone, email, note):
        self.model.appendRow([
            QtGui.QStandardItem(str(company)),
            QtGui.QStandardItem(str(contact)),
            QtGui.QStandardItem(str(phone)),
            QtGui.QStandardItem(str(email)),
            QtGui.QStandardItem(str(note))
        ])


class Window(QtWidgets.QWidget):
    """
    The main app
    """

    def __init__(self):
        super().__init__()
        self.create_csv()

        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_form_page = QtWidgets.QVBoxLayout()
        self.layout_table_page = QtWidgets.QVBoxLayout()
        self.layout_update_note_page = QtWidgets.QVBoxLayout()
        self.layout_container_form = QtWidgets.QVBoxLayout()
        self.layout_container_table = QtWidgets.QVBoxLayout()
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.layout_container_update_note_form = QtWidgets.QVBoxLayout()

        self.tabs = QtWidgets.QTabWidget()
        self.form_page = QtWidgets.QWidget()
        self.table_page = QtWidgets.QWidget()
        self.update_note_page = QtWidgets.QWidget()

        self.container_form = QtWidgets.QGroupBox("New entry")
        self.container_table = QtWidgets.QGroupBox("All entries")
        self.container_update_note = QtWidgets.QGroupBox("Update note")

        self.name_of_company = QtWidgets.QLineEdit()
        self.name_of_contact = QtWidgets.QLineEdit()
        self.contact_phone_nr = QtWidgets.QLineEdit()
        self.contact_email = QtWidgets.QLineEdit()
        self.note = QtWidgets.QTextEdit()
        self.send_button = QtWidgets.QPushButton("Send")

        self.table = Table()

        self.entry_to_update = QtWidgets.QLineEdit()
        self.update_note = QtWidgets.QTextEdit()
        self.update_note_send_button = QtWidgets.QPushButton("Send")

        self.add_pages_to_tabs()
        self.set_layouts()
        self.connect_send_buttons()
        self.add_widgets()
        self.apply_settings()

    @staticmethod
    def create_csv():
        if not os.path.exists("entries.csv"):
            with open("entries.csv", "w"):
                pass

    def apply_settings(self):
        # Main window
        self.setWindowTitle("Job-search-tool")

        # Form container
        self.container_form.setFixedWidth(500)

        # Form elements
        self.name_of_company.setMaximumWidth(500)
        self.name_of_contact.setMaximumWidth(500)
        self.contact_phone_nr.setMaximumWidth(500)
        self.contact_email.setMaximumWidth(500)
        self.note.setMaximumWidth(500)
        self.send_button.setMaximumWidth(500)

        # Table
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        # Container update note
        self.container_update_note.setFixedWidth(500)

    def set_layouts(self):
        self.setLayout(self.layout_main)
        self.form_page.setLayout(self.layout_form_page)
        self.table_page.setLayout(self.layout_table_page)
        self.update_note_page.setLayout(self.layout_update_note_page)
        self.container_form.setLayout(self.layout_container_form)
        self.container_table.setLayout(self.layout_container_table)
        self.container_update_note.setLayout(self.layout_container_update_note_form)

    def add_pages_to_tabs(self):
        self.tabs.addTab(self.form_page, "New entry")
        self.tabs.addTab(self.table_page, "All entries")
        self.tabs.addTab(self.update_note_page, "Update note")

    def connect_send_buttons(self):
        self.send_button.clicked.connect(self.send_button_clicked)
        self.update_note_send_button.clicked.connect(
            lambda: self.update_note_send_button_clicked(self.update_note.toPlainText(), self.entry_to_update.text()))

    def add_widgets(self):
        self.layout_container_form.addWidget(QtWidgets.QLabel("Name of company"))
        self.layout_container_form.addWidget(self.name_of_company)
        self.layout_container_form.addWidget(QtWidgets.QLabel("Name of contact"))
        self.layout_container_form.addWidget(self.name_of_contact)
        self.layout_container_form.addWidget(QtWidgets.QLabel("Contact phone nr"))
        self.layout_container_form.addWidget(self.contact_phone_nr)
        self.layout_container_form.addWidget(QtWidgets.QLabel("Contact email"))
        self.layout_container_form.addWidget(self.contact_email)
        self.layout_container_form.addWidget(QtWidgets.QLabel("Note"))
        self.layout_container_form.addWidget(self.note)
        self.layout_container_form.addWidget(self.send_button)

        delete = QtWidgets.QPushButton("Delete")
        delete.clicked.connect(self.delete_row)
        save = QtWidgets.QPushButton("Save")
        save.clicked.connect(self.save_table_to_csv)

        self.layout_buttons.addWidget(delete)
        self.layout_buttons.addWidget(save)

        self.layout_container_table.addWidget(self.table)
        self.layout_container_table.addLayout(self.layout_buttons)

        self.layout_container_update_note_form.addWidget(QtWidgets.QLabel("Entry to update"))
        self.layout_container_update_note_form.addWidget(self.entry_to_update)
        self.layout_container_update_note_form.addWidget(QtWidgets.QLabel("New value"))
        self.layout_container_update_note_form.addWidget(self.update_note)
        self.layout_container_update_note_form.addWidget(self.update_note_send_button)

        self.layout_form_page.addWidget(self.container_form, alignment=QtCore.Qt.AlignCenter)
        self.layout_table_page.addWidget(self.container_table)
        self.layout_update_note_page.addWidget(self.container_update_note, alignment=QtCore.Qt.AlignCenter)

        self.layout_main.addWidget(self.tabs)

    def save_table_to_csv(self):
        data = []
        for row in range(self.table.model.rowCount()):
            row_data = []
            for col in range(self.table.model.columnCount()):
                item = self.table.model.item(row, col)
                row_data.append(item.text())
            data.append(row_data)

        columns = ['Name of company', 'Name of contact', 'Contact phone nr', 'Contact email', 'Note']
        df = pd.DataFrame(data=data, columns=columns)
        df["Note"] = df["Note"].astype(str)
        df.to_csv("entries.csv", index=False)

        self.update_table()

        self.show_information("Saved successfully", "The csv-file and the table was updated")

    def update_table(self):
        self.table.model.setRowCount(0)
        self.table.populate_table()

    def delete_row(self):
        indexes = self.table.selectionModel().selectedRows()
        for index in sorted(indexes):
            self.table.model.removeRow(index.row())
        self.save_table_to_csv()

    @staticmethod
    def show_information(message, details):
        information = QtWidgets.QMessageBox()
        information.setIcon(QtWidgets.QMessageBox.Information)
        information.setWindowTitle("Information")
        information.setText(message)
        information.setDetailedText(details)
        information.exec()

    def send_button_clicked(self):
        company = self.name_of_company.text()
        contact = self.name_of_contact.text()
        phone = self.contact_phone_nr.text()
        email = self.contact_email.text()
        note = self.note.toPlainText()

        self.table.add_entry(company, contact, phone, email, note)
        self.save_table_to_csv()

        self.name_of_company.clear()
        self.name_of_contact.clear()
        self.contact_phone_nr.clear()
        self.contact_email.clear()
        self.note.clear()

    def update_note_send_button_clicked(self, text, index):
        df = pd.read_csv("entries.csv")

        if index.isnumeric() and int(index) - 1 in df.index:
            df.at[int(index) - 1, "Note"] = text
            df.to_csv("entries.csv", index=False)
            self.entry_to_update.clear()
            self.update_note.clear()
            self.update_table()
        else:
            message = "Something went wrong"
            details = f"The value you entered [ {index} ] is not in the table index"
            self.show_information(message, details)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Window()
    window.showMaximized()
    app.exec()
