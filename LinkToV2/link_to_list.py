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
                            QSizePolicy, QPushButton, QLineEdit,
                            QSpacerItem, QPixmap, QTransform)
from qtswitch.QtCore import Qt, QEvent

import link_to_selection
from link_to_qwidget import LinkToQWidget

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
    Class LinkToList: Panel to select list all parents and show connected
"""
###############################################################################
###############################################################################
###############################################################################
###############################################################################


class LinkToList(LinkToQWidget):
    """
        Init UI
    """
    def default(self, node_type=False):
        self.type = node_type
        self.s = nuke.selectedNodes()
        self.this = nuke.thisNode()

        self.init_ui()

        return self

    """
        UI
    """
    def init_ui(self):
        # QLayouts
        #
        layout_v_parent_list_frame = QVBoxLayout()

        title_parent_list_h_box_layout = QHBoxLayout()
        graph_h_layout = QHBoxLayout()

        # QLabels
        #
        self.title_parent_label.setText('Connection')

        if self.type == "Camera2":
            self.name_label.setText('Cameras list')
        else:
            self.name_label.setText('Parents list')
        self.name_label.setStyleSheet(
            'background-color: #222; padding: 1px 3px 1px 3px;'
        )

        self.info_label.setText(
            'Click on a parent to connect it to this child.'
        )

        self.name_node_label = QLabel()

        # QPushButtons
        #
        self.refresh_btn = QPushButton()
        self.refresh_btn.setText('Refresh')
        self.refresh_btn.setFocusPolicy(Qt.NoFocus)
        self.refresh_btn.clicked.connect(self.refresh)
        self.refresh_btn.setStyleSheet('background-color: #2E2E2E;')

        # QSpacers
        #
        self.spacer5 = QSpacerItem(
            50,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        # Setting layouts
        #
        if self.type == "Camera2":
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                self.this,
                self.type
            )
        else:
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                self.this
            )

        """ Global """
        self.layout_v_global.addWidget(self.parent_frame)
        self.layout_v_global.addWidget(self.frame)
        layout_h_global = QHBoxLayout()

        self.layout_v_global.addLayout(self.layout_h_top)
        self.layout_h_top.addItem(self.spacer5)
        self.layout_h_top.addWidget(self.refresh_btn)

        """ Graph """
        pixmap2 = QPixmap('%s/img/arrow.png' % (
            os.path.dirname(os.path.realpath(__file__)))
        )
        pixmap2 = pixmap2.scaled(30, 30, Qt.KeepAspectRatio)

        transform = QTransform().rotate(90)
        pixmap2 = pixmap2.transformed(transform, Qt.SmoothTransformation)

        arrow_label = QLabel()
        arrow_label.setPixmap(pixmap2)
        arrow_label.setStyleSheet('padding: 0; margin: 0;')

        self.cross_label = QLabel()

        graph_h_layout.addWidget(self.title_parent_label)
        graph_h_layout.addWidget(self.cross_label)
        graph_h_layout.addWidget(arrow_label)
        graph_h_layout.addWidget(self.name_node_label)
        graph_h_layout.addItem(self.spacer)

        self.parent_frame.setLayout(graph_h_layout)

        """ Parent list """
        self.frame.setLayout(layout_v_parent_list_frame)

        title_parent_list_h_box_layout.addWidget(self.name_label)
        title_parent_list_h_box_layout.addItem(self.spacer2)

        layout_v_parent_list_frame.addLayout(title_parent_list_h_box_layout)
        layout_v_parent_list_frame.addLayout(self.grid)
        layout_v_parent_list_frame.addWidget(self.info_label)

        self.refresh_child()
        self.refresh_parent()
        self.refresh_parent_list()

    def refresh(self):
        btn = self.sender()  # Get button

        if isinstance(btn, QPushButton):
            if self.grid.count():
                for i in reversed(range(self.grid.count())):
                    btn.setStyle(None)
                    remove_layout = self.grid.takeAt(i)  # Get layout to delete
                    remove_layout.widget().deleteLater()  # Delete layout

            if self.type == "Camera2":  # If type camera
                self.this['label'].setValue(
                    '[if {[value input.label]!= "" '
                    '&& [value input.file]== ""} '
                    '{return [value input.label]} '
                    '{return '
                    '[regexp -inline "C_\[A-Za-z0-9_]+" '
                    '[value input.file]]\\n[value input.label]'
                    '}]'
                )  # Set label to file
            else:
                self.this['label'].setValue('[value input.label]')  # Set label

            self.refresh_child()
            self.refresh_parent()
            self.refresh_parent_list()

    def connect_parent(self):
        btn = self.sender()
        old_parent = self.this.input(0)

        if self.this.inputs():
            if isinstance(btn, QPushButton):
                self.this.setInput(
                    0,
                    self.parent_list[btn.text().split('\n')[0]][0]
                )
        else:
            if isinstance(btn, QPushButton):
                self.this.setInput(
                    0,
                    self.parent_list[btn.text().split('\n')[0]][0]
                )

        if old_parent:
            self.refresh_parent()
            self.refresh_child()

            if self.parent_list:
                if self.type == "Camera2":
                    r = self.parent_list[old_parent.name()][1][0]
                    g = self.parent_list[old_parent.name()][1][1]
                    b = self.parent_list[old_parent.name()][1][2]
                else:
                    r = self.parent_list[old_parent.name()][1][0]
                    g = self.parent_list[old_parent.name()][1][1]
                    b = self.parent_list[old_parent.name()][1][2]

                if self.type == "Camera2":
                    if old_parent['label'].value() and not old_parent['file'].value():
                        btn.setText(
                            '%s\n(%s)'
                            % (
                                old_parent.name(),
                                old_parent['label'].value()
                            )
                        )

                        self.this['label'].setValue(
                            '[if {[value input.label]!= "" '
                            '&& [value input.file]== ""} '
                            '{return [value input.label]} '
                            '{return '
                            '[regexp -inline "C_\[A-Za-z0-9_]+" '
                            '[value input.file]]\\n[value input.label]'
                            '}]'
                        )
                    elif old_parent['file'].value():
                        file = old_parent['file'].value()
                        btn.setText(
                            '%s\n(%s)'
                            % (
                                old_parent.name(),
                                file.split('/')[-1].split('.')[0]
                            )
                        )

                        self.this['label'].setValue(
                            '[if {[value input.label]!= "" '
                            '&& [value input.file]== ""} '
                            '{return [value input.label]} '
                            '{return '
                            '[regexp -inline "C_\[A-Za-z0-9_]+" '
                            '[value input.file]]\\n[value input.label]'
                            '}]'
                        )
                    else:
                        btn.setText(
                            '%s\n(%s)'
                            % (
                                old_parent.name(),
                                'None'
                            )
                        )
                else:
                    if old_parent['label'].value():
                        btn.setText(
                            '%s\n(%s)'
                            % (
                                old_parent.name(),
                                old_parent['label'].value()
                            )
                        )

                        self.this['label'].setValue(
                            '[value input.label]'
                        )
                    else:
                        btn.setText(
                            '%s\n(%s)'
                            % (
                                old_parent.name(),
                                'None'
                            )
                        )

                        self.this['label'].setValue(
                            '[value input.label]'
                        )

                if self.type == "Camera2":
                    text_color = "rgb(0,0,0)"
                else:
                    if "Deep" in old_parent.Class():
                        text_color = "rgb(255,255,255)"
                    else:
                        text_color = "rgb(0,0,0)"

                btn.setStyleSheet(
                    'font-size: 9px; background-color: %s;'
                    'border: 1px solid %s; color: %s;'
                    'padding: 5px 20px 5px 20px;'
                    % (
                        'rgb(%s,%s,%s)' % (r, g, b),
                        'rgb(0,0,0)',
                        text_color
                    )
                )
                btn.setStyle(QStyleFactory.create('Plastique'))
        else:
            self.refresh()

    def refresh_child(self):
        n = link_to_selection.LinkToSelection().add_child(self.this)

        r = n[0]
        g = n[1]
        b = n[2]

        if self.this.input(0):
            if self.type == "Camera2":
                if self.this.input(0)['file'].value():
                    file = self.this.input(0)['file'].value()
                    label = file.split('/')[-1].split('.')[0]
                elif self.this.input(0)['label'].value() and not self.this.input(0)['file'].value():
                    label = self.this.input(0)['label'].value()
                else:
                    label = "None"
            else:
                if self.this.input(0)['label'].value():
                    label = self.this.input(0)['label'].value()
                else:
                    label = "None"
        else:
            label = "None"

        self.name_node_label.setText('%s\n(%s)' % (self.this.name(), label))
        self.name_node_label.setStyleSheet(
            'font-size: 9px; background-color: %s;'
            'border: 1px solid %s; color: %s;'
            'padding: 5px 20px 5px 20px;'
            % (
                'rgb(%s,%s,%s)' % (r, g, b),
                'rgb(0,0,0)',
                'rgb(0,0,0)'
            )
        )
        self.name_node_label.setAlignment(Qt.AlignCenter)
        self.name_node_label.setStyle(QStyleFactory.create('Plastique'))

    def refresh_parent(self):
        if self.type == "Camera2":
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                self.this,
                self.type
            )
        else:
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                self.this
            )
        connected_parent = self.this.input(0)

        if self.this.inputs():
            if ("linkTo_parent" not in connected_parent.name()) and ("Camera2" not in connected_parent.Class()):
                pixmap = QPixmap('%s/img/cross.png' % (
                    os.path.dirname(os.path.realpath(__file__)))
                )
                pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio)

                self.cross_label.setStyleSheet('')
                self.cross_label.setText(None)
                self.cross_label.setPixmap(pixmap)
                self.cross_label.setStyleSheet(
                    'padding: 0 0 0 20px; margin: 0;'
                )

                for i in reversed(range(self.grid.count())):
                    remove_layout = self.grid.takeAt(i)

                    if remove_layout.widget():
                        remove_layout.widget().deleteLater()
            else:
                if self.parent_list:
                    if self.type == "Camera2":
                        r = self.parent_list[connected_parent.name()][1][0]
                        g = self.parent_list[connected_parent.name()][1][1]
                        b = self.parent_list[connected_parent.name()][1][2]
                    else:
                        r = self.parent_list[connected_parent.name()][1][0]
                        g = self.parent_list[connected_parent.name()][1][1]
                        b = self.parent_list[connected_parent.name()][1][2]

                    if self.type == "Camera2":
                        if self.this.input(0)['label'].value() and not self.this.input(0)['file'].value():
                            self.cross_label.setText(
                                '%s\n(%s)'
                                % (
                                    connected_parent.name(),
                                    self.this.input(0)['label'].value()
                                )
                            )
                        elif connected_parent['file'].value():
                            file = connected_parent['file'].value()
                            self.cross_label.setText(
                                '%s\n(%s)'
                                % (
                                    connected_parent.name(),
                                    file.split('/')[-1].split('.')[0]
                                )
                            )
                        else:
                            self.cross_label.setText(
                                '%s\n(%s)'
                                % (
                                    connected_parent.name(),
                                    'None'
                                )
                            )
                    else:
                        if connected_parent['label'].value():
                            self.cross_label.setText(
                                '%s\n(%s)'
                                % (
                                    connected_parent.name(),
                                    connected_parent['label'].value()
                                )
                            )
                        else:
                            self.cross_label.setText(
                                '%s\n(%s)'
                                % (
                                    connected_parent.name(),
                                    'None'
                                )
                            )

                    if self.type == "Camera2":
                        text_color = "rgb(0,0,0)"
                    else:
                        if "Deep" in connected_parent.input(0).Class():
                            text_color = "rgb(255,255,255)"
                        else:
                            text_color = "rgb(0,0,0)"

                    self.cross_label.setStyleSheet(
                        "font-size: 9px; background-color: %s;"
                        "border: 1px solid %s; color: %s;"
                        "padding: 5px 20px 5px 20px;"
                        % (
                            'rgb(%s,%s,%s)' % (r, g, b),
                            'rgb(0,0,0)',
                            text_color
                        )
                    )
                    self.cross_label.setAlignment(Qt.AlignCenter)
                    self.cross_label.setStyle(
                        QStyleFactory.create('Plastique')
                    )
        else:
            pixmap = QPixmap('%s/img/cross.png' % (
                os.path.dirname(os.path.realpath(__file__)))
            )
            pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio)

            self.cross_label.setStyleSheet('')
            self.cross_label.setText(None)
            self.cross_label.setPixmap(pixmap)
            self.cross_label.setStyleSheet('padding: 0 0 0 20px; margin: 0;')

            for i in reversed(range(self.grid.count())):
                remove_layout = self.grid.takeAt(i)

                if remove_layout.widget():
                    remove_layout.widget().deleteLater()

    def refresh_parent_list(self):
        self.COUNTER2 = 0

        if self.type == "Camera2":
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                self.this,
                self.type
            )
        else:
            self.parent_list = link_to_selection.LinkToSelection().add_parents(
                self.this
            )

        if self.parent_list:
            if self.this.inputs():
                if self.this.input(0).name() in self.parent_list:
                    del(self.parent_list[self.this.input(0).name()])

            for n in self.parent_list:
                r = self.parent_list[n][1][0]
                g = self.parent_list[n][1][1]
                b = self.parent_list[n][1][2]

                node_item = self.parent_node(
                    'rgb(0,0,0)',
                    'rgb(%s,%s,%s)' % (r, g, b), self.parent_list[n][0]
                )
                node_item.setCursor(Qt.PointingHandCursor)
                node_item.clicked.connect(self.connect_parent)

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

            self.info_label.setText(
                'Click on a parent to connect it to this child.'
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

        else:
            R = 255 * 0.8
            G = 255 * 0.513
            B = 255 * 0.488

            self.info_label.setText(
                'No parent found in the nuke script.'
            )
            self.info_label.setStyleSheet(
                'font-size: 10px; background-color: %s;'
                'border: 1px solid %s; color: %s;'
                'padding: 2px 10px 2px 10px;'
                % (
                    'rgb(%s,%s,%s)' % (R, G, B),
                    'rgb(0,0,0)',
                    'rgb(0,0,0)'
                )
            )

    def parent_node(self, color1, color2, n):
        if n.inputs():
            if "Deep" in n.input(0).Class():
                text_color = "rgb(255,255,255)"
            else:
                text_color = "rgb(0,0,0)"
        else:
            text_color = "rgb(0,0,0)"

        push_btn = QPushButton()

        if self.type == "Camera2":
            if n['label'].value() and not n['file'].value():
                push_btn.setText('%s\n(%s)' % (
                    n.name(),
                    n['label'].value()
                ))
            elif n['file'].value():
                push_btn.setText('%s\n(%s)' % (
                    n.name(),
                    n['file'].value().split('/')[-1].split('.')[0]
                ))
            else:
                push_btn.setText('%s\n(%s)' % (n.name(), 'None'))
        else:
            if n['label'].value():
                push_btn.setText('%s\n(%s)' % (n.name(), n['label'].value()))
            else:
                push_btn.setText('%s\n(%s)' % (n.name(), 'None'))

        push_btn.setStyleSheet(
            'font-size: 9px; background-color: %s;'
            'border: 1px solid %s; color: %s;'
            'padding: 5px 20px 5px 20px;'
            % (color2, color1, text_color)
        )
        push_btn.setStyle(QStyleFactory.create('Plastique'))

        return push_btn

    def makeUI(self):
        return self

    def updateValue(self):
        pass
