import Crypto.Cipher.AES


class SecureProc:
    """Advanced Secure Cryptographic Processor™, prototype version.

    Contains:

    - unhackable write-only key storage
    - secure encryption circuitry (decryption available only in the enterprise
    """
    def __init__(self):
        self.key  = bytearray(16)
        self.data = bytearray(16)

    def write_byte(self, addr, data):
        if addr in range(0x00, 0x10):
            # Addresses 0x00-0x0f are the (write-only, unhackable) key.
            self.key[addr] = data
        elif addr in range(0x10, 0x20):
            # Addresses 0x10-0x1f are the data to encrypt.
            self.data[addr - 0x10] = data
            # Writing the final data byte triggers encryption.
            if addr == 0x1f:
                c = Crypto.Cipher.AES.new(bytes(self.key), Crypto.Cipher.AES.MODE_ECB)
                self.data[:] = c.encrypt(bytes(self.data))

    def read_byte(self, addr):
        if addr in range(0x10, 0x20):
            # Addresses 0x10-0x1f are the encrypted data.
            return self.data[addr - 0x10]
        # Unmapped address -- return default value.
        return 0xff
