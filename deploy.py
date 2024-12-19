from vyper import compile_code
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()
RPC_URL = os.getenv('RPC_URL')
MY_ADDRESS= os.getenv('MY_ADDRESS')
PRIVATE_KEY= os.getenv('PRIVATE_KEY')

#MY_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
PRICE_FEED_ADDRESS = "0x694AA1769357215DE4FAC081bf1f309aDC325306"
#PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

def main():
    print("hello world!")
    with open("fav.vy", "r") as f:
        fav_code = f.read() 
        com_details = compile_code(fav_code, output_formats=["bytecode", "abi"])

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    fv_contract= w3.eth.contract(bytecode=com_details["bytecode"], abi=com_details["abi"])

    nonce = w3.eth.get_transaction_count(MY_ADDRESS)
    transaction = fv_contract.constructor(PRICE_FEED_ADDRESS).build_transaction(
       { 
           "nonce": nonce,
           "from": MY_ADDRESS,
           "gasPrice": w3.eth.gas_price
       }
    )
    signed_transcation = w3.eth.account.sign_transaction(transaction, private_key= PRIVATE_KEY)
    print(signed_transcation)

    tx_hash= w3.eth.send_raw_transaction(signed_transcation.raw_transaction)
    print(f"My TX hash is {tx_hash}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contract Deployed at {tx_receipt.contractAddress}")


if __name__ == "__main__":
    main()