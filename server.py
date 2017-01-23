#  coding: utf-8 
import SocketServer, os, mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Modifications Copyright 2017 Kalvin Eng
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip("\r\n")
        command = self.data.split() # [method, request-uri, resource, ...]
        
        if command:
            if command[0] != "GET":
	            # send 405 error, method is not allowed
	            # note: methods are case-sensitive
	            self.request.sendall("HTTP/1.1 405 Method Not Allowed\r\n")
            else:
	            # must be a GET request
	            PATH_PREFIX = "www"
	            path = os.path.join(os.getcwd(), PATH_PREFIX + command[1])
	            
	            if os.path.exists(path):
	                # note: 302 redirects not implemented
	                if os.path.isdir(path):
	                    path += "index.html"
	                    
	                if os.path.isfile(path):
	                    f = open(path)
	                    file_contents = f.read()
	                    f.close()
	                    
	                    filetype = mimetypes.guess_type(path)[0]
	                    
	                    if filetype is not None:
	                        content_type = "Content-type:" + filetype + ";\r\n" + "\r\n" # extra \r\n to signify end of header
	                        self.request.sendall("HTTP/1.1 200 OK\r\n" + content_type + file_contents)
	                    else:
	                        # filetype cannot be identified
	                        self.request.sendall("HTTP/1.1 404 Not Found\r\n")
	            else:
	                # send 404 error, not found
	                self.request.sendall("HTTP/1.1 404 Not Found\r\n")
	    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
