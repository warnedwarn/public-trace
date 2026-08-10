import json,os,re,time
from genlayer_py import create_client,create_account
from genlayer_py.chains import testnet_bradbury
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));WORKSPACE=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
def value(name):
 s=open(os.path.join(WORKSPACE,'accounts.env'),encoding='utf-8').read();m=re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)',s,re.M);return m.group(1).strip()
def accepted(c,h):
 print(json.dumps({'submitted':h}),flush=True);c.wait_for_transaction_receipt(transaction_hash=h,status='ACCEPTED',retries=100,interval=15000);t=c.get_transaction(transaction_hash=h);print(json.dumps({'tx':h,'status':t.get('status_name'),'result':t.get('tx_execution_result_name')}),flush=True)
 if t.get('status_name')!='ACCEPTED' or t.get('tx_execution_result_name')!='FINISHED_WITH_RETURN':raise SystemExit(2)
account=create_account(account_private_key=value('ACCOUNT_2_GENLAYER_PRIVATE_KEY'));client=create_client(chain=testnet_bradbury,account=account);address=json.load(open(os.path.join(ROOT,'deployment.json')))['contract'];did='PT-WEB-'+str(int(time.time()))
h=client.write_contract(address=address,function_name='file_docket',args=[did,'GenLayer Intelligent Contracts can fetch live web content from external URLs.','GenLayer web access',['SUPPORT|https://docs.genlayer.com/developers/intelligent-contracts/features/web-access']]);accepted(client,h)
h=client.write_contract(address=address,function_name='add_source',args=[did,'CONTEXT|https://docs.genlayer.com/developers/intelligent-contracts/examples/fetch-web-content']);accepted(client,h)
h=client.write_contract(address=address,function_name='review_docket',args=[did]);accepted(client,h)
print(json.dumps({'docket':did,'contract':address}),flush=True)
