# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Thematic
                                 A QGIS plugin
 Thematic cartography tools for processing
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-07-19
        copyright            : (C) 2018 by Lionel Cacheux
        email                : lionel.cacheux@gmx.fr
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

__author__ = 'Lionel Cacheux'
__date__ = '2018-07-19'
__copyright__ = '(C) 2018 by Lionel Cacheux'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect
import os.path
from os import path
import shutil

from qgis.core import QgsProcessingAlgorithm, QgsApplication, QgsStyle, Qgis, QgsSettings

from qgis.PyQt.QtWidgets import *

from .ThematicProvider import ThematicProvider
from qgis.utils import iface
from PyQt5.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings


from .palette_dialog import AddPaletteDialog
from .remove_palette_dialog import RemovePaletteDialog

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class ThematicPlugin(object):

    def __init__(self):
        # self.provider = ThematicProvider()        
        # remplacé par
        self.provider =  None
        
    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = ThematicProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        # Ajout        
        """Init Processing provider for QGIS >= 3.8."""
        
        self.initProcessing()
        
        try:

            if 'INSEE' in os.getenv('USERDNSDOMAIN'):

                pluginPath = os.path.abspath(os.path.dirname(__file__))
                images = pluginPath + os.sep + "images" + os.sep
                self.pluginMenu = iface.settingsMenu().addMenu(QIcon(images + 'palette_2018.svg'), "Palette Insee 2018")

                self.actionAdd = QAction(QIcon(images + 'palette_2018.svg'),
                                          "Installer la palette", iface.mainWindow())
                self.actionAdd.triggered.connect(self.runAddPalette)
                self.first_start_actionAdd = True

                self.actionRemove = QAction(QIcon(images + 'palette_2018_remove.svg'),
                                          "Supprimer l'ancienne palette", iface.mainWindow())
                self.actionRemove.triggered.connect(self.runRemovePalette)
                self.first_start_actionRemove = True

                # self.actionAide.triggered.connect(showHelp)
                self.pluginMenu.addAction(self.actionAdd)
                self.pluginMenu.addAction(self.actionRemove)
        except:
            pass

        else:
            pass

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
            
        # if hasattr(self, 'actionEditor'):  iface.removeToolBarIcon(self.actionEditor)
        try:
            self.pluginMenu.parentWidget().removeAction(self.pluginMenu.menuAction())  # Remove from Extension menu
            QgsApplication.processingRegistry().removeProvider(self.provider)
        except:
            pass

    def runAddPalette(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start_actionAdd == True:
            self.first_start_actionAdd = False
            self.dlgAdd = AddPaletteDialog()

        # show the dialog
        self.dlgAdd.show()
        # Run the dialog event loop
        result = self.dlgAdd.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            qstyles = QgsStyle.defaultStyle()

            favoriteRamps = qstyles.symbolsOfFavorite(QgsStyle.StyleEntity.ColorrampEntity)
            for i in favoriteRamps:
                qstyles.removeFavorite(QgsStyle.StyleEntity.ColorrampEntity, i)

            qstyles.importXml(os.path.abspath(os.path.dirname(__file__)) + '/palettes/symbology-style.xml')

            listeGpl = os.listdir(os.path.abspath(os.path.dirname(__file__)) + '/palettes')
            for item in listeGpl:
                fichier = os.path.abspath(os.path.dirname(__file__)) + '/palettes/' + item
                shutil.copy(fichier, re.sub('\\\\', '/', QgsApplication.qgisSettingsDirPath()) + '/palettes')


                QgsApplication.qgisSettingsDirPath()

            newFavorites = ['Insee-Bleu_2P', 'Insee-Bleu_3P', 'Insee-Bleu_4P', 'Insee-Bleu_5P', 'Insee-Bleu_6P', 'Insee-Jaune_1N1P', 'Insee-Jaune_1N2P', 'Insee-Jaune_1N3P', 'Insee-Jaune_1N4P', 'Insee-Jaune_1N5P', 'Insee-Jaune_2N1P', 'Insee-Jaune_2N2P', 'Insee-Jaune_2N3P', 'Insee-Jaune_2N4P', 'Insee-Jaune_3N1P', 'Insee-Jaune_3N2P', 'Insee-Jaune_3N3P', 'Insee-Jaune_4N1P', 'Insee-Jaune_4N2P', 'Insee-Jaune_5N1P']
            for i in newFavorites:
                qstyles.addFavorite(QgsStyle.StyleEntity.ColorrampEntity,i)

            app = QgsApplication.instance()

            params = QgsSettings(
                app.qgisSettingsDirPath() + "QGIS/QGIS3.ini", QSettings.IniFormat
            )

            params.setValue('colors/showInMenuList', ['Insee2018 - Couleurs de base','Insee2018 Bleu—Jaune'])
            for item in QgsApplication.colorSchemeRegistry().schemes():
                QgsApplication.colorSchemeRegistry().removeColorScheme(item)

            # QgsApplication.colorSchemeRegistry().addUserSchemes()
            QgsApplication.colorSchemeRegistry().addDefaultSchemes()

            iface.messageBar().pushMessage("Palette", "La palette de couleurs Insee a été installée", level=Qgis.Info)


    def runRemovePalette(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start_actionRemove == True:
            self.first_start_actionRemove = False
            self.dlgRemove = RemovePaletteDialog()

        # show the dialog
        self.dlgRemove.show()
        # Run the dialog event loop
        result = self.dlgRemove.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            style = QgsStyle.defaultStyle()

            listeTagsSymbols = ['Contours', 'Analyses', 'Dossier', 'Flash', 'IP', 'Insee']
            # listeIdTagsSymbols = [style.tagId(n) for n in listeTagsSymbols]
            for symbolIdTag in [style.tagId(n) for n in listeTagsSymbols]:
                for i in style.symbolsWithTag(QgsStyle.StyleEntity.SymbolEntity, symbolIdTag):
                    style.removeSymbol(i)

            listeTagsRamps = ['Analyses_deg', 'Dossier_deg', 'Flash_deg', 'IP_deg']
            # listeIdTagsRamps = [style.tagId(n) for n in listeTagsRamps]
            for rampIdTag in [style.tagId(n) for n in listeTagsRamps]:
                for i in style.symbolsWithTag(QgsStyle.StyleEntity.ColorrampEntity, rampIdTag):
                    style.removeColorRamp(i)

            app = QgsApplication.instance()
            params = QgsSettings(
                app.qgisSettingsDirPath() + "QGIS/QGIS3.ini", QSettings.IniFormat
            )

            params.remove('colors')
            params.setValue('colors/showInMenuList', ['Insee2018 - Couleurs de base','Insee2018 Bleu—Jaune'])
            for item in QgsApplication.colorSchemeRegistry().schemes():
                QgsApplication.colorSchemeRegistry().removeColorScheme(item)

            # QgsApplication.colorSchemeRegistry().addUserSchemes()
            QgsApplication.colorSchemeRegistry().addDefaultSchemes()

            iface.messageBar().pushMessage("Palette", "L'ancienne palette a été effacée", level=Qgis.Info)


from qgis.core import *
# from qgis.gui import *
import re

@qgsfunction(args=2, group='Thematic')
def retour_ligne(values, feature, parent):
    """
        Retour &agrave; la ligne automatique
        
        <h4>Syntaxe</h4>
        <p> retour_ligne(<i>LibGeo, NbCaract&egrave;res</i>)</p>

        <h4>Arguments</h4>
        <p><i>  LibGeo</i> &rarr; Libell&eacute; g&eacute;ographique &agrave; afficher</p>
        <p><i>  NbCaract&egrave;res</i> &rarr; Nombre de caract&egrave;res minimum avant retour &agrave; la ligne</p>
        
        <h4>Exemple</h4>
        <p><!-- Show example of function.-->
        retour_ligne(LIBGEO,5) </p>
    """
    result0 = re.sub('(.{'+str(values[1])+'}[^-]*)-','\\1-\n',values[0])
    result1 = re.sub('(.{'+str(values[1])+'}[^\\s.]*)\\s','\\1\n',result0)
    return result1

@qgsfunction(3,group='Thematic')
def  tcam(values, feature, parent):
    """
        Taux de croissance annuel moyen (en %)
        
        <h4>Syntaxe</h4>
        <p> tcam(<i>Annee1, Annee2, NbAnnees</i>)</p>

        <h4>Arguments</h4>
        <p><i>  Annee1</i> &rarr; Ann&eacute;e de d&eacute;part
        <p><i>  Annee2</i> &rarr; Ann&eacute;e d'arriv&eacute;e
        <p><i>  NbAnnees</i> &rarr; Nombre d'ann&eacute;es<br></p>
        <p>Le taux de croissance annuel moyen n'est pas calcul&eacute; en cas de valeur manquante<br></p>
        
        <h4>Exemple</h4>
        <p><!-- Show example of function.-->
              tcam(POP2006, PO2011,5) </p>
    """  
    try: # si une erreur est detectee dans le bloc "try", c'est le bloc "except" qui s'execute (traitement des exceptions)
        annee1 = float(values[0]) # pour passer un nombre entier en nombre a virgule flottante
        annee2 = float(values[1])
        NbAnnees = values[2]
        return ((annee2/annee1)**(1.0/NbAnnees)-1)*100
    except:
        return None

@qgsfunction(args=2, group='Thematic')
def discontinuite_relative(values, feature, parent):
    """
        Discontinuit&eacute; relative entre deux variables
        <p>==>  max( var1 , var2 ) / min( var1 , var2 )</p>

        <h4>Syntaxe</h4>
        <p> discontinuite_relative(<i>variable1,variable2</i>)</p>

        <h4>Arguments</h4>
        <p><i>  variable1, variable2</i> &rarr; variables &agrave; comparer</p>
        
        <h4>Exemple</h4>
        <p><!-- Show example of function.-->
        discontinuite_relative("VAR1","VAR2") </p>
    """
    return max(float(values[0]),float(values[1]))/min(float(values[0]),float(values[1]))

@qgsfunction(args=2, group='Thematic')
def discontinuite_absolue(values, feature, parent):
    """
        Discontinuit&eacute; absolue entre deux variables
        <p>==>  max( var1 , var2 ) - min( var1 , var2 )</p>

        <h4>Syntaxe</h4>
        <p> discontinuite_absolue(<i>variable1,variable2</i>)</p>

        <h4>Arguments</h4>
        <p><i>  variable1, variable2</i> &rarr; variables &agrave; comparer</p>
        
        <h4>Exemple</h4>
        <p><!-- Show example of function.-->
        discontinuite_absolue("VAR1","VAR2") </p>
    """
    return max(values[0],values[1]) - min(values[0],values[1])

@qgsfunction(2,group='Thematic')
def discontRelative(values, feature, parent):
    """
        Discontinuit&eacute; relative entre deux variables
        <p>==>  max( var1 , var2 ) / min( var1 , var2 )</p>

        <h4>Syntaxe</h4>
        <p> discontRelative(<i>variable1,variable2</i>)</p>

        <h4>Arguments</h4>
        <p><i>  variable1, variable2</i> &rarr; variables &agrave; comparer</p>
        
        <h4>Exemple</h4>
        <p><!-- Show example of function.-->
        discontRelative("VAR1","VAR2") </p>
    """
    return max(float(values[0]),float(values[1]))/min(float(values[0]),float(values[1]))

@qgsfunction(2,group='Thematic')
def discontAbsolue(values, feature, parent):
    """
        Discontinuit&eacute; absolue entre deux variables
        <p>==>  max( var1 , var2 ) - min( var1 , var2 )</p>

        <h4>Syntaxe</h4>
        <p> discontAbsolue(<i>variable1,variable2</i>)</p>

        <h4>Arguments</h4>
        <p><i>  variable1, variable2</i> &rarr; variables &agrave; comparer</p>
        
        <h4>Exemple</h4>
        <p><!-- Show example of function.-->
        discontAbsolue("VAR1","VAR2") </p>
    """
    return max(values[0],values[1]) - min(values[0],values[1])
    
@qgsfunction(1,group='Thematic')
def extraire_libgeo(values, feature, parent):
    """
        Extraire un libell&eacute; g&eacute;ographique d'une chaine de caract&egrave;res de type de type Corse-du-Sud (2A)

        <h4>Syntaxe</h4>
        <p> extraire_libgeo(<i>ChaineCaractere</i>)</p>

        <h4>Arguments</h4>
        <p><i>  ChaineCaractere</i> &rarr; Chaine de caract&egrave;res contenant un libell&eacute; g&eacute;ographique + un code g&eacute;ographique entre parenth&egrave;ses</p>
        
        <h4>Exemple</h4>
        <p><!-- Show example of function.-->
        extraire_libgeo(DEP) </p>
    """
    return re.search('(.+)\s\(',values[0]).group(1)