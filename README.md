# PortalMeHpc_CreateKeys

Basic python script to create SSH keys. Supports RSA and DSA.
Requires pycrypto
```
usage: create_keys.py [-h] [-p [PUBLIC]] [-P [PRIVATE]] [-f [FROM_ARGS]] [-v]
                      [-k [KEY_TYPE]] [-K] [-u [USER]] [-H [HOSTNAME]]
                      [-X [PASSWORD]] [-t [TFA_KEY]]

Creates a RSA key pair

optional arguments:
  -h, --help            show this help message and exit
  -p [PUBLIC], --public [PUBLIC]
                        public key output location. Give full path + filename
  -P [PRIVATE], --private [PRIVATE]
                        private key output location. Give full path + filename
  -f [FROM_ARGS], --from_args [FROM_ARGS]
                        Appends to the from pattern list on the ssh public key
  -v, --verbose         increase output verbosity
  -k [KEY_TYPE], --KEY_TYPE [KEY_TYPE]
                        Key Encryption Type. rsa or dsa
  -K, --uploadkey       Attempts to automatically upload the public key
  -u [USER], --user [USER]
                        Username for your HPC. (only used for uploading key)'
  -H [HOSTNAME], --hostname [HOSTNAME]
                        Host for your HPC. (only used for uploading key)
                        'user@host...'
  -X [PASSWORD], --password [PASSWORD]
                        Password for HPC account (only used for uploading
                        key)'
  -t [TFA_KEY], --tfa_key [TFA_KEY]
                        Two Factor Key (can only be used once) for HPC account
                        (only used for uploading key)'

As an alternative to the commandline, params can be placed in a file, one per
line, and specified on the commandline like 'create_keys.py @params.conf'.
```
