# End-to-end VSPS pipeline. `make all SEED=42`; `make seeds` for 42/43/44.
# Hyperparameters live in configs/main.env. A target whose output exists is skipped.
include configs/main.env
SHELL := bash
.SHELLFLAGS := -o pipefail -ec
export NCS_DATA

STAGE1  := $(NCS_DATA)/stage1
FINAL   := $(NCS_DATA)/stage1_final
SUP     := $(NCS_DATA)/supervision
RUN     := $(NCS_DATA)/runs/sft_s$(SEED)
RESULTS := $(NCS_DATA)/results
NAME    := main_s$(SEED)

.PHONY: all seeds stage1 neutralize supervision sft eval prf funnel
all: eval prf funnel
seeds:
	for s in $(SEEDS); do $(MAKE) eval SEED=$$s || exit 1; done
	$(MAKE) prf funnel

stage1:      $(STAGE1)/.done
neutralize:  $(FINAL)/.done
supervision: $(SUP)/sft.jsonl
sft:         $(RUN)/adapter_config.json
eval:        $(RESULTS)/$(NAME)-detailed.preds.json $(RESULTS)/$(NAME)-short.preds.json
prf:         $(RESULTS)/object_prf.txt
funnel:      $(RESULTS)/recall_funnel.txt

# A prerequisite is listed only while the target is missing, so an existing output
# is never rebuilt and its upstream steps are never run. Delete it to force a rerun.
.SECONDEXPANSION:
unless_built = $(if $(wildcard $@),,$(1))

$(STAGE1)/.done:
ifeq ($(STAGE1_SHIPPED),1)
	mkdir -p $(NCS_DATA) && tar -xzf data/stage1_records/stage1_records.tar.gz -C $(NCS_DATA)
else
	$(PYTHON) scripts/generate_stage1.py --source $(SOURCE_SPLIT) --out $(STAGE1) \
	    --shard $(SHARD) --of $(SHARDS) --limit 0 --generator $(GENERATOR) --verifier $(VERIFIER) \
	    --max-entities $(MAX_ENTITIES) --max-pairs $(MAX_PAIRS) --verifier-tiles $(VERIFIER_TILES)
endif
	touch $@

$(FINAL)/.done: $$(call unless_built,$(STAGE1)/.done)
	$(PYTHON) scripts/person_uncap.py --in $(STAGE1) --out $(FINAL) --types $(UNCAP_TYPES)
	touch $@

$(SUP)/sft.jsonl: $$(call unless_built,$(FINAL)/.done)
	$(PYTHON) scripts/build_dpo_data.py --in $(FINAL) --out $(SUP) --seed $(SUP_SEED) \
	    --min-supported $(MIN_SUPPORTED) --budget $(BUDGET) --detailed-variant $(VARIANT) $(SUP_FLAGS)

$(RUN)/adapter_config.json: $$(call unless_built,$(SUP)/sft.jsonl)
	$(PYTHON) scripts/train_stage2.py --stage sft --data $(SUP) --out $(RUN) --epochs $(EPOCHS) \
	    --lr $(LR) --grad-accum $(GRAD_ACCUM) --lora-r $(LORA_R) --lora-alpha $(LORA_ALPHA) \
	    --vision-tokens $(VISION_TOKENS) --limit 0 --seed $(SEED)

$(RESULTS)/$(NAME)-%.preds.json: $$(call unless_built,$(RUN)/adapter_config.json)
	$(PYTHON) scripts/evaluate.py --model $(MODEL) --adapter $(RUN) --split $(EVAL_SPLIT) \
	    --prompt $* --name $(NAME)-$* --out $(RESULTS)/$(NAME)-$*.json --limit 0 \
	    --max-new-tokens $(MAX_NEW_TOKENS) --max-vision-tokens $(MAX_VIS_TOKENS) \
	    --segmenter $(SEGMENTER) $(EVAL_FLAGS)

$(RESULTS)/object_prf.txt: $$(call unless_built,$(RESULTS)/$(NAME)-detailed.preds.json)
	$(PYTHON) scripts/object_prf.py --results $(RESULTS) --split $(EVAL_SPLIT) | tee $@.tmp && mv $@.tmp $@

$(RESULTS)/recall_funnel.txt: $$(call unless_built,$(SUP)/sft.jsonl)
	mkdir -p $(RESULTS)
	$(PYTHON) scripts/recall_funnel.py --in $(FINAL) --sft $(SUP)/sft.jsonl | tee $@.tmp && mv $@.tmp $@
