import sys
from PyQt5 import QtWidgets, QtCore, QtNetwork
from bs4 import BeautifulSoup


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(853, 492)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 851, 21))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(0, 0, 111, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.frame)
        self.comboBox_2.setGeometry(QtCore.QRect(130, 0, 111, 21))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(self.frame)
        self.comboBox_3.setGeometry(QtCore.QRect(260, 0, 111, 21))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_4 = QtWidgets.QComboBox(self.frame)
        self.comboBox_4.setGeometry(QtCore.QRect(390, 0, 111, 21))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(739, 0, 91, 21))
        self.pushButton.setObjectName("pushButton")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 30, 851, 461))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.frame_2)
        self.verticalScrollBar.setGeometry(QtCore.QRect(836, 0, 20, 491))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.fetchData)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Thunder Client"))
        self.comboBox.setItemText(0, _translate("Dialog", "Home"))
        self.comboBox.setItemText(1, _translate("Dialog", "Client Update"))
        self.comboBox.setItemText(2, _translate("Dialog", "Quit"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "Library"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "Apps Update"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "Community"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "Image Board"))
        self.comboBox_3.setItemText(2, _translate("Dialog", "Thunder Halls"))
        self.comboBox_4.setItemText(0, _translate("Dialog", "Changelog"))
        self.comboBox_4.setItemText(1, _translate("Dialog", "Dev Blog"))
        self.pushButton.setText(_translate("Dialog", "Reload"))

    def fetchData(self):
        manager = QtNetwork.QNetworkAccessManager()
        manager.finished.connect(self.onDataReceived)
        request = QtNetwork.QNetworkRequest(QtCore.QUrl("https://korrykatti.is-a.dev/thapps/apps/00001.html"))
        manager.get(request)

    def onDataReceived(self, reply):
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            data = reply.readAll()
            soup = BeautifulSoup(data, "html.parser")
            # Extracting data from the HTML
            app_id = soup.find("h1", id="appId").text
            app_name = soup.find("h1", id="appName").text
            icon_url = soup.find("h2", id="iconUrl").text
            version = soup.find("h2", id="version").text
            repo_url = soup.find("h2", id="repoUrl").text
            main_file = soup.find("h2", id="mainFile").text
            description = soup.find("h2", id="description").text

            # Update the UI elements with fetched data
            # Assuming you have QLabel widgets to display the data
            self.label_app_id.setText(app_id)
            self.label_app_name.setText(app_name)
            self.label_icon_url.setText(icon_url)
            self.label_version.setText(version)
            self.label_repo_url.setText(repo_url)
            self.label_main_file.setText(main_file)
            self.label_description.setText(description)
        else:
            print("Error:", reply.errorString())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
