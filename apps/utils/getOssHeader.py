import hmac
import hashlib
import time

secret_key='f9OPJ1ZsyrV6YmneGfw3xc5Wvtc8SYQ4'
key_time=int(time.time())

sha1 = hashlib.sha1()
sha1_http_string = sha1.update('ExampleHttpString'.encode('utf-8')).hexdigest()

sign_key = hmac.new(secret_key.encode('utf-8'), key_time.encode('utf-8'), hashlib.sha1).hexdigest()

print(sign_key)