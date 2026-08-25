import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt)
    return receipt


@pytest.mark.integration
def test_studionet_contributor_role_assessment(default_account, secondary_account, tertiary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "credit_byline.py")
    args = ["A public-interest article combining interviews, analysis, graphics, and a reproducible notebook.", "Assign only roles supported by statements. Role order is writing, research, data, design, software, coordination."]
    deployed = _ok(factory.deploy_contract_tx(args=args, account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    owner = factory.build_contract(address, account=default_account)
    writer = factory.build_contract(address, account=secondary_account)
    analyst = factory.build_contract(address, account=tertiary_account)
    _ok(owner.invite_contributor(args=["writer", secondary_account.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(owner.invite_contributor(args=["analyst", tertiary_account.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(writer.submit_contribution(args=["writer", "Drafted the article and coordinated all source responses and revisions.", "writing,coordination"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(analyst.submit_contribution(args=["analyst", "Cleaned the data, wrote analysis code, and prepared publication charts.", "data,software,design"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(owner.lock_contributions(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = _ok(owner.assess_roles(args=["writer"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    role_mask = owner.get_contributor(args=["writer"]).call()["role_mask"]
    assert len(role_mask) == 6 and set(role_mask) <= {"0", "1"}
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": role_mask}, sort_keys=True))
