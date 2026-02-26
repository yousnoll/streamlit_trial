import typing
import time
import datetime

import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, AgGridReturn
import streamlit as st
import aggrid_test as test

import states
import utils.aggrid_helper as utils
from data.run_list_context import RunListContext


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
        ctx.change_current_df(grid_return.data, reason="cellValueChanged")
        ctx.mark_aggrid_drity()
    elif event_type == "rowDragEnd":
        # NOTE: 行ドラッグによる並び替えは、あくまでグリッド上だけのもの。
        #       だから渡しているデータの再反映的なことが起こると解除されてしまうのか。
        ctx.change_current_df(grid_return.data, reason="rowDragEnd")
        ctx.mark_aggrid_drity()
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


def on_aggrid_callback(event: AgGridReturn) -> None:
    # セルの値を変更し、他行のセルを選択したとき、ちゃんと療法くるっぽい。
    if event.event_data is not None:
        print(event.event_data.get("type"))

    pass

def on_reload_aggrid() -> None:
    ctx = RunListContext()
    ctx.reload_aggrid()


def on_reload_all() -> None:
    ctx = RunListContext()
    ctx.reload_all(clear_cache=True)
        

def on_save_df() -> None:
    ctx = RunListContext()
    ctx.save_current_df()


def on_update_df_value() -> None:
    state = states.AgGridState()
    if state.df is None:
        return
    
    row: int = st.session_state["df_update_row"]
    col: str = st.session_state["df_update_col"]
    val: str = st.session_state["df_update_val"]

    state.df.loc[row, col] = val


def on_sort_df() -> None:
    
    col: str = st.session_state["df_sort_col"]
    dir: str = st.session_state["df_sort_dir"]
    is_asc = dir == "Ascending"
    
    ctx = RunListContext()
    df = ctx.get_current_df()

    sorted_df = df.sort_values(
        by=col,
        ascending=is_asc,
        na_position="last", # NaN の扱い: デフォルト=last で末尾（JSの条件と同じか不明）
        ignore_index=True,  # インデックス降り直し
    )

    ctx.change_current_df(sorted_df)

    if ctx.is_aggird_dirty():
        ctx.reload_aggrid()
    else:
        ctx.aggrid_state.df = None


def render_aggrid(ctx: RunListContext) -> None:
    
    df = ctx.get_aggrid_df()

    # grid_return = utils.render_aggrid(
    #     df,
    #     utils.get_grid_options(df),
    #     ctx.get_agrid_key(),
    #     update_on=[
    #         "cellValueChanged",
    #         "selectionChanged",
    #         "rowDragEnd",
    #     ],
    # )

    grid_return = AgGrid(
        df,
        gridOptions=utils.get_grid_options(df),
        height=200,
        data_return_mode=DataReturnMode.AS_INPUT,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        key=ctx.get_agrid_key(),
        update_on=[
            "cellValueChanged",
            "selectionChanged",
            "rowDragEnd",
        ],
        allow_unsafe_jscode=True,
        callback=on_aggrid_callback,
    )

    _handle_grid_event(grid_return, ctx)

    return grid_return


def render_grid_buttons(ctx: RunListContext) -> None:

    with st.container(horizontal=True):
        st.button("Reload (AgGrid)", on_click=on_reload_aggrid)
        st.button("Reload (All)", on_click=on_reload_all)
        # NOTE: ボタンで保存できるなら、ページ初回時や、処理実行時の保存でもいけるかもしれん。
        st.button("Save", on_click=on_save_df, disabled=not ctx.is_curren_df_changed())

        if st.button("Rerun"):
            st.rerun()


def render_data_prosessing(ctx: RunListContext) -> None:

    df = ctx.get_aggrid_df()

    with st.container(border=True):
        # NOTE: 値変更はもちろん、ソートも問題なくできるっぽい
        st.text("Data Frame Processing")

        df_row_count = len(df)
        df_columns = df.columns

        with st.expander("Update"):
            with st.form(key="df_update_form", enter_to_submit=False):
                with st.container(horizontal=True):
                    max_value = df_row_count - 1 # index なので行数-1が最大値
                    st.number_input("Row", min_value=0, max_value=max_value, value=0, key="df_update_row")
                    st.selectbox("Column", options=df_columns, key="df_update_col")
                    st.text_input("Value", key="df_update_val")

                st.form_submit_button("Apply", on_click=on_update_df_value)

        with st.expander("Sort"):
            with st.form(key="df_sort_form", enter_to_submit=False):
                with st.container(horizontal=True):
                    st.selectbox("Column", options=df_columns, key="df_sort_col")
                    st.radio("Order", options=["Ascending", "Descending"], horizontal=True, key="df_sort_dir")

                st.form_submit_button("Apply", on_click=on_sort_df)


def render_debug_info(ctx: RunListContext, grid_return: AgGridReturn) -> None:

    with st.container(border=True):
        st.text("Debug Information")

        if grid_return.event_data is not None:
            with st.expander("event_data"):
                st.write(grid_return.event_data)

        c1, c2 = st.columns(2)

        with c1:
            with st.expander("Current DataFrame"):
                st.write(ctx.state.df)

        with c2:
            with st.expander("AgGrid DataFrame"):
                st.write(ctx.aggrid_state.df)


def render_fragment_control():
    with st.sidebar:
        st.text("Fragment Control")
        st.checkbox("Active", key="ticks_active")
        st.slider("interval",)
        pass


# @st.fragment(run_every=st.session_state.get("12_ticks_run_every", None))
@st.fragment(run_every=2)
def ticks():
    # そもそもの話、その場じゃなくて、スクリプトの最後あたりで保存処理実行させれば、UIの負荷はそんなでもない？
    dt = datetime.datetime.now()
    print("tick!", dt.strftime("%H:%M:%S.%f"))


def main():
    print("Main")

    st.set_page_config(layout="wide")

    page_state = states.PageState()
    is_first_visit = page_state.visit("page_12")
    if is_first_visit:
        print("最初の時の処理")

    ctx = RunListContext()

    grid_return = render_aggrid(ctx)
    render_grid_buttons(ctx)
    render_data_prosessing(ctx)
    render_debug_info(ctx, grid_return)
    render_fragment_control()

    # NOTE: if で分岐するとダメ。rerun の度呼ばないと実行されないらしい。
    #       これで保存処理実行させる意味なくね？
    #       グリッド部分をフラグメントにして、データ変更とファイル保存を別にする？
    ticks()




if __name__ == "__main__":
    main()
    





