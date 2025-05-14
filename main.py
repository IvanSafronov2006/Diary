# Подключение библиотек
import sys
import sqlite3
# Библиотеки PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem


# Окно входа
class Login_window(QMainWindow):
    # Функция иницилизации
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('login_window.ui', self)
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Удаление "Заголовка окна"
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Расширение окна до полноэкранного режима
        self.showMaximized()
        # Добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        # Подключение кнопок к функциям
        self.exit_button.clicked.connect(self.exit)
        self.login_button.clicked.connect(self.gateway)
        self.registration_button.clicked.connect(self.registration)
        self.old_pos = None

# Конец блока

    # Закрыть приложение
    def exit(self):
        self.close()

    # Вход в систему
    def gateway(self):
        # Список логинов
        result_1 = basa_cursor.execute('''SELECT login FROM People''').fetchall()
        spis_with_login = []
        for i in result_1:
            spis_with_login.append(i[0])
        # Проверка на существование логина и корректнось пароля
        if self.login.text() in spis_with_login:
            peop = basa_cursor.execute('''SELECT * FROM People WHERE login = (?)''', (self.login.text(),)).fetchall()[0]
            if peop[3] == self.password.text():
                #main_window.set_id_gateway(peop[0])
                # Сохранение id пользователя
                id_gateway = open('id_gateway.txt', 'w+')
                id_gateway.write(str(peop[0]))
                # Открытие окна меню
                res = self.basa_cursor.execute('''SELECT id FROM People WHERE login=(?)''', (self.login.text(),)).fetchall()[-1][0]
                main_window.set_id(res)
                main_window.set_name(peop[1])
                main_window.show()
                self.close()
            else:
                # Ошибка
                self.error.setText('Неверный логин или пароль.')
        else:
            # Ошибка
            self.error.setText('Неверный логин или пароль.')

    # Регистрация в систему
    def registration(self):
        registration_window.show()
        self.close()


class Registration_window(QMainWindow):
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('registration_window.ui', self)
        # Расширение окна до полноэкранного режима
        self.showMaximized()
        # Удаление "Заголовка" приложения
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Подключение кнопок
        self.registration_button.clicked.connect(self.check)
        self.exit_button.clicked.connect(self.exit)
        self.old_pos = None

    # Функция проверки и добавления в базу данных
    def check(self):
        # Получение информации из окна
        name = str(self.name.text())
        login = str(self.login.text())
        password_1 = str(self.password.text())
        password_2 = str(self.password_2.text())
        in_text = True
        # Получение всех логинов, во избежания повторения
        res_l = self.basa_cursor.execute('''SELECT login FROM People''').fetchall()
        logins = []
        for i in res_l:
            logins.append(i[0])
        # Проверка на содержания полей
        text = 'qwertyuiopasdfghjklzxcvbnm йцукенгшщзхъэждлорпавыфячсмитьбю_QWERTYUIOPLKJHGFDSAZXCVBNM ЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ 1234567890'
        t_1 = '@.'
        for i in name:
            if i not in text:
                in_text = False
        for i in login:
            if (i not in text) and (i not in t_1):
                in_text = False
        for i in password_1:
            if i not in text:
                in_text = False
        is_check = True
        # Проверка на корректность длинны
        if ((len(name) <= 3) or (len(name) >= 51)) or ((len(password_1) <= 3) or (len(password_1) >= 51)) or ((len(login) <= 3) or (len(login) >= 51)) or ((len(password_2) <= 3) or (len(password_2) >= 51)) :
            self.error.setText('Длинна введённых данных должна быть от 4 до 50 символов.')
            is_check = False
        # Проверка на корректность символов
        elif not in_text:
            self.error.setText('Вы можете использовать только цифры, символы латиницы и кирилицы.')
            is_check = False
        # Проверка на незанятость логина
        elif login in logins:
            self.error.setText('Этот логин уже зарегистрирован.')
            is_check = False
        # Проверка на верное повторение пароля
        elif password_1 != password_2:
            self.error.setText('Пароли не совпадают.')
            is_check = False
        # Добавление в базу данных
        if is_check:
            print(10)
            self.basa_cursor.execute('''INSERT INTO People (name, login, password) VALUES (?, ?, ?)''', (name, login, password_1))
            self.basa_d.commit()
            res = self.basa_cursor.execute('''SELECT * FROM People WHERE login=(?)''', (login,)).fetchall()[-1][0]
            print(12)
            main_window.set_id(res)
            main_window.set_name(name)
            print(14)
            main_window.show()
            self.close()

    # Закрыть приложение
    def exit(self):
        self.close()

