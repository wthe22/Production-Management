from waitress import serve
from pyramid.config import Configurator

import manufacture


if __name__ == '__main__':
    serve(manufacture.main, host='0.0.0.0', port=6543)
