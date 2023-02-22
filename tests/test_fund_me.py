from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me
from brownie import network,accounts,exceptions
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
def test_can_fund_and_withdraw():
    account=get_account()
    fund_me=deploy_fund_me()
    entrance_fee=fund_me.getEntranceFee()
    print(f"entrance_fee={entrance_fee}")# brownie test Ä©Î²ÐèÒª-s
    tx=fund_me.fund({"from":account,"value":entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address)==entrance_fee
    tx2=fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address)==0
    
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me=deploy_fund_me()
    bad_actor=accounts[1]
    print(f"bad_actor is {bad_actor}")
    # fund_me.withdraw({"from":bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw(
            {
                "from": bad_actor,
                "gas_price": 0,
                "gas_limit": 1200000,
                "allow_revert": True,
            }
        ) 