from qtswitch.QtGui import (QWidget, QCursor, QVBoxLayout, QHBoxLayout,
                            QGridLayout, QFrame, QLabel, QPushButton,
                            QStyleFactory, QSizePolicy, QPushButton,
                            QLineEdit, QSpacerItem)
from qtswitch.QtCore import Qt, QEvent


class LinkToQWidget(QWidget):
    def __init__(self):
        super(LinkToQWidget, self).__init__()

        self.resize(300, 100)
        self.setStyleSheet('background-color: #222;')
        self.setWindowFlags(Qt.FramelessWindowHint)

        cursor = QCursor()
        win_pos_x = cursor.pos().x() - (self.width() / 2)
        win_pos_y = cursor.pos().y() - (self.height() / 2) - 28
        self.move(win_pos_x, win_pos_y)

        self.COUNTER1 = -1  # Set counter to -1
        self.COUNTER2 = 0  # Set counter to 0

        self.init_default_ui()

    def init_default_ui(self):
        # QLayouts
        #
        self.layout_v_global = QVBoxLayout()
        self.layout_v_global.setContentsMargins(12, 12, 12, 12)
        self.layout_v_children_frame = QVBoxLayout()
        self.layout_v_parent_frame = QVBoxLayout()

        self.layout_h_top = QHBoxLayout()
        self.title_children_h_box_layout = QHBoxLayout()
        self.title_parent_h_box_layout = QHBoxLayout()

        self.grid = QGridLayout()

        # QFrames
        #
        self.frame = QFrame()
        self.frame.setStyleSheet('background-color: #2E2E2E;')

        self.parent_frame = QFrame()
        self.parent_frame.setStyleSheet('background-color: #2E2E2E;')

        self.name_frame = QFrame()
        self.name_frame.setStyleSheet('background-color: #2E2E2E;')

        # QLabels
        #
        self.title_parent_label = QLabel()
        self.title_parent_label.setText('Parent')
        self.title_parent_label.setStyleSheet(
            'background-color: #222; padding: 1px 3px 1px 3px;'
        )
        self.title_parent_label.setStyle(QStyleFactory.create('Plastique'))

        # Constants
        self.R = 255 * 0.513
        self.G = 255 * 0.8
        self.B = 255 * 0.488

        self.info_label = QLabel()
        self.info_label.setText(
            'Click on a child to make it a parent.'
        )
        self.info_label.setStyleSheet(
            'font-size: 10px; background-color: %s;'
            'border: 1px solid %s;'
            'color: %s; padding: 2px 10px 2px 10px;'
            % (
                'rgb(%s,%s,%s)' % (
                    self.R,
                    self.G,
                    self.B
                ),
                'rgb(0,0,0)',
                'rgb(0,0,0)'
            )
        )
        self.info_label.setStyle(QStyleFactory.create('Plastique'))

        self.name_label = QLabel()
        self.name_label.setText('Name')
        self.name_label.setStyleSheet(
            'background-color: #222; padding: 1px 3px 1px 3px;'
        )
        self.name_label.setStyle(QStyleFactory.create('Plastique'))

        # QPushButtons
        #
        self.create_btn = QPushButton()
        self.create_btn.setText('Create')
        self.create_btn.setFocusPolicy(Qt.NoFocus)
        self.create_btn.setStyleSheet('background-color: #2E2E2E;')

        # QLineEdits
        #
        self.name_line = QLineEdit()

        # QSpacers
        #
        self.spacer = QSpacerItem(
            50,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        self.spacer1 = QSpacerItem(
            50,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.spacer2 = QSpacerItem(
            50,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        self.spacer3 = QSpacerItem(
            70,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.spacer4 = QSpacerItem(
            70,
            20,
            QSizePolicy.Minimum,
            QSizePolicy.Fixed
        )

        self.setLayout(self.layout_v_global)
