import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt


# 保存するCSVファイルの名前
FILE_NAME = "kakeibo.csv"


# グラフで日本語を表示するための設定
plt.rcParams["font.family"] = "Noto Sans CJK JP"


# CSVファイルがなければ、新しく作る関数
def create_file():

    if not os.path.exists(FILE_NAME):

        with open(
            FILE_NAME,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "日付",
                "種類",
                "カテゴリ",
                "金額",
                "メモ"
            ])


# 家計簿を入力する関数
def input_data():

    print("")
    print("===== 家計簿を入力 =====")

    date = input("日付を入力してください（例：2026-07-31）：")

    while True:

        print("1. 収入")
        print("2. 支出")

        type_number = input("種類を選んでください：")

        if type_number == "1":
            record_type = "収入"
            break

        elif type_number == "2":
            record_type = "支出"
            break

        else:
            print("1または2を入力してください。")

    category = input("カテゴリを入力してください：")

    while True:

        amount_text = input("金額を入力してください：")

        try:
            amount = int(amount_text)

            if amount <= 0:
                print("1円以上の金額を入力してください。")
                continue

            break

        except ValueError:
            print("金額は数字で入力してください。")

    memo = input("メモを入力してください：")

    with open(
        FILE_NAME,
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            date,
            record_type,
            category,
            amount,
            memo
        ])

    print("")
    print("家計簿に保存しました。")


# 一覧を表示する関数
def show_list():

    print("")
    print("===== 家計簿一覧 =====")

    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)
        data_list = list(reader)

    if len(data_list) == 0:
        print("まだデータがありません。")
        return

    for number, row in enumerate(data_list, start=1):

        print("")
        print("番号：", number)
        print("日付：", row["日付"])
        print("種類：", row["種類"])
        print("カテゴリ：", row["カテゴリ"])
        print("金額：", row["金額"], "円")
        print("メモ：", row["メモ"])

# 家計簿データを1件ずつ削除する関数
def delete_data():

    print("")
    print("===== データを削除 =====")

    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)
        data_list = list(reader)

    if len(data_list) == 0:
        print("削除できるデータがありません。")
        return

    # データを番号付きで表示
    for number, row in enumerate(data_list, start=1):

        print("")
        print("番号：", number)
        print("日付：", row["日付"])
        print("種類：", row["種類"])
        print("カテゴリ：", row["カテゴリ"])
        print("金額：", row["金額"], "円")
        print("メモ：", row["メモ"])

    print("")

    while True:

        delete_number = input(
            "削除したいデータの番号を入力してください："
        )

        try:
            delete_number = int(delete_number)

            if 1 <= delete_number <= len(data_list):
                break

            else:
                print("正しい番号を入力してください。")

        except ValueError:
            print("数字を入力してください。")

    # 選んだデータを削除
    deleted_data = data_list.pop(delete_number - 1)

    # CSVファイルを書き直す
    with open(
        FILE_NAME,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "日付",
                "種類",
                "カテゴリ",
                "金額",
                "メモ"
            ]
        )

        writer.writeheader()
        writer.writerows(data_list)

    print("")
    print(
        deleted_data["日付"],
        deleted_data["カテゴリ"],
        deleted_data["金額"] + "円",
        "を削除しました。"
    )
# 収入・支出・残高を表示する関数
def show_total():

    income = 0
    expense = 0

    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:
                amount = int(row["金額"])

            except ValueError:
                continue

            if row["種類"] == "収入":
                income += amount

            elif row["種類"] == "支出":
                expense += amount

    balance = income - expense

    print("")
    print("===== 収支の合計 =====")
    print("収入：", income, "円")
    print("支出：", expense, "円")
    print("残高：", balance, "円")


# 収入と支出のグラフを表示する関数
def show_income_expense_graph():

    income = 0
    expense = 0

    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:
                amount = int(row["金額"])

            except ValueError:
                continue

            if row["種類"] == "収入":
                income += amount

            elif row["種類"] == "支出":
                expense += amount

    if income == 0 and expense == 0:
        print("グラフに表示できるデータがありません。")
        return

    labels = []
    sizes = []

    if income > 0:
        labels.append("収入")
        sizes.append(income)

    if expense > 0:
        labels.append("支出")
        sizes.append(expense)

    plt.figure(figsize=(6, 6))

    plt.pie(
    sizes,
    labels=labels,
    autopct=lambda p: f"{int(p * sum(sizes) / 100):,}円",
    startangle=90
)

    plt.title("収入と支出の割合")

    # 円をきれいな丸にする
    plt.axis("equal")

    plt.savefig("income_expense.pdf")
    plt.savefig("income_expense.png")
    plt.close()


# カテゴリ別支出のグラフを表示する関数
def show_category_graph():

    category_data = defaultdict(int)

    with open(
        FILE_NAME,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["種類"] == "支出":

                try:
                    amount = int(row["金額"])

                except ValueError:
                    continue

                category_data[row["カテゴリ"]] += amount

    if len(category_data) == 0:
        print("支出データがありません。")
        return

    labels = list(category_data.keys())
    sizes = list(category_data.values())

    plt.figure(figsize=(7, 7))

    plt.pie(
    sizes,
    labels=labels,
    autopct=lambda p: f"{int(p * sum(sizes) / 100):,}円",
    startangle=90
)

    plt.title("カテゴリ別支出")

    # 円をきれいな丸にする
    plt.axis("equal")

    plt.savefig("category_expense.pdf")
    plt.savefig("category_expense.png")
    plt.close()


# グラフメニューを表示する関数
def show_graph_menu():

    while True:

        print("")
        print("===== グラフメニュー =====")
        print("1. 収入と支出の円グラフ")
        print("2. カテゴリ別支出の円グラフ")
        print("3. メインメニューに戻る")

        choice = input("番号を入力してください：")

        if choice == "1":
            show_income_expense_graph()

        elif choice == "2":
            show_category_graph()

        elif choice == "3":
            break

        else:
            print("1から3の番号を入力してください。")

# メインメニューを表示する関数
def main():

    create_file()

    while True:

        print("")
        print("===== 家計簿アプリ =====")
        print("1. 家計簿を入力")
        print("2. 一覧を見る")
        print("3. 収入・支出・残高を見る")
        print("4. グラフを見る")
        print("5. データを1件削除")
        print("6. 終了")

        choice = input("番号を入力してください：")

        if choice == "1":
            input_data()

        elif choice == "2":
            show_list()

        elif choice == "3":
            show_total()

        elif choice == "4":
            show_graph_menu()

        elif choice == "5":
            delete_data()

        elif choice == "6":
            print("家計簿アプリを終了します。")
            break

        else:
            print("1から6の番号を入力してください。")


# このファイルを実行したときにmain関数を動かす
if __name__ == "__main__":
    main()