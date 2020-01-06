# coding=utf-8

""" For all vector layer """

import processing


def count_overlap(layer, out):
    """

    :param layer: the polygon footprint
    :param out: the output

    :return: return layer
    """

    params_join = {
        'INPUT': layer,
        'JOIN': layer,
        'PREDICATE': [2],
        'JOIN_FIELDS': [],
        'SUMMARIES': [0],
        'DISCARD_NONMATCHING': False,
        'PREFIX': '',
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }

    result = processing.run("qgis:joinbylocationsummary", params_join)

    params_delete = {
        'INPUT': result['OUTPUT'],
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }
    if out == []:
        params_delete['OUTPUT'] = out

    result = processing.runAndLoadResults("qgis:deleteduplicategeometries", params_delete)
