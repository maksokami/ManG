# This file is part of ManG.

# ManG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ManG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, operator, logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MangTableModel(QAbstractTableModel):
    def __init__(self, v_headers=[], parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.ip_list = []
        self.cb_status = True
        self.headers = v_headers
        logging.debug("Table model created")

    def rowCount(self, parent=QModelIndex()):
        return len(self.ip_list)

    def columnCount(self, index=QModelIndex()):
        return len(self.headers)

    def setData(self, v_data):
        self.ip_list = []
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        for i,key in enumerate(v_data):
            self.ip_list.append( [key.ip, key.hostname, key.state_changes, key.is_reachable] )
        logging.debug("Table model data updated - %s", self.ip_list)
        self.emit(SIGNAL("dataChanged()"))
        self.emit(SIGNAL("layoutChanged()"))

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        row = index.row()
        col = index.column()

        # Set cell value
        if role == Qt.DisplayRole:
            if (index.column() == len(self.headers) - 1) and index.row() >= 0:
                if self.ip_list[index.row()][index.column()] == 1:
                    return QVariant("OK")
                else:
                    return QVariant()
            elif (0 <= row < len(self.ip_list)) and (0 <= col < len(self.headers)):
                return QVariant(self.ip_list[index.row()][index.column()])
            else:
                return QVariant()

        # Set background color
        if role == Qt.BackgroundColorRole:
            if (index.column() == len(self.headers) - 1) and index.row() >= 0:
                bgColor = QColor(Qt.red)
                if self.ip_list[index.row()][index.column()] == 1:
                    bgColor = QColor(Qt.green)
                return QVariant(QColor(bgColor))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def cbChanged(self, arg=None):
        self.cb_status=arg

    def sort(self, v_sort_col, order):
        logging.debug("Table model sort initiated - column %s", v_sort_col)
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.ip_list = sorted(self.ip_list, key=operator.itemgetter(v_sort_col))
        if order == Qt.DescendingOrder:
            self.ip_list.reverse()
        self.emit(SIGNAL("layoutChanged()"))
