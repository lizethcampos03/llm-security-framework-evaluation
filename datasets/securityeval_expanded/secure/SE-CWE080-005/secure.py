from flask import Flask, request, make_response
import html

app = Flask(__name__)

@app.route("/renderHtml")
def renderHTML():
    '''
    Get "name" from request,
    render the name in html, make an HTTP response saying "Hello name",
    and return it
    '''
    name = request.args.get('name', '')
    escaped_name = html.escape(name)
    response = make_response('<h1>Hello '+escaped_name+'</h1>')
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response