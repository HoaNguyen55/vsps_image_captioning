export const meta = {
  name: 'expert-review',
  description: 'Expert review committee per paper (novelty, correctness, contribution, clarity), Codex external review, area-chair meta-review, then revision by a writer',
  whenToUse: 'PI asks for an expert review of papers followed by revision. args: {papers:[{key, dir, venue, notes}], revise: true|false}',
  phases: [
    { title: 'Review' },
    { title: 'Meta-review' },
    { title: 'Revise' },
  ],
}

const PAPERS = (args && args.papers) || []
const REVISE = !(args && args.revise === false)

const RULES = `Binding rules for any edit or suggestion: no new human gold labels; AI-generated labels are not evidence; one look per test set and the three-tier method (dev-explore -> dev-confirm rehearsal -> single test look); registered test FAILs are reported briefly, never hidden (PASS headline is fine); no "first" claims without verified prior art; no caption text from OpenViIC/KTVIC/UIT-ViIC in repo files; never put any personal e-mail in a web request (use vsps-research@example.org or none); no commits, no GPU. Mark judgements as AI opinion.`

const REVIEWERS = [
  { key: 'R1-domain', who: 'a senior reviewer in vision-language models and image captioning (incl. multilingual and Vietnamese NLP)' },
  { key: 'R2-methods', who: 'a methods and statistics reviewer (experimental design, preregistration, confidence intervals, multiple testing, leakage)' },
  { key: 'R3-evaluation', who: 'an evaluation-metrics specialist (caption metrics, hallucination metrics, reference panels, benchmark validity)' },
  { key: 'R4-editor', who: 'a handling editor of the target venue who judges fit, contribution size and clarity for that journal' },
]

const REVIEW = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    scores: {
      type: 'object',
      properties: {
        novelty: { type: 'number', description: '1-5' },
        correctness: { type: 'number', description: '1-5' },
        contribution: { type: 'number', description: '1-5' },
        clarity: { type: 'number', description: '1-5' },
      },
      required: ['novelty', 'correctness', 'contribution', 'clarity'],
    },
    recommendation: { type: 'string', enum: ['accept', 'minor revision', 'major revision', 'reject'] },
    confidence: { type: 'number', description: 'reviewer confidence 1-5' },
    major_issues: { type: 'array', items: { type: 'string', description: 'issue + evidence pointer file:line + requested change' } },
    minor_issues: { type: 'array', items: { type: 'string' } },
    report: { type: 'string', description: 'full review report text, journal style' },
  },
  required: ['summary', 'scores', 'recommendation', 'confidence', 'major_issues', 'minor_issues', 'report'],
}

function reviewPrompt(p, r) {
  return `You are ${r.who}, reviewing a manuscript submitted to ${p.venue}. Repo /mnt/d/vsps_image_captioning. Manuscript sources: ${p.dir} (read the outline/abstract, every section file, supplement, number manifest, bib). ${p.notes || ''}
Review it as a demanding but fair expert. Verify claims against the cited decided result files and preregistrations where the manuscript points to them; check related work with real searches (arXiv/OpenAlex/Semantic Scholar/Crossref) where novelty is claimed. Score each criterion 1-5 with justification: NOVELTY (vs named prior work), CORRECTNESS (methods, statistics, numbers match sources, claims supported, no overclaiming), CONTRIBUTION (scientific and practical significance for this venue), CLARITY (structure, writing, figures, tables). Give a recommendation and a journal-style report with numbered major and minor issues, each with a file:line pointer and a concrete requested change. ${RULES}`
}

const results = await pipeline(PAPERS,
  p => parallel([
    ...REVIEWERS.map(r => () => agent(reviewPrompt(p, r), { label: `${p.key}:${r.key}`, phase: 'Review', schema: REVIEW })),
    () => agent(`External reviewer (different model family), read-only. Review the manuscript in /mnt/d/vsps_image_captioning/${p.dir} for ${p.venue} on NOVELTY, CORRECTNESS, CONTRIBUTION, CLARITY (1-5 each), give a recommendation (accept/minor/major/reject) and numbered major/minor issues with file:line pointers. Write your report to /mnt/d/vsps_image_captioning/manuscript/reviews/${p.key}_codex_review.md and return it in <=60 lines.`,
      { label: `${p.key}:codex`, phase: 'Review', agentType: 'codex:codex-rescue' }),
  ]).then(rs => ({ p, reviews: rs.filter(Boolean) })),
  x => agent(`You are the AREA CHAIR for ${x.p.venue}. Repo /mnt/d/vsps_image_captioning. Paper: ${x.p.dir}. Below are ${x.reviews.length} expert reviews (the last one may be a text report from an external reviewer). Write the meta-review to manuscript/reviews/${x.p.key}_META_REVIEW.md: per-criterion consensus scores (novelty, correctness, contribution, clarity) with disagreement noted, a decision (accept / minor / major / reject), and a single PRIORITISED REVISION PLAN: numbered items, each with the reviewers who raised it, the file(s) to change, the exact change, whether it needs a new experiment (flag it; experiments are NOT done in this revision — they go to the coordinator), and an estimate of how much it raises the scores. Also write each reviewer's full report to manuscript/reviews/${x.p.key}_<reviewer>.md. Then write a short Vietnamese summary for the PI at the top. ${RULES}
REVIEWS:
${JSON.stringify(x.reviews, null, 1).slice(0, 150000)}`,
    { label: `${x.p.key}:meta`, phase: 'Meta-review' }).then(meta => ({ ...x, meta })),
  x => REVISE
    ? agent(`You are the corresponding author's writer for ${x.p.dir} (target ${x.p.venue}). Read manuscript/reviews/${x.p.key}_META_REVIEW.md and apply EVERY revision-plan item that needs no new experiment. Another tool also edits this repo: snapshot the sha256 of each file before editing and re-check right before writing. Keep numbers traceable to the number manifest; run python3 /tmp/claude-1000/-mnt-d-vsps-image-captioning/5a363495-c9d6-40f3-8f9c-a7285ef7a0e6/scratchpad/ngram_scan_cen.py on every edited file (0 hits). Write manuscript/reviews/${x.p.key}_RESPONSE_TO_REVIEWERS.md (point-by-point: done / partially / not done + why; experiment items listed for the coordinator). ${RULES} Return <=15 lines.`,
        { label: `${x.p.key}:revise`, phase: 'Revise' }).then(rev => ({ key: x.p.key, meta: x.meta, revise: rev }))
    : { key: x.p.key, meta: x.meta },
)
return results.filter(Boolean).map(r => ({ key: r.key, meta: String(r.meta).slice(0, 3000), revise: r.revise ? String(r.revise).slice(0, 2000) : null }))
