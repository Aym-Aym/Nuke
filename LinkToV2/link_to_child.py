"""
###
    LinkToV2 plugin by Aymeric Ballester
###
"""

import os
import sys

import nuke
import nukescripts
from qtswitch.QtGui import (QWidget, QCursor, QVBoxLayout,
                            QHBoxLayout, QGridLayout, QFrame,
                            QLabel, QPushButton, QStyleFactory,
                            QPushButton, QLineEdit, QSpacerItem,
                            QPixmap, QSizePolicy)
from qtswitch.QtCore import Qt, QEvent

import link_to_selection
import link_to_create_nodes
from link_to_qwidget import LinkToQWidget

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
    Class LinkToChild: Panel to select list all parents and show connected
"""
###############################################################################
###############################################################################
###############################################################################
###############################################################################

"""
    Class LinkToChild: Panel to select parent and children
"""


class LinkToChild(LinkToQWidget):
    """
        Init UI
    """
    def default(self):
        self.init_ui()

        return self

    """
        UI
    """
    def init_ui(self):
        """dict: qt ui"""
        # QLayouts
        #
        create_h_layout = QHBoxLayout()
        btns_h_layout = QHBoxLayout()

        # QFrames
        #
        btn_frame = QFrame()
        btn_frame.setStyleSheet('background-color: #2E2E2E;')

        # QLabels
        #
        self.title_children_label = QLabel()
        self.title_children_label.setText('Camera list')
        self.title_children_label.setStyleSheet(
            'background-color: #222; padding: 1px 3px 1px 3px;'
        )
        self.title_children_label.setStyle(QStyleFactory.create('Plastique'))

        self.cross_label = QLabel()

        # QPushButton
        #
        self.create_btn.setEnabled(False)
        self.create_btn.clicked.connect(self.create_nodes)

        self.camera_btn = QPushButton()
        self.camera_btn.setText('Cameras')
        self.camera_btn.setFocusPolicy(Qt.NoFocus)
        self.camera_btn.setCheckable(True)
        self.camera_btn.setChecked(True)
        self.camera_btn.clicked.connect(self.tab_btns)

        self.noop_btn = QPushButton()
        self.noop_btn.setText('Parents')
        self.noop_btn.setFocusPolicy(Qt.NoFocus)
        self.noop_btn.setCheckable(True)
        self.noop_btn.clicked.connect(self.tab_btns)

        # QSpacers
        #
        spacer5 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Setting layouts
        #

        """ Global """
        self.layout_v_global.addWidget(btn_frame)
        self.layout_v_global.addLayout(self.layout_h_top)
        self.layout_v_global.addLayout(create_h_layout)

        """ Btns """
        btn_frame.setLayout(btns_h_layout)
        btns_h_layout.addWidget(self.camera_btn)
        btns_h_layout.addWidget(self.noop_btn)

        """ Create """
        create_h_layout.addItem(spacer5)
        create_h_layout.addWidget(self.create_btn)

        """ Parent """
        self.layout_h_top.addWidget(self.parent_frame)

        self.parent_frame.setLayout(self.layout_v_parent_frame)

        self.layout_v_parent_frame.addLayout(self.title_parent_h_box_layout)

        self.title_parent_h_box_layout.addWidget(self.title_parent_label)
        self.title_parent_h_box_layout.addItem(self.spacer)

        self.layout_v_parent_frame.addWidget(self.cross_label)
        self.layout_v_parent_frame.addItem(self.spacer1)

        """ Children """
        self.layout_h_top.addWidget(self.frame)

        self.frame.setLayout(self.layout_v_children_frame)

        self.title_children_h_box_layout.addWidget(self.title_children_label)
        self.title_children_h_box_layout.addItem(self.spacer2)

        self.layout_v_children_frame.addLayout(
            self.title_children_h_box_layout
            )
        self.layout_v_children_frame.addLayout(self.grid)
        self.layout_v_children_frame.addItem(self.spacer3)
        self.layout_v_children_frame.addWidget(self.info_label)

        self.refresh_parent()
        self.refresh_parent_list()

        self.setLayout(self.layout_v_global)

    def create_nodes(self):
        """ create parent list """
        parent = []
        parent.append(self.dict_nodes['parent'].keys()[0])

        """ create children list """
        children = []
        for child in nuke.selectedNodes():
            children.append(child)

        """ create parent and child nodes """
        link_to_create_nodes.LinkToCreateNodes(
            parent,
            children,
            self.name_line.text()
        ).create_children()
        self.close()

    def edit_parent(self):
        btn = self.sender()
        new_color = btn.styleSheet()

        if isinstance(btn, QPushButton):
            if self.camera_btn.isChecked():
                parents = nuke.allNodes('Camera2')
            else:
                parents = nuke.allNodes('NoOp')

            parent_list = []

            for parent in parents:
                if self.camera_btn.isChecked():
                    parent_list.append(parent)
                else:
                    if "parent" in parent.name():
                        parent_list.append(parent)

            self.dict_nodes = link_to_selection.LinkToSelection(
                parent_list
            ).set_nodes_dict('parents')

            new_parent = btn.text()  # get new parent name
            new_parent_name = new_parent.split("\n")
            self.dict_nodes = link_to_selection.LinkToSelection().update_nodes_dict(
                new_parent_name[0],
                self.dict_nodes
            )

            if self.cross_label.text():
                parent = self.cross_label
                new_text = btn.text()
                new_color = btn.styleSheet()

                btn.setText(parent.text())
                btn.setStyleSheet(parent.styleSheet())
                parent.setText(new_text)
                parent.setStyleSheet(new_color)

                self.create_btn.setEnabled(True)
            else:
                self.cross_label.setText(btn.text())
                self.cross_label.setAlignment(Qt.AlignCenter)
                self.cross_label.setStyleSheet(new_color)
                self.cross_label.setStyle(QStyleFactory.create('Plastique'))
                self.create_btn.setEnabled(True)

                new_widget = self.grid.takeAt(self.grid.count()-1).widget()
                btn.setStyleSheet(new_widget.styleSheet())
                btn.setText(new_widget.text())
                new_widget.setStyle(None)
                new_widget.deleteLater()

    def refresh_parent(self):
        pixmap = QPixmap(
            '%s/img/cross.png'
            % (
                os.path.dirname(os.path.realpath(__file__))
            )
        )
        pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio)

        self.cross_label.setStyleSheet('')
        self.cross_label.setText(None)
        self.cross_label.setPixmap(pixmap)
        self.cross_label.setStyleSheet('padding: 0 0 0 20px; margin: 0;')

    def refresh_parent_list(self):
        self.COUNTER2 = 0
        if self.camera_btn.isChecked():
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                None,
                'Camera2'
            )
        else:
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                None
            )

        if self.parent_list:
            for node in self.parent_list:
                r = self.parent_list[node][1][0]
                g = self.parent_list[node][1][1]
                b = self.parent_list[node][1][2]

                node_item = self.parent_node(
                    'rgb(0,0,0)',
                    'rgb(%s,%s,%s)' % (r, g, b),
                    self.parent_list[node][0]
                )
                node_item.setCursor(Qt.PointingHandCursor)
                node_item.clicked.connect(self.edit_parent)

                if self.COUNTER2 % 3:
                    self.grid.addWidget(
                        node_item,
                        self.COUNTER1,
                        self.COUNTER2 % 3
                    )
                else:
                    self.COUNTER1 += 1
                    self.grid.addWidget(
                        node_item,
                        self.COUNTER1,
                        self.COUNTER2 % 3
                    )
                self.COUNTER2 += 1

            if self.camera_btn.isChecked():
                self.info_label.setText(
                    'Click on a camera in the list to make it a parent.'
                )
                self.info_label.setStyle(QStyleFactory.create('Plastique'))
            else:
                self.info_label.setText(
                    'Click on a parent in the list to make it a parent.'
                )
                self.info_label.setStyle(QStyleFactory.create('Plastique'))

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

        else:
            r = 255 * 0.8
            g = 255 * 0.513
            b = 255 * 0.488

            if self.camera_btn.isChecked():
                self.info_label.setText(
                    'No camera found in the nuke script.'
                    'You need at least one camera.'
                )
                self.info_label.setStyle(QStyleFactory.create('Plastique'))
            else:
                self.info_label.setText(
                    'No parent found in the nuke script.'
                    'You need to create at least one parent.'
                )
                self.info_label.setStyle(QStyleFactory.create('Plastique'))

            self.info_label.setStyleSheet(
                'font-size: 10px; background-color: %s;'
                'border: 1px solid %s; color: %s;'
                'padding: 2px 10px 2px 10px;'
                % (
                    'rgb(%s,%s,%s)' % (r, g, b),
                    'rgb(0,0,0)',
                    'rgb(0,0,0)'
                )
            )

    def parent_node(self, color1, color2, node):
        if node.inputs():
            if "Deep" in node.input(0).Class():
                text_color = 'rgb(255,255,255)'
            else:
                text_color = "rgb(0,0,0)"
        else:
            text_color = "rgb(0,0,0)"

        push_btn = QPushButton()

        if self.camera_btn.isChecked():
            if node['file'].value():
                push_btn.setText(
                    '%s\n(%s)'
                    % (
                        node.name(),
                        node['file'].value().split('/')[-1].split('.')[0]
                    )
                )
            else:
                push_btn.setText(
                    '%s\n(%s)'
                    % (
                        node.name(),
                        'None'
                    )
                )
        else:
            if node['label'].value():
                push_btn.setText(
                    '%s\n(%s)'
                    % (
                        node.name(),
                        node['label'].value()
                    )
                )
            else:
                push_btn.setText(
                    '%s\n(%s)'
                    % (
                        node.name(),
                        'None'
                    )
                )

        push_btn.setStyleSheet(
            'font-size: 9px; background-color: %s;'
            'border: 1px solid %s; color: %s;'
            'padding: 5px 20px 5px 20px;'
            % (
                color2,
                color1,
                text_color
            )
        )
        push_btn.setStyle(QStyleFactory.create('Plastique'))

        return push_btn

    def tab_btns(self):
        btn = self.sender()

        if btn.text() == "Cameras":
            if btn.isChecked():
                self.title_children_label.setText('Camera list')
                self.noop_btn.setChecked(False)
            else:
                self.title_children_label.setText('Parent list')
                self.noop_btn.setChecked(True)
        else:
            if btn.isChecked():
                self.title_children_label.setText('Parent list')
                self.camera_btn.setChecked(False)
            else:
                self.title_children_label.setText('Camera list')
                self.camera_btn.setChecked(True)

        self.create_btn.setEnabled(False)

        if isinstance(btn, QPushButton):
            if self.grid.count():
                for i in reversed(range(self.grid.count())):
                    remove_layout = self.grid.takeAt(i)
                    remove_layout.widget().setStyle(None)
                    remove_layout.widget().deleteLater()

        self.refresh_parent()
        self.refresh_parent_list()

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
