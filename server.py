#  coding: utf-8 
import socketserver
import os
from pathlib import Path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Cenab Batu Bora
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


BASEURL = "http://127.0.0.1:8080"
class MyWebServer(socketserver.BaseRequestHandler):
    #https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        string_list = self.data.decode("utf-8").split(' ')     # Split request from spaces
        print(string_list)
        method = string_list[0]
        path = string_list[1]
        myfile = path.split('?')[0].lstrip('/') # After the "?" symbol not relevent here
        myfile = 'www/' + myfile
        print(myfile)
        if (myfile[0:6] == "www/.."):
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
            final_response = header.encode('utf-8')
            final_response += response
            self.request.sendall(final_response)
        elif method != "GET":
            header = 'HTTP/1.1 405 Method Not Allowed\n\n'
            response = '<html><body><center><h3>Error 405: Method Not Allowed</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
            final_response = header.encode('utf-8')
            final_response += response
            self.request.sendall(final_response)
        elif os.path.exists(myfile) == False:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
            final_response = header.encode('utf-8')
            final_response += response
            self.request.sendall(final_response)
        elif os.path.isdir(myfile):
            if myfile[-1] != "/":
                myfile = myfile + "/"
                http_get_minimum = "HTTP/1.1 301 Moved Permanently\n\n Retry-After: 0\n\nLocation: "+BASEURL+myfile+"\n\n"
                self.request.send(http_get_minimum.encode('utf-8'))
                m = self.request.recv(4096)
                print(m)
            header = 'HTTP/1.1 200 OK' + '\r\nContent-Type: text/html\r\n\r\n'
            response = '<html><body><center><h3>Error 200: File found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
            final_response = header.encode('utf-8')
            final_response += response
            self.request.sendall(final_response)
        elif os.path.isfile(myfile):
            print("is png here?")
            try:
                #file = open(myfile,'rb') # open file , r => read , b => byte format
                file_path = Path(myfile)
                print(file_path)
                header = 'HTTP/1.1 200 OK\n'

                if(myfile.endswith(".png")):
                    mimetype = 'png'
                elif(myfile.endswith(".css")):
                    mimetype = 'css'
                else:
                    mimetype = 'html'
                
                print(mimetype)

                response = 'HTTP/1.1 ' + "200 OK" + '\r\nContent-Type: text/'
                if mimetype == 'png':
                    self.request.sendall(bytearray(response + mimetype + '\r\n\r\n' + file_path.read_bytes() + '\r\n', 'utf-8'))
                    print(bytearray(response + mimetype + '\r\n\r\n' + file_path.read_bytes() + '\r\n', 'utf-8').decode())
                else:
                    self.request.sendall(bytearray(response + mimetype + '\r\n\r\n' + file_path.read_text() + '\r\n', 'utf-8')) 
                    print(bytearray(response + mimetype + '\r\n\r\n' + file_path.read_text() + '\r\n', 'utf-8').decode())
    
            except Exception as e:
                header = 'HTTP/1.1 404 Not Found\n\n'
                response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
                final_response = header.encode('utf-8')
                final_response += response
                self.request.sendall(final_response)
        

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
