from typing import Optional

import pandas as pd

from .session_state_wrapper import SessionStateWrapper


# 最新のデータフレームを扱うイメージ
class RunListState(SessionStateWrapper):
    def __init__(self, prefix: str = "run_list"):
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

    #region: is_df_changed property

    @property
    def is_df_changed(self) -> bool:
        return self._get_val("is_df_changed", False)

    @is_df_changed.setter
    def is_df_changed(self, value: bool) -> None:
        self._set_val("is_df_changed", value)

    @is_df_changed.deleter
    def is_df_changed(self) -> None:
        self._del_val("is_df_changed")

    #endregion

    #region: df_changed_reasons property

    @property
    def df_changed_reasons(self) -> Optional[set[str]]:
        return self._get_val("df_changed_reasons")

    @df_changed_reasons.setter
    def df_changed_reasons(self, value: Optional[set[str]]) -> None:
        self._set_val("df_changed_reasons", value)

    @df_changed_reasons.deleter
    def df_changed_reasons(self) -> None:
        self._del_val("df_changed_reasons")

    #endregion

    # TODO: これ単純にフラグじゃなくて、セル編集とドラッグで持たせていた方がいいかも？
    #       ドラッグだけなら融通利く

    def change_df(self, df: pd.DataFrame, *, reason: Optional[str] = None):
        self.df = df
        self.is_df_changed = True

        if reason is None:
            return
        
        if self.df_changed_reasons is None:
            self.df_changed_reasons = {reason}
        else:
            self.df_changed_reasons.add(reason)

