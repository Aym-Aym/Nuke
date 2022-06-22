##linkToV2 install READ ME
linkToV2 plugin by Aymeric Ballester

files:
list:

	linkToV2.py
	linkToChild.py
	linkToCreateNodes.py
	linkToCreate.py
	linkToList.py


menu.py:
import:

	import linkToV2
	import linkToCreate
	import linkToCreateNodes
	import linkToChild
	import linkToList

menu and shortcuts:

	m = nuke.menu('Nuke') // select menu type
	m.addCommand('Python/Nodes Links/Link To',"panel = linkToChild.LinkToChild(); panel.show()","#left") // "alt + left" used to create a child link to an existing parent or camera
	m.addCommand('Python/Nodes Links/Connect Nodes',"panel = linkToCreate.LinkToCreate(); panel.show()","#right") // "alt + right" used to create a child linked to a parent
	m.addCommand('Python/Nodes Links/Create Parent',"linkToCreateNodes.LinkToCreateNodes(nuke.selectedNodes()).create_parents()") // create a parent node