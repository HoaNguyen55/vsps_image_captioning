# VSPS-J E1+E2 AMENDMENT_3: E1b cost cap 5.0 -> 6.0 GPU-h (running block, no result seen)

Status: DRAFT for a one-judge diff read (REVERSIBLE, bar >= 90), 2026-10-31 ~16:40Z. Not committed.
Parent: AMENDMENT_2 as committed in 9ad0410 (CC-209b). PREREG section "Projection and cap rules" says: "Never: a subset,
another model, or a cap raise without a new ruling." This amendment asks for that ruling.
Trigger: OPS-1031e1bcaprisk (operator, m7 / ckey 103705).

## C1. Facts at the time of drafting (operator report; no result, score or P(yes) summary has been read)
- E1b launched 15:56Z on one RTX 4090; smoke OK. Pre-pass projection 4.21 h, image-200 projection 4.30 h, both stop false.
- The realised rate is 0.050-0.055 s per probe (GPU-bound, about 95 % utilisation). The projections used the smoke
  median; the mean is higher.
- At the cumulative rate the pass needs about 4.99 h; at the last-10k rate about 5.2 h. The 5.0 h cap trips at 20:57:11Z,
  at about 96-97 % of the 345,768 probes. A CAP_STOP makes E1b STOP (no resume, no score), wasting the block.

## C2. Change
- `CAP_H["e1b"]`: 5.0 -> 6.0 GPU-h, in `scripts/vsps_j_e1e2/e1e2.py` (one constant). E1a's cap (7.5) is unchanged.
- The projection rules are unchanged. The projection files already written (stop false) stay as they are.
- Cost: at most about +1 h x 14,535 VND/h, about +15k VND (PI-1031k).

## C3. Operation (single resume, AMENDMENT_1 W6 operator rule)
1. Gatekeeper commit of this amendment, the code change and the SUMS, after a CC-209c GO.
2. Before 20:57Z the operator kills the running `e1e2.py` by exact PID. This is a crash: no STOP marker, no stop record.
3. The operator stages the committed `e1e2.py` on m7 and verifies its sha. Then it resumes **once** into the same OUT
   folder `/root/e1b_run/out`.
   - `launch.json` keeps t0, so the clock is unchanged and includes the downtime.
   - The smoke is reused and finished probes are skipped.
4. If the pass still exceeds 6.0 h, CAP_STOP stands. No further raise.
5. OPS lines record the PID kill, the staged sha, the resume and the outcome.

## C4. What does not change
- No rule, threshold, grid, seed, SESOI, statistic, plan, order, image set or scoring step changes.
- No subset. No other model.
- The decision is made on running speed only: no outcome of E1b has been looked at.