class Main_window(QMainWindow):
    # Функция иницилизации
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('main_window.ui', self)
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Удаление "Заголовка окна"
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Расширение окна до полноэкранного режима
        self.showMaximized()
        # Добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        # Подключение кнопок к функциям
        self.p1.clicked.connect(self.inp_1_1)
        self.p2.clicked.connect(self.inp_1_2)
        self.exit_button.clicked.connect(self.exit)
        self.pz.clicked.connect(self.zapis)
        self.pf.clicked.connect(self.open_f)
        self.pr.clicked.connect(self.open_r)
        self.old_pos = None
        self.hide()
        self.calendar.clicked['QDate'].connect(self.click)

    def open_r(self):
        schedule_window.set_id(self.id_peop)
        schedule_window.show()

    def open_f(self):
        finans_window.set_id(self.id_peop)
        finans_window.show()

    def zapis(self):
        zapis_window.set_id(self.id_peop)
        zapis_window.show()

    def add_entries(self, text, date):
        self.basa_cursor.execute('''INSERT INTO Entries (id_people, date, record) VALUES (?, ?, ?)''', (self.id_peop, date, text))
        self.basa_d.commit()
        self.click()

    def add_tasks(self, text, date):
        self.basa_cursor.execute('''INSERT INTO Tasks (id_people, date, task) VALUES (?, ?, ?)''', (self.id_peop, date, text))
        self.basa_d.commit()
        self.click()
        
    def inp_1_1(self):
        input1_window.work(1)
        
    def inp_1_2(self):
        input1_window.work(2)

    def click(self):
        s = self.calendar.selectedDate().toString('dd-MM-yyyy')
        res = self.basa_cursor.execute('''SELECT * FROM Entries WHERE id_people=(?) AND date=(?)''', (self.id_peop, s)).fetchall()
        strok_1 = 'Дела на ' + s + ':'
        for i in enumerate(res):
            strok_1 += '\n'
            strok_1 += str(i[0]+1)
            strok_1 += ') '
            strok_1 += i[1][-1]
        self.pt1.setPlainText(strok_1)
        res = self.basa_cursor.execute('''SELECT * FROM Tasks WHERE id_people=(?)''', (self.id_peop,)).fetchall()
        strok_2 = 'Цели:'
        for i in res:
            d1, m1, y1 = list(map(int, i[1].split('-')))
            d2, m2, y2 = list(map(int, s.split('-')))
            a = y2<y1
            b = (y2==y1) and (m2<m1)
            c = (y2==y1) and (m2==m1) and (d2<=d1)
            if a or b or c:
                strok_2 += '\n'
                strok_2 += 'До '
                strok_2 += i[1]
                strok_2 += ' '
                strok_2 += i[-1]
        self.pt2.setPlainText(strok_2)
        

    def set_id(self, id_p):
        self.id_peop = id_p
        self.click()
        
    # Закрыть приложение
    def exit(self):
        self.close()

    def set_name(self, name):
        self.name.setText(name)


class Put_window(QMainWindow):
    # Функция иницилизации
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('input_1.ui', self)
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Закрепление размера
        self.setFixedSize(500, 200)
        # Добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        # Подключение кнопок к функциям
        self.pushButton.clicked.connect(self.retur)
        self.hide()

    def retur(self):
        tx = self.lineEdit.text()
        date = self.dateEdit.dateTime().toString('dd-MM-yyyy')
        if self.type_ == 1:
            main_window.add_entries(tx, date)
        else:
            main_window.add_tasks(tx, date)
        self.hide()
        
    def work(self, n):
        self.show()
        self.type_ = n


