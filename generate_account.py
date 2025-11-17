from algosdk.account import generate_account
from algokit_utils import AlgorandClient
from dotenv import load_dotenv, set_key
import os

load_dotenv()

def generate_a_test_account():
    sk = os.getenv('sk')
    pk = os.getenv('pk')
    is_github_actions_environ = os.getenv('IS_GITHUB_ACTIONS_ENVIRONMENT')
    if not sk and not pk and is_github_actions_environ == 'N':
        sk, pk = generate_account()
        set_key('.env', 'sk', sk)
        set_key('.env', 'pk', pk)
        input(
            'An account did not exist in this project directory, please visit https://bank.testnet.algorand.network/' \
            'and fund the account with Algorand, paste this address into the input field on the website:\n' \
            f'Address: {pk}\n\n' \
            'Press any key after you have funded the account . . .'
        )
    elif not sk and not pk and is_github_actions_environ == 'Y':
        print(f'A prefunded account is necessary in Github Actions environment variables for testing')

    else:
        print(f'Account successfully loaded!')
        account_funded = False
        while not account_funded:
            account_funded = check_balance(is_github_actions_environ, pk)
            print(f'Account is funded!')

def check_balance(is_github_actions_environ: bool, pk: str):
    algorand = AlgorandClient.testnet()
    account_info = algorand.account.get_information(pk)
    available_balance = account_info.amount - account_info.min_balance
    if available_balance < 1_000_000:
        if is_github_actions_environ:
            raise RuntimeError(
                'Account balance is less than 1 Algo, please fund the account via https://bank.testnet.algorand.network/'
                f'Address: {pk}\n\n' \
                'Exiting Github Action Job'
            )
        else:
            input(
                'Account balance is less than 1 Algo, please fund the account via https://bank.testnet.algorand.network/'
                f'Address: {pk}\n\n' \
                'Press any key after you have funded the account . . .'
            )
        return False
    else:
        return True

# Funded account via https://bank.testnet.algorand.network/
