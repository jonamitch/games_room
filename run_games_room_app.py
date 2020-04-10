"""
Runner for the flask app - run this script to set-up the local server - also enabled for shell context
"""

from app import app
import os
import logging
from datetime import datetime


@app.shell_context_processor
def make_shell_context():
    return {}


if __name__ == '__main__':
    log_file_name = os.path.join('logs', 'games-log-{}.log'.format(datetime.now().strftime('%Y-%m-%d %H-%M-%S')))
    logging.basicConfig(level=logging.DEBUG,
                        # filename=log_file_name,
                        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    app.run(host='0.0.0.0', port=5000, debug=False, use_debugger=False, use_reloader=True, passthrough_errors=True)
