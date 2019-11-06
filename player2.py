import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, \
    QScrollArea, QPushButton, QListWidget, QLineEdit, QRadioButton, QButtonGroup
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
import os
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3
from qtpy import QtGui


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    # создание переменных, списков, словарей; считывание музыкальных файлов из папки
    def initUI(self):
        self.setGeometry(400, 200, 1100, 700)
        self.setWindowTitle('AudioPlayer')

        image = QImage("backgroundv.png")
        image_size = image.scaled(QSize(1100, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(image_size))
        self.setPalette(palette)

        self.filter_field = QLabel(self)
        self.filter_field.move(10, 20)
        self.filter_field.resize(270, 660)
        self.filter_field.setStyleSheet("QLabel { border-style: solid; "
                                        "border-width: 2px; "
                                        "border-color: #7E12AA }")

        self.search = QLineEdit(self)
        self.search.move(20, 70)
        self.search.resize(210, 30)
        self.search.setStyleSheet('QLineEdit { background-color: #FFFFFF }')

        self.searc_button = QPushButton('🔍', self)
        self.searc_button.move(230, 70)
        self.searc_button.resize(30, 30)
        self.searc_button.setStyleSheet('QPushButton { background-color: #CB0077; '
                                        'color: #FFFFFF }')
        self.searc_button.clicked.connect(self.clicked_search_button)

        self.musician = QLabel('Исполнитель: ', self)
        self.musician.move(20, 150)
        self.musician.setStyleSheet('QLabel { color: #FFFFFF }')

        self.artists_list = QComboBox(self)
        self.artists_list.addItem('любой')
        self.artists_list.resize(150, 30)
        self.artists_list.move(110, 150)
        self.artists_list.setStyleSheet('QComboBox { background-color: #FFFFFF }')

        self.year = QLabel('Год: ', self)
        self.year.move(20, 230)
        self.year.setStyleSheet('QLabel { color: #FFFFFF }')

        self._from = QLabel('с', self)
        self._from.move(90, 230)
        self._from.setStyleSheet('QLabel { color: #FFFFFF }')

        self.list_of_years = QComboBox(self)
        self.list_of_years.addItem('любой')
        self.list_of_years.resize(150, 30)
        self.list_of_years.move(110, 230)
        self.list_of_years.setStyleSheet('QComboBox { background-color: #FFFFFF }')

        self._to = QLabel('по', self)
        self._to.move(90, 270)
        self._to.setStyleSheet('QLabel { color: #FFFFFF }')

        self.second_list_of_years = QComboBox(self)
        self.second_list_of_years.addItem('любой')
        self.second_list_of_years.resize(150, 30)
        self.second_list_of_years.move(110, 270)
        self.second_list_of_years.setStyleSheet('QComboBox { background-color: #FFFFFF }')

        self.album = QLabel('Альбом: ', self)
        self.album.move(20, 190)
        self.album.setStyleSheet('QLabel { color: #FFFFFF }')

        self.album_combobox = QComboBox(self)
        self.album_combobox.addItem('любой')
        self.album_combobox.resize(150, 30)
        self.album_combobox.move(110, 190)
        self.album_combobox.setStyleSheet('QComboBox { background-color: #FFFFFF }')

        self.second_search = QPushButton('🔍', self)
        self.second_search.move(20, 330)
        self.second_search.resize(240, 30)
        self.second_search.setStyleSheet('QPushButton { background-color: #CB0077; '
                                         'color: #FFFFFF }')
        self.second_search.clicked.connect(self.clicked_second_search_button)

        self.name = QRadioButton('По названию', self)
        self.name.move(20, 400)
        self.name.setStyleSheet('QRadioButton { color: #FFFFFF }')

        self.length = QRadioButton('По увеличению длительности', self)
        self.length.move(20, 430)
        self.length.resize(255, 20)
        self.length.setStyleSheet('QRadioButton { color: #FFFFFF }')

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.name)
        self.button_group.addButton(self.length)
        self.button_group.buttonClicked.connect(self.radiobutton_clicked)

        self.music_list = QListWidget(self)
        self.music_list.setFont(QtGui.QFont('Consolas'))
        self.music_list.setStyleSheet('QListWidget { background-color: #FFFFFF; '
                                      'color: #000000 }')

        self.area = QScrollArea(self)
        self.area.setWidgetResizable(True)
        self.area.move(290, 220)
        self.area.resize(780, 460)
        self.area.setWidget(self.music_list)

        self.layoutV = QVBoxLayout(self)
        self.layoutV.addWidget(self.area)
        self.setLayout(self.layoutV)

        self.track_info = QLabel(self)
        self.track_info.move(290, 20)
        self.track_info.resize(780, 190)
        self.track_info.setStyleSheet("QLabel { border-width: 2px; "
                                      "border-style: solid; "
                                      "border-color: #7E12AA; "
                                      "background-color: #9015C1 }")

        self.track_name = QLabel(self)
        self.track_name.resize(780, 20)
        self.track_name.move(300, 30)
        self.track_name.setFont(QtGui.QFont('Segoe UI', 10))
        self.track_name.setStyleSheet('QLabel { color: #FFFFFF }')

        self.track_artist = QLabel(self)
        self.track_artist.resize(780, 20)
        self.track_artist.move(300, 60)
        self.track_artist.setFont(QtGui.QFont('Segoe UI', 10))
        self.track_artist.setStyleSheet('QLabel { color: #FFFFFF }')

        self.track_album = QLabel(self)
        self.track_album.resize(780, 20)
        self.track_album.move(300, 90)
        self.track_album.setFont(QtGui.QFont('Segoe UI', 10))
        self.track_album.setStyleSheet('QLabel { color: #FFFFFF }')

        self.track_year = QLabel(self)
        self.track_year.resize(780, 20)
        self.track_year.move(300, 120)
        self.track_year.setFont(QtGui.QFont('Segoe UI', 10))
        self.track_year.setStyleSheet('QLabel { color: #FFFFFF }')

        self.track_length = QLabel(self)
        self.track_length.resize(780, 20)
        self.track_length.move(300, 150)
        self.track_length.setFont(QtGui.QFont('Segoe UI', 10))
        self.track_length.setStyleSheet('QLabel { color: #FFFFFF }')

        self.artists = []

        self.albums = []

        self.years = []

        self.years2 = []

        self.length_of_track = {}

        for file in os.listdir(os.getcwd() + '/music'):
            filename, file_extension = os.path.splitext(os.getcwd() + '/music/' + file)
            if file_extension == '.mp3':
                track = ID3(os.getcwd() + '/music/' + file)
                mp3_track = MP3(os.getcwd() + '/music/' + file)
                tit_num = len(track['TIT2'].text[0])
                space = 77 - tit_num
                self.music_list.addItem(track['TIT2'].text[0] + space * ' ' + track['TPE1'].text[0])
                self.length_of_track[mp3_track.info.length] = track['TIT2'].text[0]
                if track['TPE1'].text[0] not in self.artists:
                    self.artists.append(track['TPE1'].text[0])
                if str(mp3_track['date'])[2:-2] not in self.years:
                    self.years.append(str(mp3_track['date'])[2:-2])
                if str(mp3_track['date'])[2:-2] not in self.years2:
                    self.years2.append(str(mp3_track['date'])[2:-2])
                if track['TALB'].text[0] not in self.albums:
                    self.albums.append(track['TALB'].text[0])
        self.years = sorted(self.years)
        self.years2 = sorted(self.years2)
        for i in self.artists:
            self.artists_list.addItem(i)
        for year in self.years:
            self.list_of_years.addItem(year)
        for year2 in self.years2:
            self.second_list_of_years.addItem(year2)
        for alb in self.albums:
            self.album_combobox.addItem(alb)

        self.music_list.itemClicked.connect(self.clicked_item)

        self.music_list.itemDoubleClicked.connect(self.double_clicked_item)

    # поиск совпадений по исполнителю, названию или альбому
    def clicked_search_button(self):
        line = self.search.text()
        self.music_list.clear()
        for file in os.listdir(os.getcwd() + '/music'):
            filename, file_extension = os.path.splitext(os.getcwd() + '/music/' + file)
            if file_extension == '.mp3':
                track = ID3(os.getcwd() + '/music/' + file)
                if line.lower() in track['TIT2'].text[0].lower() or line in track['TPE1'].text[0].lower() \
                        or line in track['TALB'].text[0].lower():
                    tit_num = len(track['TIT2'].text[0])
                    space = 77 - tit_num
                    self.music_list.addItem(track['TIT2'].text[0] + space * ' ' + track['TPE1'].text[0])

    # фильтр по испонителю, альбому и году
    def clicked_second_search_button(self):
        artist_value = self.artists_list.currentText()
        album_value = self.album_combobox.currentText()
        first_year_value = self.list_of_years.currentText()
        second_year_value = self.second_list_of_years.currentText()
        possible_years = self.years
        if first_year_value != 'любой' and second_year_value != 'любой':
            num1 = self.years.index(first_year_value)
            num2 = self.years.index(second_year_value)
            possible_years = self.years[num1:num2 + 1]
        if first_year_value == 'любой' and second_year_value != 'любой':
            num2 = self.years.index(second_year_value)
            possible_years = self.years[:num2 + 1]
        if first_year_value != 'любой' and second_year_value == 'любой':
            num1 = self.years.index(first_year_value)
            possible_years = self.years[num1:]
        if first_year_value == 'любой' and second_year_value == 'любой':
            possible_years = self.years
        if artist_value == 'любой':
            possible_artist = self.artists
        else:
            possible_artist = [artist_value]
        if album_value == 'любой':
            possible_album = self.albums
        else:
            possible_album = [album_value]

        self.music_list.clear()

        for file in os.listdir(os.getcwd() + '/music'):
            filename, file_extension = os.path.splitext(os.getcwd() + '/music/' + file)
            if file_extension == '.mp3':
                track = ID3(os.getcwd() + '/music/' + file)
                mp3_track = MP3(os.getcwd() + '/music/' + file)
                if track['TPE1'].text[0] in possible_artist and \
                        str(mp3_track['date'])[2:-2] in possible_years \
                        and track['TALB'].text[0] in possible_album:
                    tit_num = len(track['TIT2'].text[0])
                    space = 77 - tit_num
                    self.music_list.addItem(track['TIT2'].text[0] + space * ' ' + track['TPE1'].text[0])

    # сортировка песен по названию или длительности
    def radiobutton_clicked(self, button):
        criterion = button.text()
        all_items = []
        list_of_current_length = {}
        for i in range(self.music_list.count()):
            index = self.music_list.item(i).text().find('   ')
            item = self.music_list.item(i).text()[:index]
            all_items.append(item)
        print(all_items)
        if criterion == 'По увеличению длительности':
            for file in os.listdir(os.getcwd() + '/music'):
                filename, file_extension = os.path.splitext(os.getcwd() + '/music/' + file)
                if file_extension == '.mp3':
                    track = ID3(os.getcwd() + '/music/' + file)
                    if track['TIT2'].text[0] in all_items:
                        mp3_track = MP3(os.getcwd() + '/music/' + file)
                        list_of_current_length[mp3_track.info.length] = track['TIT2'].text[0]
            self.music_list.clear()
            for key, value in sorted(list_of_current_length.items(), key=lambda x: x[0]):
                for file in os.listdir(os.getcwd() + '/music'):
                    filename, file_extension = os.path.splitext(os.getcwd() + '/music/' + file)
                    if file_extension == '.mp3':
                        track = ID3(os.getcwd() + '/music/' + file)
                        if track['TIT2'].text[0] == value:
                            tit_num = len(track['TIT2'].text[0])
                            space = 77 - tit_num
                            self.music_list.addItem(track['TIT2'].text[0] + space * ' ' + track['TPE1'].text[0])
        else:
            self.music_list.sortItems()

    # выведение информации о песне
    def clicked_item(self, item):
        temp_name = item.text()
        number = temp_name.find('   ')
        final_name = temp_name[:number]
        for file in os.listdir(os.getcwd() + '/music'):
            filename, file_extension = os.path.splitext(os.getcwd() + '/music/' + file)
            if file_extension == '.mp3':
                checked_track = ID3(os.getcwd() + '/music/' + file)
                checked_track2 = MP3(os.getcwd() + '/music/' + file)
                if final_name == checked_track['TIT2'].text[0]:
                    self.track_name.clear()
                    self.track_name.setText('Название: ' + checked_track['TIT2'].text[0])
                    self.track_artist.clear()
                    self.track_artist.setText('Исполнитель: ' + checked_track['TPE1'].text[0])
                    self.track_album.clear()
                    self.track_album.setText('Альбом: ' + checked_track['TALB'].text[0])
                    self.track_year.clear()
                    self.track_year.setText('Год: ' + str(checked_track2['date'])[2:-2])
                    self.track_length.clear()
                    self.track_length.setText('Длительность: ' + str(checked_track2.info.length // 60)[0] +
                                              ':' + str(round(checked_track2.info.length % 60)).zfill(2))

    # воспроизведение песни
    def double_clicked_item(self, item):
        name1 = item.text()
        number = name1.find('   ')
        final_name = name1[:number]
        for file in os.listdir(os.getcwd() + '/music'):
            filename, file_extension = os.path.splitext(os.getcwd() + '/music/' + file)
            if file_extension == '.mp3':
                checked_track = ID3(os.getcwd() + '/music/' + file)
                if final_name == checked_track['TIT2'].text[0]:
                    os.startfile(os.getcwd() + '/music/' + file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
