import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, simpledialog
import io

# Tkinterのルートウィンドウを隠す
root = Tk()
root.withdraw()

# ファイルダイアログを使ってExcelファイルを選択
file_path = filedialog.askopenfilename(title='Excelファイルを選択してください', filetypes=[('Excel files', '*.xlsx *.xls')])

if not file_path:
    print("ファイルが選択されませんでした。プログラムを終了します。")
    exit()

# Excelファイルのシート名を取得
with open(file_path, 'rb') as file:
    xls = pd.ExcelFile(io.BytesIO(file.read()))
available_sheets = xls.sheet_names

print(f"利用可能なシート名: {available_sheets}")

# ユーザーにシート名のリストを入力させる
def get_sheet_names():
    sheet_names = []
    for i in range(num_sheets):
        while True:
            sheet_name = input(f'{i+1}つ目のシート名を入力してください (戻るには "back" と入力): ')
            if sheet_name == 'back':
                return None
            if sheet_name in available_sheets:
                sheet_names.append(sheet_name)
                break
            else:
                print(f"エラー: シート名 '{sheet_name}' は存在しません。もう一度入力してください。")
    return sheet_names

while True:
    num_sheets = int(input('シートの数を入力してください: '))
    sheet_names = get_sheet_names()
    if sheet_names is not None:
        break

# データフレームとしてExcelファイルを読み込む
dfs = pd.read_excel(file_path, sheet_name=sheet_names)

# 各シートのカラム名を表示
for sheet_name, df in dfs.items():
    print(f"\nシート '{sheet_name}' のカラム名: {df.columns.tolist()}")

# 入力履歴を保存するためのリスト
input_history = []

def input_with_back(prompt, previous_value=None):
    while True:
        user_input = input(prompt)
        if user_input == 'back':
            if input_history:
                return input_history.pop()
            else:
                print("戻る操作はできません。最初の入力です。")
                continue
        input_history.append(user_input)
        return user_input

# ユーザーにカラム名を入力させる
x_column = input_with_back('X軸のカラム名を入力してください: ')
y_column = input_with_back('Y軸のカラム名を入力してください: ')

# ユーザーに軸ラベルを入力させる
x_label = input_with_back('X軸のラベルを入力してください: ')
y_label = input_with_back('Y軸のラベルを入力してください: ')

# Tkinterのメインループを更新
root.update()

# ユーザーにグラフのタイトルを入力させる
title = simpledialog.askstring("Input", "グラフのタイトルを入力してください:")

# グラフの作成
plt.figure(figsize=(10, 6))

# 各シートのデータをプロット
for sheet_name, df in dfs.items():
    x = df[x_column]
    y = df[y_column]
    plt.plot(x, y, marker='o', linestyle='-', label=sheet_name)

# 軸ラベルの設定
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title)

# グリッドの表示
plt.grid(True)

# 凡例の表示
plt.legend()

# グラフの表示
plt.show()

# Tkinterのメインループを終了
root.destroy()
