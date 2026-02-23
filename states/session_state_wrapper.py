from typing import Any, Optional

import streamlit as st


class SessionStateWrapper:
    def __init__(self, prefix: str):
        self._prefix = prefix
        pass

    def _get_full_key(self, key: str) -> str:
        return f"{self._prefix}__state__{key}"

    def _get_val(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        return st.session_state.get(self._get_full_key(key), default)
    
    def _set_val(self, key: str, value: Optional[Any]) -> None:
        st.session_state[self._get_full_key(key)] = value

    def _del_val(self, key: str) -> None:
        st.session_state.pop(self._get_full_key(key), None)