from socket import *
import socket
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(32)
			if data:
				# Ubah data menjadi string
				data = data.decode('utf-8')
				# Periksa apakah data memenuhi ketentuan
				if data.startswith('TIME') and data.endswith('\r\n'):
					current_time = time.strftime('%H:%M:%S', time.localtime())
					response = f"JAM {current_time}\r\n"

					# Kirim respon ke client
					self.connection.sendall(response.encode('utf-8'))
				else:
					# Kirim pesan error jika data tidak sesuai format
					error_message = "ERROR: Invalid request format\r\n"
					self.connection.sendall(error_message.encode('utf-8'))
			else:
				break
		self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0', 45000)) # Mengubah port menjadi 45000
		self.my_socket.listen(1)
		logging.warning(f"waiting for connection on port 45000") # Menunggu koneksi.
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()

