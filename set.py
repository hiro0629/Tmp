import sys
import pandas as pd

# コマンドライン引数を取得（スクリプト名は sys.argv[0] に入る）
if len(sys.argv) < 2:
    print("ファイル名を指定してください")
    sys.exit(1)

filename = sys.argv[1]

col_remove=[
"受渡日","銘柄コード","限月","コールプット区分","権利行使価格","権利行使価格通貨","カバードワラント商品種別","通貨","受渡通貨","市場","口座","信用区分","コンバージョンレート","手数料","手数料消費税","新規手数料","新規手数料消費税","管理費","名義書換料","金利","貸株料","品貸料","前日分値洗","経過利子（円貨）","経過利子（外貨）","経過日数（外債）","所得税（外債）","地方税（外債）","金利・価格調整額（CFD）","配当金調整額（CFD）","売建単価（くりっく365）","買建単価（くりっく365）","円貨スワップ損益","外貨スワップ損益","約定金額（円貨）","約定金額（外貨）","決済金額（外貨）","実現損益（円貨）","実現損益（外貨）","実現損益（円換算額）","受渡金額（外貨）","備考"
]

# CSVファイルを読み込む
df = pd.read_csv(filename)

# 複数の列を削除（リストで指定）
df = df.drop(columns=col_remove)

# "決済金額（円貨）"と "受渡金額（円貨）"の値が同じ行だけを残す（違う行を削除）
df = df[df["決済金額（円貨）"] == df["受渡金額（円貨）"]]

# "受渡金額（円貨）"カラムの削除
df = df.drop(columns="受渡金額（円貨）")

# column name to english
new_col_name = [
"date_time","trade_category","trade_id","currency_pair","bid_ask","executed_amount","executed_price","entry_price","profit_loss"
]
df.columns = new_col_name

# trade_category column as Eng
df.loc[df["trade_category"] == "FXネオ新規", "trade_category"] = "entry"
df.loc[df["trade_category"] == "FXネオ決済", "trade_category"] = "exit"
df.loc[df["trade_category"] == "FXネオスワップ", "trade_category"] = "swap"
# currency_pai remove slash
df["currency_pair"] = df["currency_pair"].str.replace("/", "", regex=False)
# bid_ask column as Eng
df.loc[df["bid_ask"] == "買", "bid_ask"] = "buy"
df.loc[df["bid_ask"] == "売", "bid_ask"] = "sell"

# データ型を一括変換
df["date_time"] = pd.to_datetime(df["date_time"])  # object → datetime
df["trade_id"] = df["trade_id"].astype(int)  # float → int

newfilename = "setup.csv"
# 新しいCSVファイルとして保存
df.to_csv(newfilename, index=False)

