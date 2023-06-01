import string
import base64
import secrets
import hashlib
import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import serialization


class PwdLocker:
	def __init__(self):
		self.key = ""
		self.pfile = ""
		self.kfile = ""
		self.decData = b''
		self.data = b''
		self.FileNotFoundError = None
		self.ValueError = None 
		self.Empty = None

	def pad(self, s):
		block_size = algorithms.AES.block_size // 8
		padder = padding.PKCS7(block_size * 8).padder()
		padded_data = padder.update(s) + padder.finalize()
		return padded_data

	def unpad(self, s):
		unpad = padding.PKCS7(algorithms.AES.block_size).unpadder()
		unpadded_data = unpad.update(s) + unpad.finalize()
		return unpadded_data

	def encrypt_aes_256(self, key, plain_text):
		salt = os.urandom(16)
		kdf = Scrypt(
			salt=salt,
			length=32,
			n=2**14,
			r=8,
			p=1,
			backend=default_backend()
		)
		key = kdf.derive(key)

		iv = os.urandom(algorithms.AES.block_size // 8)
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
		encryptor = cipher.encryptor()

		padded_text = self.pad(plain_text)
		cipher_text = encryptor.update(padded_text) + encryptor.finalize()

		return {
			'cipher_text': base64.b64encode(cipher_text).decode(),
			'salt': base64.b64encode(salt).decode(),
			'iv': base64.b64encode(iv).decode()
		}

	def decrypt_aes_256(self, key, enc_dict):
		enc_dict = json.loads(enc_dict.decode())
		salt = base64.b64decode(enc_dict['salt'])
		iv = base64.b64decode(enc_dict['iv'])
		cipher_text = base64.b64decode(enc_dict['cipher_text'])

		kdf = Scrypt(
			salt=salt,
			length=32,
			n=2**14,
			r=8,
			p=1,
			backend=default_backend()
		)
		key = kdf.derive(key)

		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
		decryptor = cipher.decryptor()

		decrypted_text = decryptor.update(cipher_text) + decryptor.finalize()
		unpadded_text = self.unpad(decrypted_text)

		return unpadded_text

	def show(self):
		try:
			data_list= []
			self.Empty = False
			for line in (self.decData.decode()).splitlines():
				self.page, self.user, self.pwd = line.split(";")
				data_list.append((self.page ,self.user, self.pwd))			
			return data_list
		except AttributeError:
			self.Empty = True

	def create_key(self, path):
		self.key = base64.urlsafe_b64encode(secrets.token_bytes(32))
		with open(path, "wb") as f:
			f.write(self.key)

	def load_key(self, path):
		try:
			with open(path, "rb") as f:
				self.key = f.read()
			self.FileNotFoundError = False
		except FileNotFoundError:
			self.FileNotFoundError = True

	def generate_password_file(self, path):
		with open(path, "wb") as f:
			pass

	def load_password_file(self, path):
		self.pfile = path
		try:
			with open(self.pfile, "rb") as f:
				self.data = f.read()
				self.FileNotFoundError = False
		except FileNotFoundError:
			self.FileNotFoundError = True
		if len(self.data) > 0:
			self.decData = self.decrypt_aes_256(self.key, self.data)

	def add_password(self, site, user, password):
		self.load_password_file(self.pfile)
		bite_data = f"{site};{user};{password}\n".encode()
		
		try:
			self.decData += bite_data
		except AttributeError:
			self.decData = b''
			self.decData += bite_data


	def save(self, key, decoded_data):
		try:
			self.ValueError = False
			encData = self.encrypt_aes_256(key, decoded_data)
			with open(self.pfile, "wb") as f:
				f.write(json.dumps(encData).encode())
		except ValueError:
			self.ValueError = True

	def generate_password(self, length, special, digits, uppercase):
		# Generate a password with given length
		special = "!#$%&'()*+, -./:;<=>?@[]^_`{|}~"
		if special and digits and uppercase:
			chars = string.ascii_letters + string.digits + special
		elif not special and digits and uppercase:
			chars = string.ascii_letters + string.digits
		elif special and not digits and uppercase:
			chars = string.ascii_letters + special
		elif special and digits and not uppercase:
			chars = string.ascii_lowercase + special
		elif not special and not digits and uppercase:
			chars = string.ascii_letters
		elif special and not digits and not uppercase:
			chars = string.ascii_lowercase + special
		elif not special and digits and not uppercase:
			chars = string.ascii_lowercase + string.digits
		elif not special and not digits and not uppercase:
			chars = string.ascii_lowercase
		gen_pwd = "".join(secrets.choice(chars) for i in range(length))
		return gen_pwd