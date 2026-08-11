# PublicTrace

PublicTrace turns a disputed public claim into an inspectable evidence docket. It does not ask visitors to vote on what feels true. It records the exact claim, registers supporting and counter-sources, and preserves validator-authenticated snapshots on GenLayer before producing an on-chain finding.

## From URL to finding

1. `file_docket` opens a claim and asks independent validators to fetch and summarize its first public source.
2. `add_source` expands the record with supporting, counter, or contextual evidence. Every added URL receives its own consensus-authenticated snapshot.
3. `review_docket` seals the docket and derives a stable `SUPPORTED`, `CONTESTED`, or `UNDETERMINED` finding from the classified authenticated record.
4. `get_docket` and `get_finding` return the live contract state rendered by the interface—there are no hard-coded findings.

This split keeps unreliable live HTML out of the final decision while retaining GenLayer's independent web verification where it matters: when evidence enters the public record.

## Live deployment

- App: https://warnedwarn-public-trace.pages.dev/
- Network: GenLayer StudioNet
- Contract: `0x94FF9eB9f73C002cC170b15390Cd3465f69dA2cb`
- Deployment transaction: `0x406f43e404db682b050217444b2f047f727c3a43225fe63d61610294243a18a1`

The complete smoke workflow is in `scripts/smoke_workflow.py`. Its latest StudioNet run confirmed `file_docket`, `add_source`, and `review_docket` as accepted, then read a `SUPPORTED` finding with 68% confidence from contract state.

## Run the interface

```bash
cd frontend
npm install
npm run dev
```

The wallet flow requests StudioNet automatically and shows every transaction from approval through validator consensus.
