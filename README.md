# Source Jury

Source Jury is a live GenLayer evidence-docket application for claims that should remain inspectable after a decision. A user opens one precise claim, adds public records from distinct HTTPS origins, and asks validators to classify what each fetched record actually supports. Caller labels are hints, never accepted as evidence by themselves.

[Open the public application](https://warnedwarn-source-jury.pages.dev/) | [Inspect the StudioNet contract](https://explorer-studio.genlayer.com/address/0xbCc1F35FC4cd378CF16D065cD2B56d7A55F8FbDe)

## Docket route

```text
OPEN ONE SOURCE
      |
      v
ADD INDEPENDENT ORIGINS
      |
      v
VALIDATORS REFETCH EVERY RECORD
      |
      v
REVIEWED: SUPPORTED | CONTESTED | UNDETERMINED
```

`file_docket` freezes the claim, subject, owner, and first source. `add_source` is owner-only while the docket remains open and rejects repeated normalized origins. `review_docket` requires at least two origins, invokes one supported nondeterministic consensus flow, and seals the docket once. `get_docket`, `get_finding`, `get_summary`, and `list_dockets` expose the stored result to the frontend.

## What validators decide

Every validator independently retrieves the complete source bodies. The candidate result must classify every index exactly once as support, counter-evidence, or context. Validators also verify the closed verdict and missing-evidence codes against the exact stored claim. Ordered SHA-256 response digests bind the finding to the fetched bytes. A forged digest order or overlapping classification fails validation.

Free-form rationale and confidence are not trusted model fields. They are derived deterministically from the validator-approved verdict and index partition, which removes prose variation from consensus and prevents an unchecked score from influencing the stored result.

## Hard boundaries

- Only clean HTTPS URLs without credentials, fragments, invalid ports, or decoded path traversal are accepted.
- Source origins must be distinct after hostname and port normalization.
- Docket IDs are canonicalized and cannot be overwritten.
- Only the docket owner may add evidence or request review.
- A reviewed docket cannot be changed or replayed.
- Unavailable sources and malformed model output fail closed.
- The interface waits for `FINALIZED` and successful execution before reading authoritative state. `ACCEPTED` is never displayed as completion.

## Reproduce the proof

```bash
genvm-lint contracts/contract.py
python -m pytest -q
cd frontend
npm install
npm run build
```

The test suite covers the complete lifecycle, malformed output, source failure, duplicate IDs and origins, invalid paths, unauthorized mutation, replay, forged digests, and invalid evidence partitions.

Run `python scripts/verify_deployment.py` to compare the deployed source with this repository and verify the recorded StudioNet lifecycle. The public proof docket is `PT-WEB-1789329322`. Its deployment, filing, source addition, and review transactions all reached `FINALIZED` with successful execution. The stored finding is `SUPPORTED` with two ordered digests.

## Deployment record

- Network: GenLayer StudioNet
- Contract: `0xbCc1F35FC4cd378CF16D065cD2B56d7A55F8FbDe`
- Deployment transaction: `0x4e87fd430aed5eff5b0978f76da015edf8a8c82d9d1e390d838dbda0f227b6e5`
- Reviewed contract source commit: `8aeab9317bb506621fb52284371941fcbd59cde3`
- Contract SHA-256: `4a1cde67f5ea4ba8b8797d9f07d253de97bf48781853e0e7d9fea8bfb9246abd`

The IANA and RFC records used in the public run are reproducible technical fixtures. Distinct origins prove source separation for the contract; they do not assert independent ownership by the project operator.
