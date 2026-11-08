# Codex read-only review: Paper C CIDEr-VI pin (2026-11-08)

**Subject:**
- manuscript/prereg/2026-11-02_c_pvr_tier1/CIDER_VI_PIN_v1.md (0ff30613)
- scripts/c_pvr/c_pvr_cider_vi.py (ae1bd10e)
- scripts/c_pvr/requirements_c_pvr_cider.lock (1bb358ae)

**Compared against:**
- scripts/c_pvr/c_pvr_score.py
- CC-293, section G-1

Codex ran read-only and edited no files. The coordinator transcribed its findings below.

## Findings

1. **Medium:** scripts/c_pvr/c_pvr.py:543, reached through CP.rdr. The producer runs whichever `java` comes first on PATH and never checks its version. The pin records OpenJDK 21.0.12.1, so a different JVM could change segmentation silently.
   - Fix: before starting RDR, check the Java version against the pinned one and FAULT if they differ. Record the version in the producer's run record.

## No issue found
Codex found no issue on the other checks:
- The CIDEr computation uses the pinned kit scorer, default per-set DF and ×100.
- References and candidates go through the same text route: NFC, whitespace collapse, RDR, then lower case.
- The as-written and stripped punctuation columns follow the pin.
- The output JSON shape matches what c_pvr_score.py reads.
- The FAULT paths check required arms, A0, complete outputs, reference coverage and guard-half membership before scoring.
- Pinned inputs are hash-checked.
- The producer starts no CUDA process.
