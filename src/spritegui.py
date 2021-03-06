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
import sys
import os
import shutil
import string
from PyQt4.Qt import Qt
from PyQt4 import QtGui, QtCore
from PIL import Image

class SpriteGUI(QtGui.QWidget):
  
    def __init__(self, main, icon, dirname, tree):
        super(SpriteGUI, self).__init__()
        self.main = main
        self.dirname = dirname
        self.icon = str(icon)
        self.tree = tree
        
        try:
            self.extension = self.tree.spr_parser.get(self.icon, 'extension')
        except:
            self.extension = "png"
        
        self.image_file = os.path.join(self.dirname, "Sprites", "%s"%(self.icon))
        
        try:
            self.xorig = self.tree.spr_parser.get(self.icon, 'xorig')
            self.yorig = self.tree.spr_parser.get(self.icon, 'yorig')
        except:
            self.xorig = 0
            self.yorig = 0

        try:
            self.framenumber = int(self.tree.spr_parser.get(self.icon, 'framenumber'))
        except:
            self.framenumber = 0
        
        try:
            self.image_handle = open(self.image_file+"."+self.extension, 'rb')
            self.frames = 1
        except:
            self.image_handle = open(self.image_file+"-0."+self.extension, 'rb')
            self.image_file = os.path.join(self.dirname, "Sprites", self.icon+"-0."+self.extension)
            self.frames = 0
            files = [f for f in os.listdir(os.path.join(self.dirname, "Sprites"))]
            for f in files:
                if self.icon in f:
                    self.frames += 1

        self.img = Image.open(self.image_handle)
        self.width, self.height = self.img.size
        self.format = self.extension
        self.initUI()
        
    def initUI(self):

        #Groupbox Container-----------------------------------
        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
                
        self.BtnOK = QtGui.QPushButton('OK')
        self.BtnOK.setIcon(QtGui.QIcon(os.path.join('Data','accept.png')))
        self.BtnOK.clicked.connect(self.ok)

        self.LblShow = QtGui.QLabel('Show:')
        self.BtnNext = QtGui.QPushButton()
        #self.BtnNext.clicked.connect(self.nextframe)
        self.connect(self.BtnNext,QtCore.SIGNAL("clicked()"),self.nextframe)
        self.BtnNext.setIcon(QtGui.QIcon(os.path.join('Data','nextimg.png')))
        
        self.ShowImage = QtGui.QLabel(str(self.framenumber))
        #self.connect(self.ShowImage,QtCore.SIGNAL("textChanged()"),self.previewframe)
        
        self.BtnPrev = QtGui.QPushButton()
        self.BtnPrev.clicked.connect(self.previousframe)
        if self.framenumber == self.frames-1 or self.frames == 1:
            self.BtnNext.setEnabled(False)
        
        if self.framenumber == 0:
            self.BtnPrev.setEnabled(False)
        self.BtnPrev.setIcon(QtGui.QIcon(os.path.join('Data','previmg.png')))

        self.ShowFrame = QtGui.QFrame()
        self.showlayout = QtGui.QGridLayout()
        self.showlayout.setMargin (0)
        self.showlayout.addWidget(self.LblShow,1,0)
        self.showlayout.addWidget(self.BtnNext,1,3)
        self.showlayout.addWidget(self.ShowImage,1,2)
        self.showlayout.addWidget(self.BtnPrev,1,1)
        
        self.ShowFrame.setLayout(self.showlayout)
        
        #Scroll Area------------------------------------------
        self.sprite = QtGui.QPixmap(self.image_file)                         
        
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
        
		
        self.BtnLoad = QtGui.QPushButton('Load Sprite')
        self.BtnLoad.setIcon(QtGui.QIcon('Data/folder.png'))
        self.BtnLoad.clicked.connect(self.LoadSprite)

        self.BtnSave = QtGui.QPushButton('Save Sprite')
        self.BtnSave.setIcon(QtGui.QIcon('Data/save.png'))
        self.BtnSave.clicked.connect(self.SaveSprite)
 
        self.BtnEdit = QtGui.QPushButton('Edit Sprite')
        self.BtnEdit.setIcon(QtGui.QIcon('Data/editbutton.png'))
        self.BtnEdit.setEnabled(False)#This is currently not implemented
        self.BtnEdit.clicked.connect(self.EditSprite)

        self.LblName = QtGui.QLabel('Name:') 
        self.qleSprite = QtGui.QLineEdit("%s"%(self.icon))
        
        self.NameFrame = QtGui.QFrame()
        
        self.namelayout = QtGui.QGridLayout()
        self.namelayout.setMargin (0)
        self.namelayout.addWidget(self.LblName,0,0)
        self.namelayout.addWidget(self.qleSprite,0,1)
        
        self.NameFrame.setLayout(self.namelayout)

        self.OriginBox = QtGui.QGroupBox("Origin")
        self.LblX = QtGui.QLabel('X:')
        self.LblX.setAlignment(QtCore.Qt.AlignRight)
        self.LblY = QtGui.QLabel('Y:')
        self.LblY.setAlignment(QtCore.Qt.AlignRight)
        self.EdirXorig = QtGui.QLineEdit(str(self.xorig))
        self.EdirYorig = QtGui.QLineEdit(str(self.yorig))

        self.BtnCenter = QtGui.QPushButton('Center')
        self.BtnCenter.clicked.connect(self.CenterSprite)

        self.originlayout = QtGui.QGridLayout()
        self.originlayout.setMargin (3)
        self.originlayout.addWidget(self.LblX,7,0)
        self.originlayout.addWidget(self.EdirXorig,7,1)
        self.originlayout.addWidget(self.LblY,7,2)
        self.originlayout.addWidget(self.EdirYorig,7,3)
        self.originlayout.addWidget(self.BtnCenter,8,1,2,2)
        
        self.OriginBox.setLayout(self.originlayout)

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
        self.nameandlayout.addWidget(self.LblSubimages,6,0)
        self.nameandlayout.addWidget(self.ShowFrame,7,0)
        self.nameandlayout.addWidget(self.BtnNext,7,1)
        
        self.nameandlayout.addWidget(self.OriginBox,9,0)
        
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
        pen = QtGui.QPen(QtCore.Qt.red)
        line = str(self.click_positions)
        positions = line.replace(')', '(')
        positions = positions.replace(',', '(')
        positions = positions.replace(' ', '')
        lista = positions.split('(')
        self.xorig = lista[1]
        self.yorig = lista[2]
        self.EdirXorig.setText(self.xorig)
        self.EdirYorig.setText(self.yorig)
        self.click_positions = []


    def nextframe(self):
        self.framenumber+= 1
        self.ShowImage.setText(str(self.framenumber))
        self.previewframe()
                    
    def previousframe(self):
        self.framenumber-=1
        self.ShowImage.setText(str(self.framenumber))   
        self.previewframe()
        
    def previewframe(self):
       # print (self.framenumber)
        if self.framenumber==0:
            self.BtnPrev.setEnabled(False)
        else:
            self.BtnPrev.setEnabled(True)

        if self.framenumber==(self.frames-1):
            self.BtnNext.setEnabled(False)
        else:
            self.BtnNext.setEnabled(True)
            
        self.actualframe = os.path.basename(self.image_file)
        self.actualframe = string.split(self.image_file,"-")
        self.finalsprite = self.actualframe[0]+"-"+str(self.framenumber)+"."+self.extension 
        self.sprite = QtGui.QPixmap(self.finalsprite)
        #print (self.finalsprite)
        self.spriteLbl.setPixmap(self.sprite)
        
        
    def LoadSprite(self):
        self.asprite = str(QtGui.QFileDialog.getOpenFileName(self, 'Open Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)")))
        
        if self.asprite is not '':
            shutil.copy(self.asprite, self.image_file)

            sprite = os.path.basename(self.asprite)
            self.extension = sprite[-3:]

            self.image_file = os.path.join(self.dirname, 'Sprites', '%s.%s' %(self.icon, self.extension))
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
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Sprite(s)', 
                '', self.tr("Image file (*.png)"))

        if self.fname !='':
            shutil.copy(self.image_file, self.fname)


    def EditSprite(self):
        os.startfile(self.image_file)#TO BE DONE :)

    def ok(self):
        self.close()
        icon = str(self.qleSprite.text())
        if self.icon != icon:
            self.tree.spr_parser.remove_section(self.icon)
            self.tree.spr_parser.add_section(icon)

            in_fname = os.path.join(self.dirname, 'Sprites', "%s.%s" %
                                    (self.icon, self.extension))
            out_fname = os.path.join(self.dirname, 'Sprites', "%s.%s" % 
                                        (icon, self.extension)) 

            self.image_handle.close()
            os.rename(in_fname, out_fname)
            self.icon = str(self.qleSprite.text())

        self.tree.spr_parser.set(self.icon, 'xorig', str(self.EdirXorig.text()))
        self.tree.spr_parser.set(self.icon, 'yorig', str(self.EdirYorig.text()))
        self.tree.spr_parser.set(self.icon, 'extension', self.extension)
        self.tree.spr_parser.set(self.icon, 'framenumber', str(self.ShowImage.text()))

        self.tree.write_sprites()

        self.main.updatetree()
        self.main.qmdiarea.activeSubWindow().close()

