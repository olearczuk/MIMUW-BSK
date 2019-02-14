from pwn import *
import Crypto.Cipher.AES

conn = remote('localhost', 31337);
ciphers = []


def get_data():
	result = ''
	for i in range(0x10, 0x20):
		conn.sendline('r ' + hex(i))
		result += conn.recvline().decode().strip()

	return result


def send_w_message(index, val):
	conn.sendline('w {0} {1}'.format(hex(index), val).encode())


def set_data_for_0():
	for i in range(0x00, 0x10):
		send_w_message(i + 0x10, 0)

conn.sendline('easy')

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

ciphertext = get_data()

key = ''
for key_index in range(0x00, 0x10):
	for val in range(0x00, 0x100):
		send_w_message(key_index, hex(val));
		set_data_for_0();
		data = get_data()
		if data == ciphertext:
			print('found keys byte number {0}, value {1}'.format(key_index, hex(val)[2:] if len(hex(val)) == 4 else '0' + hex(val)[2:]))
			key += hex(val)[2:] if len(hex(val)) == 4 else '0' + hex(val)[2:]
			break

key_byte = bytearray(16);
for i in range(16):
	key_byte[i] = int(key[2 * i: 2 * i + 2], 16)


c = Crypto.Cipher.AES.new(bytes(key_byte), Crypto.Cipher.AES.MODE_ECB)

result = ''

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

print(result[:58])

conn.close()
