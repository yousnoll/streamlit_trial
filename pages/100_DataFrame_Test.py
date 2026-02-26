import pandas as pd
import streamlit as st


def get_dataframe1() -> pd.DataFrame:
    return pd.DataFrame([
        ["E011", "佐藤 太郎", 28, "営業部", "2020-04-01"],
        ["E002", "鈴木 花子", 32, "総務部", "2018-10-15"],
        ["E013", "高橋 健", 41, "開発部", "2015-07-20"],
        ["E004", "田中 美咲", 29, "営業部", "2021-01-05"],
        ["E005", "伊藤 翼", 35, "開発部", "2017-03-12"],
    ], columns=["社員ID", "氏名", "年齢", "部署", "入社日"])


def get_dataframe2() -> pd.DataFrame:
    return pd.DataFrame([
        ["E001", "佐藤 太郎", 28, "営業部", "2020-04-01"],
        ["E002", "鈴木 花子", 32, "総務部", "2018-10-15"],
        ["E003", "高橋 健", 41, "開発部", "2015-07-20"],
        ["E004", "田中 美咲", 29, "営業部", "2021-01-05"],
        ["E005", "伊藤 翼", 35, "開発部", "2017-03-12"],
    ], columns=["社員ID", "氏名", "年齢", "部署", "入社日"])


def get_changed_index(df: pd.DataFrame, compare_to: pd.DataFrame):
    return df.index[get_changed_mask(df, compare_to)]


def get_changed_mask(df: pd.DataFrame, compare_to: pd.DataFrame):
    # df 基準に変化があったもののmaskを得る。
    # その前に df 基準に compare_to を揃える
    # ここにモデルの列にしたものを渡せば、全行列挙しなくてもいいのでは？
    compare_to = compare_to.reindex(index=df.index)

    return (df != compare_to).any(axis=1)


def main() -> None:

    st.button("Rerun")

    df1 = get_dataframe1()
    df2 = get_dataframe2()
    sorted_df = df2.sort_values("年齢")

    with st.container(horizontal=True):
        
        st.write(df1)
        st.write(df2)
        st.write(sorted_df)

        changed_index = get_changed_index(df1, sorted_df.sort_index())
        st.write(changed_index)

        mask = get_changed_mask(df1, sorted_df.sort_index())
        rows = df1.loc[mask]
        st.write(rows)

    # 一部列の抜き出し
    with st.container(horizontal=True):
        a = df1.loc[:, ["氏名", "年齢"]] # loc の場合、ちゃんと行と列を指定する必要がある
        st.write(a)

        b = sorted_df[["氏名", "年齢"]] # こっちはいい感じにしてくれる
        st.write(b)

        # a.compare

        

    pass


if __name__ == "__main__":
    main()
