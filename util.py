from flask import Response
import json


def json_response(status: int, obj: object):
	return Response(response=json.dumps(obj, ensure_ascii=False, indent=2),
									status=200,
									mimetype="application/json")
