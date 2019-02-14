from pwn import *
import Crypto.Cipher.AES

conn = remote('localhost', 31337);
response = 'a'
ciphers = []

def get_data():
	result = ''
	for i in range(0x10, 0x20):
		conn.sendline('r ' + hex(i))
		result += conn.recvline().decode().strip()

	return result


def send_w_message(index):
	conn.sendline(f'w {hex(index)} 0'.encode())


def set_data_for_0():
	for i in range(0x00, 0x10):
		send_w_message(i + 0x10)

conn.sendline('hard')

while True:
	response = conn.recvline().decode()
	if response == 'Send "r <addr>" to read a byte from the secure processor.\n':
		break
	if response[:13] == 'The encrypted':
		response = response[22:-2]
		i = 0
		while i < len(response):
			ciphers.append(response[i:i + 32])
			i += 32

set_data_for_0()

# Zbieranie bazy wyników dla odpowiednich kluczy
ciphertexts = [get_data()]

for i in range(15):
	send_w_message(0x0f - i)
	set_data_for_0()
	ciphertext = get_data()
	ciphertexts.append(ciphertext)

ciphertexts = ciphertexts[::-1]

key_bytes = bytearray(16)
enc_bytes = bytearray(16)

# Znajdowanie kolejnych bajtóœ klucza
for i in range(16):
	for val in range(256):
		key_bytes[i] = val
		c = Crypto.Cipher.AES.new(bytes(key_bytes), Crypto.Cipher.AES.MODE_ECB)
		encrypted = c.encrypt(bytes(enc_bytes))
		result = ''
		
		for j in range(16):
			char = hex(encrypted[j])[2:]
			result += char if len(char) == 2 else '0' + char
		if result == ciphertexts[i]:
			break

c = Crypto.Cipher.AES.new(bytes(key_bytes), Crypto.Cipher.AES.MODE_ECB)
result = ''

# Odszyfrowywanie
for i in range(len(ciphers) - 1):
	cipher0 = ciphers[i]
	cipher1 = ciphers[i + 1]

	byte_cipher0 = bytearray(16)
	byte_cipher1 = bytearray(16)

	for i in range(16):
		byte_cipher0[i] = int(cipher0[2 * i: 2 * i + 2], 16)
		byte_cipher1[i] = int(cipher1[2 * i: 2 * i + 2], 16)
	
	decrypted = c.decrypt(bytes(byte_cipher1))

	for i in range(16):
		result += chr(decrypted[i] ^ byte_cipher0[i])

print(result[:52])

conn.close()
