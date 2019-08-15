# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AssimilaDatacCubeDialog
                                 A QGIS plugin
 This plugin let's you visualise the datacube.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-08-07
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Assimila
        email                : jenny.lin@assimila.eu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import math,  os,  tempfile
from os.path import expanduser
from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt import QtNetwork
from qgis.PyQt.QtCore import pyqtSlot,  Qt,  QUrl,  QFileInfo
from qgis.PyQt.QtGui import QIntValidator
from qgis.PyQt.QtWidgets import *
from qgis.PyQt import QtWidgets
from qgis.core import (QgsProcessingParameterString,)
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply,  QNetworkAccessManager


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'assimila_datacube_dialog.ui'))


class AssimilaDatacCubeDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        super(AssimilaDatacCubeDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface


    @pyqtSlot()
    def on_btn_extent_clicked(self):

        # Gets the coordinates of the extent
        crsDest = QgsCoordinateReferenceSystem(4326)  # WGS84
        crsSrc =self.iface.mapCanvas().mapSettings().destinationCrs()
        xform = QgsCoordinateTransform()
        xform.setSourceCrs(crsSrc)
        xform.setDestinationCrs(crsDest)
        extent = xform.transform(self.iface.mapCanvas().extent())

        # Sets the value to the individual widgets
        self.W_spinBox.setValue((math.floor(extent.xMinimum())))
        self.E_spinBox.setValue((math.ceil(extent.xMaximum())))
        self.S_spinBox.setValue((math.floor(extent.yMinimum())))
        self.N_spinBox.setValue((math.ceil(extent.yMaximum())))
        #print('set canvas')
    
    @pyqtSlot()
    def on_btn_browse_keyfile_clicked(self):
        # Gets directory for the keyfile - default: /users/{user_name}/Documents
        self.dir = QFileDialog.getExistingDirectory(None, self.tr("Open Directory"),
                                                    os.path.join(expanduser("~"), "Documents"),
                                                    QFileDialog.ShowDirsOnly 
                                                    | QFileDialog.DontResolveSymlinks)

        # Appends the key file name .assimila_dq to the directory path
        self.key_file = os.path.join(self.dir, ".assimila_dq")       

        # Displays in lineEdit                             
        self.lineEdit.setText(self.key_file)   
