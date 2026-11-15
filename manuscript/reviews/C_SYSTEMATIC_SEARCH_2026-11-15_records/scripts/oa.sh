#!/bin/bash
# oa.sh ID PAGE FILTER -> one OpenAlex list call; body to raw/ID_pPAGE.json, headers to raw/ID_pPAGE.hdr; prints a log line.
# The key is read by curl from its file (never on a command line, never printed); the effective URL is never printed.
set -u
W=/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/search_2026-11-15
id=$1; page=$2; filter=$3
ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
code=$(curl -sS -G "https://api.openalex.org/works" -m 90 -A "vsps-research (mailto:vsps-research@example.org)" \
  --data-urlencode "filter=$filter" --data-urlencode "per-page=200" --data-urlencode "page=$page" \
  --data-urlencode "select=id,doi,title,publication_date,type,primary_location,abstract_inverted_index,cited_by_count" \
  --data-urlencode "mailto=vsps-research@example.org" --data-urlencode "api_key@$HOME/.config/openalex/key" \
  -D "$W/raw/${id}_p${page}.hdr" -o "$W/raw/${id}_p${page}.json" -w '%{http_code}')
n=$(python3 -I -c "import json,sys; j=json.load(open(sys.argv[1])); print(j.get('meta',{}).get('count'), len(j.get('results',[])), j.get('meta',{}).get('cost_usd', ''), sep='\t')" "$W/raw/${id}_p${page}.json" 2>/dev/null || echo "ERR")
rem=$(grep -i -E '^x-ratelimit-remaining|^x-ratelimit-credits|^x-credits|^x-api-credits' "$W/raw/${id}_p${page}.hdr" | tr -d '\r' | tr '\n' ' ')
printf '%s\tOpenAlex\t%s\tpage %s\tHTTP %s\thits/fetched/cost: %s\t%s\t%s\n' "$ts" "$id" "$page" "$code" "$n" "$rem" "$filter" | tee -a "$W/log.tsv" | cut -c1-260
