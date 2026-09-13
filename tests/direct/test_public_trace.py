import hashlib
from conftest import CONTRACT

SOURCES = [
    'SUPPORT|https://registry.example/report',
    'COUNTER|https://audit.example/rebuttal',
]
BODIES = [
    b'The published inspection confirms the bridge reopened after structural review.',
    b'The independent audit disputes the reopening date and lists unresolved defects.',
]
CLAIM = 'The North Bridge reopened after a completed structural inspection.'
RESULT = '{"verdict":"CONTESTED","supports":[0],"counters":[1],"context":[],"missing":[]}'

def prepared(vm, deploy, alice, audit_status=200, result=RESULT):
    vm.sender = alice
    contract = deploy(CONTRACT)
    contract.file_docket('bridge-1', CLAIM, 'North Bridge', [SOURCES[0]])
    contract.add_source('bridge-1', SOURCES[1])
    vm.mock_web(r'registry\.example', {'status': 200, 'body': BODIES[0].decode()})
    vm.mock_web(r'audit\.example', {'status': audit_status, 'body': BODIES[1].decode() if audit_status == 200 else ''})
    vm.mock_llm(r'.*PublicTrace evidence review.*', result)
    vm.mock_llm(r'.*PublicTrace verifier.*', '{"valid":true}')
    return contract

def test_end_to_end_consensus_and_attribution(direct_vm, direct_deploy, direct_alice):
    contract = prepared(direct_vm, direct_deploy, direct_alice)
    contract.review_docket('BRIDGE-1')
    finding = contract.get_finding('bridge-1')
    assert finding['verdict'] == 'CONTESTED'
    assert finding['supports'] == [0]
    assert finding['counters'] == [1]
    assert finding['digests'] == [hashlib.sha256(x).hexdigest() for x in BODIES]
    assert finding['confidence'] == 75
    assert 'support indexes [0]' in finding['rationale']
    assert contract.get_docket('bridge-1')['status'] == 'reviewed'

def test_duplicate_id_origin_and_path_are_rejected(direct_vm, direct_deploy, direct_alice):
    contract = prepared(direct_vm, direct_deploy, direct_alice)
    with direct_vm.expect_revert('unique docket'):
        contract.file_docket('bridge-1', CLAIM, 'North Bridge', [SOURCES[0]])
    with direct_vm.expect_revert('new source origin'):
        contract.add_source('bridge-1', 'CONTEXT|https://registry.example/other')
    with direct_vm.expect_revert('normalized source path'):
        contract.file_docket('bad', CLAIM, 'North Bridge', ['SUPPORT|https://safe.example/a/%2e%2e/secret'])

def test_unauthorized_mutation_and_replay_fail(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = prepared(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert('open owner docket'):
        contract.add_source('bridge-1', 'CONTEXT|https://third.example/note')
    with direct_vm.expect_revert('owner and at least two'):
        contract.review_docket('bridge-1')
    direct_vm.sender = direct_alice
    contract.review_docket('bridge-1')
    with direct_vm.expect_revert('owner and at least two'):
        contract.review_docket('bridge-1')

def test_forged_digest_and_invalid_partition_fail_validator(direct_vm, direct_deploy, direct_alice):
    contract = prepared(direct_vm, direct_deploy, direct_alice)
    result = contract._review(contract.dockets['BRIDGE-1'])
    assert direct_vm.run_validator(leader_result=result) is True
    forged = dict(result)
    forged['digests'] = list(reversed(result['digests']))
    assert direct_vm.run_validator(leader_result=forged) is False
    forged = dict(result)
    forged['supports'] = [0, 1]
    forged['counters'] = [1]
    assert direct_vm.run_validator(leader_result=forged) is False

def test_source_failure_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = prepared(direct_vm, direct_deploy, direct_alice, audit_status=503)
    with direct_vm.expect_revert('source unavailable'):
        contract.review_docket('bridge-1')

def test_malformed_model_output_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = prepared(direct_vm, direct_deploy, direct_alice, result='{"verdict":"SUPPORTED"}')
    with direct_vm.expect_revert('every source must be classified once'):
        contract.review_docket('bridge-1')
