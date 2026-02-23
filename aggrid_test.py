import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import streamlit as st

GRID_KEY = 'grid_key'

def get_test_df() -> pd.DataFrame:
    return pd.DataFrame({
        "名前": ["佐藤", "鈴木", "田中"],
        "業種": ["Technology", "Finance", "Healthcare"],
        "評価": ["Hot", "Warm", "Cold"]
    })

def get_grid_options(data) -> dict:
    gb = GridOptionsBuilder.from_dataframe(data)

    gb.configure_default_column(
        editable=True,
        sorteable=True,
        filterable=True,
        resizable=True,
    )

    gb.configure_grid_options(rowDragManaged=True)
    gb.configure_column("名前", rowDrag=True)

    # 行選択（複数行選択）を有効化
    gb.configure_selection('single')
    return gb.build()

def render(data, update_on=["cellValueChanged", "selectionChanged", "filterChanged", "sortChanged", "rowDragEnd"]):

    opts = get_grid_options(data)

    resp = AgGrid(
        data,
        gridOptions=opts,
        height=200,
        data_return_mode=DataReturnMode.AS_INPUT,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        key=GRID_KEY,
        update_on=update_on,
    )

    return resp
