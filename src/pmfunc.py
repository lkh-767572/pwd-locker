import random
import string
import base64
from cryptography.fernet import Fernet

class PwdLocker:
	def __init__(self):
		self.key = ""
		self.pfile = ""
		self.kfile = ""
		self.decDa = b''
		self.data = b''
		self.FNF = None
		self.EMT = None

	def encrypt(self):
		f = Fernet(self.key)
		self.data = f.encrypt(self.decDa)

	def decrypt(self):
		f = Fernet(self.key)
		self.decDa = f.decrypt(self.data)

	def show(self):
		try:
			self.EMT = False
			for line in (self.decDa.decode()).splitlines():
				self.page, self.user, self.pwd = line.split(";")
			data_list= []
			data_list.append((self.page ,self.user, self.pwd))
			return data_list
		except AttributeError:
			self.EMT = True

	def create_key(self, path):
		self.key = base64.b64encode((''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))).encode('ascii'))
		with open(path, "wb") as f:
			f.write(self.key)

	def load_key(self, path):
		try:
			with open(path, "rb") as f:
				self.key = f.read()
			self.FNF = False
		except FileNotFoundError:
			self.FNF = True

	def generate_password_file(self, path):
		with open(path, "wb") as f:
			pass

	def load_password_file(self, path):
		self.pfile = path
		try:
			with open(self.pfile, "rb") as f:
				self.data = f.read()
				self.FNF = False
		except FileNotFoundError:
			self.FNF = True
		if len(self.data) > 0:
			self.decrypt()

	def add_password(self, page, user, password):
		self.decDa += (f"{page};{user};{password}\n").encode()

	def save(self):
		try:
			self.encrypt()
			with open(self.pfile, "wb") as f:
				f.write(self.data)
		except ValueError:
			pass # !! TODO: CHANGE NO DATA ADDED OR LOADED

	def generate_password(self, lenght):
		#generate a password with given lenght
		chars = string.ascii_letters + string.digits + "!#$%&'()*+, -./:;<=>?@[]^_`{|}~"
		gen_pwd = "".join(random.choice(chars) for i in range(lenght))
		print(f"Your generated password is: {gen_pwd}")