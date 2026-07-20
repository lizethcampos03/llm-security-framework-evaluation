from flask import Flask
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def do_computation():
    raise Exception("Secret info")

@app.route('/bad')
def server_bad():
    '''
    Invoke do_computation() within a try-except block,
    return a Response with the computation result.
    '''
    try:
        do_computation()
    except Exception as e:
        logger.error(f"An error occurred during computation: {str(e)}", exc_info=True)
        return "An error occurred while processing your request.", 500