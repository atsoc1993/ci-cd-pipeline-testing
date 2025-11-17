from algopy import ARC4Contract, subroutine, UInt64, Global, itxn, Txn, arc4, BoxMap, Account, gtxn
from algopy.arc4 import abimethod


@subroutine
def get_mbr() -> UInt64:
    return Global.current_application_address.min_balance

@subroutine
def refund_excess_mbr(excess: UInt64) -> None:
    itxn.Payment(
        receiver=Txn.sender,
        amount=excess
    ).submit()

class TestContract(ARC4Contract):
    def __init__(self) -> None:
        self.global_counter = arc4.UInt64(0)
        self.test_box_map = BoxMap(Account, arc4.UInt64, key_prefix='')

    @abimethod
    def create_box(self, mbr_payment: gtxn.PaymentTransaction) -> None:
        pre_mbr = get_mbr()
        self.test_box_map[Txn.sender] = self.global_counter
        self.increment_global_counter()
        post_mbr = get_mbr()
        refund_excess_mbr(mbr_payment.amount - (post_mbr - pre_mbr))

    @subroutine
    def increment_global_counter(self) -> None:
        self.global_counter = arc4.UInt64(self.global_counter.as_uint64() + 1)
        

        