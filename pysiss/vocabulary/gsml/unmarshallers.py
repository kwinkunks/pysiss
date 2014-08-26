""" file:   unmarshallers.py (pysiss.vocabulary.gml)
    author: Jess Robertson
            CSIRO Mineral Resources Flagship
    date:   Monday 25 August, 2014

    description: Unmarshalling functions for GeoSciML/GML objects
"""

from ...coverage.vector import MappedFeature
from ..namespaces import NamespaceRegistry, expand_namespace, shorten_namespace
from ..gml.unmarshallers import UNMARSHALLERS as GML_UNMARSHALLERS

NAMESPACES = NamespaceRegistry()


def mapped_feature(elem):
    """ Unmarshal a gsml:MappedFeature element
    """
    # Shape and projection data
    shape_elem = elem.xpath('./gsml:shape', namespaces=NAMESPACES)[0]
    shape_data = shape(shape_elem)
    shape_elem.clear()  # Remove shape element from metadata

    # Identifier
    ident = elem.get(expand_namespace('gml:id')) or None

    return MappedFeature(ident=ident, shape=shape_data['shape'],
                         projection=shape_data['projection'],
                         metadata=elem)


def shape(elem):
    """ Unmarshal a gsml:shape element

        Here we just pass through to underlying gml shape data
    """
    child = elem[0]
    unmarshal = GML_UNMARSHALLERS[shorten_namespace(child.tag)]
    return unmarshal(child)


def get_value(elem):
    """ Unmashall an element containing a gsml:value element somewhere in its
        descendents.

        Returns the text value for a given element, stripping out children of
        the given element
    """
    result = elem.xpath('.//gsml:value/text()',
                        namespaces=NAMESPACES)
    if result:
        return result[0]
    else:
        return None


def cgi_termrange(elem):
    """ Unmarshal a gsml:CGI_TermRange element

        Return the value range for a given element
    """
    return map(get_value,
               elem.xpath('.//gsml:CGI_TermValue',
                          namespaces=NAMESPACES))


def sampling_frame(elem):
    """ Unmarshal a gsml:samplingFrame element
    """
    return elem.get(expand_namespace('xlink:href'))


UNMARSHALLERS = {
    'gsml:shape': shape,
    'gsml:value': get_value,
    'gsml:CGI_TermValue': get_value,
    'gsml:CGI_TermRange': cgi_termrange,
    'gsml:preferredAge': get_value,
    'gsml:observationMethod': get_value,
    'gsml:positionalAccuracy': get_value,
    'gsml:samplingFrame': sampling_frame,
    'gsml:MappedFeature': mapped_feature
}

__all__ = (UNMARSHALLERS,)
