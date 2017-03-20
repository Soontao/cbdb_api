import os

from flask import Flask

from util import json_response
from routes import routes

app = Flask(__name__)
routes(app)
port = os.getenv("PORT", 3001)


@app.errorhandler(Exception)
def error(e):
	r = {
		"err": "error happened",
		"err_type": type(e).__name__,
		"err_msg": e.args[0]
	}
	return json_response(500, r)


if __name__ == '__main__':
	# Run the app, listening on all IPs with our chosen port number
	app.run(host='0.0.0.0', port=port)