class Zapis_window(QMainWindow):
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('zapis_window.ui', self)
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Закрепление размера
        self.setFixedSize(600, 800)
        # Добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        self.p1.clicked.connect(self.previous)
        self.p2.clicked.connect(self.next)
        self.ps.clicked.connect(self.soxr)
        self.pp.clicked.connect(self.perexod)
        # Подключение кнопок к функциям
        self.hide()

    def perexod(self):
        a = self.pt.toPlainText()
        if self.now in list(self.slov.keys()):
            self.basa_cursor.execute('''UPDATE Notepad SET note=(?) WHERE id_people=(?) AND page=(?)''', (a, self.id_peop, self.now))
            self.basa_d.commit()
            self.slov[self.now] = a
        else:
            self.basa_cursor.execute('''INSERT INTO Notepad (id_people, page, note) VALUES (?, ?, ?)''', (self.id_peop, self.now, a))
            self.basa_d.commit()
            self.slov[self.now] = a
        a = self.spinBox.value()
        self.now = a
        self.label.setText('Текущая страница: ' + str(self.now))
        if self.now in list(self.slov.keys()):
            self.pt.setPlainText(self.slov[self.now])
        else:
            self.pt.setPlainText('')

    def soxr(self):
        a = self.pt.toPlainText()
        if self.now in list(self.slov.keys()):
            self.basa_cursor.execute('''UPDATE Notepad SET note=(?) WHERE id_people=(?) AND page=(?)''', (a, self.id_peop, self.now))
            self.basa_d.commit()
            self.slov[self.now] = a
        else:
            self.basa_cursor.execute('''INSERT INTO Notepad (id_people, page, note) VALUES (?, ?, ?)''', (self.id_peop, self.now, a))
            self.basa_d.commit()
            self.slov[self.now] = a

    def previous(self):
        a = self.pt.toPlainText()
        if self.now in list(self.slov.keys()):
            self.basa_cursor.execute('''UPDATE Notepad SET note=(?) WHERE id_people=(?) AND page=(?)''', (a, self.id_peop, self.now))
            self.basa_d.commit()
            self.slov[self.now] = a
        else:
            self.basa_cursor.execute('''INSERT INTO Notepad (id_people, page, note) VALUES (?, ?, ?)''', (self.id_peop, self.now, a))
            self.basa_d.commit()
            self.slov[self.now] = a
        if self.now > 0:
            self.now -= 1
            self.label.setText('Текущая страница: ' + str(self.now))
            if self.now in list(self.slov.keys()):
                self.pt.setPlainText(self.slov[self.now])
            else:
                self.pt.setPlainText('')
                
    def next(self):
        a = self.pt.toPlainText()
        if self.now in list(self.slov.keys()):
            self.basa_cursor.execute('''UPDATE Notepad SET note=(?) WHERE id_people=(?) AND page=(?)''', (a, self.id_peop, self.now))
            self.basa_d.commit()
            self.slov[self.now] = a
        else:
            self.basa_cursor.execute('''INSERT INTO Notepad (id_people, page, note) VALUES (?, ?, ?)''', (self.id_peop, self.now, a))
            self.basa_d.commit()
            self.slov[self.now] = a
        if self.now < 99:
            self.now += 1
            self.label.setText('Текущая страница: ' + str(self.now))
            if self.now in list(self.slov.keys()):
                self.pt.setPlainText(self.slov[self.now])
            else:
                self.pt.setPlainText('')
                

    def set_id(self, id_peop):
        self.id_peop = id_peop
        res = self.basa_cursor.execute('''SELECT * FROM Notepad WHERE id_people=(?)''', (self.id_peop,)).fetchall()
        self.slov = {}
        for i in res:
            self.slov[i[1]] = i[2]
        a = self.spinBox.value()
        self.now = a
        self.label.setText('Текущая страница: ' + str(a))
        if a in list(self.slov.keys()):
            self.pt.setPlainText(self.slov[a])
        else:
            self.pt.setPlainText('')

class Finans_window(QMainWindow):
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('finans_window.ui', self)
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Закрепление размера
        self.setFixedSize(600, 800)
        # Добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        self.pb1.clicked.connect(self.add)
        self.pb2.clicked.connect(self.delet)
        # Подключение кнопок к функциям
        self.hide()
        self.t1 = 'Доходы:'
        self.t2 = 'Расходы:'

    def add(self):
        try:
            a = int(self.line1.text())
            b = self.line2.text()
            self.basa_cursor.execute('''INSERT INTO Wallet (id_people, type, count, comment) VALUES (?, ?, ?, ?)''', (self.id_peop, 1, a, b))
            self.basa_d.commit()
            s = '\n' + str(a) + ' - ' + b
            self.summ += a
            self.t1 = self.t1.split('\n')[0] + '\n' + s + '\n'.join(self.t1.split('\n')[1:])
            self.p1.setPlainText(self.t1)
            if self.summ <= 100000:
                self.number.display(self.summ)
        except:
            print('Error')

    def delet(self):
        try:
            a = int(self.line1.text())
            b = self.line2.text()
            self.basa_cursor.execute('''INSERT INTO Wallet (id_people, type, count, comment) VALUES (?, ?, ?, ?)''', (self.id_peop, 2, a, b))
            self.basa_d.commit()
            s = '\n' + str(a) + ' - ' + b
            self.summ -= a
            self.t2 = self.t2.split('\n')[0] + '\n' + s + '\n'.join(self.t2.split('\n')[1:])
            self.p2.setPlainText(self.t2)
            if self.summ <= 100000:
                self.number.display(self.summ)
        except:
            print('Error')


    def set_id(self, id_peop):
        self.id_peop = id_peop
        a = self.basa_cursor.execute('''SELECT * FROM Wallet WHERE id_people=(?)''', (self.id_peop,)).fetchall()
        self.summ = 0
        for i in a[::-1]:
            if i[1] == 1:
                self.t1 += '\n' + str(i[2]) + ' - ' + str(i[3])
                self.summ += i[2]
            else:
                self.t2 += '\n' + str(i[2]) + ' - ' + str(i[3])
                self.summ -= i[2]
        self.p1.setPlainText(self.t1)
        self.p2.setPlainText(self.t2)
        self.number.setDigitCount(12)
        if self.summ <= 10000:
            self.number.display(self.summ)


