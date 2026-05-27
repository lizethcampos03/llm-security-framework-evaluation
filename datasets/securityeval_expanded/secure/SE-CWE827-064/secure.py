from lxml import etree


def getXmlRoot():
    '''
    Create an XML parser and parse the resources/c.xml file and return the root element
    '''
    parser = etree.XMLParser(resolve_entities=False, no_network=True, dtd_validation=False, load_dtd=False)
    tree = etree.parse('resources/c.xml', parser)
    root = tree.getroot()
    return root