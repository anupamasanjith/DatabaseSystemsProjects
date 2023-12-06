import base64
import json
import psycopg as pg
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Customer:
    HOST = '35.226.106.60'
    CT = """
         CREATE TABLE IF NOT EXISTS customer(
         id int NOT NULL,
         ccinfo text,
         PRIMARY KEY(id)
        ) 
    """

    INS = "INSERT INTO customer VALUES(%s,%s)"
    SEL = "SELECT ccinfo FROM customer WHERE id = %s"
    DEL = "DELETE FROM customer WHERE id = %s"

    def __init__(self):
        # Establish a connection to the PostgreSQL database
        self.cursor = None
        with open('../pgpass.txt', 'r') as f:
            self.conn = pg.connect(
                host=Customer.HOST,
                user='asanj2',
                dbname='asanj',
                password=f.readline().strip())

    def create_table(self):
        # Create the customer table if it does not exist
        self.conn.execute(Customer.CT)
        self.conn.commit()

    def insert(self, cid: int, first: str, last: str, ccnum: str, ccexp: str, cvv: str):
        # Construct a JSON object with credit card information
        ccjson = {
            'name': first + ' ' + last,
            'ccnum': ccnum,
            'exp': ccexp,
            'cvv': cvv

        }
        ccbytes = json.dumps(ccjson).encode()
        # Read the encryption key and IV from external files
        with open('../key.txt','r') as f:
            key = f.readline().strip()
        with open('../iv.txt','r') as f:
            iv = f.readline().strip()

        key = bytes.fromhex(key)
        iv = bytes.fromhex(iv)

        # Encrypt the credit card information using AES
        aesCipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        aesEncryptor = aesCipher.encryptor()
        ciphertext = aesEncryptor.update(ccbytes) + aesEncryptor.finalize()
        b64ct = base64.b64encode(ciphertext).decode()
        # Insert the encrypted credit card information into the database
        self.conn.execute(Customer.INS, (cid, b64ct))
        self.conn.commit()

    def lookup(self, cid: int) -> dict:
        # Retrieve the encrypted credit card information from the database
        result = self.conn.execute(Customer.SEL, (cid,)).fetchone()
        b64ct = result[0].encode()
        ciphertext = base64.b64decode(b64ct)
        # Read the decryption key and IV from external files
        with open('../key.txt','r') as f:
            key = f.readline().strip()
        with open('../iv.txt','r') as f:
            iv = f.readline().strip()
        key = bytes.fromhex(key)
        iv = bytes.fromhex(iv)

        # Decrypt the credit card information using AES
        aesCipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        aesDecryptor = aesCipher.decryptor()
        ccbytes = aesDecryptor.update(ciphertext) + aesDecryptor.finalize()
        ccjson = json.loads(ccbytes.decode())
        return ccjson

    def delete(self,cid: int) -> None:
        # Delete the customer record from the database
        self.conn.execute(Customer.DEL, (cid,))
        self.conn.commit()
