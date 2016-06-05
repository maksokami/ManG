# ManG lets you ping a range of IPs at the same time and see the status.

# ManG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Copyright (C) 2016  Maria Krovatkina
# Email author: maksokami@gmail.com

import sys, logging, os

import mang_utils, time
from mang_ip import MangIP
from mang_tmodel  import MangTableModel
from mang_settings  import MangSettings
from PyQt4 import QtGui, QtCore
from threading import Thread



class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 500, 600)
        self.setWindowTitle('ManG')

        #Main menu
        menu_action1 = QtGui.QAction('&Export to CSV', self)
        menu_action1.setShortcut('Ctrl+S')
        menu_action1.setStatusTip('Export grid output to CSV')
        menu_action1.triggered.connect(self.export_to_csv)
        menu_action2 = QtGui.QAction('&Quit', self)
        menu_action2.setShortcut('Ctrl+Q')
        menu_action2.setStatusTip('Close application')
        menu_action2.triggered.connect(self.close_app)
        menu_action4 = QtGui.QAction('&Settings', self)
        menu_action4.setShortcut('Ctrl+O')
        menu_action4.setStatusTip('Settings')
        menu_action4.triggered.connect(self.settings_dialog)
        menu_action3 = QtGui.QAction('&About', self)
        menu_action3.setShortcut('F1')
        menu_action3.setStatusTip('About')
        menu_action3.triggered.connect(self.about)

        self.statusBar()
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(menu_action1)
        file_menu.addAction(menu_action2)
        file_menu = main_menu.addMenu('&Help')
        file_menu.addAction(menu_action4)
        file_menu.addAction(menu_action3)

        self.custom_show()

    ip_list = []
    ping_interval = 5
    gui_interval = 5
    ping_timeout = 4

    gui_button = None
    gui_grid = None
    gui_edit = None
    gui_grid_model = None
    grid_headers = ['IP', 'Hostname', 'State changes', 'State']
    grid_data = []

    def gui_create_table(self):
        tv = QtGui.QTableView()
        self.gui_grid_model = MangTableModel(self.grid_headers, self)
        self.gui_grid_model.setData(self.grid_data)
        tv.setModel(self.gui_grid_model)

        tv.resizeColumnsToContents()
        tv.resizeRowsToContents()
        tv.resize(tv.sizeHint())
        tv.setSortingEnabled(True)
        return tv

    def gui_grid_resize(self):
        self.gui_grid.resizeColumnsToContents()
        self.gui_grid.resizeRowsToContents()

    def gui_create_label(self):
        fnt = QtGui.QFont("Arial", 11, QtGui.QFont.Bold)
        lb = QtGui.QLabel()
        lb.resize(lb.sizeHint())
        lb.setText(">> MONITORING STOPPED <<")
        lb.setAlignment(QtCore.Qt.AlignLeft)
        lb.setFont(fnt)
        return lb

    def gui_create_button(self):
        bt = QtGui.QPushButton("START", self)
        # gui_button.clicked.connect(QtCore.QCoreApplication.instance().quit) #Exit
        bt.clicked.connect(self.bulk_ping)
        bt.resize(bt.sizeHint())
        bt.setDefault(True)
        return bt

    def gui_create_edit(self):
        ed = QtGui.QLineEdit()
        ed.setText('127.0.0.1')
        ed.resize(ed.sizeHint())
        ed.move(60, 10)
        return ed

    def custom_show(self):
        # Layout
        gl = QtGui.QGridLayout()

        vbl = QtGui.QHBoxLayout()
        vbl.setStretch(1,1)

        self.gui_edit = self.gui_create_edit()      # TextEdit
        self.gui_grid = self.gui_create_table()     # TableGrid
        self.gui_button = self.gui_create_button()  # Start/stop button
        self.gui_label = self.gui_create_label()    # Status label

        vbl.addWidget(self.gui_edit)
        vbl.addWidget(self.gui_button)
        gl.addLayout(vbl, 0, 0)
        gl.addWidget(self.gui_grid, 1,  0)
        gl.addWidget(self.gui_label, 2,  0)

        # Layout
        q = QtGui.QWidget()
        q.setLayout(gl)
        self.setCentralWidget(q)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.show()

    is_start = 0

    def bulk_ping(self):
        self.is_start = not self.is_start
        if not(self.is_start):
            self.gui_button.setText('START')
            self.gui_label.setText("MONITORING STOPPED")
            for val in self.ip_list:
                val.p_stop_thread = 1
                logging.debug("Sending 'end' signal to a thread for IP -  %s", str(val.ip))
        else:
            self.ip_list = []
            # Get a List of IP addresses from the range in QLineEdit
            L = mang_utils.prase_ip_range(str(self.gui_edit.text()))
            logging.debug("IP range parsing - %s", str(L))

            if L:
                self.gui_button.setText('STOP')
                self.gui_label.setText("...MONITORING...")
                for i, val in enumerate(L):
                    tmp_ip = MangIP()
                    tmp_ip.set_ip(val)
                    self.ip_list.append(tmp_ip)
                logging.debug("IP list created parsing -  %s", str(self.ip_list))
                # Start threading
                for i, key in enumerate(self.ip_list):
                    logging.debug("Starting a thread for IP -  %s", str(key.ip))
                    t = Thread(target=key.start_check, args=(self.ping_interval,))
                    t.start()

                logging.debug("Grid refresh thread started")
                t = Thread(target=self.gui_table_refresh, args=(self.gui_interval,))
                t.start()
                self.gui_grid_resize()
            else: # L = None, can't parse IP string
                self.is_start = not self.is_start
                self.error_dialog()

    def gui_table_refresh(self, v_interval):
        while self.is_start:
            self.gui_grid_model.setData(self.ip_list)
            time.sleep(v_interval)
        logging.debug("Grid refresh thread stopped")

    def close_app(self):
        sys.exit()

    def export_to_csv(self):
        pth = getScriptPath()
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Export to CSV', pth,
                                                     selectedFilter='*.csv')
        if fileName:
            with open(fileName, "w") as f:
                f.write("IP,HOSTNAME,STATE CHANGES,CURRENT STATE\n")
                for val in self.ip_list:
                    f.write(val.to_str()+"\n")

    def about(self):
        text = "ManG  Copyright (C) 2016  Maria Krovatkina\nThis program comes with NO WARRANTY\n\nGNU GPL"
        # Controls
        d = QtGui.QDialog()
        lbl = QtGui.QLabel(text, d)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        b1 = QtGui.QPushButton("OK", d)
        b1.clicked.connect(d.close)

        # Layout
        layout = QtGui.QVBoxLayout(d)
        layout.addWidget(lbl)
        layout.addWidget(b1)
        d.setWindowTitle("Dialog")
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.exec_()

    def close_dialog(self):
        self.close()

    def settings_dialog(self):
        try:
            pi, pt, gi, ok = MangSettings.getSettings()
            if ok:
                self.ping_interval = pi
                self.ping_timeout = pt
                self.gui_interval = gi
                for val in self.ip_list:
                    val.p_timeout = pt
        except Exception as e:
            self.error_dialog("Incorrect settings!")

    def error_dialog(self, msg = "Can't parse IP string!"):
        d = QtGui.QDialog()
        lbl = QtGui.QLabel(msg, d)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        b1 = QtGui.QPushButton("Close", d)
        b1.clicked.connect(d.close)

        # Layout
        layout = QtGui.QVBoxLayout(d)
        layout.addWidget(lbl)
        layout.addWidget(b1)
        d.setWindowTitle("Error")
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.exec_()


def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def app_main():
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', filename="log.txt")
    logging.debug("APPLICATION START")
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

app_main()