from contract_files.TestClient import TestContractFactory, TestContractClient, CreateBoxArgs
from algokit_utils import AlgorandClient, SigningAccount, PaymentParams, AlgoAmount, CommonAppCallParams 
from dotenv import load_dotenv
from generate_account import generate_a_test_account
import os

load_dotenv()

sk = os.getenv('sk')
pk = os.getenv('pk')
test_account = SigningAccount(
    private_key=sk,
    address=pk
)

algorand = AlgorandClient.testnet()

factory = TestContractFactory(
    algorand=algorand,
    default_sender=pk,
    default_signer=test_account.signer,
)

def deploy_contract() -> tuple[str, TestContractClient]:
    print(f'Deploying Test Application . . .')
    typed_client, deploy_response = factory.send.create.bare()
    app_id = typed_client.app_id
    app_address = typed_client.app_address
    print(f'Successfully Deployed App\nApp ID: {app_id}\nApp Address: {app_address}\n')
    return app_address, typed_client

def fund_app_with_account_mbr(app_address: str) -> None:

    print(f'Funding Test Application with Account MBR . . .')
    fund_app_tx = algorand.send.payment(
        params=PaymentParams(
            sender=pk,
            signer=test_account.signer,
            receiver=app_address,
            amount=AlgoAmount(micro_algo=100_000),
            validity_window=1000
        )
    )

    print(f'Funded App with Account Minimum Balance Requirement!\nTx ID: {fund_app_tx.tx_id}')
    return

def test_create_box_method(typed_client: TestContractClient) -> None:
    mbr_payment = algorand.create_transaction.payment(
        PaymentParams(
            sender=pk,
            signer=test_account.signer,
            receiver=typed_client.app_address,
            amount=AlgoAmount(micro_algo=100_000),
            validity_window=1000
        )
    )

    print(f'Calling Create Box Method . . .')
    method_call_response = typed_client.send.create_box(
        args=CreateBoxArgs(
            mbr_payment=mbr_payment,
        ),
        params=CommonAppCallParams(
            max_fee=AlgoAmount(micro_algo=10_000),
            validity_window=1000
        ),
        send_params={
            'cover_app_call_inner_transaction_fees': True,
            'populate_app_call_resources': True
        }
    )
    print(f'Created Box Successfully!\nTx ID: {method_call_response.tx_id}')

if __name__ == '__main__':
    generate_a_test_account()
    app_address, typed_client = deploy_contract()
    fund_app_with_account_mbr(app_address)
    test_create_box_method(typed_client)
