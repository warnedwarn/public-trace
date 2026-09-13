import base64, hashlib, json, os, re
from genlayer_py import create_client, create_account
from genlayer_py.chains import studionet

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
ADDRESS = '0xbCc1F35FC4cd378CF16D065cD2B56d7A55F8FbDe'
TXS = {
    'deployment': '0x4e87fd430aed5eff5b0978f76da015edf8a8c82d9d1e390d838dbda0f227b6e5',
    'file': '0x4e37c27bb7fd6d08d77f95b0eae92ef3ae7bbb2eeff008814e40711f7574516b',
    'source': '0x42c9d4beafe8a765d228c0912e7fb782c266506204a9d2cf0270d1529562897b',
    'review': '0x1a0b1de877ac810bde6e0a17c96752fd57e57aa80c6a8f46843574a9a0f94509',
}

def execution(tx):
    receipts = (tx.get('consensus_data') or {}).get('leader_receipt') or []
    return receipts[0].get('execution_result') if receipts else tx.get('tx_execution_result_name')

text = open(os.path.join(WORKSPACE, 'accounts.env'), encoding='utf-8').read()
key = re.search(r'^\s*ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', text, re.M).group(1).strip()
account = create_account(account_private_key=key)
client = create_client(chain=studionet, account=account)
records = {name: client.get_transaction(transaction_hash=value) for name, value in TXS.items()}
deployed = base64.b64decode(records['deployment']['data']['contract_code']).decode()
local = open(os.path.join(ROOT, 'contracts', 'contract.py'), encoding='utf-8').read()
dockets = client.read_contract(address=ADDRESS, function_name='list_dockets', args=[])
latest = dockets[-1]
finding = client.read_contract(address=ADDRESS, function_name='get_finding', args=[latest['id']])
proof = {
    'contract': ADDRESS,
    'sourceSha256': hashlib.sha256(local.encode()).hexdigest(),
    'sourceMatches': deployed == local,
    'wallet': account.address,
    'walletMatchesOwner': latest['owner'].lower() == account.address.lower(),
    'docket': {'id': latest['id'], 'status': latest['status'], 'sourceCount': len(latest['sources'])},
    'finding': {'verdict': finding['verdict'], 'confidence': finding['confidence'], 'digestCount': len(finding['digests'])},
    'transactions': {name: {'hash': TXS[name], 'status': tx.get('status_name'), 'execution': execution(tx)} for name, tx in records.items()},
}
assert proof['sourceMatches'] and proof['walletMatchesOwner']
assert proof['docket']['status'] == 'reviewed' and proof['docket']['sourceCount'] == 2 and proof['finding']['digestCount'] == 2
assert all(item['status'] == 'FINALIZED' and item['execution'] == 'SUCCESS' for item in proof['transactions'].values())
print(json.dumps(proof, indent=2))
