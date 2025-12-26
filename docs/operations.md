# 運用ドキュメント（人間オペレーター向け）

## 目的
- 47都道府県の議会中継／会議録状況をCSVに落とし込む作業を、再現性高く進めるための手順まとめ。
- AIエージェント（Claude Code）のSkill運用と、人間オペレーターの役割分担を明確にする。

## データの原則（READMEの要点）
- 主成果物：`data/prefectures/<code>_<name>/municipalities.csv`
- 列順固定：`prefecture,subprefecture,municipality_type,municipality_name_ja,live_streaming,recorded_streaming,video_platform,video_page_url,minutes_published,minutes_format,minutes_url,latest_minutes_date,notes`
- 値ルール：`YES/NO/UNKNOWN/ToBeInvestigated`（YESなら対応URL必須）
- latest_minutes_date は `YYYY-MM-DD` か `UNKNOWN/ToBeInvestigated`

## 人間オペレーターの標準フロー
1) 対象都道府県のCSVを確認し、`ToBeInvestigated`/`UNKNOWN` 行をピックアップ。
2) Claude Code に Skill を使ったプロンプトを渡し、調査・編集を指示。
3) Claude からの diff/報告をレビューし、必要なら再調査を依頼。
4) `python scripts/validate_csv.py <csv>` を実行し、OK を確認。
5) コミット＆プッシュ。

## Claude Code の Skill 一覧（抜粋）
- `researching-municipal-councils`  
  - CSV編集は Skill 内で実施（Edit/Write/Task）。行順保持、ヘッダー厳守。触る行だけ変更。
  - minutes_* の扱い：YESならURL必須／要約ページは議事録扱いにしない／latest_minutes_dateは日付かUNKNOWN。
  - 作業後に進捗報告：`Progress: XX.X% (completed/total rows) <csv path>`（ToBeInvestigatedでない live/recorded/minutes_published/latest_minutes_date を基準）。
  - 可能なら `python scripts/validate_csv.py <csv>` を実行して結果報告。
- `auditing-yes-no-calls`  
  - YES/NO判定の再確認。NOは複数ルート探索が条件。疑わしければUNKNOWNへ。
- `validating-csv-quality`  
  - スキーマ・値・URL必須チェック。バリデーション結果を報告。

## 推奨プロンプト例（Hokkaido minutes穴埋め）
```
Skill: researching-municipal-councils を使って、
data/prefectures/01_hokkaido/municipalities.csv の minutes_published / minutes_format / minutes_url / latest_minutes_date / notes だけを15件埋めてください。
対象行: 上から「minutes_published が ToBeInvestigated または UNKNOWN」の自治体を15件。
ライブ系列（live_streaming / recorded_streaming / video_*）は原則変更しない。明確な誤りを見つけた場合のみ、notesに理由を明記し最小限修正。

必須ルール:
- CSV編集はスキル内で Edit/Write/Task を使い、行順・ヘッダーを保持。触る行だけ変更・追加。
- minutes_published=YES のとき minutes_url は必ず入口URLを入れる。
- 「会議結果/概要/議会だより」だけなら議事録扱いにしない。notesに「要約のみ」等を明記し、minutes_published は UNKNOWN または NO へ。
- latest_minutes_date は PDF表紙や検索システムの会議日から YYYY-MM-DD を取得。取れなければ UNKNOWN（未調査ではないので ToBeInvestigated に戻さない）。
- 可能なら作業後に `python scripts/validate_csv.py data/prefectures/01_hokkaido/municipalities.csv` を実行し、結果を報告。
- 進捗報告: 完了後に `Progress: XX.X% (completed/total rows) data/prefectures/01_hokkaido/municipalities.csv` を出力（ToBeInvestigated でない4列: live_streaming, recorded_streaming, minutes_published, latest_minutes_date を基準）。

最終出力に含めるもの:
- 実行した変更の要約（該当行の自治体名と minutes_* の変更点）。
- バリデーション結果（OK/エラー）。
- 進捗報告のパーセントと分子/分母。
```

## コミュニケーションのコツ
- AIが大きなCSVをチャットに貼ろうとしたら、「CSVは編集のみ、全文貼り付け禁止」と明示。
- NO判定は慎重に。迷ったらUNKNOWNに倒し、notesに調査経路を書く。
- 外部サイトが動的で日付取得できない場合は UNKNOWN とし、理由を notes に書く。

## 人間のレビュー観点
- YES/NOの根拠URLが妥当か（公式入口を優先）。
- minutes_published=YES で minutes_url が空になっていないか。
- latest_minutes_date の形式が正しいか。UNKNOWNでよいか。
- notes に調査メモが残っているか（NO/UNKNOWNのとき特に）。

## 便利コマンド
- バリデーション: `python scripts/validate_csv.py data/prefectures/01_hokkaido/municipalities.csv`
- 差分確認: `git diff -- data/prefectures/01_hokkaido/municipalities.csv`

