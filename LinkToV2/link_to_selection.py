"""
###
    linkToV2 plugin by Aymeric Ballester
###
"""

import sys

import nuke
import nukescripts

import link_to_create
import link_to_create_nodes
import link_to_child
import link_to_list

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
    Class LinkToConnect: Generate connections
"""
###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
    Dir LinkToNodesColor:
"""
link_to_nodes_color = [
    {' Blur C_Blur2_1 C44Matrix ColorMatrix CurveBlur Defocus DegrainSimple DirBlurWrapper DustBust EdgeBlur EdgeDetect FilterErode LightWrap ZDefocus2 ': [255 * 0.8, 255 * 0.502, 255 * 0.306]},
    {' AddMix ChannelMerge Keymix Merge2 ': [255 * 0.294, 255 * 0.369, 255 * 0.776]},
    {' Clamp ColorCorrect ColorLookup dnColorCorrect dnColorLookup Grade Multiply Saturation ': [255 * 0.478, 255 * 0.663, 255 * 1]},
    {' C_SphericalTransform2_1 CornerPin2D Crop Reformat SphericalTransform Transform TransformMasked ': [255 * 0.647, 255 * 0.478, 255 * 0.667]},
    {' Roto RotoPaint ': [255 * 0.443, 255 * 0.776, 255 * 0.443]},
    {' AddChannels Copy CopyBBox CopyMetaData Shuffle ': [255 * 0.62, 255 * 0.235, 255 * 0.388]},
    {' AddTimeCode AppendClip ClipTest dnRetime Retime TimeOffset ': [255 * 0.69, 255 * 0.643, 255 * 0.365]},
    {' FileOut Write ': [255 * 0.749, 255 * 0.749, 255 * 0]},
    {' Axis C_CameraIngest2_1 C_CameraSolver2_1 Camera2 CameraToMeta CameraTracker Card2 Card3D ScanlineRender ': [255 * 0.612, 255 * 0, 255 * 0]},
    {' DeepBlackOutside DeepColorCorrect2 DeepConvert DeepExpression DeepFromImage DeepHoldout2 DeepMerge DeepRead DeepRecolor DeepReformat DeepSample DeepToImage DeepToPoints DeepTransform DeepWrite ': [255 * 0, 255 * 0, 255 * 0.376]},
    {' ChromaKeyer Keyer Primatte3 ': [255 * 0, 255 * 1, 255 * 0]},
    {'None': [255 * 0.8, 255 * 0.8, 255 * 0.8]}
]


