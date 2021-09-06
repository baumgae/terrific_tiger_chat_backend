import logging

from flask_restplus import Api
import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Terrific Tiger Chat API',
          description='Mobile Web Applications Project using Flask, Angular, MongoDB and WebRTC')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

