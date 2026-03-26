# IRPAPERS
A Visual Document Benchmark for Scientific Retrieval and Question Answering.

- You can also find the dataset on [HuggingFace](https://huggingface.co/datasets/weaviate/IRPAPERS).
- The experimental code used to produce the analysis in our paper can be found [here](https://www.github.com/weaviate/query-agent-benchmarking).

## Retrieval Leaderboard 🔎

| Rank | Retriever | Type | Recall@1 | Recall@5 | Recall@20 |
|------|-----------|------|----------|----------|-----------|
| 1 | Query Agent Search Mode (Voyage 4 Large) | Text | 61% | 86% | 92% |
| 2 | Mixedbread* | Image | 59% | 91% | 96% |
| 3 | Multimodal Hybrid (Cohere Embed v4.0 + Voyage 3 Large + BM25) | Hybrid | 58% | 91% | 98% |
| 4 | Cohere Embed v4.0 | Image | 58% | 87% | 97% |
| 5 | Voyage 4 Large | Text | 53% | 91% | 96% |
| 6 | Voyage 3 Large | Text | 52% | 86% | 95% |
| 7 | ColQwen2 | Image | 49% | 81% | 94% |
| 8 | Multimodal Hybrid (ColModernVBERT + Arctic 2.0 + BM25) | Hybrid | 49% | 81% | 95% |
| 9 | Hybrid Text Search (Arctic 2.0 + BM25) | Text | 46% | 78% | 91% |
| 10 | ColPali | Image | 45% | 79% | 93% |
| 11 | BM25 | Text | 45% | 71% | 90% |
| 12 | Arctic 2.0 | Text | 44% | 76% | 88% |
| 13 | ColModernVBERT | Image | 43% | 78% | 93% |
| 14 | ColModernVBERT + MUVERA (ef=1024) | Image | 41% | 75% | 88% |
| 15 | ColModernVBERT + MUVERA (ef=512) | Image | 37% | 68% | 78% |
| 16 | ColModernVBERT + MUVERA (ef=256) | Image | 35% | 61% | 66% |

*: Mixedbread is refering to [Mixedbread Stores](https://www.mixedbread.com/docs/quickstart), a search api powered by [Mixedbread Wholembed v3](https://www.mixedbread.com/blog/wholembed-v3). Please find the reproduction script [here](https://gist.github.com/aamir-s18/87c31924679b872b6cd4566edb850089).

## Question Answering Leaderboard 💬

| Rank | System | Type | Alignment Score | Avg Input Tokens | Avg Output Tokens |
|------|--------|------|-----------------|------------------|-------------------|
| 1 | TextRAG (k=5) | Text | 0.82 | 6,022 | 243 |
| 2 | Oracle Text Retrieval (k=1) | Text | 0.74 | 1,294 | 155 |
| 3 | ImageRAG (k=5) | Image | 0.71 | 5,200 | 178 |
| 4 | Oracle Image Retrieval (k=1) | Image | 0.68 | 1,208 | 125 |
| 5 | TextRAG (k=1) | Text | 0.62 | 1,366 | 160 |
| 6 | ImageRAG (k=1) | Image | 0.40 | 1,228 | 124 |
| 7 | Hard Negative Text Context (k=1) | Text | 0.39 | 1,304 | 162 |
| 8 | No Retrieval Baseline | — | 0.16 | 173 | 135 |
| 9 | Hard Negative Image Context (k=1) | Image | 0.12 | 1,233 | 134 |

## Citation
Please consider citing our paper if you find this work useful:

```bibtex
@misc{shorten2026,
      title={IRPAPERS: A Visual Document Benchmark for Scientific Retrieval and Question Answering}, 
      author={Connor Shorten and Augustas Skaburskas and Daniel M. Jones and Charles Pierse and Roberto Esposito and John Trengrove and Etienne Dilocker and Bob van Luijt},
      year={2026},
      eprint={2602.17687},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/pdf/2602.17687}, 
}
```
