from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "credit_byline.py"
SDK = "v0.2.16"
PROMPT = "Independently assign contributor-credit roles"
ARGS = (
    "A public-interest data article combining interviews, analysis, graphics, and an open-source notebook.",
    "Assign only roles supported by the contributor statement. Role order is writing, research, data, design, software, coordination. A byline requires unanimous approval.",
)


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), *ARGS, sdk_version=SDK)


def prepare(contract, vm, alice, bob, charlie):
    contract.invite_contributor("writer", "0x" + bob.hex())
    contract.invite_contributor("analyst", "0x" + charlie.hex())
    vm.sender = bob
    contract.submit_contribution("writer", "Interviewed five sources, drafted the article, and coordinated fact-check responses.", "writing,research,coordination")
    vm.sender = charlie
    contract.submit_contribution("analyst", "Cleaned the dataset, wrote the analysis notebook, and prepared the reproducible charts.", "data,software,design")
    vm.sender = alice
    contract.lock_contributions()


def test_roles_and_unanimous_byline(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    direct_vm.mock_llm(PROMPT, json.dumps({"role_mask": "110001"}))
    contract.assess_roles("writer")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"role_mask": "001110"}))
    contract.assess_roles("analyst")
    contract.propose_byline("writer,analyst")
    direct_vm.sender = direct_bob
    contract.approve_byline("writer")
    direct_vm.sender = direct_charlie
    contract.approve_byline("analyst")
    direct_vm.sender = direct_alice
    contract.finalize_byline()
    assert contract.get_state()["phase"] == "FINALIZED"
    assert contract.get_contributor("analyst")["role_mask"] == "001110"
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_one_contributor_challenge_reopens_assessment(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    direct_vm.mock_llm(PROMPT, json.dumps({"role_mask": "100001"}))
    contract.assess_roles("writer")
    contract.assess_roles("analyst")
    direct_vm.sender = direct_bob
    contract.challenge_roles("writer", "The role mask omitted the documented interviews and source research described in my statement.")
    assert contract.get_state()["phase"] == "ASSESSING_ROLES"
    direct_vm.sender = direct_alice
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"role_mask": "110001"}))
    contract.assess_roles("writer")
    assert contract.get_state()["phase"] == "READY_FOR_BYLINE"


def test_authorization_byline_membership_and_bad_mask(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.invite_contributor("writer", "0x" + direct_bob.hex())
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_contributor"):
        contract.submit_contribution("writer", "An unrelated account must not be able to claim another person's documented contribution.", "writing")
    direct_vm.sender = direct_bob
    contract.submit_contribution("writer", "Drafted and revised the complete article based on the approved outline and interview notes.", "writing")
    direct_vm.sender = direct_alice
    contract.invite_contributor("editor", "0x" + direct_charlie.hex())
    direct_vm.sender = direct_charlie
    contract.submit_contribution("editor", "Coordinated review, verified sources, and organized the final publication schedule.", "research,coordination")
    direct_vm.sender = direct_alice
    contract.lock_contributions()
    direct_vm.mock_llm(PROMPT, json.dumps({"role_mask": "12"}))
    with direct_vm.expect_revert("invalid_role_mask"):
        contract.assess_roles("writer")
    assert contract.get_state()["assessed_count"] == 0

