import { createAccount, createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';

const client = createClient({
  chain: studionet,
  endpoint: 'https://studio.genlayer.com/api',
  account: createAccount(),
});
const address = '0xbCc1F35FC4cd378CF16D065cD2B56d7A55F8FbDe';
const docket = await client.readContract({
  address,
  functionName: 'get_docket',
  args: ['PT-WEB-1789329322'],
});
const finding = await client.readContract({
  address,
  functionName: 'get_finding',
  args: ['PT-WEB-1789329322'],
});
console.log(JSON.stringify({ docket, finding }, null, 2));
