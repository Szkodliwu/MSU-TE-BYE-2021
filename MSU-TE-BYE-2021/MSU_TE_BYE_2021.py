# Подключаем нужные библиотеки
# Стандартные
import os
import sys

# Библиотеки PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

# переменные которые нужны для скрывания toolbar's
tf = True
te = True
tfor = True
ts = True
tst = True

class MainWindow(QMainWindow):
    
    # Конструктор
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setGeometry(100, 100, 900, 600) # Установка геометрии окна
        self.setWindowIcon(QIcon("images/иконка.png"))
        layout = QVBoxLayout() # Создание макета
        self.editor = QTextEdit(self) # Создание объекта QTextEdit

        # Установка шрифта в редакторе 
        fixedfont  = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        self.path = None #

        layout.addWidget(self.editor) # Добавление редактора в макет

        container = QWidget() # Создание макета QWidget
        container.setLayout(layout) # Установка макета в контейнер
        self.setCentralWidget(container) # Устанавливает контейнер центральным виджетом

        self.status = QStatusBar() # Cоздание объекта строки состояния 
        self.setStatusBar(self.status) # Установка панели статистики в окно

        #######################################################################################

        self.file_toolbar = QToolBar('Файл') # Cоздание файловой панели инструментов
        self.file_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.file_toolbar) # Добавление панели инструментов файла в окно
        file_menu = self.menuBar().addMenu('&Файл') # Создание файлового меню

        # Создание действий для добавления в меню файла
        new_file_action = QAction(QIcon(os.path.join('images', 'новый-файл.png')), 'Новый файл', self) # Создание действия с открытым файлом
        new_file_action.setStatusTip('Новый файл') # Установка подсказки по статусу 
        new_file_action.triggered.connect(self.new_file) # Добавление действия к открытому файлу
        file_menu.addAction(new_file_action) # Добавление этого в меню файла
        self.file_toolbar.addAction(new_file_action) # Добавление этого на панель инструментов

        # Создание действий для добавления в меню файла
        open_file_action = QAction(QIcon(os.path.join('images', 'открыть-файл.png')), 'Открыть файл', self) # Создание действия с открытым файлом
        open_file_action.setStatusTip('Открыть файл') # Установка подсказки по статусу 
        open_file_action.triggered.connect(self.file_open) # Добавление действия к открытому файлу
        file_menu.addAction(open_file_action) # Добавление этого в меню файла
        self.file_toolbar.addAction(open_file_action) # Добавление этого на панель инструментов

        # Создание действий для сохранения файла
        save_file_action = QAction(QIcon(os.path.join('images', 'сохранить-файл.png')), 'Сохранить', self)
        save_file_action.setStatusTip('Сохранить текущий файл')
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        self.file_toolbar.addAction(save_file_action)

        # Создание действий для сохранения файла в указанный им путь
        saveas_file_action = QAction(QIcon(os.path.join('images', 'сохранить.как-файл.png')), 'Сохранить как', self)
        saveas_file_action.setStatusTip('Сохранить текущий файл в указанный путь')
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        self.file_toolbar.addAction(saveas_file_action)

        file_menu.addSeparator() # Добавление полоски
        self.file_toolbar.addSeparator() # Добавление полоски

        # Создание действий для печати файла
        print_action = QAction(QIcon(os.path.join('images', 'печать.png')), 'Печать', self)
        print_action.setStatusTip('Печать текущего файла')
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        self.file_toolbar.addAction(print_action)

        # Создание действий для предварительный просмотра печати файла
        printPreview_action = QAction(QIcon(os.path.join('images', 'предварительный просмотр печати.png')), 'Предварительный просмотр печати', self)
        printPreview_action.setStatusTip('Предварительный просмотр печати текущего файла')
        printPreview_action.triggered.connect(self.file_Previewprint)
        file_menu.addAction(printPreview_action)
        self.file_toolbar.addAction(printPreview_action)

        # Создание действий для экспортирование файла в PDF
        pdf_action = QAction(QIcon(os.path.join('images', 'pdf.png')), 'Эскпортирование в PDF', self)
        pdf_action.setStatusTip('Экспортирование текущего файла в PDF формат')
        #pdf_action.triggered.connect(self.file_pdf)
        file_menu.addAction(pdf_action)
        self.file_toolbar.addAction(pdf_action)

        file_menu.addSeparator() # Добавление полоски

        # Создание действий для выхода из приложения
        exit_action = QAction(QIcon(os.path.join('images', 'выйти.png')), "Выйти из приложения", self)
        exit_action.setStatusTip("Выход из приложения")
        exit_action.triggered.connect(self.exit)
        file_menu.addAction(exit_action)

        self.edit_toolbar = QToolBar("Редактирование") # Создание еще одной панели инструментов для редактирования текста
        self.edit_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.edit_toolbar) # Добавляем эту панель инструментов в главное окно
        edit_menu = self.menuBar().addMenu("&Редактирование") # Создание строки меню редактирования

        # Добавление действий на панель инструментов и строку меню

        # Создание отмены действия 
        undo_action = QAction(QIcon(os.path.join('images', 'отменить.png')), "Отменить", self)
        undo_action.setStatusTip("Отменить последнее изменение")
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.editor.undo)
        self.edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        # Создание возращения отмены действия
        redo_action = QAction(QIcon(os.path.join('images', 'повторить.png')), 'Повторить', self)
        redo_action.setStatusTip('Повторить последнее изменение')
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.editor.redo)
        self.edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator() # Добавление полоски
        self.edit_toolbar.addSeparator() # Добавление полоски

        # Действие вырезания
        cut_action = QAction(QIcon(os.path.join('images', 'вырезать.png')), 'Вырезать', self)
        cut_action.setStatusTip('Вырезать выделенный текст')
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        self.edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        # Действие копирования
        copy_action = QAction(QIcon(os.path.join('images', 'скопировать.png')), "Копировать", self)
        copy_action.setStatusTip("Копировать выделенный текст")
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        self.edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        # Действие вставки
        paste_action = QAction(QIcon(os.path.join('images', 'вставить.png')), "Вставить", self)
        paste_action.setStatusTip("Вставить из буфера обмена")
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        self.edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        self.format_toolbar = QToolBar("Формат")
        self.format_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.format_toolbar)
        format_menu = self.menuBar().addMenu("&Формат")

        # Добавление действий на панель инструментов и строку меню

        # Создание изменения шрифта
        font_action = QAction(QIcon(os.path.join('images', 'хирагана-ма.png')), 'Шрифт', self)
        font_action.setStatusTip('Изменения шрифта')
        font_action.triggered.connect(self.font)
        self.format_toolbar.addAction(font_action)
        format_menu.addAction(font_action)

        # Создание изменения цвета
        color_action = QAction(QIcon(os.path.join('images', 'цвет.png')), 'Цвет', self)
        color_action.setStatusTip('Изменения цвета')
        color_action.triggered.connect(self.ColorText)
        self.format_toolbar.addAction(color_action)
        format_menu.addAction(color_action)

        highlighter_action = QAction(QIcon(os.path.join('images', 'маркер.png')), 'Текстовыделитель', self)
        highlighter_action.setStatusTip('Текстовыделитель')
        highlighter_action.triggered.connect(self.highlighter)
        self.format_toolbar.addAction(highlighter_action)
        format_menu.addAction(highlighter_action)


        self.style_toolbar = QToolBar("Стиль")
        self.style_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.style_toolbar)
        style_menu = self.menuBar().addMenu("&Стиль")

        # Добавление действий на панель инструментов и строку меню

        bold_action = QAction(QIcon(os.path.join('images', 'жирный.png')), "Жирный", self)
        bold_action.setStatusTip("Жирный")
        bold_action.setShortcut(QKeySequence.Bold)
        bold_action.triggered.connect(self.bold)
        self.style_toolbar.addAction(bold_action)
        style_menu.addAction(bold_action)

        italic_action = QAction(QIcon(os.path.join('images', 'курсив.png')), "Курсив", self)
        italic_action.setStatusTip("Курсив")
        italic_action.setShortcut(QKeySequence.Italic)
        italic_action.triggered.connect(self.italic)
        self.style_toolbar.addAction(italic_action)
        style_menu.addAction(italic_action)

        underline_action = QAction(QIcon(os.path.join('images', 'подчеркивание.png')), "Подчеркнутый", self)
        underline_action.setStatusTip("Подчеркнутый")
        underline_action.setShortcut(QKeySequence.Underline)
        underline_action.triggered.connect(self.underline)
        self.style_toolbar.addAction(underline_action)
        style_menu.addAction(underline_action)

        style_menu.addSeparator() # Добавление полоски
        self.style_toolbar.addSeparator() # Добавление полоски

        alignl_action = QAction(QIcon(os.path.join('images', 'выровнять-по-левому-краю.png')), "Выровнять по левому краю", self)
        alignl_action.setStatusTip("Выровнять текст по левому краю")
        alignl_action.triggered.connect(self.alignl)
        self.style_toolbar.addAction(alignl_action)
        style_menu.addAction(alignl_action)

        alignc_action = QAction(QIcon(os.path.join('images', 'выровнять-по-центру.png')), "Выровнять по центру", self)
        alignc_action.setStatusTip("Выровнять текст по центру")
        alignc_action.triggered.connect(self.alignc)
        self.style_toolbar.addAction(alignc_action)
        style_menu.addAction(alignc_action)

        alignr_action = QAction(QIcon(os.path.join('images', 'выровнять-по-правому-краю.png')), "Выровнять по правому краю", self)
        alignr_action.setStatusTip("Выровнять текст по правому краю")
        alignr_action.triggered.connect(self.alignr)
        self.style_toolbar.addAction(alignr_action)
        style_menu.addAction(alignr_action)

        alignj_action = QAction(QIcon(os.path.join('images', 'выровнять-по-обоим-краям.png')), "Выровнять по обоим краям", self)
        alignj_action.setStatusTip("Выровнять текст по обоим краям")
        alignj_action.triggered.connect(self.alignj)
        self.style_toolbar.addAction(alignj_action)
        style_menu.addAction(alignj_action)

        kind_menu = self.menuBar().addMenu("&Вид")

        toggleFile = QAction(QIcon(os.path.join('images', 'показать.png')), "Скрыть панель файла", self, checkable=True)
        toggleFile.triggered.connect(self.handleToggleFile)
        kind_menu.addAction(toggleFile)

        toggleEdit = QAction(QIcon(os.path.join('images', 'показать.png')), "Скрыть панель редактирования", self, checkable=True)
        toggleEdit.triggered.connect(self.handleToggleEdit)
        kind_menu.addAction(toggleEdit)

        toggleFormat = QAction(QIcon(os.path.join('images', 'показать.png')), "Скрыть панель формата", self, checkable=True)
        toggleFormat.triggered.connect(self.handleToggleFormat)
        kind_menu.addAction(toggleFormat)

        toggleStyle = QAction(QIcon(os.path.join('images', 'показать.png')), "Скрыть панель стиля", self, checkable=True)
        toggleStyle.triggered.connect(self.handleToggleStyle)
        kind_menu.addAction(toggleStyle)

        toggleStatus = QAction(QIcon(os.path.join('images', 'показать.png')), "Скрыть панель статуса", self, checkable=True)
        toggleStatus.triggered.connect(self.handleToggleStatus)
        kind_menu.addAction(toggleStatus)

        self.status = self.statusBar()
        self.editor.cursorPositionChanged.connect(self.CursorPosition)

        about_menu = self.menuBar().addMenu("&Сведения")

        about_action = QAction(QIcon(os.path.join('images', 'информация.png')), "Сведения о проекте", self)
        about_action.triggered.connect(self.about)
        about_menu.addAction(about_action)

        # Иницализация
        self.update_title() # Вызов метода обновления заголовка
        self.show()

    def dialog_critical(self, s): # Создание критического метода диалога (чтобы показать ошибки)
        dlg = QMessageBox(self) # Создание объекта QMessageBox
        dlg.setText(s) # Установка текста в dlg
        dlg.setIcon(QMessageBox.Critical) # Установка значка для него
        dlg.show() # Выводим 


    # Действие, вызываемое действием нового файла
    def new_file(self):
        self.editor.clear() # Очищает editor

    # Действие, вызываемое действием открытия файла
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Открыть файл', '', 'Текстовый файл(*.txt)') # Получение пути и логического значения

        if path: # Если путь верен
            try: # Попробует открыть путь
                with open(path, 'rU') as f:
                    text = f.read() # Читает файл

            except Exception as e: # Если произошла ошибка
                self.dialog_critical(str(e)) # Показать ошибку критическим методом

            else: # Еще
                self.path = path # Обновляет значение пути
                self.editor.setPlainText(text) # Обновляет текст
                self.update_title() # Обновляет заголовок
                 
    def file_save(self):
        if self.path is None:
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Сохранить как', '', 'Текстовый документ(*.txt')

        if not path:
            return
        
        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()

        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def file_Previewprint(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrinterPreviewDialog(printer, self)
        previweDialog.paintRequested.connect(self.printPreviwe)
        previewDialog.exec_()

    def printerPreview(self, printer):
        self.editor.print_(printer)

    def exit(self):
        self.close()

    def undo(self):
        self.editor.undo()

    def redo(self):
        self.editor.redo()

    def cut(self):
        self.editor.cut()

    def copy(self):
        self.editor.copy()

    def paste(self):
        self.editor.paste()

    def font(self, font):
        font, ok = QFontDialog.getFont()

        if ok:
            self.editor.setFont(font)

    def ColorText(self):
        color = QColorDialog.getColor()
        self.editor.setTextColor(color)

    def highlighter(self):
        hr = QColorDialog.getColor()
        self.editor.setTextBackgroundColor(hr)

    def bold(self):
        b = self.editor.fontWeight()
        if b == 50:
            self.editor.setFontWeight(QFont.Bold)
        elif b == 75:
            self.editor.setFontWeight(QFont.Normal)

    # Курсив
    def italic(self):
        i = self.editor.fontItalic()
         
        if i == False:
            self.editor.setFontItalic(True)
        elif i == True:
            self.editor.setFontItalic(False)

    # Подчеркнутый
    def underline(self):
        ul = self.editor.fontUnderline()
 
        if ul == False:
            self.editor.setFontUnderline(True) 
        elif ul == True:
            self.editor.setFontUnderline(False)

    # Выровнять по левому краю
    def alignl(self): 
        self.editor.setAlignment(Qt.AlignLeft)

    # Выровнять по центру
    def alignc(self):
        self.editor.setAlignment(Qt.AlignCenter)

    # Выровнять по правому краю
    def alignr(self):
        self.editor.setAlignment(Qt.AlignRight)

    # Выровнять по обоим краям
    def alignj(self):
        self.editor.setAlignment(Qt.AlignJustify)

    def handleToggleFile(self):
        global tf
 
        if tf == True:
            self.file_toolbar.hide()
            tf = False
        else:
            self.file_toolbar.show()
            tf = True

    def handleToggleEdit(self):
        global te
 
        if te == True:
            self.edit_toolbar.hide()
            te = False
        else:
            self.edit_toolbar.show()
            te = True

    def handleToggleFormat(self):
        global tfor
 
        if tfor == True:
            self.format_toolbar.hide()
            tfor = False
        else:
            self.format_toolbar.show()
            tfor = True

    def handleToggleStyle(self):
        global ts
 
        if ts == True:
            self.style_toolbar.hide()
            ts = False
        else:
            self.style_toolbar.show()
            ts = True

    def handleToggleStatus(self):
        global tst
 
        if tst == True:
            self.status.hide()
            tst = False
        else:
            self.status.show()
            tst = True

    def CursorPosition(self):
        line = self.editor.textCursor().blockNumber()
        col = self.editor.textCursor().columnNumber()
        linecol = ("Строки: "+str(line)+" | "+"Кол-во символов: "+str(col))
        self.status.showMessage(linecol)

    def about(self):
        QMessageBox.about(self, "Сведения", "Это информация об программе")

    # Обновление название файла
    def update_title(self):
        self.setWindowTitle('%s - MSU_TE_BYE_2021' %(os.path.basename(self.path)
                                                     if self.path else 'Безымяный'))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName('MSU_TE_BYE_2021')

    window = MainWindow()
    app.exec_()

