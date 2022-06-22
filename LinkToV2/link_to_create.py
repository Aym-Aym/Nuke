"""
###
    LinkToV2 plugin by Aymeric Ballester
###
"""

import sys

import nuke
import nukescripts
from qtswitch.QtGui import (QWidget, QCursor, QVBoxLayout, QHBoxLayout,
                            QGridLayout, QFrame, QLabel, QPushButton,
                            QStyleFactory, QSizePolicy, QPushButton,
                            QLineEdit, QSpacerItem
                            )
from qtswitch.QtCore import Qt, QEvent

import link_to_selection
import link_to_create_nodes
from link_to_qwidget import LinkToQWidget

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
    Class LinkToSettings: Change for defaults values
"""
###############################################################################
###############################################################################
###############################################################################
###############################################################################

"""
    Class LinkToCreate: Panel to select parent and children
"""


class LinkToCreate(LinkToQWidget):
    """
        Init UI
    """
    def default(self):
        self.s = nuke.selectedNodes()
        self.dict_nodes = link_to_selection.LinkToSelection(self.s).set_nodes_dict()

        if len(self.s) >= 1:
            self.init_ui()
        else:
            self.error()

        return self

    """
        UI
    """
    def init_ui(self):
        # QLayouts
        #
        name_h_layout = QHBoxLayout()

        # QFrames
        #

        title_children_label = QLabel()
        title_children_label.setText('Children')
        title_children_label.setStyleSheet(
            'background-color: #222; padding: 1px 3px 1px 3px;'
        )
        title_children_label.setStyle(QStyleFactory.create('Plastique'))

        r = self.dict_nodes['parent'][self.dict_nodes['parent'].keys()[0]][0]
        g = self.dict_nodes['parent'][self.dict_nodes['parent'].keys()[0]][1]
        b = self.dict_nodes['parent'][self.dict_nodes['parent'].keys()[0]][2]

        if "Deep" in self.dict_nodes['parent'].keys()[0].Class():
            text_color = "rgb(255,255,255)"
        else:
            text_color = "rgb(0,0,0)"

        self.name_parent_label = QLabel()
        self.name_parent_label.setText(
            self.dict_nodes['parent'].keys()[0].name()
        )
        self.name_parent_label.setStyleSheet(
            'font-size: 9px; background-color: %s;'
            'border: 1px solid %s; color: %s;'
            'padding: 5px 20px 5px 20px;'
            % (
                'rgb(%s,%s,%s)' % (r, g, b),
                'rgb(0,0,0)',
                text_color
            )
        )
        self.name_parent_label.setAlignment(Qt.AlignCenter)
        self.name_parent_label.setStyle(QStyleFactory.create('Plastique'))

        # QPushButtons
        #
        self.create_btn.clicked.connect(self.create_nodes)

        self.remove_btn = QPushButton()
        self.remove_btn.setText('Remove child')
        self.remove_btn.setCheckable(True)
        self.remove_btn.clicked.connect(self.deleteChildBtn)
        self.remove_btn.setFocusPolicy(Qt.NoFocus)

        # Setting layouts
        #

        """ Global """
        self.layout_v_global.addLayout(self.layout_h_top)
        self.layout_v_global.addWidget(self.name_frame)

        """ Name """
        self.name_frame.setLayout(name_h_layout)

        name_h_layout.addWidget(self.name_label)
        name_h_layout.addWidget(self.name_line)
        name_h_layout.addWidget(self.create_btn)

        """ Parent """
        self.layout_h_top.addWidget(self.parent_frame)

        self.parent_frame.setLayout(self.layout_v_parent_frame)

        self.layout_v_parent_frame.addLayout(self.title_parent_h_box_layout)

        self.title_parent_h_box_layout.addWidget(self.title_parent_label)
        self.title_parent_h_box_layout.addItem(self.spacer)

        self.layout_v_parent_frame.addWidget(self.name_parent_label)
        self.layout_v_parent_frame.addItem(self.spacer1)
        self.layout_v_parent_frame.addWidget(self.remove_btn)

        """ Children """
        self.layout_h_top.addWidget(self.frame)

        self.frame.setLayout(self.layout_v_children_frame)

        self.title_children_h_box_layout.addWidget(title_children_label)
        self.title_children_h_box_layout.addItem(self.spacer2)

        self.layout_v_children_frame.addLayout(
            self.title_children_h_box_layout
        )
        self.layout_v_children_frame.addLayout(self.grid)
        self.layout_v_children_frame.addItem(self.spacer3)
        self.layout_v_children_frame.addWidget(self.info_label)

        """ Set nodes buttons """
        for node in self.dict_nodes['children']:
            r = self.dict_nodes['children'][node][0]
            g = self.dict_nodes['children'][node][1]
            b = self.dict_nodes['children'][node][2]

            child_node = self.child_node(
                'rgb(0,0,0)',
                'rgb(%s,%s,%s)' % (r, g, b),
                '%s' % (node.name())
            )
            child_node.setCursor(Qt.PointingHandCursor)
            child_node.clicked.connect(self.edit_parent)

            if self.COUNTER2 % 3:
                self.grid.addWidget(
                    child_node,
                    self.COUNTER1,
                    self.COUNTER2 % 3
                )
            else:
                self.COUNTER1 += 1
                self.grid.addWidget(
                    child_node,
                    self.COUNTER1,
                    self.COUNTER2 % 3
                )

            self.COUNTER2 += 1

    def create_nodes(self):
        """ create parent list """
        parent = []
        parent.append(self.dict_nodes['parent'].keys()[0])

        """ create children list """
        children = []
        for child in self.dict_nodes['children'].keys():
            children.append(child)

        """ create parent and child nodes """
        link_to_create_nodes.LinkToCreateNodes(
            parent,
            children,
            self.name_line.text()
        ).create_parent()

        self.close()

    def child_node(self, color1, color2, text):
        """ if node is a deep, set text color to white """
        if "Deep" in text:
            text_color = "rgb(255,255,255)"
        else:
            text_color = "rgb(0,0,0)"

        """ create node button in panel """
        push_btn = QPushButton()
        push_btn.setStyle(QStyleFactory.create('Plastique'))
        push_btn.setText('%s' % text)
        push_btn.setStyleSheet(
            'font-size: 9px; background-color: %s;'
            'border: 1px solid %s; color: %s;'
            'padding: 5px 20px 5px 20px;'
            % (color2, color1, text_color)
        )

        return push_btn

    def edit_parent(self):
        """ get button click """
        btn = self.sender()

        if isinstance(btn, QPushButton):
            if self.remove_btn.isChecked():  # verify remove button is checked
                del_node = btn.text()  # get name of node to remove
                """ del node if there is more than one node left """
                if self.grid.count() > 2:
                    self.dict_nodes = link_to_selection.LinkToSelection().delete_nodes_dict(
                        del_node,
                        self.dict_nodes
                    )  # delete node from the dictionary

                    nuke.toNode(del_node)['selected'].setValue(False)
                    self.s = nuke.selectedNodes()

                    btn.setStyle(None)
                    remove_layout = self.grid.takeAt(self.grid.indexOf(btn))
                    remove_layout.widget().deleteLater()

                    self.info_label.setText('Click on a child to remove it.')

                elif self.grid.count() > 1:
                    self.dict_nodes = link_to_selection.LinkToSelection().delete_nodes_dict(
                        del_node,
                        self.dict_nodes
                    )  # delete node from the dictionary

                    nuke.toNode(del_node)['selected'].setValue(False)
                    self.s = nuke.selectedNodes()

                    btn.setStyle(None)
                    remove_layout = self.grid.takeAt(self.grid.indexOf(btn))
                    remove_layout.widget().deleteLater()

                    self.info_label.setText(
                        'You must keep at least one child.'
                    )
                else:
                    self.info_label.setText(
                        'You must keep at least one child.'
                    )
            else:  # else make node as parent
                old_parent = self.dict_nodes['parent']

                new_parent = btn.text()  # get new parent name
                self.dict_nodes = link_to_selection.LinkToSelection().update_nodes_dict(
                    new_parent,
                    self.dict_nodes
                )  # update directory

                parent = self.name_parent_label
                new_text = btn.text()
                new_color = btn.styleSheet()

                btn.setText(parent.text())
                btn.setStyleSheet(parent.styleSheet())
                parent.setText(new_text)
                parent.setStyleSheet(new_color)

    """ set remove btn state """
    def deleteChildBtn(self):
        remove_btn = self.sender()
        if isinstance(remove_btn, QPushButton):
            if remove_btn.isChecked():
                R = 255 * 0.8
                G = 255 * 0.513
                B = 255 * 0.488

                if self.grid.count() > 1:
                    self.info_label.setText('Click on a child to remove it.')
                else:
                    self.info_label.setText(
                        'You must keep at least one child.'
                    )

                self.info_label.setStyleSheet(
                    'font-size: 10px; background-color: %s;'
                    'border: 1px solid %s; color: %s;'
                    'padding: 2px 10px 2px 10px;'
                    % ('rgb(%s,%s,%s)' % (R, G, B), 'rgb(0,0,0)', 'rgb(0,0,0)')
                )
            else:
                self.info_label.setText(
                    'Click on a child to make it a parent.'
                )
                self.info_label.setStyleSheet(
                    'font-size: 10px; background-color: %s;'
                    'border: 1px solid %s; color: %s;'
                    'padding: 2px 10px 2px 10px;'
                    % (
                        'rgb(%s,%s,%s)' % (self.R, self.G, self.B),
                        'rgb(0,0,0)',
                        'rgb(0,0,0)'
                    )
                )

    def error(self):
        label_v_layout = QVBoxLayout()
        title_h_layout = QHBoxLayout()

        self.frame = QFrame()
        self.frame.setStyleSheet('background-color: #2E2E2E;')

        title_label = QLabel()
        title_label.setText('Error')
        title_label.setStyleSheet(
            'background-color: #222; padding: 1px 3px 1px 3px;'
        )
        title_label.setStyle(QStyleFactory.create('Plastique'))

        error_label = QLabel()
        error_label.setText('Select at least two nodes.')
        error_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.spacer = QSpacerItem(
            50,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.layout_v_global.addWidget(self.frame)

        self.frame.setLayout(label_v_layout)

        label_v_layout.addLayout(title_h_layout)

        title_h_layout.addWidget(title_label)
        title_h_layout.addItem(self.spacer)

        label_v_layout.addWidget(error_label)

    def event(self, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()

            return True
        elif event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Escape:
                self.close()

                return True
            elif key == Qt.Key_Return:
                self.create_nodes()

                return True
            else:
                return QWidget.event(self, event)
        else:
            return QWidget.event(self, event)
