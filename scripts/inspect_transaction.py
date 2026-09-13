import json, os, re, sys
from genlayer_py import create_client, create_account
from genlayer_py.chains import studionet

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
text = open(os.path.join(WORKSPACE, 'accounts.env'), encoding='utf-8').read()
key = re.search(r'^\s*ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', text, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=key))
tx = client.get_transaction(transaction_hash=sys.argv[1])
if tx is None:
    print(json.dumps({'hash': sys.argv[1], 'status': 'NOT_INDEXED'}))
    raise SystemExit(0)
receipts = (tx.get('consensus_data') or {}).get('leader_receipt', [])
print(json.dumps({
    'hash': sys.argv[1],
    'status': tx.get('status_name'),
    'consensus': tx.get('result_name'),
    'execution': receipts[0].get('execution_result') if receipts else tx.get('tx_execution_result_name'),
}, indent=2, default=str))
