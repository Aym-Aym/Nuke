"""
###
    LinkToV2 plugin by Aymeric Ballester
###
"""

import sys

import nuke
import nukescripts

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
    Class LinkToCreateNodes: Panel to select list all parents & show connected
"""
###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
    Class LinkToCreateNodes: Panel to select parent and children
"""


class LinkToCreateNodes():
    def __init__(self, parent, children=None, label=None):
        nukescripts.clear_selection_recursive()  # Clear selection

        self.parents = parent
        self.children = children
        self.label = label
        self.parent = None

    def create_children(self):
        s = nuke.allNodes('NoOp')

        if not self.parent:
            self.parent = self.parents[0]

        numbers = []
        self.child = nuke.createNode(
            'NoOp',
            inpanel=False
        )  # Create NoOp child node

        if self.parents[0].Class() == "Camera2":  # If parent camera
            for n in s:
                if "_camera" in n.name():
                    numbers.append(
                        n.name().split('linkTo_camera')[1]
                    )  # Add name in list

            if len(numbers):  # If other nodes exist
                self.child.setName(
                    'linkTo_camera%i' % (int(max(numbers))+1)
                )  # Set name with number
            else:
                self.child.setName('linkTo_camera1')  # Set name at 1

            hex_cam_color = int('%02x%02x%02x%02x' % (
                255 * 0.612,
                255 * 0,
                255 * 0,
                1), 16)
            self.child['tile_color'].setValue(hex_cam_color)

            knob = nuke.PyCustom_Knob(
                'linkToList',
                '',
                'link_to_list.LinkToList().default(\'Camera2\')'
            )

            self.child['label'].setValue(
                '[if {[value input.label]!= "" && [value input.file]== ""} '
                '{return [value input.label]} '
                '{return '
                '[regexp -inline "C_\[A-Za-z0-9_]+" '
                '[value input.file]]\\n[value input.label]'
                '}]'
            )
        else:
            for n in s:
                if "_child" in n.name():
                    # Add name in list
                    numbers.append(n.name().split('linkTo_child')[1])

            if len(numbers):  # If other nodes exist
                # Set name with number
                self.child.setName('linkTo_child%i' % (int(max(numbers))+1))
            else:
                self.child.setName('linkTo_child%i' % (1))  # Set name at 1

            knob = nuke.PyCustom_Knob(
                'linkToList',
                '',
                'link_to_list.LinkToList().default()'
            )

            self.child['label'].setValue('[value input.label]')

        self.child.addKnob(knob)
        self.child['User'].setName('link_to_selection')
        self.child.setInput(0, self.parent)
        self.child['hide_input'].setValue(True)

        if self.children:  # Set children
            self.child['xpos'].setValue(self.children[0]['xpos'].value() - 250)
            self.child['ypos'].setValue(self.children[0]['ypos'].value() - 200)

            dot = False

            if len(self.children) > 1:  # If many children selected
                dot = nuke.createNode('Dot', inpanel=False)  # Create dot
                node = dot
            else:
                node = self.child

            for n in self.children:
                if "ScanlineRender" in n.name():
                    n.setInput(2, node)
                else:
                    if n.inputs():
                        if not n.input(0):
                            n.setInput(0, node)
                        elif n.input(0) and not n.input(1):
                            n.setInput(1, node)
                        else:
                            n.setInput(2, node)
                    else:
                        n.setInput(0, node)

    def create_parent(self, child=True):
        s = nuke.allNodes('NoOp')

        numbers = []
        if s:
            for n in s:
                if "_parent" in n.name():
                    """ Add name in list """
                    numbers.append(n.name().split('linkTo_parent')[1])
        else:
                    numbers.append(0)

        """ Create NoOp parent node """
        self.parent = nuke.createNode('NoOp', inpanel=False)

        if len(numbers):  # If other nodes exist
            """ Set name with number """
            self.parent.setName('linkTo_parent%i' % (int(max(numbers))+1))
        else:
            self.parent.setName('linkTo_parent%i' % (1))  # Set name at 1

        self.parent['xpos'].setValue(self.parents[0]['xpos'].value() + 230)
        self.parent['ypos'].setValue(self.parents[0]['ypos'].value() + 100)
        self.parent.setInput(0, self.parents[0])
        self.parent['label'].setValue(self.label)

        if child:
            self.create_children()

    def create_parents(self):
        for parent in self.parents:
            self.create_parent(False)
