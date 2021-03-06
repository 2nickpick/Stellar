#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2013 Emilio Coppola
#
# This file is part of Stellar.
#
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

from __future__ import print_function

import os
import shutil
from PyQt4 import QtGui, QtCore
from PIL import Image

class BackgroundGUI(QtGui.QWidget):
  
    def __init__(self, main, icon, dirname, tree):
        super(BackgroundGUI, self).__init__()
        self.main = main
        self.dirname = dirname
        self.icon = str(icon)
        self.tree = tree

        #self.extension = self.tree.spr_parser.get(self.icon, 'extension')
        self.extension = "png"
        self.image_file = os.path.join(self.dirname, "Backgrounds", "%s.%s"%(self.icon, self.extension))
        #self.xorig = self.tree.spr_parser.get(self.icon, 'xorig')
        #self.yorig = self.tree.spr_parser.get(self.icon, 'yorig')
        self.xorig=0
        self.yorig=0
        
        self.image_handle = open(self.image_file, 'rb')
        self.img = Image.open(self.image_handle)
        self.width, self.height = self.img.size

        self.format = self.extension
        self.frames = 1
        
        self.initUI()
                        
    def initUI(self):

        #Groupbox Container-----------------------------------
        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        
                
        self.BtnOK = QtGui.QPushButton('OK')
        self.BtnOK.setIcon(QtGui.QIcon('Data/accept.png'))
        self.BtnOK.clicked.connect(self.ok)

        self.LblShow = QtGui.QLabel('Show:')
        self.BtnNext = QtGui.QPushButton()
        self.BtnNext.setIcon(QtGui.QIcon('Data/nextimg.png'))
        self.ShowImage = QtGui.QLineEdit("0")
        self.BtnPrev = QtGui.QPushButton()
        self.BtnPrev.setIcon(QtGui.QIcon('Data/previmg.png'))

        
        self.ShowFrame = QtGui.QFrame()
        self.showlayout = QtGui.QGridLayout()
        self.showlayout.setMargin (0)
        self.showlayout.addWidget(self.LblShow,1,0)
        self.showlayout.addWidget(self.BtnNext,1,3)
        self.showlayout.addWidget(self.ShowImage,1,2)
        self.showlayout.addWidget(self.BtnPrev,1,1)
        
        self.ShowFrame.setLayout(self.showlayout)
        

        #Scroll Area------------------------------------------
        self.sprite = QtGui.QPixmap(os.path.join(self.dirname, "Backgrounds", "%s.%s"%(self.icon, self.extension)))
                                    
        
        self.spriteLbl = QtGui.QLabel(self.main)
        self.spriteLbl.setPixmap(self.sprite)
        self.spriteLbl.setAlignment(QtCore.Qt.AlignTop)
                                    
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.spriteLbl)
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.mouseMoveEvent = self.pixelSelect
        self.scrollArea.mousePressEvent = self.pixelSelect 
        
        self.click_positions = []
        
        self.scrollArea.setWidgetResizable(True)
        
        
        #Groupbox General-------------------------------------
        self.GeneralBox = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()		
        self.NameAndThingsBox = QtGui.QFrame() 
        
		
        self.BtnLoad = QtGui.QPushButton('Load Background')
        self.BtnLoad.setIcon(QtGui.QIcon('Data/folder.png'))
        self.BtnLoad.clicked.connect(self.LoadSprite)

        self.BtnSave = QtGui.QPushButton('Save Background')
        self.BtnSave.setIcon(QtGui.QIcon('Data/save.png'))
        self.BtnSave.clicked.connect(self.SaveSprite)
 
        self.BtnEdit = QtGui.QPushButton('Edit Background')
        self.BtnEdit.setEnabled(False)
        self.BtnEdit.setIcon(QtGui.QIcon('Data/editbutton.png'))
        self.BtnEdit.clicked.connect(self.EditSprite)

        self.LblName = QtGui.QLabel('Name:') 
        self.qleSprite = QtGui.QLineEdit("%s"%(self.icon))
        
        self.NameFrame = QtGui.QFrame()
        
        self.namelayout = QtGui.QGridLayout()
        self.namelayout.setMargin (0)
        self.namelayout.addWidget(self.LblName,0,0)
        self.namelayout.addWidget(self.qleSprite,0,1)
        
        self.NameFrame.setLayout(self.namelayout)

        self.Lblspacer = QtGui.QLabel(" ")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)



        self.LblWidth = QtGui.QLabel('Width:   %d Pixels'%(self.width)) 
 
        self.LblHeight = QtGui.QLabel('Height:  %d Pixels'%(self.height))
        
        self.LblSubimages = QtGui.QLabel('Number of subimages: %d'%(self.frames))

        

        self.LblFormat = QtGui.QLabel('File Format:  %s'%(self.format)) 

        self.nameandlayout = QtGui.QGridLayout()
        self.nameandlayout.setMargin (1)
        self.nameandlayout.addWidget(self.NameFrame,0,0,1,2)	
        self.nameandlayout.addWidget(self.Lblspacer,1,0)
        self.nameandlayout.addWidget(self.BtnLoad,1,0,1,2)
        self.nameandlayout.addWidget(self.BtnSave,2,0,1,2)
        self.nameandlayout.addWidget(self.BtnEdit,3,0,1,2)
        self.nameandlayout.addWidget(self.LblWidth,4,0)
        self.nameandlayout.addWidget(self.LblHeight,5,0)
        
        self.NameAndThingsBox.setLayout(self.nameandlayout)

		
        self.layout.addWidget(self.NameAndThingsBox)
        self.layout.addItem(spacerItem)
        self.layout.addWidget(self.BtnOK)
		
        self.GeneralBox.setMaximumWidth (170)
        self.GeneralBox.setLayout(self.layout)
		
        self.ContainerGrid.setSpacing(0)
		
        self.spritesplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.spritesplitter.addWidget(self.GeneralBox)
        self.spritesplitter.addWidget(self.scrollArea)
        self.ContainerGrid.addWidget(self.spritesplitter)

        self.setLayout(self.ContainerGrid)
        
        self.image_handle.close()
        
    def CenterSprite(self, event):
        self.EdirXorig.setText(str(self.img.size[0] / 2))
        self.EdirYorig.setText(str(self.img.size[1] / 2))
        #TO DO: create cross in sprite
	
	
    def pixelSelect(self, event):
        self.click_positions.append(event.pos())

        
    def LoadSprite(self):
        self.asprite = str(QtGui.QFileDialog.getOpenFileName(self, 'Open Background', 
                '', self.tr("Image file (*.png *.gif *.jpg)")))
        
        if self.asprite is not '':
            shutil.copy(self.asprite, self.image_file)

            sprite = os.path.basename(self.asprite)
            self.extension = sprite[-3:]

            self.image_file = os.path.join(self.dirname, 'Backgrounds', '%s.%s' %(self.icon, self.extension))
            self.image_handle = open(self.image_file, 'rb')
            
            self.sprite = QtGui.QPixmap(self.image_file)
            self.spriteLbl.setPixmap(self.sprite)

            self.img = Image.open(self.image_handle)
            self.width, self.height = self.img.size
            self.format  = str(self.extension)
            self.LblWidth.setText('Width:   %d Pixels'%(self.width))
            self.LblHeight.setText('Height:  %d Pixels'%(self.height))
            self.LblFormat.setText('File Format:  %s'%(self.format))
            self.image_handle.close()

            self.tree.main.updatetree()
                

    def SaveSprite(self):
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Background', 
                '', self.tr("Image file (*.png)"))

        if self.fname !='':
            shutil.copy(self.image_file, self.fname)


    def EditSprite(self):
        os.startfile(self.image_file)#TO BE DONE :)

    def ok(self):
        self.close()
        icon = str(self.qleSprite.text())
        if self.icon is not icon:
            self.tree.spr_parser.remove_section(self.icon)
            self.tree.spr_parser.add_section(icon)

            in_fname = os.path.join(self.dirname, 'Backgrounds', "%s.%s" %
                                    (self.icon, self.extension))
            out_fname = os.path.join(self.dirname, 'Backgrounds', "%s.%s" % 
                                        (icon, self.extension)) 

            #self.image_handle.close()
            os.rename(in_fname, out_fname)
            self.icon = str(self.qleSprite.text())

        self.main.updatetree()
        self.main.qmdiarea.activeSubWindow().close()

