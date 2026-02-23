import pandas as pd
import streamlit as st

from .session_state_wrapper import SessionStateWrapper


class AgGridState(SessionStateWrapper):
    def __init__(self, prefix: str = "aggrid"):
        super().__init__(prefix)
    
    #region: df property

    @property
    def df(self) -> pd.DataFrame | None:
        return self._get_val("df")

    @df.setter
    def df(self, value: pd.DataFrame | None) -> None:
        self._set_val("df", value)

    @df.deleter
    def df(self) -> None:
        self._del_val("df")

    #endregion

    #region: key

    #region: key_ver property

    @property
    def key_ver(self) -> int:
        return self._get_val("key_ver", 0)

    @key_ver.setter
    def key_ver(self, value: int) -> None:
        self._set_val("key_ver", value)

    @key_ver.deleter
    def key_ver(self) -> None:
        self._del_val("key_ver")

    #endregion

    def get_key(self) -> str:
        return f"{self._prefix}-{self.key_ver}" 

    def change_key(self) -> None:
        self.key_ver += 1

    def contains_key(self) -> bool:
        return self.get_key() in st.session_state

    #endregion

    def get_grid_data(self):
        # st.session_state から AgGrid のキーの値を取得。
        # AgGridReturn が入ってるので、最後の返却データっぽい。
        # だから AgGrid が描画されても None のままの場合がある。
        return st.session_state.get(self.get_key())
