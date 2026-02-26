import typing
from dataclasses import dataclass, asdict

import streamlit as st

import states
import utils.aggrid_helper as utils
from data.run_list_context import RunListContext


PAGE_ID: typing.Final[str] = "11"

st.set_page_config(layout="wide")

page_state = states.PageState()
if page_state.visit(PAGE_ID):
    print("最初の時の処理")

st.button("rerun")


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

run_list_ctx = RunListContext()
aggrid_df = run_list_ctx.get_aggrid_df()
aggrid_state = run_list_ctx.aggrid_state

grid_return = _render_aggrid_with_state(aggrid_state)