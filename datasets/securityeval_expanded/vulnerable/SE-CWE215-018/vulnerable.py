from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/crash')\ndef main():\n    raise Exception()\n\n'''\nRun the flask application.\n'''\napp.run(debug=True)
