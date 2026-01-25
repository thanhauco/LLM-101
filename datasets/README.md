# Datasets

Keep small, reviewable sample datasets here and place large raw or processed datasets in ignored subfolders:

- `datasets/raw`: original documents and exports
- `datasets/processed`: chunked documents, eval sets, and training examples
- `datasets/instruction_samples.jsonl`: small LoRA demo data

Recommended dataset types:

- RAG evals with question, answer, contexts, and ground truth fields
- Instruction tuning records in Alpaca or chat format
- Tool-use traces for agent evaluation
- OCR samples with source image and expected extracted text
