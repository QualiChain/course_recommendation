import logging
import sys


from views.app import app

from settings import API_PORT

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.info("Course recommendation services")
    app.run(host='0.0.0.0', port=API_PORT, debug=True)