class LinkToSelection():
    def __init__(self, s=False):
        self.selection = {
            "parent": {}, "children": {}
        }
        self.nodes_list = s

    def set_nodes_dict(self, list_type=False):
        """
        function: set_nodes_dict
        args:
            list_type (str)
        return:
        {
        'children':
            {
            <nuke_node>: [red,green,blue]
            },
        'parent':
            {
            <nuke_node>: [red,green,blue]
            }
        }

        self.selection return example:
        {
        'children':
            {
            <Grade14 at 0x1c2bf790>: [121.89, 169.065, 255],
            <Grade16 at 0x1c2bff90>: [121.89, 169.065, 255],
            <Grade12 at 0x1c2bf8b0>: [121.89, 169.065, 255],
            <Grade13 at 0x1c2bfbb0>: [121.89, 169.065, 255],
            <Grade15 at 0x1c2bfe30>: [121.89, 169.065, 255]
            },
        'parent':
            {
            <Roto5 at 0x1c2bfd90>: [112.965, 197.88, 112.965]
            }
        }
        """
        if self.nodes_list:
            if not list_type:
                parent = self.nodes_list[0]
                self.selection['parent'][parent] = None

                children = self.nodes_list
                children.pop(0)

                for child in children:
                    self.selection['children'][child] = None

                self.set_colors()  # set color list
            else:
                children = self.nodes_list
                for child in children:
                    self.selection['children'][child] = None

                self.set_colors()  # set color list

        return self.selection

    def set_colors(self):
        color_state = False

        if self.selection['parent']:
            for color in link_to_nodes_color:
                if " %s " % (self.selection['parent'].keys()[0].Class()) in color.keys()[0]:
                    self.selection['parent'][self.selection['parent'].keys()[0]] = color[color.keys()[0]]

                    color_state = True

            if not color_state:
                self.selection['parent'][self.selection['parent'].keys()[0]] = color['None']

        if self.selection['children']:
            for node in self.selection['children']:
                color_state = False

                for color in link_to_nodes_color:
                    if " %s " % (node.Class()) in color.keys()[0]:
                        self.selection['children'][node] = color[color.keys()[0]]

                        color_state = True

                if not color_state:
                    self.selection['children'][node] = color['None']

    def update_nodes_dict(self, new_parent, update_dict):
        """
        function: update_nodes_dict
        inputs:
            - new_parent: nuke node name
            - update_dict:
                {
                'children':
                    {
                    <nuke_node1>: [color_list],
                    <nuke_node2>: [color_list]
                    },
                'parent':
                    {
                    <nuke_node>: [color_list]
                    }
                }

                update_dict example:
                {
                'children':
                    {
                    <Grade14 at 0x1c2bf790>: [121.89, 169.065, 255],
                    <Grade16 at 0x1c2bff90>: [121.89, 169.065, 255],
                    <Grade12 at 0x1c2bf8b0>: [121.89, 169.065, 255],
                    <Grade13 at 0x1c2bfbb0>: [121.89, 169.065, 255],
                    <Grade15 at 0x1c2bfe30>: [121.89, 169.065, 255]
                    },
                'parent':
                    {
                    <Roto5 at 0x1c2bfd90>: [112.965, 197.88, 112.965]
                    }
                }
        """
        if update_dict['parent'] and update_dict['children']:
            old_parent_item = update_dict['parent']

            new_parent_item = {}
            new_parent_item[nuke.toNode(new_parent)] = update_dict['children'][nuke.toNode(new_parent)]
            del update_dict['children'][nuke.toNode(new_parent)]

            update_dict['children'][old_parent_item.keys()[0]] = old_parent_item[old_parent_item.keys()[0]]
            update_dict['parent'] = new_parent_item
        else:
            old_child_item = update_dict['children']

            new_parent_item = {}
            new_parent_item[nuke.toNode(new_parent)] = update_dict['children'][nuke.toNode(new_parent)]

            del update_dict['children'][nuke.toNode(new_parent)]
            update_dict['parent'] = new_parent_item

        return update_dict

    def delete_nodes_dict(self, node, update_dict, list_type=False):
        """
        function: update_nodes_dict
        inputs:
            - node: nuke node name
        return:
        {
        'children':
            {
            <nuke_node>: [color_list]
            },
        'parent':
            {
            <nuke_node>: [color_list]
            }
        }
        example:
        {
        'children':
            {
            <Grade14 at 0x1c2bf790>: [121.89, 169.065, 255],
            <Grade16 at 0x1c2bff90>: [121.89, 169.065, 255],
            <Grade12 at 0x1c2bf8b0>: [121.89, 169.065, 255],
            <Grade13 at 0x1c2bfbb0>: [121.89, 169.065, 255],
            <Grade15 at 0x1c2bfe30>: [121.89, 169.065, 255]
            },
        'parent':
            {
            <Roto5 at 0x1c2bfd90>: [112.965, 197.88, 112.965]
            }
        }
        """
        if list_type:
            del update_dict[list_type][nuke.toNode(node)]
        else:
            del update_dict['children'][nuke.toNode(node)]

        return update_dict

    def add_child(self, child):
        """
        function: add_child
        inputs:
            - child: <nuke_node>
        return:
        [red, green, blue]
        example:
        [204.0, 204.0, 204.0]
        """

        color_state = False

        for color in link_to_nodes_color:
            if " %s " % (child.Class()) in color.keys()[0]:
                child_list_color = color[color.keys()[0]]

                color_state = True

        if not color_state:
            child_list_color = color['None']

        return child_list_color

    def add_parents(self, nodes_selection, node_class=False):
        """
        function: add_parents
        inputs:
            - nodes_selection: nodes list
            - nodes_class: node class name (False or "Camera2")
        return:
        {
            'node_name1': [
                <nuke_node1>, [red, green, blue]
            ],
            'node_name2': [
                <nuke_node2>, [red, green, blue]
            ]
        }
        example:
        {
            'linkTo_parent1': [
                <linkTo_parent1 at 0x3e76550>, [112.965, 197.88, 112.965]
            ],
            'linkTo_parent2': [
                <linkTo_parent2 at 0x3e763d0>, [112.965, 197.88, 112.965]
            ],
            'linkTo_parent3': [
                <linkTo_parent3 at 0x3e76dd0>, [112.965, 197.88, 112.965]
            ],
            'linkTo_parent4': [
                <linkTo_parent4 at 0x3e762f0>, [112.965, 197.88, 112.965]
            ]
        }
        """
        if node_class:
            parents = nuke.allNodes('Camera2')
        else:
            parents = nuke.allNodes('NoOp')

            if nodes_selection in parents:
                parents.pop(parents.index(nodes_selection))

        parents_dict = {}

        for node in parents:
            if node_class:
                if "Camera2" in node.Class():
                    color_state = False

                    if node.inputs():
                        parent_class = node.input(0).Class()
                    else:
                        parent_class = node.Class()

                    for color in link_to_nodes_color:
                        if " %s " % parent_class in color.keys()[0]:
                            parents_dict[node.name()] = []
                            parents_dict[node.name()].append(node)
                            parents_dict[node.name()].append(
                                color[color.keys()[0]]
                            )

                            color_state = True

                    if not color_state:
                        parents_dict[node.name()] = []
                        parents_dict[node.name()].append(node)
                        parents_dict[node.name()].append(color['None'])
            else:
                if "_parent" in node.name():
                    color_state = False

                    if node.inputs():
                        parent_class = node.input(0).Class()
                    else:
                        parent_class = node.Class()

                    for color in link_to_nodes_color:
                        if " %s " % parent_class in color.keys()[0]:
                            parents_dict[node.name()] = []
                            parents_dict[node.name()].append(node)
                            parents_dict[node.name()].append(
                                color[color.keys()[0]]
                            )

                            color_state = True

                    if not color_state:
                        parents_dict[node.name()] = []
                        parents_dict[node.name()].append(node)
                        parents_dict[node.name()].append(color['None'])

        return parents_dict
