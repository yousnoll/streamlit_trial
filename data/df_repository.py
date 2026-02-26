import io
import os
import pathlib
from typing import Final

import pandas as pd
import streamlit as st
from streamlit import config

import states
import utils.aggrid_helper as utils


# NOTE: RunListデータフレームをファイルから読み書きするイメージ
#       実際にやるのがめんどうなので st.session_state を使う。


# TODO: キャッシュするべきか？

def get_file_path() -> str:
    dir = os.path.dirname(__file__)
    return os.path.join(dir, "datafarame.csv")


def read_df() -> pd.DataFrame:

    path = get_file_path()

    print(f"Read dataframe (path={path})")

    if os.path.exists(path):
        df = pd.read_csv(path, index_col="index")
    else:
        df = utils.get_test_df()
        write_df(df)

    return df


@st.cache_data()
def get_saved_df() -> pd.DataFrame:
    return read_df()


def write_df(df: pd.DataFrame):

    path = get_file_path()

    df.index.name = "index"
    df.to_csv(path)

    print(f"Write dataframe (path={path})")
    print(df)
