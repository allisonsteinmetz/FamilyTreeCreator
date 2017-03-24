from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

HOST_NAME = ""
PORT_NUMBER = 8000

class myHandler(BaseHTTPRequestHandler):

	# Handle GET request
	def do_GET(self):

		# Set the homepage
		if self.path == "/":
			self.path = "/login.html";

		# Set content-type of return
		if self.path.endswith(".html"):
			mimeType = "text/html"
		elif self.path.endswith(".jpg"):
			mimeType = "image/jpg"
		elif self.path.endswith(".gif"):
			mimeType = "image/gif"
		elif self.path.endswith(".txt"):
			mimeType = "text/plain"
		elif self.path.endswith(".json"):
			mimeType = "application/json"
		elif self.path.endswith(".js"):
			mimeType = "application/javascript"
		elif self.path.endswith(".css"):
			mimeType = "text/css"
		else:
			mimeType = "text/plain" # for unknown types

		try:
			# Open the requested file
			f = open(curdir + sep + self.path, 'rb')
			# The request is okay
			self.send_response(200);
			# Set header
			self.send_header('Content-type',mimeType)
			self.end_headers()
			# Send the request file
			self.wfile.write(f.read())
			# Close the request file
			f.close()
		except IOError:
			# Handle bad request
			self.send_error(404)

try:
	# Create a web server and define the handler to manage the
    # incoming request
	server = HTTPServer((HOST_NAME, PORT_NUMBER), myHandler)
	print("Start http server on port ", PORT_NUMBER)

	# Keep server running forever
	server.serve_forever()
except KeyboardInterrupt:
	# Use default ctr+c to close the server
    print ('^C received, shutting down the web server')
    server.socket.close()
