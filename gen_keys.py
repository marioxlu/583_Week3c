from web3 import Web3
import eth_account
import os

def get_keys(challenge,keyId = 0, filename = "eth_mnemonic.txt"):
    """
    Generate a stable private key
    challenge - byte string
    keyId (integer) - which key to use
    filename - filename to read and store mnemonics

    Each mnemonic is stored on a separate line
    If fewer than (keyId+1) mnemonics have been generated, generate a new one and return that
    """

    w3 = Web3()
    
    # Ensure mnemonic file exists
    if not os.path.exists(filename):
        open(filename, 'w').close()

    # Read or generate private key
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    if keyId < len(lines):
        # Load existing private key
        private_key = lines[keyId].strip()
    else:
        # Generate a new private key and store it
        new_account = eth_account.Account.create()
        private_key = new_account.privateKey.hex()
        with open(filename, 'a') as file:
            file.write(f"{private_key}\n")

    # Create an account from the private key
    acct = eth_account.Account.from_key(private_key)
    eth_addr = acct.address

    msg = eth_account.messages.encode_defunct(challenge)
    sig = acct.sign_message(msg)

	#YOUR CODE HERE

    assert eth_account.Account.recover_message(msg,signature=sig.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return sig, acct #acct contains the private key
    return sig.signature.hex(), eth_addr

if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= get_keys(challenge=challenge,keyId=i)
        print( addr )
