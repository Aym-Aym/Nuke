############################
### reloadPlugin.py v1.1 ###
### Aymeric    Ballester ###
############################

from qtswitch.QtGui import *
from qtswitch.QtCore import *

import importlib
import os
import sys
import nuke
import menu

class reloadPlugin(QWidget):

#######################
#### CONFIG WINDOW ####
#######################

	def __init__(self):
		super(reloadPlugin, self).__init__()

		self.setWindowTitle('Reload plugins')
		self.move(QCursor.pos())   
		
		self.initUI()

#######################
#######################


######################
#### SETUP WINDOW ####
######################

    	def initUI(self):


#################
#### LAYOUTS ####

		layout1 = QVBoxLayout()
        	layout2 = QHBoxLayout()
        	layout3 = QHBoxLayout()
        
#################


################
#### LABELS ####

		label1 = QLabel()
		label1.setText('Select plugins')

################


###################
#### QLINEEDIT ####

		self.line_edit1 = QLineEdit()
		self.line_edit1.setPlaceholderText('Search for plugin...')
		
###################


###############
#### QLIST ####

		self.list1 = QListWidget()
		self.list1.setSelectionMode(QAbstractItemView.ExtendedSelection)
		
		self.listUpdate()
		
###############


#####################
#### PUSH BUTTON ####

		self.push1 = QPushButton()
		self.push1.setText('Refresh List')
		
		self.push2 = QPushButton()
		self.push2.setText('Reload Plugin')
		
		self.push3 = QPushButton()
		self.push3.setText('Close')
		
		self.push4 = QPushButton()
		self.push4.setText('Try Plugin')

#####################


##################
#### CHECKBOX ####

		self.checkbox1 = QCheckBox()
		self.checkbox1.setText('Keep panel open')

#####################


##################
#### CONNECTS ####
		
		self.push1.pressed.connect(self.listUpdate)
		self.push2.pressed.connect(self.reloadScript)
		self.push2.pressed.connect(self.listUpdate)
		#self.push4.pressed.connect(self.tryPlugin)
		self.line_edit1.textChanged.connect(self.listUpdate)
		#self.push3.pressed.connect(self.close)
        		

##################


###############################
#### SET WIDGETS  & LAYOUT ####

		layout1.addLayout(layout2)
		layout2.addWidget(label1)
		layout1.addWidget(self.line_edit1)
		#layout2.addWidget(self.checkbox1)
		layout1.addWidget(self.list1)
		layout1.addLayout(layout3)
		layout3.addWidget(self.push1)
		#layout3.addWidget(self.push4)
		layout3.addWidget(self.push2)
		#layout3.addWidget(self.push3)

		self.setLayout(layout1)       

###############################


######################
######################


