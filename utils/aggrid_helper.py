from collections import defaultdict

import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, AgGridReturn


def get_test_df() -> pd.DataFrame:
    return pd.DataFrame({
        "番号": [1, 2, 3, 4, 5],
        "名前": ["佐藤", "鈴木", "田中", "高橋", "赤城"],
        "業種": ["Technology", "Finance", "Healthcare", "Teacher", "Other"],
        "評価": ["Hot", "Warm", "Cold", "Warm", "Warm"]
    })


def get_grid_options(data) -> defaultdict:
    gb = GridOptionsBuilder.from_dataframe(data)

    gb.configure_default_column(
        editable=True,
        sorteable=True,
        filterable=True,
        filter=True, # ドキュメントに書いてないけど、こっちらしい？
        resizable=True,
    )

    gb.configure_grid_options(rowDragManaged=True)
    gb.configure_column("番号", rowDrag=True)

    # 行選択（複数行選択）を有効化
    gb.configure_selection('single')
    return gb.build()


def render_aggrid(
        df: pd.DataFrame,
        options: dict,
        key: str,
        update_on=["cellValueChanged", "selectionChanged", "filterChanged", "sortChanged", "rowDragEnd"],
) -> AgGridReturn:

    return AgGrid(
        df,
        gridOptions=options,
        height=200,
        data_return_mode=DataReturnMode.AS_INPUT,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        key=key,
        update_on=update_on,
        allow_unsafe_jscode=True,
    )

