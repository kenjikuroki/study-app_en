# Source Traceability Policy

StudyApp はすべてのIR・問題・修正案について、根拠資料まで追跡できることを必須とする。

## Trace Flow

question
source_ir_id
IR
source_document_path or source_url
source_section

## Rejection Rules

以下は rejected とする。

- source_ir_id がない問題
- source_document_path / source_url がないIR
- source_section がないIR
- source_last_checked がないIR
- source確認できない問題
- 根拠が曖昧な問題

## Important

Speed is less important than traceability.
If traceability cannot be confirmed, do not approve the item.

## Required Rules

- すべてのIRは `source_document_path` または `source_url` を持つ
- すべてのIRは `source_section` を持つ
- すべての問題は `source_ir_id` を持つ
- すべての問題は `source_ir_id` からIRへ追跡できる
- `source_last_checked` を記録する
- source確認を省略した場合は `skip_reason` を必ず記録する
- 古い資料・バージョン不明資料は `notes` に明記する
- `source_quote_or_summary` は短い要約にする
- 長文引用は禁止
