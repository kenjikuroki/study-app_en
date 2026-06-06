# StudyApp

資格アプリ・暗記アプリ向けの問題作成・監査システムです。

## 目的

- 問題作成
- 問題監査
- 古い問題の検出
- 修正案作成
- 承認済み修正の反映
- ソース資料管理
- ログ管理
- バックアップ管理

## 拡張方法

資格アプリが増える場合は、以下にアプリIDごとのフォルダを追加します。

apps/active_apps/{app_id}/

例：

apps/active_apps/unkou_ryokaku/
apps/active_apps/drone_2nd/
apps/active_apps/boiler_2nd/

各アプリフォルダには、app_config.json と questions.json を配置します。

## 基本フロー

1. sources に公式資料や参考資料を格納
2. questions.json に既存問題を格納
3. question_creator が不足問題を作成
4. question_auditor が問題を監査
5. revision_creator が修正案を作成
6. 人間が approved_revisions に承認済み修正を配置
7. revision_applier が questions.json に反映
8. validate_questions と shuffle_questions を実行
9. final_questions に完成版を出力
10. backups と logs に履歴を保存

## 注意

夜間監査エージェントは本番 questions.json を直接変更しないでください。
修正反映は、人間が承認した approved_revisions のみを対象にしてください。
