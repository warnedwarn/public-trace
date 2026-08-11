import json,os,re
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));WORKSPACE=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
def value(name):
    text=open(os.path.join(WORKSPACE,'accounts.env'),encoding='utf-8').read();m=re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)',text,re.M)
    if not m:raise SystemExit(name+' missing')
    return m.group(1).strip()
def find(x):
    if isinstance(x,dict):
        if x.get('recipient') and str(x.get('tx_execution_result',''))=='1':return x['recipient']
        for k,v in x.items():
            if k in ('contract_address','contractAddress') and isinstance(v,str):return v
            r=find(v)
            if r:return r
    if isinstance(x,list):
        for v in x:
            r=find(v)
            if r:return r
def main():
    key=value('ACCOUNT_2_GENLAYER_PRIVATE_KEY');username=value('ACCOUNT_2_GITHUB_USERNAME')
    if username!='warnedwarn':raise SystemExit('Account slot mismatch')
    account=create_account(account_private_key=key);client=create_client(chain=studionet,account=account);code=open(os.path.join(ROOT,'contracts','contract.py'),encoding='utf-8').read()
    h=client.deploy_contract(code=code,args=[]);print('deployTx',h,flush=True);receipt=client.wait_for_transaction_receipt(transaction_hash=h,status='ACCEPTED',retries=60,interval=30000);address=find(receipt)
    if not address:raise SystemExit('No contract address in accepted receipt')
    out={'contract':address,'deployTx':h,'network':'studionet','deployer':account.address};open(os.path.join(ROOT,'deployment.json'),'w',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
if __name__=='__main__':main()
