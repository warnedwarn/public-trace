import json,os,re,time
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));WORKSPACE=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
def value(name):
 s=open(os.path.join(WORKSPACE,'accounts.env'),encoding='utf-8').read();m=re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)',s,re.M);return m.group(1).strip()
def finalized(c,h):
 print(json.dumps({'submitted':h}),flush=True);c.wait_for_transaction_receipt(transaction_hash=h,status='FINALIZED',retries=180,interval=5000);t=c.get_transaction(transaction_hash=h);status=t.get('status_name');receipts=t.get('consensus_data',{}).get('leader_receipt',[]);result=receipts[0].get('execution_result') if receipts else t.get('tx_execution_result_name');print(json.dumps({'tx':h,'status':status,'result':result}),flush=True)
 if status!='FINALIZED' or result not in ('SUCCESS','FINISHED_WITH_RETURN'):raise SystemExit(2)
account=create_account(account_private_key=value('ACCOUNT_2_GENLAYER_PRIVATE_KEY'));client=create_client(chain=studionet,account=account);address=json.load(open(os.path.join(ROOT,'deployment.json')))['contract'];did='PT-WEB-'+str(int(time.time()))
h=client.write_contract(address=address,function_name='file_docket',args=[did,'The domain example.com is reserved for documentation and illustrative examples.','Reserved example domains',['SUPPORT|https://www.iana.org/help/example-domains']]);finalized(client,h);file_tx=h
h=client.write_contract(address=address,function_name='add_source',args=[did,'SUPPORT|https://www.rfc-editor.org/rfc/rfc2606.txt']);finalized(client,h);source_tx=h
h=client.write_contract(address=address,function_name='review_docket',args=[did]);finalized(client,h);review_tx=h
docket=client.read_contract(address=address,function_name='get_docket',args=[did]);finding=client.read_contract(address=address,function_name='get_finding',args=[did]);print(json.dumps({'docketId':did,'contract':address,'fileTx':file_tx,'sourceTx':source_tx,'reviewTx':review_tx,'docket':docket,'finding':finding},flush=True,default=str))
