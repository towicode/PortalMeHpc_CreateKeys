#!/usr/bin/env python
#

import sys
import argparse
import logging
from os import chmod
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
import os
import pexpect
import time


def login_uofa(args, mem_file):
    """ logins into the uofa hpc and adds the key given to the authorized keys.

    Expects all arguments to be valid"""

    child = pexpect.spawn("ssh " + str(args.user) +
                          "@" + str(args.hostname) + "")
    
    index = child.expect(['Are you sure you want to continue connecting*', pexpect.EOF, pexpect.TIMEOUT], timeout=2)
    if index == 0: 
        child.sendline("yes")  

    index = child.expect(['~]\$', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
    if index != 0:
                
        child.expect("Password*")
        child.sendline(args.password)
        child.expect("Enter a passcode*")
        child.sendline(args.tfa_key)
        child.expect("~]\$")
        time.sleep(3)

    logging.debug("hopefully we are inside the HPC")
    child.sendline('echo "' + mem_file +
                   '" | cat >> ~/.ssh/authorized_keys')
    time.sleep(1)
    child.expect("~]\$")
    logging.debug(child.before)

    child.sendline("touch .portalme")
    time.sleep(1)
    child.expect("~]\$")
    logging.debug(child.before)

    child.sendline("ls -lah")
    child.expect("~]\$")
    logging.debug(child.before)

    # logging.debug(child.after)
    logging.info("Created file!")
    #logging.debug(str(child))

    # gargs = args.commands.split("..")

    # #   Allow multiple commands
    # for garg in gargs:
    #     #   expect and sendlines are seperated by a '-'
    #     commands = garg.split("-")
    #     #   if the user gave a bad input die gracefully
    #     if len(commands) is not 2:
    #         printf("Bad command in commands")
    #         return -1

    #     expecting = commands[0]
    #     sendline = commands[1]
    #     logging.debug("Expecting '" + expecting +
    #                   "' and Sending '" + sendline)

    #     child.expect(expecting)
    #     child.sendline(sendline)
    #     print child.before

    # if not args.skipappend:
    #     logging.debug("hopefully we are inside the HPC")
    #     child.sendline('echo "' + mem_file +
    #                     '" | cat >> ~/.ssh/authorized_keys')
    #     child.sendline('ls')


def main(args, loglevel, use_dsa):
    """ Handles the actual generation of the key pair

    uses pycrypto to generate the key """

    # Set up logging levels to seperate debug and info messages.
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    logging.debug("Creating Key pair at " +
                  str(args.public) + " " + str(args.private))

    # DSA support
    if use_dsa:
        # This line uses subprocess to do three things
        # 1. Generate the DSA key
        # 2. Rename the public key to whatever the user provides
        # 3. Adds the from prepend
        if args.from_args is not "":
            os.system("ssh-keygen -t dsa -N '' -f " + args.private + " && mv " + args.private + ".pub " +
                      args.public + " && " + "sed -i.old '1s;^;from=\"" + args.from_args + "\" ;' " + args.public)
        else:
            os.system("ssh-keygen -t dsa -N '' -f " + args.private +
                      " && mv " + args.private + ".pub " + args.public)

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
    mem_file = ""
    with open(args.public, 'w') as content_file:
        if args.from_args is not "":
            content_file.write("from=")
            mem_file += "from="
            content_file.write('"' + args.from_args + '" ')
            mem_file += '\\"' + args.from_args + '\\" '
        export = pubkey.exportKey('OpenSSH')
        content_file.write(export)
        mem_file += export
    logging.debug("Created public Key")
    logging.info("Success!")

    logging.debug("Our public key out is:")
    logging.debug(mem_file)

    if (args.uploadkey):
        logging.info("Attempting to copy public key to host.")

        if not args.user:
            logging.error("user not provided")
            return -1
        if not args.hostname:
            logging.error("host not provided")
            return -1
        if not args.password:
            logging.error("password not provided")
            return -1

        if not args.tfa_key:
            logging.error("tfa key not provided")
            return -1

        login_uofa(args, mem_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates a RSA key pair",
        epilog=" As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-p",
        "--public",
        help="public key output location. Give full path + filename",
        nargs="?",
        default="/tmp/public.key",
        type=str)

    parser.add_argument(
        "-P",
        "--private",
        help="private key output location. Give full path + filename",
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

    parser.add_argument(
        "-K",
        "--uploadkey",
        help="Attempts to automatically upload the public key",
        action="store_true")

    parser.add_argument(
        "-u",
        "--user",
        help="Username for your HPC. (only used for uploading key)'",
        nargs="?",
        required=False,
        type=str)

    parser.add_argument(
        "-H",
        "--hostname",
        help="Host for your HPC. (only used for uploading key) 'user@host...'",
        nargs="?",
        default="hpc.arizona.edu",
        type=str)

    parser.add_argument(
        "-X",
        "--password",
        help="Password for HPC account (only used for uploading key)'",
        nargs="?",
        required=False,
        type=str)

    parser.add_argument(
        "-t",
        "--tfa_key",
        help="Two Factor Key (can only be used once) for HPC account (only used for uploading key)'",
        nargs="?",
        required=False,
        type=str)

    # parser.add_argument(
    #     "-Z",
    #     "--skipappend",
    #     help="Only use this argument if you are appending the key yourself in the commands argument.",
    #     action="store_true")

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    if (args.from_args is not None and args.from_args is not ""):
        args.from_args = args.from_args.replace("-", "/")
        args.from_args = args.from_args.replace("..", ",")

    use_dsa = False
    if (args.KEY_TYPE.lower() == "dsa"):
        use_dsa = True

    main(args, loglevel, use_dsa)