class Schedule_window(QMainWindow):
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('schedule_window.ui', self)
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Закрепление размера
        self.setFixedSize(600, 800)
        # Добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        # Подключение кнопок к функциям
        self.pushButton.clicked.connect(self.save)
        self.hide()

    def save(self):
        res = self.basa_cursor.execute('''SELECT * FROM Schedule WHERE id_people=(?)''', (self.id_peop,)).fetchall()
        if len(res)!=0:
            self.basa_cursor.execute('''UPDATE Schedule SET text1=(?) WHERE id_people=(?)''', (self.plainTextEdit.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text2=(?) WHERE id_people=(?)''', (self.plainTextEdit_2.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text3=(?) WHERE id_people=(?)''', (self.plainTextEdit_3.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text4=(?) WHERE id_people=(?)''', (self.plainTextEdit_4.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text5=(?) WHERE id_people=(?)''', (self.plainTextEdit_5.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text6=(?) WHERE id_people=(?)''', (self.plainTextEdit_6.toPlainText(), self.id_peop))
            basa_d.commit()
        else:
            self.basa_cursor.execute('''INSERT INTO Schedule (id_people, text1, text2, text3, text4, text5, text6) VALUES (?, ?, ?, ?, ?, ?, ?)''', (self.id_peop, '1', '1', '11','1','1','111'))
            basa_d.commit()
            self.basa_cursor.execute('''UPDATE Schedule SET text1=(?) WHERE id_people=(?)''', (self.plainTextEdit.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text2=(?) WHERE id_people=(?)''', (self.plainTextEdit_2.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text3=(?) WHERE id_people=(?)''', (self.plainTextEdit_3.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text4=(?) WHERE id_people=(?)''', (self.plainTextEdit_4.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text5=(?) WHERE id_people=(?)''', (self.plainTextEdit_5.toPlainText(), self.id_peop))
            self.basa_cursor.execute('''UPDATE Schedule SET text6=(?) WHERE id_people=(?)''', (self.plainTextEdit_6.toPlainText(), self.id_peop))
            basa_d.commit()

    def set_id(self, id_peop):
        self.id_peop = id_peop
        res = self.basa_cursor.execute('''SELECT * FROM Schedule WHERE id_people=(?)''', (self.id_peop,)).fetchall()
        if len(res)!=0:
            self.plainTextEdit.setPlainText(str(res[0][1]))
            self.plainTextEdit_2.setPlainText(str(res[0][2]))
            self.plainTextEdit_3.setPlainText(str(res[0][3]))
            self.plainTextEdit_4.setPlainText(str(res[0][4]))
            self.plainTextEdit_5.setPlainText(str(res[0][5]))
            self.plainTextEdit_6.setPlainText(str(res[0][6]))

        
if __name__ == '__main__':
    # База данных
    basa_d = sqlite3.connect('basa.db')
    basa_cursor = basa_d.cursor()
    # Создание окон
    app = QApplication(sys.argv)
    # Окно входа
    login_window = Login_window(basa_d)
    login_window.setObjectName("Вход")
    login_window.setStyleSheet("#Вход{border-image:url(photo.png)}")
    # Окно регистрации
    registration_window = Registration_window(basa_d)
    registration_window.setObjectName("Регистрация")
    registration_window.setStyleSheet("#Регистрация{border-image:url(photo.png)}")
    # Окно главного меню
    main_window = Main_window(basa_d)
    main_window.setObjectName("Ежедневник")
    main_window.setStyleSheet("#Ежедневник{border-image:url(photo_2.png)}")
    # Окна создания задач
    input1_window = Put_window(basa_d)
    input1_window.setObjectName("Ежедневник")
    input1_window.setStyleSheet("#Ежедневник{border-image:url(photo_2.png)}")
    # Окно блокнота
    zapis_window = Zapis_window(basa_d)
    zapis_window.setObjectName("Ежедневник")
    zapis_window.setStyleSheet("#Ежедневник{border-image:url(photo_2.png)}")
    # Окно финансов
    finans_window = Finans_window(basa_d)
    finans_window.setObjectName("Ежедневник")
    finans_window.setStyleSheet("#Ежедневник{border-image:url(photo_2.png)}")
    # Окно расписания
    schedule_window = Schedule_window(basa_d)
    schedule_window.setObjectName("Ежедневник")
    schedule_window.setStyleSheet("#Ежедневник{border-image:url(photo_3.png)}")
    # Начало работы
    login_window.show()
    # Конец работы
    sys.exit(app.exec_())
    # Сохранение базы данных
    basa_d.commit()
    basa_d.close()
    basa_cursor.close()
