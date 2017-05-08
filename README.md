# PortalMeHpc_CreateKeys

Basic python script to create SSH keys. Supports RSA and DSA.
Requires pycrypto
```
usage: create_keys.py [-h] [-p [PUBLIC]] [-P [PRIVATE]] [-f [FROM_ARGS]] [-v]
                      [-k [KEY_TYPE]]

Creates a RSA key pair

optional arguments:
  -h, --help            show this help message and exit
  -p [PUBLIC], --public [PUBLIC]
                        public key location. Give full path + filename
  -P [PRIVATE], --private [PRIVATE]
                        private key location. Give full path + filename
  -f [FROM_ARGS], --from_args [FROM_ARGS]
                        Appends to the from pattern list on the ssh public key
  -v, --verbose         increase output verbosity
  -k [KEY_TYPE], --KEY_TYPE [KEY_TYPE]
                        Key Encryption Type. rsa or dsa

As an alternative to the commandline, params can be placed in a file, one per
line, and specified on the commandline like 'create_keys.py @params.conf'.
```
