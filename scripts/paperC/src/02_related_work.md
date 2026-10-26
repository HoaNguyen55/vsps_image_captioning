## 2. Related work

<!-- Citation keys are placeholders for the .bib. Every [CITE ...] marks an entry whose details are not yet pinned. -->

**Retrieval for captioning.** Nearest-neighbour captioning borrows a caption from the most similar training image [Devlin2015NN, arXiv 1505.04467]. Our `nn_top1` and `nn_cons` baselines follow that idea and show how far copying alone would go. Later systems condition a trained decoder on retrieved captions [Ramos2023SmallCap]. LMCap prompts a text-only language model with captions retrieved across languages and evaluates on XM3600 [Ramos2023LMCap, arXiv 2305.19821]. We instead show the image to the model, use an in-domain Vietnamese memory, and compare retrieval with random examples from the same memory.

Li et al. [Li2024RetrievalRobustness, ACL 2024, doi 10.18653/v1/2024.acl-long.503] find that retrieval-augmented captioners copy tokens from the retrieved captions and are sensitive to their order and selection. This motivates our copy diagnostics (4-gram copy rate, near-verbatim share) and our neighbour-only object analysis.

**Highest overlap.** The closest work is a training-free multilingual captioning study for remote sensing [Rebelo2025RSCap, arXiv 2512.00887]. It retrieves examples with SigLIP2, includes variants in which the model sees the image, and re-ranks the examples with PageRank across ten languages. Our study differs in four ways:
- everyday images in Vietnamese;
- random and fixed example controls at equal k;
- count-matched object precision;
- a preregistered one-look test.

Negative Entity Suppression [Lu2025NES, arXiv 2511.08909] also targets objects that retrieval brings in. It filters entities absent from the input out of retrieved captions and suppresses them at the attention level; Section 3.4 contrasts it with our post-decode step.

**In-context configurations in large multimodal models.** Yang et al. [Yang2023ICLConfig, arXiv 2305.14800] compare image-selection and caption-assignment strategies for in-context captioning in English. Li et al. [Li2025UnveilingICL, arXiv 2507.08021] analyse shot count, retrieval and attention inside such models. dos Santos et al. [dosSantos2025ContextVLM, arXiv 2510.24331] ask how much vision-language models use the images and texts placed in their context. GRIP [Allabadi2026GRIP, arXiv 2606.12744] trains an example retriever from model feedback. We train no retriever. Our examples are captions only, shown as text, and the configuration space (k, order, prompt tail, guard threshold) was searched only on development data.

**Vietnamese image captioning.** The public Vietnamese benchmarks are UIT-ViIC [Lam2020UITViIC], KTVIC [Pham2024KTVIC, arXiv 2401.08100], UIT-OpenViIC [Bui2023OpenViIC, arXiv 2305.04166] and the Vietnamese references of XM3600 [Thapliyal2022XM3600]. ViG [Vu2026ViG, doi 10.1109/mapr72750.2026.11685699] adapts a frozen English-pretrained captioner to Vietnamese by training lightweight grounding branches on Vietnamese data. Our study trains nothing: it compares text-only in-context examples against a random-example control. VELVET [Vu2025VELVET, doi 10.15625/vap.2025.0261] is a multitask, multilingual prompting vision-language model for Vietnamese, pretrained on image-text data translated from English. A search of the arXiv API on 2026-10-21 for Vietnamese, captioning and in-context learning returned only the KTVIC and UIT-OpenViIC dataset papers. We make no priority claim and state only differences from the closest work.

**Object hallucination and its measurement.** CHAIR [Rohrbach2018CHAIR] counts mentioned objects that the gold does not support. Companion submission A shows that object precision depends on how many objects a caption names, and defines the count-matched comparison we use as P2. On XM3600 we score verified precision against the released Open Images V7 human-verified labels [Kuznetsova2020OpenImages], following A's mapping rule.

Post-hoc checking with a second model is common [Yin2023Woodpecker]. Our study registered such a guard, but its hypothesis was {{DF:ov_dev_b.H_G.passed|v:passed}} at the development test and is reported only as a registered negative (Section 6.7).
