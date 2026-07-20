from lxml import etree
from io import StringIO
from django.http import HttpResponse
import re


def xpath_query(request):
    '''
    Get the `xpath` value from the GET request,
    get the 'xml' value from the GET request,
    construct and parse the xml payload,
    return the result of the XPath query "/tag[@id={}]" format from the parsed xml
    '''
    value = request.GET['xpath']
    
    # Validate and sanitize the xpath parameter
    # Only allow alphanumeric characters, hyphens, and underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        return []
    
    f = StringIO(request.GET['xml'])
    tree = etree.parse(f)
    
    # Use parameterized XPath query with proper escaping
    # Using XPath variables to prevent injection
    result = tree.xpath("/tag[@id=$id]", id=value)
    return result