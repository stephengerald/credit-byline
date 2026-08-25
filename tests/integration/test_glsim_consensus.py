from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Independently assign contributor-credit roles"
ARGS = ["A public-interest article combining interviews, analysis, graphics, and a reproducible notebook.", "Assign only roles supported by statements. Role order is writing, research, data, design, software, coordination."]


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"role_mask": "100001"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_credit_and_byline_workflow():
    owner, writer, analyst = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "credit_byline.py")
    deployed = factory.deploy_contract_tx(args=ARGS, account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    owner_contract = factory.build_contract(address, account=owner)
    writer_contract = factory.build_contract(address, account=writer)
    analyst_contract = factory.build_contract(address, account=analyst)
    ok(owner_contract.invite_contributor(args=["writer", writer.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner_contract.invite_contributor(args=["analyst", analyst.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(writer_contract.submit_contribution(args=["writer", "Drafted the article and coordinated all source responses and revisions.", "writing,coordination"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(analyst_contract.submit_contribution(args=["analyst", "Cleaned the data, wrote analysis code, and prepared the publication charts.", "data,software,design"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner_contract.lock_contributions(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner_contract.assess_roles(args=["writer"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner_contract.assess_roles(args=["analyst"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner_contract.propose_byline(args=["writer,analyst"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(writer_contract.approve_byline(args=["writer"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(analyst_contract.approve_byline(args=["analyst"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(owner_contract.finalize_byline(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert owner_contract.get_state(args=[]).call()["phase"] == "FINALIZED"

