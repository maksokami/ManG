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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MangSettings(QDialog):
    def __init__(self, parent = None, v_values = [5,4,5]):
        super(QDialog, self).__init__(parent)

        layout = QVBoxLayout(self)
        l1 = QHBoxLayout()
        l2 = QHBoxLayout()
        l3 = QHBoxLayout()
        layout.addLayout(l1)
        layout.addLayout(l2)
        layout.addLayout(l3)
        self.setWindowTitle("Interval in sec")
        # nice widget for editing the date
        self.editPI = QLineEdit(str(v_values[0])) # Ping interval
        self.editPT = QLineEdit(str(v_values[1])) # Ping timeout
        self.editGI = QLineEdit(str(v_values[2])) # GUI refresh interval
        lbl1 = QLabel("Ping interval")
        lbl2 = QLabel("Ping timeout")
        lbl3 = QLabel("GUI refresh")
        l1.addWidget(lbl1)
        l2.addWidget(lbl2)
        l3.addWidget(lbl3)
        l1.addWidget(self.editPI)
        l2.addWidget(self.editPT)
        l3.addWidget(self.editGI)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getVlalues(self):
        return (int(self.editPI.text()), int(self.editPT.text()), int(self.editGI.text()))

    @staticmethod
    def getSettings(parent = None):
        dialog = MangSettings(parent)
        result = dialog.exec_()
        k,l,m = dialog.getVlalues()
        return (k,l,m, result == QDialog.Accepted)

