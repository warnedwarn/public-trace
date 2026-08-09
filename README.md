# PublicTrace

PublicTrace is an open evidence instrument for claims that affect the public record. Instead of reducing a dispute to a poll, it preserves the exact claim, maps supporting and counter-evidence, and asks independent GenLayer validators to produce a reasoned finding.

## The evidence field

Each docket begins with one precise claim and at least one public source. More records can be attached while the docket is open. When its owner convenes review, GenLayer validators independently compare the claim against every source and agree on `SUPPORTED`, `CONTESTED`, or `UNDETERMINED`, including missing evidence and confidence.

## Contract surface

- `file_docket` — opens an immutable public claim
- `add_source` — expands the adversarial record before review
- `review_docket` — runs the intelligent-contract evidence judgment
- `get_docket` / `get_finding` — expose the record and result

Deployed on GenLayer Bradbury: `0x93E035719116B260eEA50C920d82c920802b0989`

## Run

```bash
cd frontend
npm install
npm run dev
```

The interface automatically requests the Bradbury network when a wallet connects. Production output is generated with `npm run build`.
