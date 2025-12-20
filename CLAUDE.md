# gyosei-watch / CLAUDE.md

このファイルはClaude Code(Claude Code=AnthropicのCLI型AIエージェント)向けのプロジェクトメモリ(memory=継続指示)だ。このリポジトリは**リサーチ専用**であり、サービス開発はスコープ外だ。

## 0. 目的
全国47都道府県の自治体議会について、以下の公開状況をCSV(CSV=カンマ区切りの表データ)で網羅する。
- 議会中継（生中継・録画）
- 会議録/議事録（議事録=会議の記録。逐語か要約かはnotesに明記）
目的は「将来、議会映像から文字起こし(STT=音声→テキスト変換)できるか」を評価できる土台データを作ること。

## 1. スコープ外（やらないこと）
- Webサービス/アプリの実装
- 常時稼働のクローラ(crawler=自動巡回収集)運用
- 文字起こしそのものの実行（ここでは「入力の所在」の調査に限る）

## 2. データ配置（必須）
都道府県ごとにフォルダを作り、成果物を置く。
- `data/prefectures/<NN_prefecture>/municipalities.csv`
- `data/prefectures/<NN_prefecture>/sources.md`（任意。補助リンクや注意点）

例：
- `data/prefectures/01_hokkaido/municipalities.csv`

## 3. CSVスキーマ（列順固定）
列の追加・削除・並べ替えは禁止。列順は固定。
- prefecture
- subprefecture（振興局等。無い県は空欄でよい）
- municipality_type（市/町/村/区 など）
- municipality_name_ja
- live_streaming
- recorded_streaming
- video_platform
- video_page_url
- minutes_published
- minutes_format
- minutes_url
- latest_minutes_date
- notes

### 3.1 値のルール（最重要）
- `ToBeInvestigated`：未調査で不明
- `UNKNOWN`：調査したが確定できなかった（情報不足/取得失敗/曖昧表示など）
- `YES/NO`：根拠がある場合のみ。推測で入れない
- `YES`を入れたら、対応するURL(URL=ウェブ上の住所)を必ず埋める（空欄禁止）
  - 動画なら `video_page_url`
  - 議事録なら `minutes_url`
- `latest_minutes_date`は `YYYY-MM-DD`。取れないなら`UNKNOWN`。未調査なら`ToBeInvestigated`

### 3.2 「NO」判定の注意
「無い」判定が一番間違いやすい。最低でも以下を確認してからNOにする。
- 公式サイト内で「議会」「議会中継」「会議録」「議事録」「会議録検索」を探す
- 検索エンジンで「<自治体名> 議会 中継」「<自治体名> 会議録」を探す
それでも見つからない場合のみNOにし、notesに「確認した導線」を短く書く。

## 4. リサーチ手順（標準）
1) 公式サイトの「議会」配下を優先して探索（入口URLを取る）
2) 見つからなければ公式サイトのサイト内検索、または検索エンジンで探索
3) YouTube(YouTube=動画プラットフォーム)が出た場合も、可能なら公式サイト側の案内ページを入口URLに採用する（再現性が高い）
4) 「会議結果（要点だけ）」と「会議録（発言ベース）」を混同しない
   - 要点のみなら `minutes_published=UNKNOWN` か `NO` に倒し、notesに「要点のみ」等を明記（逐語でないことを記録）
5) 取得できた範囲をnotesに書く（例：一般質問のみ/委員会のみ/期間限定公開 など）

## 5. 出力（作業完了の定義）
作業対象の自治体について、少なくとも以下を満たす。
- 動画（live/recorded）をYES/NO/UNKNOWNに確定し、入口URLを1つ以上確保
- 議事録（minutes_*）をYES/NO/UNKNOWNに確定し、入口URLを1つ以上確保
- 不確定ならUNKNOWNにして理由をnotesに残す（推測で埋めない）

## 6. PR/コミット運用（推奨）
- 1PR(PR=Pull Request。変更提案)は「1都道府県」か「まとまりの自治体群」に限定
- PR本文に「更新した自治体名」「変更点」「根拠URLの代表」を書く
- diff(diff=差分)が読みやすいよう、CSVの列順と行順を勝手に並べ替えない

## 7. 倫理・法務（必須）
- 公式情報を優先する
- 規約違反のスクレイピング(scraping=無差別自動収集)や過剰アクセスをしない
- 個人情報(個人情報=個人を特定し得る情報)を新規に収集・保存しない
- ログイン必須/有料/転載サイトは原則参照しない（参照せざるを得ない場合はnotesに明記し、公式導線の有無も書く）

## 8. 迷ったときの判断基準（簡易）
- 迷ったらUNKNOWN（断定しない）
- 「入口URLが取れないYES」はしない
- 「見当たらない」だけでNOにしない（確認導線を2〜3本）
