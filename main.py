import sys
from typing import Union

import datetime
import time

from VKBDposter import VKBDposter
from pathlib import Path #Если захочется менять картинку

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QPushButton, QCalendarWidget,
                             QDialog, QTimeEdit, QLineEdit, QCheckBox)
from PyQt6.QtCore import QDate, QTime, Qt, QDateTime
from PyQt6.QtGui import QPixmap

class DateTimePicker(QWidget):
    """Класс с логикой ui"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добромёт")

        layout = QVBoxLayout()

        self.selected_date = QDate.currentDate()  # значение по умолчанию
        self.selected_time = QTime.currentTime()   # значение по умолчанию

        #Тоггл на отложенный пост
        self.Postpone_toggle = QCheckBox("Отложенный пост")
        self.Postpone_toggle.setChecked(False)
        self.Postpone_toggle.stateChanged.connect(self.Postponed_Toggle)
        layout.addWidget(self.Postpone_toggle)

        # Значения по умолчанию
        self.date_start = self.selected_date.toString("dd-MM-yyyy") if not self.Postpone_toggle.isChecked() else self.date_end
        self.date_end = self.selected_date.addDays(7).toString("dd-MM-yyyy") if not self.Postpone_toggle.isChecked() else self.date_end
        self.Post_date = QDateTime(self.selected_date, self.selected_time).toString(("dd-MM-yyyy"))
        self.UniDate = int(QDateTime(self.selected_date, self.selected_time).toSecsSinceEpoch())

        #Выбор др
        self.BDlabel = QLabel("Выберите дату рождения (день и месяц):")
        layout.addWidget(self.BDlabel)

        #Строка для дня
        BD_layout = QHBoxLayout()

        self.BD_day_label = QLineEdit()
        self.BD_day_label.setMaxLength(2)
        self.BD_day_label.setText(f"{self.selected_date.day()}")
        #Привязка к функции, проверяющей, что ввод 1<x<31
        self.BD_day_label.textChanged.connect(self.Validate_day_input)
        BD_layout.addWidget(self.BD_day_label)

        #Строка для месяца
        self.BD_month_label = QLineEdit()
        self.BD_month_label.setMaxLength(2)
        self.BD_month_label.setText(f"{self.selected_date.month()}")
        # Привязка к функции, проверяющей, что ввод 1<x<12
        self.BD_month_label.textChanged.connect(self.Validate_month_input)
        BD_layout.addWidget(self.BD_month_label)

        layout.addLayout(BD_layout)

        #Выбор даты и времени поста
        self.Post_date_label = QLabel("Выберите дату публикации:")
        layout.addWidget(self.Post_date_label)

        # Кнопка для выбора даты
        self.Post_date_button = QPushButton("Выбрать дату")
        self.Post_date_button.clicked.connect(lambda: self.show_calendar(self.Post_date_display))
        layout.addWidget(self.Post_date_button)
        self.Post_date_display = QLineEdit()
        self.Post_date_display.setReadOnly(True)
        self.Post_date_display.setText(self.Post_date)
        layout.addWidget(self.Post_date_display)

        #Выбор времени публикации
        time_layout = QHBoxLayout()

        self.time_label = QLabel("Выберите время:")
        time_layout.addWidget(self.time_label)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())  # устанавливаем текущее время
        time_layout.addWidget(self.time_edit)

        layout.addLayout(time_layout)

        #Выбор даты начала скидки
        self.Sale_date_label = QLabel("Выберите дату начала скидки:")
        layout.addWidget(self.Sale_date_label)

        # Кнопка для выбора даты
        self.Sale_date_button = QPushButton("Выбрать дату")
        self.Sale_date_button.clicked.connect(lambda: self.show_calendar(self.Sale_date_display))
        layout.addWidget(self.Sale_date_button)
        self.Sale_date_display = QLineEdit()
        self.end_date_display = QLineEdit()
        self.Sale_date_display.setReadOnly(True)
        self.Sale_date_display.setText(self.date_start)
        self.end_date_display.setText(self.date_end)
        layout.addWidget(self.Sale_date_display)

        #Кнопка подтверждения выбора
        self.confirm_button = QPushButton('Подтвердить')
        self.confirm_button.clicked.connect(self.update_result_label)
        layout.addWidget(self.confirm_button)

        #Поля, отображающие выбор
        self.Bresult_label = QLabel("Выбранная дата рождения: ")
        layout.addWidget(self.Bresult_label)
        self.Post_result_label = QLabel("Выбранная дата публикации: ")
        layout.addWidget(self.Post_result_label)
        self.result_label = QLabel("Выбранная дата начала скидки: ")
        layout.addWidget(self.result_label)
        self.End_result_label = QLabel("Выбранная дата окончания скидки скидки: ")
        layout.addWidget(self.End_result_label)

        self.setLayout(layout)

        self.update_result_label()# Задание значений по умолчанию

        #Кнопка запуска
        self.launch_button = QPushButton('Причинить добро')
        self.launch_button.clicked.connect(self.launch_poster)
        layout.addWidget(self.launch_button)

        self.Postponed_Toggle() #Скрытие отложенного поста

    def Validate_day_input(self,text):
        """Функция-ограничитель для дней 1<x<31"""
        if not text:
            return

        try:
            value = int(text)
            if value < 1 or value > 31:
                self.BD_day_label.setText(text[:-1])
                self.BD_day_label.setCursorPosition(len(text[:-1]))
                return
        except ValueError:
            # Если не является целым числом, последний символ удаляется
            self.BD_day_label.setText(text[:-1])
            self.BD_day_label.setCursorPosition(len(text[:-1]))

    def Validate_month_input(self,text):
        """Функция-ограничитель для месяцев 1<x<12"""
        if not text:
            return

        try:
            value = int(text)
            if value < 1 or value > 12:
                self.BD_month_label.setText(text[:-1])
                self.BD_month_label.setCursorPosition(len(text[:-1]))
                return
        except ValueError:
            self.BD_month_label.setText(text[:-1])
            self.BD_month_label.setCursorPosition(len(text[:-1]))

    def Postponed_Toggle(self):
        """Функционал кнопки отложенного поста"""
        if self.Postpone_toggle.isChecked():
            self.setFixedSize(400, 430)

            self.BDlabel.show()
            self.BD_day_label.show()
            self.BD_month_label.show()

            self.Sale_date_label.show()
            self.Sale_date_button.show()
            self.Sale_date_display.show()

            self.Post_date_label.show()
            self.Post_date_button.show()
            self.Post_date_display.show()
            self.time_label.show()
            self.time_edit.show()

            self.confirm_button.show()
            self.Bresult_label.show()
            self.Post_result_label.show()
            self.result_label.show()
            self.End_result_label.show()
        else:
            self.setFixedSize(400, 100)
            self.BDlabel.hide()
            self.BD_day_label.hide()
            self.BD_month_label.hide()

            self.Sale_date_label.hide()
            self.Sale_date_button.hide()
            self.Sale_date_display.hide()


            self.Post_date_label.hide()
            self.Post_date_button.hide()
            self.Post_date_display.hide()

            self.time_label.hide()
            self.time_edit.hide()

            self.confirm_button.hide()
            self.Bresult_label.hide()
            self.Post_result_label.hide()
            self.result_label.hide()
            self.End_result_label.hide()

    def show_calendar(self, Caller: QLineEdit):
        """Отображает диалог с QCalendarWidget для выбора даты."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбрать дату")
        dialog.setModal(True)
        dialog.setWindowFlag(Qt.WindowType.Window)

        calendar = QCalendarWidget(dialog)
        calendar.setSelectedDate(self.selected_date) # устанавливаем ранее выбранную дату

        def select_date():
          self.selected_date = calendar.selectedDate()
          if Caller == self.Post_date_display:
            Caller.setText(self.selected_date.toString("dd.MM.yyyy")) # меняем текст в поле ввода
          else:
            Caller.setText(self.selected_date.toString("dd.MM.yyyy"))  # меняем текст в поле ввода
            self.end_date_display.setText(self.selected_date.addDays(7).toString("dd.MM.yyyy"))

          dialog.close()

        button_ok = QPushButton("ОК", dialog)
        button_ok.clicked.connect(select_date)
        button_cancel = QPushButton("Отмена", dialog)
        button_cancel.clicked.connect(dialog.close)

        cal_layout = QVBoxLayout()
        cal_layout.addWidget(calendar)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(button_ok)
        buttons_layout.addWidget(button_cancel)
        cal_layout.addLayout(buttons_layout)
        dialog.setLayout(cal_layout)

        dialog.exec()

    def update_result_label(self):
        """Обновляем текст с выбранной датой и временем"""
        try:
            #Обновление данных полей
            self.date_start = self.Sale_date_display.text() if self.Postpone_toggle.isChecked() else self.date_start
            self.date_end = self.end_date_display.text() if self.Postpone_toggle.isChecked() else self.date_end
            self.Post_date = self.Post_date_display.text() if self.Postpone_toggle.isChecked() else self.Post_date
            self.Post_date = f"{self.Post_date} {self.time_edit.text()}"
            self.BDdate = f"{self.BD_day_label.text()}.{self.BD_month_label.text()}"

            if self.Postpone_toggle.isChecked():
                date_format = '%d.%m.%Y %H:%M'
                date_format_disc = '%d.%m.%Y'
                #Проверки установленных дат на "будущее"
                Chron = datetime.datetime.now()
                self.UniDate = datetime.datetime.strptime(self.Post_date, date_format)
                self.Discount = datetime.datetime.strptime(self.date_start, date_format_disc)
                if self.UniDate < Chron:
                    raise Exception('Дата публикации отложенного поста не может быть раньше текущей даты (и времени)')
                if self.Discount < Chron:
                    raise Exception('Дата начала скидки не может быть раньше текущей даты')
                #Перевод времени в unix (для вк)
                self.UniDate = int(time.mktime(self.UniDate.timetuple()))

            #Обновление самих строк с текстом
            self.Bresult_label.setText(f"Выбранная дата рождения: {self.BDdate}")
            self.Post_result_label.setText(f"Выбранная дата публикации: {self.Post_date}")
            self.result_label.setText(f"Выбранная дата начала скидки: {self.date_start}")
            self.End_result_label.setText(f"Выбранная дата окончания скидки: {self.date_end}")

            return self.UniDate, self.BDdate, self.date_start, self.date_end
        except Exception as e:
            #Обработка ошибок
            self.Errorist("Ошибкаааааа!!!11", "erricon.png", str(e))

    def Errorist(self, Title: str, Icon_path: Union[str, Path], e: Exception):
        """Функция поп-апов (ошибки и окно "успеха")"""
        dialog = QDialog()
        dialog.setWindowTitle(Title)

        icon_label = QLabel()
        pixmap = QPixmap(Icon_path) #Указан тип строки или пути, если захочется потом поменять иконку или добавить возможность пользователю кастомизировать её
        icon_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

        text_label = QLabel(e)
        text_label.setWordWrap(True)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)

        hbox = QHBoxLayout()
        hbox.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignLeft)
        hbox.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignLeft)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignRight)

        dialog.setLayout(vbox)
        dialog.exec()
        return dialog

    def launch_poster(self):
        """Функция запуска поста"""
        if self.Postpone_toggle.isChecked():
            try:
                VKBDposter(UniDate=self.UniDate, BD = self.BDdate, date_start=self.date_start, date_end=self.date_end)
                #Вызов окна успеха операции
                self.Errorist("Ура!", "success.png", "Распределение добра завершено")
            except Exception as e:
                self.Errorist("Ошибкаааааа!!!11", "erricon.png", str(e))
        else:
            #Создание поста со стандартными значениями
            try:
                VKBDposter(UniDate=None, BD=None, date_start=None, date_end=None)
                # Вызов окна успеха операции
                self.Errorist("Ура!", "success.png", "Распределение добра завершено")
            except Exception as e:
                self.Errorist("Ошибкаааааа!!!11", "erricon.png", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DateTimePicker()
    window.show()
    sys.exit(app.exec())