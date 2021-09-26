import socket, json, time

class Client():

	def __init__(self, client_file, sock=None):

		if sock == None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.s = sock

		client_info = self.setClientInfo(client_file)

		# Connect to the server 
		print("-connecting to ip: " + self.ip + ', socket: ' + str(self.port))
		print()
		self.s.connect((self.ip, self.port))

		# Register client to the server
		self.register()

		# Perform the client actions
		action_counter = 0
		if self.actions != None:
			for action in self.actions:
				#split the action and the amount
				tmp = action.split()
				action_type = tmp[0]
				action_amount = tmp[1]

				action_counter += 1
				print(str(action_counter) + ' ' + action_type)

				if action_type == 'INCREASE':
					print('increase')
					self.Increase(action_amount)

				elif action_type == 'DECREASE':
					print('decrease')
					self.Decrease(action_amount)

				else:
					raise NameError("action type does not exist: " + action_type)

		else:
			print("no action found")

		# disconnect the client from the server
		self.s.close()
		

	# Register the client to the server
	def register(self):
		message = 'register,' + self.id + ',' + self.password
		self.s.send(message.encode('utf-8'))

		answer = self.s.recv(1024).decode('utf-8')
		print(answer)
		

	# Increase the client counter
	def Increase(self, amount):
		self.delay(int(self.action_delay))
		message = 'INCREASE,' + self.id + ',' + amount
		self.s.send(message.encode('utf-8'))
		answer = self.s.recv(1024).decode('utf-8')
		print(answer)
		return 
		

	# decreases the client counter
	def Decrease(self, amount):
		self.delay(int(self.action_delay))
		message = 'DECREASE,' + self.id + ','  + amount 
		self.s.send(message.encode('utf-8'))
		answer = self.s.recv(1024).decode('utf-8')
		print(answer)
		return 


	# delay the messages
	def delay(self, amount):
		print("Delay: " + str(amount))
		time.sleep(amount)
		return


	# Extract the informations from the json file
	def setClientInfo(self, file):
		with open(file) as json_file:
			data = json.load(json_file)

			self.port = int(data['server']['port'])
			self.ip = data['server']['ip']

			self.id = data['id']
			self.password = data['password']
			
			self.action_delay = data['action']['delay']
			self.actions = data['action']['steps']
			

if __name__ == '__main__':
	file = "client1.json"
	client = Client(file)