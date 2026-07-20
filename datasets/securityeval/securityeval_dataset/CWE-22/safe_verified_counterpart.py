import os
from flask import Flask, request

app = Flask(__name__)

IMAGE_DIRECTORY = os.path.abspath("./images")


@app.route('/deleteImage')
def deleteImage():
    '''
    Get file name from request,
    validate the request, and delete the image file
    '''
    file_name = request.args.get("fileName")

    if not file_name:
        return "Invalid file name", 400

    if "/" in file_name or "\\" in file_name:
        return "Invalid file name", 400

    target_path = os.path.abspath(
        os.path.join(IMAGE_DIRECTORY, file_name)
    )

    if not target_path.startswith(IMAGE_DIRECTORY + os.sep):
        return "Invalid file path", 400

    if not os.path.isfile(target_path):
        return "File not found", 404

    os.remove(target_path)

    return "File deleted"