"use client";
import { createAccount, createClient } from "genlayer-js";
import { testnetBradbury } from "genlayer-js/chains";
export const CONTRACT =
  "0xA577c4f2155C306CcA838d6fadDf640E72480fe6" as `0x${string}`;
export const EXPLORER = "https://explorer-bradbury.genlayer.com/tx";
const endpoint = "https://rpc-bradbury.genlayer.com";
const reader: any = createClient({
  chain: testnetBradbury,
  endpoint,
  account: createAccount(),
});
let wallet: any;
const wait = (n: number) => new Promise((r) => setTimeout(r, n));
const retryable = (e: any) =>
  /gas rate limit|rate limit|too many requests|backpressure|not currently accepting|failed to fetch|network|timeout/i.test(
    String(e?.message || e),
  );
export async function connect() {
  const eth = (window as any).ethereum;
  if (!eth) throw Error("Install Rabby or MetaMask first.");
  const [a] = await eth.request({ method: "eth_requestAccounts" });
  const id = "0x107d";
  if (
    String(await eth.request({ method: "eth_chainId" })).toLowerCase() !== id
  ) {
    try {
      await eth.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: id }],
      });
    } catch (e: any) {
      if (e?.code !== 4902) throw Error("Approve the Bradbury network switch.");
      await eth.request({
        method: "wallet_addEthereumChain",
        params: [
          {
            chainId: id,
            chainName: "GenLayer Bradbury Testnet",
            nativeCurrency: { name: "GEN", symbol: "GEN", decimals: 18 },
            rpcUrls: [endpoint],
            blockExplorerUrls: ["https://explorer-bradbury.genlayer.com"],
          },
        ],
      });
      await eth.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: id }],
      });
    }
  }
  wallet = createClient({
    chain: testnetBradbury,
    endpoint,
    account: a,
    provider: eth,
  });
  await wallet.initializeConsensusSmartContract?.().catch(() => {});
  return a as string;
}
export async function read<T>(name: string, args: any[] = []) {
  return (await reader.readContract({
    address: CONTRACT,
    functionName: name,
    args,
  })) as T;
}
export async function write(
  name: string,
  args: any[],
  progress: (s: string, h?: string) => void,
) {
  if (!wallet) throw Error("Connect wallet first.");
  progress("WALLET APPROVAL");
  const hash: string = await wallet.writeContract({
    address: CONTRACT,
    functionName: name,
    args,
    value: BigInt(0),
  });
  progress("AI CONSENSUS", hash);
  let receipt: any, last: any;
  for (let i = 0; i < 2; i++) {
    try {
      receipt = await wallet.waitForTransactionReceipt({
        hash,
        status: "ACCEPTED",
        retries: 30,
        interval: 30000,
      });
      break;
    } catch (e) {
      last = e;
      if (!retryable(e)) throw e;
      progress("RECONNECTING", hash);
      await wait(4000);
    }
  }
  if (!receipt) throw last;
  const tx: any = await wallet.getTransaction({ hash }).catch(() => null);
  const result =
    tx?.consensus_data?.leader_receipt?.[0]?.execution_result ??
    receipt?.tx_execution_result;
  if (String(result) === "2") throw Error("Contract execution rolled back.");
  progress("WRITTEN", hash);
  return hash;
}
