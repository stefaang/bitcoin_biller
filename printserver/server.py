from time import time
# HTTP Server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
# Printer
from printer import Printer

class MyHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		param = parse_qs(urlparse(self.path).query)
		# Identifier
		try:
			i = param['i'][0]
		except KeyError:
			i = str(time())
		# Amount
		try:
			b = param['b'][0]
		except KeyError:
			b = '0'
		# Address
		try:
			a = param['a'][0]
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.send_header('Access-Control-Allow-Origin', '*')
			self.end_headers()
			self.wfile.write('{"i":"' + i + '","time":"' + str(time()) + '"}')
			Printer().main(a, b, i)
		except KeyError:
			self.send_response(412)
			self.send_header('Content-type','plain/text')
			self.end_headers()

def main():
	try:
		server = HTTPServer(('', 80), MyHandler)
		print 'Server - Start '
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()

