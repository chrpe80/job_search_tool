from PySide6 import QtWidgets, QtGui
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
        """
        The constructor creates an instance of Model
        It sets the model of the QTableView to this model
        It applies settings and populates the table with the content of entries.csv
        """
        super().__init__()
        self.model = Model(['Name of company', 'Name of contact', 'Contact phone nr', 'Contact email', 'Note'])
        self.setModel(self.model)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.populate_table()

    def populate_table(self):
        """Tries to Populate the table with the content of entries.csv"""

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
        """Takes the form values as arguments and appends them to the table"""

        self.model.appendRow([
            QtGui.QStandardItem(str(company)),
            QtGui.QStandardItem(str(contact)),
            QtGui.QStandardItem(str(phone)),
            QtGui.QStandardItem(str(email)),
            QtGui.QStandardItem(str(note))
        ])


class Window(QtWidgets.QWidget):
    """The main app"""

    def __init__(self):
        super().__init__()
        # The main layout is set
        # The main layout is set
        self.layout = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tabs)

        self.layout = QtWidgets.QVBoxLayout(self)

        # Form page
        self.form_widget = QtWidgets.QWidget()
        self.form_layout = QtWidgets.QVBoxLayout(self.form_widget)

        # The widgets are created
        self.name_of_company = QtWidgets.QLineEdit()
        self.name_of_company.setMaximumWidth(500)
        self.name_of_contact = QtWidgets.QLineEdit()
        self.name_of_contact.setMaximumWidth(500)
        self.contact_phone_nr = QtWidgets.QLineEdit()
        self.contact_phone_nr.setMaximumWidth(500)
        self.contact_email = QtWidgets.QLineEdit()
        self.contact_email.setMaximumWidth(500)
        self.note = QtWidgets.QTextEdit()
        self.note.setMaximumWidth(500)
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.setMaximumWidth(500)

        # Table page
        self.table_widget = QtWidgets.QWidget()
        self.table_layout = QtWidgets.QVBoxLayout(self.table_widget)
        self.table = Table()

        # The selection behavior of the table is set
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        # Method calls
        self.create_csv()
        self.apply_window_settings()
        self.set_layout()
        self.connect_send_button()
        self.add_widgets()

    @staticmethod
    def create_csv():
        """Creates the necessary csv file"""

        if not os.path.exists("entries.csv"):
            with open("entries.csv", "w"):
                pass

    def apply_window_settings(self):
        """Applies settings to the main window"""

        self.setWindowTitle("Job-search-tool")

    def set_layout(self):
        """Sets the layout"""

        self.setLayout(self.layout)
        self.add_tabs_to_layout()

    def connect_send_button(self):
        """Connects the 'send' button to the send_button_clicked method"""

        self.send_button.clicked.connect(self.send_button_clicked)

    def add_widgets(self):
        """Adds the widgets"""

        # The container that will hold the form is created
        container_form = QtWidgets.QGroupBox("New entry")
        container_form_layout = QtWidgets.QHBoxLayout()
        container_form.setLayout(container_form_layout)

        form_layout = QtWidgets.QVBoxLayout()
        form_layout.addWidget(QtWidgets.QLabel("Name of company"))
        form_layout.addWidget(self.name_of_company)
        form_layout.addWidget(QtWidgets.QLabel("Name of contact"))
        form_layout.addWidget(self.name_of_contact)
        form_layout.addWidget(QtWidgets.QLabel("Contact phone nr"))
        form_layout.addWidget(self.contact_phone_nr)
        form_layout.addWidget(QtWidgets.QLabel("Contact email"))
        form_layout.addWidget(self.contact_email)
        form_layout.addWidget(QtWidgets.QLabel("Note"))
        form_layout.addWidget(self.note)
        form_layout.addWidget(self.send_button)

        container_form_layout.addStretch()
        container_form_layout.addLayout(form_layout)
        container_form_layout.addStretch()

        self.form_layout.addWidget(container_form)
        self.tabs.addTab(self.form_widget, "Form")

        # The container that will hold the table is created
        container_table = QtWidgets.QGroupBox("Overview")
        container_table_layout = QtWidgets.QVBoxLayout()
        container_table.setLayout(container_table_layout)

        # The layout that will hold the action buttons is created
        actions_layout = QtWidgets.QHBoxLayout()

        # The action buttons are created
        delete = QtWidgets.QPushButton("Delete")
        delete.clicked.connect(self.delete_row)
        save = QtWidgets.QPushButton("Save")
        save.clicked.connect(self.save_to_csv)

        # The action buttons are added to their layout
        actions_layout.addWidget(delete)
        actions_layout.addWidget(save)

        # The table and the actions_layout are added to the container_table_layout
        container_table_layout.addWidget(self.table)
        container_table_layout.addLayout(actions_layout)

        # The table container is added to the table layout
        self.table_layout.addWidget(container_table)

        # The table widget page is added to the tab menu
        self.tabs.addTab(self.table_widget, "Table")

    def save_to_csv(self):
        """Saves the table to a csv file"""

        data = []
        for row in range(self.table.model.rowCount()):
            row_data = []
            for col in range(self.table.model.columnCount()):
                item = self.table.model.item(row, col)
                row_data.append(item.text())
            data.append(row_data)

        columns = ['Name of company', 'Name of contact', 'Contact phone nr', 'Contact email', 'Note']
        df = pd.DataFrame(data=data, columns=columns)
        df.to_csv("entries.csv", index=False)

    def delete_row(self):
        """Deletes the selected row"""

        indexes = self.table.selectionModel().selectedRows()
        for index in sorted(indexes):
            self.table.model.removeRow(index.row())
        self.save_to_csv()

    def send_button_clicked(self):
        """When the 'send' button is clicked, this method is called"""

        company = self.name_of_company.text()
        contact = self.name_of_contact.text()
        phone = self.contact_phone_nr.text()
        email = self.contact_email.text()
        note = self.note.toPlainText()

        self.table.add_entry(company, contact, phone, email, note)
        self.save_to_csv()

        self.name_of_company.clear()
        self.name_of_contact.clear()
        self.contact_phone_nr.clear()
        self.contact_email.clear()
        self.note.clear()

    def add_tabs_to_layout(self):
        self.layout.addWidget(self.tabs)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Window()
    window.showMaximized()
    app.exec()
