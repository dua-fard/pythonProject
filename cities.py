from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.QtWidgets import QMessageBox
add_or_edit=[]
table_row=[]
id_holder=[]
type_edit=[]
class Add_city(QDialog):
    def __init__(self,db):
       super().__init__()
       self.db_connection = db
       if add_or_edit[0]==1:
           self.setWindowTitle("Add New Cities")
       elif add_or_edit[0]==2:
           self.setWindowTitle("Edit An Existing City")

       self.setGeometry(100, 100, 330, 400)
       self.setStyleSheet("background-color : cadetblue")
       self.formGroupBox = QGroupBox()
       self.formGroupBox.setStyleSheet("background-color : white")
       if add_or_edit[0] == 1:
                self.citynameLineEdit = QLineEdit()
                self.citycodeLineEdit = QLineEdit()
       elif add_or_edit[0] == 2:
                self.citynameLineEdit = QLineEdit(type_edit[1],self)
                self.citycodeLineEdit = QLineEdit(type_edit[2],self)

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

        name = self.citynameLineEdit.text()
        code = self.citycodeLineEdit.text()


        self.setStyleSheet("background-color :lightgray")
        if name == "" and code != "":
            QMessageBox.about(self, "Warning", " Enter City Name! ")
        elif code == "" and name != "":
            QMessageBox.about(self, "Warning", " Enter City Code!")
        elif name == "" and code == "":
            QMessageBox.about(self, "Warning", " Enter City Name And City Code!")
        else:

            if add_or_edit[0]==1:

                       sql = f"""insert into City(id,city_name,city_code)values(NULL,'{name}','{code}') """
                       self.db_connection.execute(sql)
                       self.db_connection.commit()
            elif add_or_edit[0]==2:


                iid = []
                selected_id=id_holder[table_row[0]]
                iid.append(selected_id)
                self.db_connection.execute("""UPDATE City SET
                                           city_name= :cityname,
                                           city_code= :citycode
                                           where id= :iid""",
                           {
                               'cityname': name,
                               'citycode': code,
                               'iid': iid[0],
                           }
                           )
                iid.clear()
                self.db_connection.commit()


        self.close()


    def createForm(self):

        layout = QFormLayout()

        layout.addRow(QLabel("City Name"), self.citynameLineEdit)
        layout.addRow(QLabel("City Code"), self.citycodeLineEdit)

        self.formGroupBox.setLayout(layout)

class CitiesWindow(QWidget):
    def __init__(self,db):
        super().__init__()
        self.db_connection = db

        self.title = "Cities"
        self.setStyleSheet("background-color: cadetblue;")
        self.top = 100
        self.left = 100
        self.width = 500
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
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['                  City Name                  ',
                                                 '                  City Code                  '])
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


        buttons_info = [(' Add ', 'Add A New City ',"background-color : lavender", 50,self.add_new),
                        (' Edit ', 'Edit An Existing City ',"background-color : lavender", 100,self.edit_existing),
                        (' Delete ', 'Delete An Existing City ',"background-color : coral", 150,self.delete_existing)]
        for i in range(len(buttons_info)):
            self.b = QPushButton(buttons_info[i][0], self)
            self.b.setToolTip(buttons_info[i][1])
            self.b.setStyleSheet(buttons_info[i][2])
            self.b.setGeometry(200, 150, 150, 40)
            self.b.move(300, buttons_info[i][3])
            self.vBoxLayout.addWidget(self.b)
            self.b.clicked.connect(buttons_info[i][4])

        self.tableWidget.resizeColumnsToContents()
        self.setLayout(self.vBoxLayout)
        self.show_table()

    def filter(self):
        value = self.filter_bar.text()
        id_holder.clear()
        self.tableWidget.setRowCount(0)

        c = self.db_connection.cursor()
        c.execute(
            f"SELECT * FROM City WHERE city_name like '%{value}%'or city_code like '%{value}%' order by city_name")

        records = c.fetchall()

        self.tableWidget.setRowCount(1)

        for i in range(len(records)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.setItem(i, 0, QTableWidgetItem(records[i][1]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(records[i][2])))
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.tableWidget.insertRow(rowPosition)
            id_holder.append(records[i][0])


    def add_new(self):
        add_or_edit.clear()
        add_or_edit.append(1)
        self.W = Add_city(self.db_connection)
        self.show_table()

    def show_table(self):
                id_holder.clear()
                self.tableWidget.setRowCount(0)

                c = self.db_connection.cursor()
                c.execute("SELECT * FROM City order by city_name")
                records = c.fetchall()
                self.tableWidget.setRowCount(1)

                for i in range(len(records)):
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(records[i][1]))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(records[i][2])))
                    self.tableWidget.horizontalHeader().setStretchLastSection(True)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch)
                    self.tableWidget.insertRow(rowPosition)
                    id_holder.append(records[i][0])


    def edit_existing(self):

        s=self.tableWidget.currentRow()

        if s!=-1:
                            add_or_edit.clear()
                            type_edit.clear()
                            table_row.append(s)
                            add_or_edit.append(2)

                            co = self.db_connection.cursor()
                            selected_id = id_holder[table_row[0]]
                            co.execute(f"select * from City where id={selected_id} order by city_name")
                            records=co.fetchall()
                            for i in range(3):
                                     type_edit.append(str(records[0][i]))

                            self.W = Add_city(self.db_connection)
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
                buttonReply = QMessageBox.question(self, 'Warning', "Do You Want To Permanently Delete Your Record?", QMessageBox.Yes | QMessageBox.No )


                if buttonReply == QMessageBox.Yes:
                    table_row.append(s)

                    selected_id = id_holder[table_row[0]]

                    self.db_connection.execute(f"DELETE from City WHERE id={selected_id}")

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
    window = CitiesWindow()
    sys.exit(app.exec_())