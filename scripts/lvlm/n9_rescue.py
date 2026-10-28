#!/usr/bin/env python3
"""N9 rescue rules: GPU cap, start rule and attempt gates (manuscript/prereg/2026-10-28_n9_rescue_addendum.md §3-§5).

Called by scripts/lvlm/n9_rescue_job.sh on M3 (stdlib only). Every constant below is quoted in the addendum.
  used     --ledger L                          GPU seconds charged so far (all N9 rescue steps)
  plan     --ledger L --attempt A [--now T]    after K_F PASS: writes cap.json; exit 3 = method decodes must not start
  left     --ledger L --attempt A              seconds the next method run may use (0 = CAP STOP)
  clock                                       exit 1 at or after the 11-08 hard stop (no N9 stage starts)
  kfok     --dir D                             exit 0 iff D/kf.json is a K_F PASS on D/n9_base.json by this scorer
  trigger2 --dir D                             exit 0 iff attempt 1 failed K_F and its base hit the 512-token limit
  score1024 <score_k2_n9.py args>              attempt 2 only: the unchanged scorer, expecting max_new_tokens 1024
  --selftest
"""
import hashlib, importlib.util, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCORER = REPO / 'scripts/lvlm/score_k2_n9.py'
CEILING_S = 6 * 3600                  # CC-140 r3: 6 GPU-h for all N9 rescue GPU time (both base attempts included)
CAP_FACTOR = 8 * 1.5                  # CC-140 r3: measured base time x 8 runs x 1.5
N_METHOD_RUNS = 7                     # prereg §1: six methods + n9_povid_fullmerge
START_DEADLINE = '2026-11-06T12:00:00Z'   # CC-140 r3: no method decode if the projected finish is later
HARD_STOP = '2026-11-08T12:00:00Z'        # CC-142 W1: no N9 stage starts later; no result by then = NOT-TESTABLE
MAX_NEW_TOKENS = {1: 512, 2: 1024}    # attempt 2 = LiM model_vqa.py l.71 (addendum §2)
epoch = lambda s: int(datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).timestamp())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ledger(path):
    """Rows 'name<TAB>start<TAB>t0' then 'name<TAB>end<TAB>seconds'. A start without its end fails closed."""
    open_, done = {}, []
    for row in Path(path).read_text().splitlines() if Path(path).exists() else []:
        name, kind, val = row.split('\t')
        if kind == 'start':
            if name in open_:
                raise SystemExit(f'ledger: {name} started twice without an end (hard kill?): JOB STOP, judge')
            open_[name] = int(val)
        else:
            open_.pop(name)
            done.append((name, int(val)))
    if open_:
        raise SystemExit(f'ledger: unfinished step {sorted(open_)}: JOB STOP, judge')
    return done


def used(path, prefix=''):
    return sum(s for n, s in ledger(path) if n.startswith(prefix))


def plan(path, attempt, now):
    """Cap and start rule (addendum §3, §4). Returns (ok, record)."""
    base_s = used(path, f'a{attempt}/n9_base')  # all segments, if the base decode was resumed
    cap = int(min(CAP_FACTOR * base_s, CEILING_S - used(path)))
    need = N_METHOD_RUNS * base_s
    rec = {'attempt': attempt, 'base_wall_s': base_s, 'cap_s': cap, 'need_s': need, 'used_before_methods_s': used(path),
           'ceiling_s': CEILING_S, 'now_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
           'projected_finish_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now + max(cap, 0))),
           'start_deadline_utc': START_DEADLINE}
    rec['reasons'] = [r for r, bad in (('need exceeds cap or ceiling', need > cap),
                                       ('projected finish after the start deadline', now + cap > epoch(START_DEADLINE)))
                      if bad]
    return not rec['reasons'], rec


def left(path, attempt, cap):
    return max(0, min(cap - used(path, f'a{attempt}/') + used(path, f'a{attempt}/n9_base'),
                      CEILING_S - used(path)))


def kfok(d):
    d = Path(d)
    kf = json.loads((d / 'kf.json').read_text())
    return (kf.get('mode') == 'kf' and kf['K_F']['verdict'] == 'PASS' and kf['script_sha256'] == sha(SCORER)
            and kf['run']['sha256'] == sha(d / 'n9_base.json'))


def trigger2(d):
    """Base-only: attempt 1 K_F FAIL and >= 1 base caption at the 512-token limit (else 1024 is inert under greedy)."""
    d = Path(d)
    kf = json.loads((d / 'kf.json').read_text())
    base = json.loads((d / 'n9_base.json').read_text())
    hits = sum(bool(p['hit_max_new_tokens']) for p in base['preds'])
    return kf['K_F']['verdict'] == 'FAIL' and kf['run']['sha256'] == sha(d / 'n9_base.json') and hits >= 1, hits


