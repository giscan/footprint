# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Footprint
                                 A QGIS plugin
 This plugin manages the footprint of aerial imagery
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-12-04
        copyright            : (C) 2019 by GISCAN
        email                : contact@giscan.com
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

__author__ = 'GISCAN'
__date__ = '2019-12-04'
__copyright__ = '(C) 2019 by GISCAN'
__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterVectorDestination)
import processing


class FootprintOverlapAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm will count the overlap of the aerial imagery footprint
    """

    # Constants used to refer to parameters and outputs.

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config):
        """
        define the input and output properties
        """

        # the polygon input
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Footprint Polygon'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        # the output
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Overlap')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        the processing
        """

        # Get Input
        footprint = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
        )

        # Get Output
        output = self.parameterAsOutputLayer(
            parameters,
            self.OUTPUT,
            context
        )

        feedback.pushInfo('Join Attributes by Location Summary')
        result = processing.run("qgis:joinbylocationsummary", {
            'INPUT': footprint,
            'JOIN': footprint,
            'PREDICATE': [2],
            'JOIN_FIELDS': [],
            'SUMMARIES': [0],
            'DISCARD_NONMATCHING': False,
            'PREFIX': '',
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }, context=context, feedback=feedback)

        feedback.pushInfo('Delete Duplicate Geometries')
        result = processing.runAndLoadResults("qgis:deleteduplicategeometries", {
            'INPUT': result['OUTPUT'],
            'OUTPUT': output
        }, context=context, feedback=feedback)

        return {self.OUTPUT: result['OUTPUT']}

    def name(self):
        """
        Returns the algorithm name
        """
        return 'Overlap'

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to.
        """
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return FootprintOverlapAlgorithm()
