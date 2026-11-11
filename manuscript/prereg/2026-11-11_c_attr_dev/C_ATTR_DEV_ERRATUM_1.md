# C-ATTR-DEV registration v1.1 (sha256 44f81329): erratum 1 (CC-338)

Written before any block-1 output exists. It changes no set, arm, seed, threshold, SESOI or family. Where it differs from v1.1, it binds. Label: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.

- E1 (§7.4, DETECTED). The step-down takes the claims in order of p (ties by claim name) and stops at the first claim that fails either θ̂ ≥ +2.0 or p ≤ α_j; no later claim is DETECTED.
- E2 (§7.4, DETECTED). "except at bootstrap ties" reads "except when exactly 50 of the 2,000 bootstrap means are ≤ 0 (the percentile lower bound can then exceed 0 while p = 51/2,001 > 0.025)". The p rule decides.
- E3 (§5, refusals). The stage-2 carve-out applies: the 925 OV-dev-B files of `lists.json` `refuse` are not refused (OV-dev-B is a development set of this table); every other OpenViIC file of `refuse`, every file of `sets.xm_test2500` and every Flickr30K test file name stay refused, and so does every test set.
- E4 (§11.1, paths). The list file and the stored-input pins are `scripts/c_attr/c_attr_lists.json` (with its `.sha256` sidecar) and `scripts/c_attr/STORED_SHA256`, not files in this folder.
- E5 (§6.3, §9, CC-331 N12). One host-parity verdict per backbone: a check (a) failure on OV-dev-B or on OV-dev-A triggers the fallback for every set of that backbone's `perm` step.
- E6 (CC-332 W2). §13 Q10 answer: "Replaced by X3 (CC-331): POST HOC on OV-dev-B, Flickr30K carve and val; first look at κ on XM-dev500." §13 Q7 answer and §7.10: the LMCap rows carry "re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers"; the `ret_img` against `rand_img` row carries "image-caption-pair prompt format, as used by RAGCap; not RAGCap", and the row name "RAGCap-style" is withdrawn.
- E7 (CC-332 W3). §7.13 ends with: "Values are for m = 1; with m nominated claims the first Holm step is at 0.025/m and power is lower."
- E8 (CC-332 W4). §11.1, `c_attr_score.py` self-test: "labels at the boundaries (θ̂ = 2.0; p = α_j)".
