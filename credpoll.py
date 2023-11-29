import argparse
import os
import sys
from datetime import datetime
from util import get_cred_files, get_hashes

__version__ = "0.1"


def list_accounts(logs_dir: str) -> list:
    hashes = get_hashes(get_cred_files(logs_dir))
    # Generate list of accounts from hash files
    new_accounts = []
    for hash in hashes:
        identity = f"{hash.split(':')[2]}\\{hash.split(':')[0]}"
        if (identity.lower() not in map(str.lower, new_accounts) and
                identity.lower() not in map(str.lower, CACHE)):
            new_accounts.append(identity)

    return new_accounts


def extract_creds(logs_dir: str) -> str:
    accounts = list_accounts(logs_dir)
    print()
    option_idx = 0
    for account in accounts:
        option_idx += 1
        print(f'{option_idx}) {account}')
    print()
    try:
        extract_account = int(input("[!] Pick an account to extract credentials for: "))
    except ValueError:
        sys.exit("[-] Invalid choice!")

    if (extract_account-1) not in range(0, len(accounts)):
        print('[-] Invalid choice!')
        sys.exit(1)
    else:
        extract_account = accounts[extract_account-1]

    hashes = get_hashes(get_cred_files(logs_dir))
    for hash in hashes:
        if (hash.split(":")[0] == extract_account.split("\\")[1] and
                hash.split(":")[2] == extract_account.split("\\")[0]):
            return hash

    return "ERROR: Hash not found"


def generate_hashlist(logs_dir: str):
    hashes = get_hashes(get_cred_files(logs_dir))
    hashlist = []
    for hash in hashes:
        identity = f"{hash.split(':')[2]}\\{hash.split(':')[0]}"
        if (identity.lower() not in map(str.lower, CACHE)
                and identity.lower() not in map(str.lower, hashlist)):
            hashlist.append(hash)
            CACHE.append(identity)

    return hashlist


def check_and_load_cache():
    if os.path.exists(CACHE_FILE):
        print("[+] Found existing cache, loading...")
        with open(CACHE_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        return []


def save_cache():
    if not os.path.exists(CACHE_FILE):
        print("[-] No previous cache found, creating...")
    with open(CACHE_FILE, 'w+') as file:
        file.write("\n".join(map(str, CACHE)))


def reset_cache():
    if os.path.exists(CACHE_FILE):
        print("[+] Found existing cache, deleting...")
        os.remove(CACHE_FILE)
    else:
        print("[-] No previous cache found, aborting...")


def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(
        description="Credential Polling for Responder",
    )
    parser.add_argument('--responder-logs-dir',
                        type=str,
                        default="/usr/share/responder/logs",
                        help="Responder logs directory to poll")
    parser.add_argument('action',
                        choices=['list', 'extract', 'hashlist', 'reset'],
                        help='action to perform')

    args = parser.parse_args()
    
    global CACHE
    CACHE = check_and_load_cache()
    
    # Process directory and get absolute path
    if os.path.isabs(args.responder_logs_dir):
        logs_dir = args.responder_logs_dir
    else:
        logs_dir = os.path.abspath(args.responder_logs_dir)

    # Process Actions
    if args.action == 'list':
        new_accounts = list_accounts(logs_dir)
        if new_accounts:
            print("\n[+] The following accounts have newly captured hashes:\n")
            for account in new_accounts:
                print(account)
        else:
            print("[-] No new hashes captured since the last rotation")
        if CACHE:
            print("\n[+] The hashes for the following accounts were previously captured:\n")
            for account in CACHE:
                print(account)
    elif args.action == 'extract':
        hash = extract_creds(logs_dir)
        print(f'\n{hash}')
    elif args.action == 'hashlist':
        hashlist = generate_hashlist(logs_dir)
        if hashlist:
            now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
            outfile_name = f'{os.getcwd()}/rotator-hashlist-{now}.hashes'
            with open(outfile_name, 'w+') as file:
                file.write("\n".join(map(str, hashlist)))
            print(f"[+] Generated hashlist at {outfile_name}")
        else:
            print("[-] No new hashes captured since the last rotation")
        save_cache()
    elif args.action == 'reset':
        reset_cache()

    sys.exit(0)


if __name__ == "__main__":
    CACHE_FILE = f"{os.path.expanduser('~')}/.rotator"
    global CACHE
    CACHE = []
    main()
