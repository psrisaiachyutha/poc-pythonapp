# This is a sample Python script.
from threading import Thread

from flask import jsonify
from dotenv import load_dotenv

from utils.rabbitmq import start_rabbitmq_consumer


def run_flask_app():
    from flask import Flask
    from controllers.report import report
    from controllers.search import search
    from gevent.pywsgi import WSGIServer
    # from flask_cors import  CORS

    app = Flask(__name__)

    # Register the API blueprints
    app.register_blueprint(report, url_prefix='/api/v1/report')
    app.register_blueprint(search, url_prefix='/api/v1/search')

    @app.errorhandler(400)
    def bad_request(e):
        # TODO NEED TO STRUCTURE THE PROPER MESSAGE AND STRUCTURE FOR THE RESPONSE
        return jsonify(error=str(e)), 400

    print(app.url_map)
    app.run()

    # TODO Enable the below lines for production
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()


if __name__ == '__main__':
    # TODO create logger instead of print statements and write proper logs
    load_dotenv()
    consumer_thread = Thread(target=start_rabbitmq_consumer)
    try:
        print('thread is starting')
        consumer_thread.start()
    except Exception as e:
        print('error message', e)
    run_flask_app()


