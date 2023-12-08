from http.server import SimpleHTTPRequestHandler, HTTPServer



def run_webserver(directory):
	hostName = 'localhost'
	serverPort = 8080
	webServer = HTTPServer((hostName, serverPort), 
		SimpleHTTPRequestHandler)

	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print('server stopped')

