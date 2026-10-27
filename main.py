# main.py
from core.pseudocode import process_block, daily_work_recalculation
from models.wallet import Wallet

def main():
    print("Crowd-Cloud System starting...")
    network_wallets = []
    wallet = Wallet("root_master")
    daily_work_recalculation(wallet, {"all_wallets": network_wallets})
    block = {"transactions": [], "header": ""}
    hash = process_block(block)
    print(f"Block mined: {hash}")

if __name__ == "__main__":
    main()
