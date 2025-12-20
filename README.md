# gyosei-watch
This directory contains research for evaluating a service that monitors local government assemblies in Japan.

# gyosei-watch

自治体議会の「中継・会議録（議事録=会議の記録）」公開状況を、全国47都道府県ぶん網羅していくためのリサーチ専用リポジトリだ。  
目的は、政治・行政の情報コストを下げ、誰でも短時間で「いま何が議論されているか」に到達できる土台データを整備することにある。

## このリポジトリでやること
- 都道府県ごとに、市区町村の議会情報を調査してCSV（CSV=カンマ区切りの表データ）に蓄積する
- 調査結果を再現可能にするため、根拠URL（URL=ウェブ上の住所）とメモを残す
- AIエージェント（AIエージェント=自動で調査や更新を行うプログラム）での並列リサーチを前提に、形式・ルール・検証を整える

## やらないこと（スコープ外）
- Webサービス／アプリケーションの開発
- クローラ（crawler=自動巡回収集）による大規模自動収集の常時運用
- 文字起こし（STT=音声→テキスト変換）そのものの実行基盤構築

---

## データの考え方
「議会の文字起こしを将来できるか」を左右するのは、ざっくり次の2点だ。
1) 動画に到達できるか（生中継/録画/プラットフォーム）  
2) 会議録に到達できるか（公開有無/形式/最新性）

このリポジトリは、まずここを確実に押さえる。

---

- `municipalities.csv` が主成果物
- `sources.md` は補助（補足URL、サイト構造メモ、注意点など）
- `prompts/` はCLI（CLI=コマンドライン操作）型エージェントに渡す指示書のテンプレ
- `scripts/` は検証や集計の補助

---

## CSVスキーマ（schema=列定義）
基本列は以下。列順は固定にする。

| column | meaning |
|---|---|
| prefecture | 都道府県 |
| subprefecture | 振興局/総合振興局など（無い県は空でよい） |
| municipality_type | 市/町/村/区 など |
| municipality_name_ja | 自治体名（日本語） |
| live_streaming | 生中継の有無（YES/NO/UNKNOWN/ToBeInvestigated） |
| recorded_streaming | 録画公開の有無（YES/NO/UNKNOWN/ToBeInvestigated） |
| video_platform | YouTube/公式サイト/その他/UNKNOWN/ToBeInvestigated |
| video_page_url | 動画入口URL |
| minutes_published | 会議録公開の有無（YES/NO/UNKNOWN/ToBeInvestigated） |
| minutes_format | PDF/HTML/検索システム/UNKNOWN/ToBeInvestigated |
| minutes_url | 会議録入口URL |
| latest_minutes_date | 本会議の最新日付（YYYY-MM-DD / UNKNOWN / ToBeInvestigated） |
| notes | 例外・範囲・注意（「一般質問のみ」「委員会のみ」など） |

### 値のルール（最重要）
- `ToBeInvestigated` = 未調査で不明
- `UNKNOWN` = 調査したが確定できなかった（情報不足、取得失敗、曖昧表示など）
- `YES/NO` は根拠があるときだけ
- `YES` の場合は、対応する `*_url` を必ず埋める（空欄禁止）

---

## リサーチ手順（標準）
1. 公式サイト内で「議会」「議会中継」「会議録」「議事録」「会議録検索」を探索
2. 見つからなければ検索エンジンで  
   - 「<自治体名> 議会 インターネット中継」  
   - 「<自治体名> 会議録 検索」  
   - 「site:<自治体ドメイン> 議会 中継」
3. YouTubeが出た場合も、可能なら公式サイト側の案内ページを入口URLに採用する（再現性が高い）
4. 「会議結果（要点だけ）」と「会議録（発言ベース）」を混同しない  
   - 逐語（逐語=発言単位）でない場合は `notes` に明記

---

## AIエージェントでの進め方（推奨）
### 役割分離
- 調査役：CSVを埋める
- 監査役：YES/NO行だけ再チェックする（特にNO判定を重点）

### 二重化が難しい場合の最低ライン
- 都道府県ごとにランダム10%を抜き取り監査（sampling=抜き取り検査）
- NO判定は「導線を2〜3本確認してから」に限定

---

## 検証（CI=自動検査）
GitHub Actions（GitHub Actions=GitHub上の自動実行）などで、最低限これを落とすのが望ましい。

- 列が揃っている
- 値が `YES/NO/UNKNOWN/ToBeInvestigated` のいずれか
- `YES` なのにURLが空欄になっていない
- `latest_minutes_date` が `YYYY-MM-DD` か `UNKNOWN/ToBeInvestigated` になっている

---

## コントリビュート（contribute=参加）
PR（PR=変更提案の提出）歓迎。差分（diff=変更箇所）レビューしやすいよう、次を守る。

- 1PRは1都道府県、または1まとまりの自治体群に限定
- 更新した自治体名と変更点の要約をPR本文に書く
- 根拠URLとnotesを必ず残す
- 迷ったらUNKNOWNに倒す（断定しない）

---

## 倫理・法務
- 公式情報を優先する
- 規約違反の自動収集や過剰アクセスをしない
- 個人情報（個人情報=個人を特定し得る情報）を新規に収集・保存しない
- 判断に迷う場合はUNKNOWNにし、notesで状況を書く

---

## ライセンス
- コード：MIT License（MIT=緩い利用許諾）
- データ（CSV）：（ここは決め次第追記。例：CC BY 4.0 など）

---

## ステータス
このリポジトリは「調査の完遂」を第一のマイルストーンとする。  
各都道府県フォルダにCSVが存在し、全自治体の `ToBeInvestigated` が解消され、検証が通っている状態を完了とみなす。
