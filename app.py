#!flask/bin/python
from flask import Flask, request, abort, make_response, jsonify
import twillio_manager
from config import BUSINESS_NUMBER
import logging

app = Flask(__name__)


@app.route('/api/v1.0/sendsms', methods=['POST'])
def send_sms_api():
    """Receives encoded post data of the form {replyto:*customers number*,name:*customer name*,body:*message*}
        Returns json"""
    if not request.form or 'replyto' not in request.form or 'name' not in request.form:
        abort(400)
    body = _build_body_from_xwww(request.form)
    message = twillio_manager.send_sms(to=BUSINESS_NUMBER, body=body)
    if isinstance(message, str):
        abort(500)
    elif message.status in ['failed', 'undelivered']:
        error_text = 'Failed to send, error code:{code}'.format(message.errorcode)
        logging.error(error_text)
        make_response(jsonify({'error': error_text}), 501)
    return make_response(jsonify({'success': 'Message sent'}), 200)


def _build_body_from_xwww(xwwwobj):
    """Takes the raw x-www-form-urlencoded and returns a body formed in the way we want"""
    xwwwobj = {key: str(value) for key, value in xwwwobj.iteritems()}
    return "From: {replyto}\nName: {name}\nBody:{body}".format(**xwwwobj)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': '{}'.format(error)}), 400)

if __name__ == '__main__':
    app.run(debug=True)
