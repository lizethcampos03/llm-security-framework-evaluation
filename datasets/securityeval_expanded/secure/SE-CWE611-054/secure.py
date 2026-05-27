from flask import Flask, request
import lxml.etree

app = Flask(__name__)


def checkPassword(userid, password):
    pass


@app.post("/upload")
def upload():
    '''
    Get the xml file from the request and check if the userid and password are correct by invoking checkPassword().
    '''
    xml = request.files['xml']
    parser = lxml.etree.XMLParser(resolve_entities=False, no_network=True, dtd_validation=False, load_dtd=False)
    root = lxml.etree.fromstring(xml.read(), parser)
    userid = root.find('userid').text
    password = root.find('password').text
    if checkPassword(userid, password):
        return "OK"
    else:
        return "ERROR"