def score1024(argv):
    """Run score_k2_n9.py unchanged (its sha, e1check and K2 checks intact) with the expected max_new_tokens = 1024."""
    spec = importlib.util.spec_from_file_location('score_k2_n9', SCORER)
    S = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S)
    orig = S.registration

    def registration():
        r, th = orig()
        r['decoding']['max_new_tokens'] = MAX_NEW_TOKENS[2]
        return r, th
    S.registration = registration
    rc = S.main(argv)
    out = Path(argv[argv.index('--out') + 1])
    d = json.loads(out.read_text())
    d['n9_rescue_wrapper'] = {'path': 'scripts/lvlm/n9_rescue.py', 'sha256': sha(__file__), 'expected_max_new_tokens': 1024}
    out.write_text(json.dumps(d, indent=1) + '\n')
    return rc


def selftest():
    import tempfile
    t = Path(tempfile.mkdtemp()) / 'gpu_seconds.tsv'
    t.write_text('a1/n9_base\tstart\t0\na1/n9_base\tend\t1800\n')
    now = epoch('2026-11-01T00:00:00Z')
    ok, r = plan(t, 1, now)                       # 0.5 h base: cap = min(6 h, 6 h - 0.5 h) = 5.5 h, need 3.5 h
    assert ok and r['cap_s'] == 19800 and r['need_s'] == 12600, r
    ok, r = plan(t, 1, epoch('2026-11-06T08:00:00Z'))   # 08:00 + 5.5 h = 13:30 > 12:00
    assert not ok and r['reasons'] == ['projected finish after the start deadline'], r
    t.write_text('a1/n9_base\tstart\t0\na1/n9_base\tend\t3600\n')
    ok, r = plan(t, 1, now)                       # 1 h base: need 7 h > cap 5 h
    assert not ok and r['reasons'] == ['need exceeds cap or ceiling'], r
    t.write_text('a1/n9_base\tstart\t0\na1/n9_base\tend\t600\n')
    ok, r = plan(t, 1, now)                       # 10 min base: cap = 12 x 600 = 7200 < ceiling
    assert ok and r['cap_s'] == 7200, r
    t.write_text(t.read_text() + 'a1/n9_povid\tstart\t1\na1/n9_povid\tend\t7000\n')
    assert left(t, 1, 7200) == 200 and used(t) == 7600
    t.write_text(t.read_text() + 'a1/n9_rlaifv\tstart\t2\n')
    try:
        used(t)
        raise AssertionError('open ledger step accepted')
    except SystemExit:
        pass
    t.write_text('a1/n9_base\tstart\t0\na1/n9_base\tend\t400\na1/n9_base\tstart\t9\na1/n9_base\tend\t200\n')
    assert plan(t, 1, now)[1]['base_wall_s'] == 600       # a resumed base is charged and measured in full
    d = t.parent / 'a1'
    d.mkdir()
    (d / 'n9_base.json').write_text(json.dumps({'preds': [{'hit_max_new_tokens': False}, {'hit_max_new_tokens': True}]}))
    kf = lambda v, s: (d / 'kf.json').write_text(json.dumps(
        {'mode': 'kf', 'script_sha256': s, 'run': {'sha256': sha(d / 'n9_base.json')}, 'K_F': {'verdict': v}}))
    kf('PASS', sha(SCORER))
    assert kfok(d) and not trigger2(d)[0]
    kf('PASS', '0' * 64)
    assert not kfok(d)                                     # K_F from another scorer version does not count
    kf('FAIL', sha(SCORER))
    assert not kfok(d) and trigger2(d) == (True, 1)
    (d / 'n9_base.json').write_text(json.dumps({'preds': [{'hit_max_new_tokens': False}]}))
    assert trigger2(d)[0] is False                         # sha no longer matches, and no caption hit 512
    assert epoch(START_DEADLINE) < epoch(HARD_STOP) and MAX_NEW_TOKENS[1] == 512
    print('n9_rescue selftest ok')
    return 0


def main(a):
    if a[:1] == ['--selftest']:
        return selftest()
    if a[:1] == ['score1024']:
        return score1024(a[1:])
    if not a:
        raise SystemExit(__doc__)
    cmd, kw = a[0], dict(zip(a[1::2], a[2::2]))
    if cmd == 'used':
        print(used(kw['--ledger']))
    elif cmd == 'plan':
        ok, rec = plan(kw['--ledger'], int(kw['--attempt']), int(kw.get('--now', time.time())))
        print(json.dumps(rec))
        return 0 if ok else 3
    elif cmd == 'left':
        cap = json.loads((Path(kw['--ledger']).parent / f"a{kw['--attempt']}/cap.json").read_text())['cap_s']
        print(left(kw['--ledger'], int(kw['--attempt']), cap))
    elif cmd == 'clock':
        return 0 if time.time() < epoch(HARD_STOP) else 1
    elif cmd == 'kfok':
        return 0 if kfok(kw['--dir']) else 1
    elif cmd == 'trigger2':
        ok, hits = trigger2(kw['--dir'])
        print(f'attempt-1 base captions at the 512-token limit: {hits}')
        return 0 if ok else 1
    else:
        raise SystemExit(__doc__)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
