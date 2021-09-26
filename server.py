import socket, json
from threading import Thread

class Server():
	def __init__(self, port):

		self.registered = {} # list of registered client
		self.counters = {}

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind(('127.0.0.1', port))
		self.s.listen(1)
		self.port = port

		self.run()
		

	def run(self):
		print('waiting for incoming')
		# client_socket, adress = self.s.accept() 
		while True:
			(conn, (ip, port)) = self.s.accept()
			Thread(target = self.handle_incoming, args=(conn, ip, port)).start()

	def handle_incoming(self, conn, ip, port):
		while True:
			# data = client_socket.recv(1024).decode('utf-8').split(',')
			data = conn.recv(1024).decode('utf-8').split(',')

			if not data:
				return

			elif data[0] == 'register':
				print('start register process')

				if data[0] in self.registered: # Check if the id already exist in the dictionnary 
					response = "ERROR: id already exist, please choose another id"
					print("send answer to client")
					conn.send(response.encode('utf-8'))

				else: # Create the new client and set his counter to 0
					self.registered[data[1]] = data[2]
					self.counters[data[1]] = 0

					# Send confirmation message to client
					response = 'registration completed'
					print("registration done")
					conn.send(response.encode('utf-8'))

			elif data[0] == 'INCREASE':
				print('increase')

				self.counters[data[1]] = self.counters[data[1]] + int(data[2])
				response = "counter increased by: " + data[2]
				conn.send(response.encode('utf-8'))

			elif data[0] == 'DECREASE':
				print('decrease')

				self.counters[data[1]] = self.counters[data[1]] - int(data[2])
				response = "counter decreased by: " + data[2]
				conn.send(response.encode('utf-8'))


if __name__ == '__main__':
	server = Server(10050)