########################
#### list_update ####
########################

	def listUpdate(self):
		self.scripts_path, self.script_name = os.path.split(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
		listdir = os.listdir('%s/python' % (self.scripts_path))
		
		self.list1.clear()
		
		self.list1.addItem('menu.py')
		item1 = self.list1.findItems('menu.py',Qt.MatchExactly)
		
		path = '%s/menu.py' % (self.scripts_path)
		
		if os.path.isfile('%sc' % (path)):
			if os.path.getctime(path) > os.path.getctime('%sc' % (path)):
				item1[0].setBackground(QColor('#964f50'))
				item1[0].setForeground(QColor('#441c1c'))
			else:
				item1[0].setBackground(QColor('#5f965b'))
				item1[0].setForeground(QColor('#1c441c'))
		else:
			item2[0].setBackground(QColor('#964f50'))
			item2[0].setForeground(QColor('#441c1c'))

		self.list1.addItem('-------------------------------------------------')

		searchs = self.line_edit1.text().split(' ')

		memory = []

		if self.line_edit1.text():
			for folder in listdir:
				for search in searchs:
					if search:
						if search.lower() in folder.lower():
							if folder.lower() not in memory:
								memory.append(folder.lower())
								path = '%s/python/%s/%s.py' % (self.scripts_path,folder,folder)

								self.list1.addItem(folder)
								item2 = self.list1.findItems(folder,Qt.MatchExactly)
								
								if os.path.isfile(path+'c'):
									if os.path.getctime(path) > os.path.getctime(path+'c'):
										item2[0].setBackground(QColor('#964f50'))
										item2[0].setForeground(QColor('#441c1c'))
									else:
										item2[0].setBackground(QColor('#5f965b'))
										item2[0].setForeground(QColor('#1c441c'))
								else:
									item2[0].setBackground(QColor('#964f50'))
									item2[0].setForeground(QColor('#441c1c'))

					else:
						if folder.lower() not in memory:
							path = '%s/python/%s/%s.py' % (self.scripts_path,folder,folder)
							
							#if folder != '.git':
							self.list1.addItem(folder)
							item2 = self.list1.findItems(folder,Qt.MatchExactly)
							
							if os.path.isfile(path+'c'):
								if os.path.getctime(path) > os.path.getctime(path+'c'):
									item2[0].setBackground(QColor('#964f50'))
									item2[0].setForeground(QColor('#441c1c'))
								else:
									item2[0].setBackground(QColor('#5f965b'))
									item2[0].setForeground(QColor('#1c441c'))
							else:
								item2[0].setBackground(QColor('#964f50'))
								item2[0].setForeground(QColor('#441c1c'))

		else:
			for folder in listdir:
				path = '%s/python/%s/%s.py' % (self.scripts_path,folder,folder)
				
				#if folder != 'reloadPlugin':
				self.list1.addItem(folder)
				item2 = self.list1.findItems(folder,Qt.MatchExactly)
				
				if os.path.isfile(path+'c'):
					if os.path.getctime(path) > os.path.getctime(path+'c'):
						item2[0].setBackground(QColor('#964f50'))
						item2[0].setForeground(QColor('#441c1c'))
					else:
						item2[0].setBackground(QColor('#5f965b'))
						item2[0].setForeground(QColor('#1c441c'))
				else:
					item2[0].setBackground(QColor('#964f50'))
					item2[0].setForeground(QColor('#441c1c'))


########################
#### RELOAD SCRIPTS ####
########################

	def reloadScript(self):
		for plugin in self.list1.selectedItems():
			if plugin.text() != '-------------------------------------------------':
				if plugin.text() == 'menu.py':
					scriptPath = '%s/menu.pyc' % (self.scripts_path)
					
					if os.path.isfile(scriptPath):
						os.remove(scriptPath)

					reload(menu)
					
					from menu import *
				else:
					if plugin.text() == 'linkToV2dsfsdg':
						scriptPath = '%s/python/linkToV2/qwidget_default.pyc' % (self.scripts_path)
						
						if os.path.isfile(scriptPath):
							os.remove(scriptPath)

						reload(sys.modules[str("qwidget_default")])

					allScript = os.listdir('%s/python/%s'% (self.scripts_path,plugin.text()))

					for file in allScript:
						if file != ".git" and file != ".gitignore" and file != "README.MD" and file != "README.txt" and file != "qwidget_default":
							if ('icons' not in file) and ('json' not in file) and ('img' not in file):
								scriptPath = '%s/python/%s/%s.pyc' % (self.scripts_path,plugin.text(),file)
						
								if os.path.isfile(scriptPath):
									os.remove(scriptPath)

								fileName = file.split('.py')

								reload(sys.modules[str(fileName[0])])
			
				print '%s has been reloaded!' % (plugin.text())
		
########################
########################

####################
#### TRY PLUGIN ####
####################

	def tryPlugin(self):
		for plugin in self.list1.selectedItems():
			exec('import %s' %(plugin.text()))
			exec('%s.%s()' % (plugin.text(),plugin.text()))