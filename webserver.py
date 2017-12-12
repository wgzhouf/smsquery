#!/bin/python3
# coding=utf-8

import os
from http.server import HTTPServer, CGIHTTPRequestHandler



def getserver(name='', port=80):
    webdir = os.path.join('.', 'webroot')
    print("webdir: \"%\", port: %s", (webdir, port))
    os.chdir(webdir)
    serveraddr = (name, port)
    CGIHTTPRequestHandler.cgi_directories = ['/bin']
    serverobj = HTTPServer(serveraddr, CGIHTTPRequestHandler)
    return serverobj


if __name__ == '__main__':
    server1 = getserver("", 8089)
    server1.serve_forever()
