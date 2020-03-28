from gevent.pywsgi import WSGIServer
from app import saveInfo_app

http_server = WSGIServer(('0.0.0.0', 7497), saveInfo_app)
http_server.serve_forever()