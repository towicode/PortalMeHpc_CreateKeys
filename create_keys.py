#!/usr/bin/env python
#

import sys, argparse, logging
from os import chmod
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
import os



def main(args, loglevel, use_dsa):
  """ Handles the actual generation of the key pair

  uses pycrypto to generate the key """

  # Set up logging levels to seperate debug and info messages.
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  
  logging.debug("Creating Key pair at " + str(args.public) + " " + str(args.private))
  

  # DSA support
  if use_dsa:
    # This line uses subprocess to do three things
    # 1. Generate the DSA key
    # 2. Rename the public key to whatever the user provides
    # 3. Adds the from prepend
    if args.from_args is not "":
      os.system("ssh-keygen -t dsa -N '' -f " + args.private+ " && mv " + args.private + ".pub " + args.public + " && " + "sed -i.old '1s;^;from=\""+args.from_args+"\" ;' "+args.public)
    else:
      os.system("ssh-keygen -t dsa -N '' -f " + args.private+ " && mv " + args.private + ".pub " + args.public)

    return -1
  
  # Generate an RSA Key
  key = RSA.generate(2048)

  # Open the private key file and write the key export
  with open(args.private, 'w') as content_file:
    chmod(args.private, 0600)
    content_file.write(key.exportKey('PEM'))
  logging.debug("Created Private Key")

  # Create a public key
  pubkey = key.publickey()
  # Open the public key file and write the key export based on openssh
  # additionally append any info to the 'from' column
  with open(args.public, 'w') as content_file:
    if args.from_args is not "":
      content_file.write("from=")
      content_file.write('"'+ args.from_args+'" ')
    content_file.write(pubkey.exportKey('OpenSSH'))
  logging.debug("Created public Key")
  logging.info("Success!")
 


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description = "Creates a RSA key pair",
    epilog = " As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
    fromfile_prefix_chars = '@' )
  parser.add_argument(
                      "-p",
                      "--public",
                      help="public key location. Give full path + filename",
                      nargs="?",
                      default="/tmp/public.key",
                      type=str)

  parser.add_argument(
                      "-P",
                      "--private",
                      help="private key location. Give full path + filename",
                      nargs="?",
                      default="/tmp/private.key",
                      type=str)

  parser.add_argument(
                      "-f",
                      "--from_args",
                      help="Appends to the from pattern list on the ssh public key",
                      nargs="?",
                      default="",
                      type=str)

  parser.add_argument(
                      "-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")

  parser.add_argument(
                      "-k",
                      "--KEY_TYPE",
                      help="Key Encryption Type. rsa or dsa",
                      nargs="?",
                      default="",
                      type=str)

  args = parser.parse_args()
  
  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO
  
  use_dsa = False
  if (args.KEY_TYPE.lower() == "dsa"):
    use_dsa = True

  main(args,loglevel,use_dsa)

