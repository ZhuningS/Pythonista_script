#! python2
'''FTP server for Pythonista (iOS)

You can use this to exchange files with a Mac/PC or a file management app on the same device (e.g. Transmit).

If you use a Mac, you can connect from the Finder, using the "Go -> Connect to Server..." menu item.
'''

import os
from socket import gethostname

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading

def main():
	authorizer = DummyAuthorizer()
	authorizer.add_anonymous(os.path.expanduser('~/Documents'), perm='elradfmwM')
	handler = FTPHandler
	handler.authorizer = authorizer
	server = FTPServer(('0.0.0.0', 21), handler)
	t = threading.Thread(target=server.serve_forever)
	t.start()
	try:
		while True: pass
	except KeyboardInterrupt:
		server.close_all()
		print('Server stopped')

if __name__ == '__main__':
	main()

