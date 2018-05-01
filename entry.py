#!/usr/bin/env python
from livereload import Server
server = Server()
server.watch('docs/*')
server.serve(port=8080, root='./docs')
