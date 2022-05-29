from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.QtWidgets import QMessageBox

add_or_edit = []
table_row = []
id_holder = []
type_edit = []
combo_title = []
city_id_combo = []
combo_id_holder = []

class Add_contact(QDialog):
    def __init__(self,db):
        super().__init__()
        self.db_connection = db

        if add_or_edit[0] == 1:
            self.setWindowTitle("Add New Contacts")
        elif add_or_edit[0] == 2:
            self.setWindowTitle("Edit An Existing Contact")

        self.setGeometry(100, 100, 330, 400)
        self.setStyleSheet("background-color : cadetblue")
        self.formGroupBox = QGroupBox()
        self.formGroupBox.setStyleSheet("background-color : white")
        self.cityComboBox = QComboBox()
        self.cityComboBox.setStyleSheet("background-color :light gray")

        c = self.db_connection.cursor()
        c.execute("SELECT * FROM City ORDER BY city_name")
        records = c.fetchall()


        combo_title.clear()
        city_id_combo.clear()
        combo_id_holder.clear()
        for i in range(len(records)):
            combo_title.append(records[i][1])
            city_id_combo.append(records[i][0])

        self.cityComboBox.addItems(combo_title)

        if add_or_edit[0] == 1:
            self.firstnameLineEdit = QLineEdit()
            self.lastnameLineEdit = QLineEdit()
            self.phoneLineEdit = QLineEdit()


        elif add_or_edit[0] == 2:
            self.firstnameLineEdit = QLineEdit(type_edit[1], self)
            self.lastnameLineEdit = QLineEdit(type_edit[2], self)
            self.phoneLineEdit = QLineEdit(type_edit[3], self)



        self.createForm()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setStyleSheet("background-color :lightgray")

        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.setLayout(mainLayout)
        self.exec_()

    def getInfo(self):

        name = self.firstnameLineEdit.text()
        last = self.lastnameLineEdit.text()
        city = self.cityComboBox.currentText()
        combo_id_holder.append(self.cityComboBox.currentIndex())
        phone = self.phoneLineEdit.text()
        selected=city_id_combo[combo_id_holder[0]]
        self.setStyleSheet("background-color :lightgray")
        if name == "" and phone != "":
            QMessageBox.about(self, "Warning", " Enter First Name! ")
        elif phone == "" and name != "":
            QMessageBox.about(self, "Warning", " Enter Phone Number !")
        elif name == "" and phone == "":
            QMessageBox.about(self, "Warning", " Enter First Name And Phone Number!")
        else:
            if add_or_edit[0] == 1:

                sql = f"""insert into Contacts(id,first_name,last_name,phone_no,city_id)values(NULL,'{name}','{last}','{phone}','{selected}') """
                self.db_connection.execute(sql)
                self.db_connection.commit()
            elif add_or_edit[0] == 2:


                iid = []
                selected_id = id_holder[table_row[0]]
                iid.append(selected_id)
                self.db_connection.execute("""UPDATE Contacts SET
                                           first_name= :firstname,
                                           last_name= :lastname,
                                           phone_no= :phonee,
                                           city_id= :cityname
                                           where id= :iid""",
                           {
                               'firstname': name,
                               'lastname': last,
                               'phonee': phone,
                               'cityname': selected,
                               'iid': iid[0],
                           }
                           )
                iid.clear()
                self.db_connection.commit()

        self.close()

    def createForm(self):

        layout = QFormLayout()

        layout.addRow(QLabel("Fiest Name"), self.firstnameLineEdit)
        layout.addRow(QLabel("Last Name"), self.lastnameLineEdit)
        layout.addRow(QLabel("City"), self.cityComboBox)
        layout.addRow(QLabel("Phone"), self.phoneLineEdit)

        self.formGroupBox.setLayout(layout)


class ContactsWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db_connection = db

        self.title = "Contacts"
        self.setStyleSheet("background-color: cadetblue;")
        self.top = 100
        self.left = 100
        self.width =890
        self.height = 700
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.creatingTables()
        self.show()

    def creatingTables(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['                  First Name                  ',
                                                    '                  Last Name                  ',
                                                    '                  Phone                  ',
                                                    '                  City                  ','              City Code              '])
        self.tableWidget.setStyleSheet("background-color : white")

        pallete = self.tableWidget.palette()
        hightlight_brush = pallete.brush(QPalette.Highlight)
        hightlight_brush.setColor(QColor('dodgerblue'))
        pallete.setBrush(QPalette.Highlight, hightlight_brush)
        self.tableWidget.setPalette(pallete)
        self.vBoxLayout = QVBoxLayout()
        self.filter_bar = QLineEdit("Filter...", self)
        self.filter_bar.setStyleSheet("background-color : white")
        self.button_Filter = QPushButton('Enter', self)
        self.button_Filter.setStyleSheet("background-color : lavender")
        self.button_Filter.clicked.connect(self.filter)
        self.vBoxLayout.addWidget(self.filter_bar)
        self.vBoxLayout.addWidget(self.button_Filter)
        self.vBoxLayout.addWidget(self.tableWidget)

        buttons_info = [(' Add ', 'Add A New City ', "background-color : lavender", 50, self.add_new),
                        (' Edit ', 'Edit An Existing City ', "background-color : lavender", 100, self.edit_existing),
                        (' Delete ', 'Delete An Existing City ', "background-color : coral", 150, self.delete_existing)]
        for button_info in buttons_info:
            self.b = QPushButton(button_info[0], self)
            self.b.setToolTip(button_info[1])
            self.b.setStyleSheet(button_info[2])
            self.b.setGeometry(200, 150, 150, 40)
            self.b.move(300, button_info[3])
            self.vBoxLayout.addWidget(self.b)
            self.b.clicked.connect(button_info[4])
        self.tableWidget.resizeColumnsToContents()
        self.setLayout(self.vBoxLayout)
        self.show_table()

    def filter(self):
        value = self.filter_bar.text()
        id_holder.clear()
        self.tableWidget.setRowCount(0)
        conn = self.db_connection
        c = self.db_connection.cursor()
        c.execute(
            f"SELECT * FROM Contacts WHERE first_name like '%{value}%'or last_name like '%{value}%'"
            f"or phone_no like '%{value}%' order by first_name")

        records = c.fetchall()

        self.tableWidget.setRowCount(1)

        for i in range(len(records)):
            rowPosition = self.tableWidget.rowCount()
            c.execute(f"SELECT * FROM City where id ={records[i][4]} order by city_name")
            result = c.fetchone()
            self.tableWidget.setItem(i, 0, QTableWidgetItem(records[i][1]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(records[i][2]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(records[i][3])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(result[1]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(result[2])))
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.tableWidget.insertRow(rowPosition)
            id_holder.append(records[i][0])


    def add_new(self):
        add_or_edit.clear()
        type_edit.clear()
        add_or_edit.append(1)
        self.W = Add_contact(self.db_connection)
        self.show_table()

    def show_table(self):
        id_holder.clear()
        self.tableWidget.setRowCount(0)

        c = self.db_connection.cursor()
        c.execute("SELECT * FROM Contacts order by first_name")
        records = c.fetchall()
        print(records)

        self.tableWidget.setRowCount(1)

        for i in range(len(records)):
            rowPosition = self.tableWidget.rowCount()
            c.execute(f"SELECT * FROM City where id ={records[i][4]} order by city_name")
            result = c.fetchone()
            self.tableWidget.setItem(i, 0, QTableWidgetItem(records[i][1]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(records[i][2]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(records[i][3])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(result[1]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(result[2])))
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.tableWidget.insertRow(rowPosition)
            id_holder.append(records[i][0])

    def edit_existing(self):

        s = self.tableWidget.currentRow()

        if s != -1:
            add_or_edit.clear()
            type_edit.clear()
            table_row.append(s)
            add_or_edit.append(2)

            co = self.db_connection.cursor()
            selected_id = id_holder[table_row[0]]
            co.execute(f"select * from Contacts where id={selected_id}")
            records = co.fetchall()
            for i in range(5):
                type_edit.append(str(records[0][i]))

            self.W = Add_contact(self.db_connection)
            self.show_table()
            table_row.clear()
        else:
            self.setStyleSheet("background-color :lightgray")
            QMessageBox.about(self, "Warning", "You Have To Make A Selection! ")
            self.setStyleSheet("background-color : cadetblue")

    def delete_existing(self):
        s = self.tableWidget.currentRow()

        if s != -1:
            self.setStyleSheet("background-color :lightgray")
            buttonReply = QMessageBox.question(self, 'Warning', "Do You Want To Permanently Delete Your Contact?",
                                               QMessageBox.Yes | QMessageBox.No)

            if buttonReply == QMessageBox.Yes:
                table_row.append(s)




                selected_id = id_holder[table_row[0]]

                self.db_connection.execute(f"DELETE from Contacts WHERE id={selected_id}")

                self.db_connection.commit()
                self.setStyleSheet("background-color : cadetblue")
                self.show_table()
                table_row.clear()
            else:
                self.show()
                self.setStyleSheet("background-color : cadetblue")
        else:
            self.setStyleSheet("background-color :lightgray")
            QMessageBox.about(self, "Warning", "You Have To Make A Selection! ")
            self.setStyleSheet("background-color : cadetblue")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactsWindow()
    sys.exit(app.exec_())
