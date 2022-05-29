from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3
from cities import CitiesWindow
from contacts import ContactsWindow
db=sqlite3.connect('main.sqlite')
db.execute('''create table if not exists City
( id integer primary key,
  city_name string,
  city_code integer 
)''')
db.execute('''create table if not exists Contacts
(         id integer primary key,
          first_name  string,
          last_name   string,
          phone_no    string,
          city_id integer references City on update cascade on delete restrict 
)''')

class window(QMainWindow):
    def __init__(self):
       super().__init__()

       buttons_info=[('Contacts','Create or edit contacts ',"background-color : lavender",0,0,self.window1),
                     ('Cities','Define Cities ',"background-color : lavender",160, 0,self.window2)]
       for i in range(len(buttons_info)):
           self.b=QPushButton(buttons_info[i][0], self)
           self.b.setToolTip(buttons_info[i][1])
           self.b.setStyleSheet(buttons_info[i][2])
           self.b.setGeometry(200, 150, 150, 40)
           self.b.move(buttons_info[i][3],buttons_info[i][4])
           self.b.clicked.connect(buttons_info[i][5])
       self.main_window()

    def main_window(self):
        self.setStyleSheet("background-color: slategray;")
        self.setWindowTitle("Contact Book")
        self.setGeometry(0, 0,309, 150)
        self.show()

    def window1(self):
        self.w = ContactsWindow(db)
        self.w.show()

    def window2(self):
        self.w = CitiesWindow(db)
        self.w.show()
def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)

if __name__ == "__main__":
    sys.excepthook=excepthook
    app = QApplication(sys.argv)
    window = window()
    sys.exit(app.exec_())

