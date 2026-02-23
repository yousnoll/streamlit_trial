import typing

import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, AgGridReturn
import streamlit as st
import aggrid_test as test

import states
import utils.aggrid_helper as utils
from data.run_list_context import RunListContext

PAGE_ID: typing.Final[str] = "10"

st.set_page_config(layout="wide")

page_state = states.PageState()
if page_state.first_time(PAGE_ID):
    print("最初の時の処理")


def _render_aggrid_with_state(state: states.AgGridState):
    
    return utils.render_aggrid(
        state.df,
        utils.get_grid_options(state.df),
        state.get_key(),
        update_on=[
            "cellValueChanged",
            "selectionChanged",
            "sortChanged",
            "rowDragEnd",
        ] 
    )


def _handle_grid_event(grid_return: AgGridReturn, ctx: RunListContext):
    # イベントの処理関数

    if grid_return.event_data is None:
        return

    event_type = grid_return.event_data.get("type")

    # TODO: イベント内容に従ってデータフレームを更新する。
    #       AgGrid に渡すものは変更しない。反映されない、再度アニメーションされたりする。

    # NOTE: セル編集は行の情報もあるので、その都度ファイル保存が可能かも？

    if event_type == "cellValueChanged":
        # NOTE: パラメーターファイルの保存タイミングとしても使えそう
        ctx.state.change_df(grid_return.data, reason="cellValueChanged")
    elif event_type == "rowDragEnd":
        # NOTE: 行ドラッグによる並び替えは、あくまでグリッド上だけのもの。
        #       だから渡しているデータの再反映的なことが起こると解除されてしまうのか。
        ctx.state.change_df(grid_return.data, reason="rowDragEnd")
    elif event_type == "sortChanged":
        # TODO: 多分利用しないけど、一応残しておく
        # 見た目上なので、ソートだけでなく、フィルターも影響を受けてしまう。
        # reindex_ids = grid_return.rows_id_after_sort_and_filter
        # reindex_ids = pd.Index(reindex_ids)
        # data = grid_return.data.reindex(index=reindex_ids).reset_index(drop=True)

        print("**sortChanged**")

        # NOTE: とりあえずソート情報を取り出す処理だけ
        #       これでソートの有無と、対象の列と並び順が得られる。
        cs = grid_return.columns_state
        sort_col_state = next((cstate for cstate in cs if cstate.get("sort") is not None), None)

        if sort_col_state is not None:
            keys = ["colId", "sort"]
            small_dict = {k: sort_col_state[k] for k in keys if k in sort_col_state}
            print("sort_col_state = ", small_dict)
        else:
            print("sort_col_state = ", None)


run_list_ctx = RunListContext()
aggrid_df = run_list_ctx.get_aggrid_df()
aggrid_state = run_list_ctx.aggrid_state

grid_return = _render_aggrid_with_state(aggrid_state)

_handle_grid_event(grid_return, run_list_ctx)


with st.container(horizontal=True):
    st.button("Reload (AgGrid)", on_click=run_list_ctx.reload_aggrid)
    st.button("Reload (All)", on_click=run_list_ctx.reload_all)
    # NOTE: ボタンで保存できるなら、ページ初回時や、処理実行時の保存でもいけるかもしれん。
    st.button("Save", on_click=run_list_ctx.save_current_df, disabled=not run_list_ctx.state.is_df_changed)

    if st.button("Rerun"):
        st.rerun()


# region: コード上でのDF変更

def update_df_value() -> None:
    state = states.AgGridState()
    if state.df is None:
        return
    
    row: int = st.session_state["df_update_row"]
    col: str = st.session_state["df_update_col"]
    val: str = st.session_state["df_update_val"]

    state.df.loc[row, col] = val


def sort_df() -> None:
    state = states.AgGridState()
    if state.df is None:
        return
    
    col: str = st.session_state["df_sort_col"]
    dir: str = st.session_state["df_sord_dir"]
    is_asc = dir == "Ascending"

    state.df.sort_values(
        by=col,
        ascending=is_asc,
        na_position="last", # NaN の扱い: デフォルト=last で末尾（JSの条件と同じか不明）
        ignore_index=True,  # インデックス降り直し
        inplace=True,       # 元オブジェクトを変更
    )

with st.container(border=True):
    # NOTE: 値変更はもちろん、ソートも問題なくできるっぽい
    st.text("Data Frame Processing")

    df_row_count = len(aggrid_df)
    df_columns = aggrid_df.columns

    with st.expander("Update"):
        with st.form(key="df_update_form", enter_to_submit=False):
            with st.container(horizontal=True):
                max_value = df_row_count - 1 # index なので行数-1が最大値
                st.number_input("Row", min_value=0, max_value=max_value, value=0, key="df_update_row")
                st.selectbox("Column", options=df_columns, key="df_update_col")
                st.text_input("Value", key="df_update_val")

            st.form_submit_button("Apply", on_click=update_df_value)

    with st.expander("Sort"):
        with st.form(key="df_sort_form", enter_to_submit=False):
            with st.container(horizontal=True):
                st.selectbox("Column", options=df_columns, key="df_sort_col")
                st.radio("Order", options=["Ascending", "Descending"], horizontal=True, key="df_sord_dir")

            st.form_submit_button("Apply", on_click=sort_df)


# endregion

# region: デバッグ用の情報表示

with st.container(border=True):
    st.text("Debug Information")

    if grid_return.event_data is not None:
        with st.expander("event_data"):
            st.write(grid_return.event_data)

    c1, c2 = st.columns(2)

    with c1:
        with st.expander("Current DataFrame"):
            st.write(run_list_ctx.state.df)

    with c2:
        with st.expander("AgGrid DataFrame"):
            st.write(run_list_ctx.aggrid_state.df)

# endregion