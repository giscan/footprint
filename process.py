# coding=utf-8

"""all of the actions"""

from footprint.gis.tools import count_overlap


def count_overlap_action(layer, out):
    """ Delete all geometries duplicated"""

    result = count_overlap(layer, out)
    return result
