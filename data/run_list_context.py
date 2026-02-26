from typing import Literal, Optional

import pandas as pd
import streamlit as st

import data.df_repository as repo
import states


class RunListContext:
    def __init__(self):
        self.state = states.RunListState()
        self.aggrid_state = states.AgGridState()
        pass


    def get_current_df(self, refresh: bool = False) -> pd.DataFrame:

        if self.state.df is None or refresh:
            self.state.df = repo.get_saved_df()

        return self.state.df

    def change_current_df(self, df: pd.DataFrame, *, reason: Optional[str] = None):
        self.state.change_df(df, reason=reason)

    def is_curren_df_changed(self) -> bool:
        return self.state.is_df_changed

    # TODO: 引数でcsvのみか、各パラメーターファイルも保存するとか？
    #      
    def save_current_df(self, force: bool = False) -> bool:

        # 強制 or 変更フラグが立っているとき保存する
        need_save = force or self.state.is_df_changed
        if not need_save:
            return False
        
        repo.write_df(self.get_current_df())
        
        print("df_changed_reasons = ", self.state.df_changed_reasons)

        self.state.is_df_changed = False
        self.state.df_changed_reasons = None
        return True


    def get_aggrid_df(self) -> pd.DataFrame:

        if self.aggrid_state.df is None:
            self.aggrid_state.df = self.get_current_df()

        # キーがない=グリッドが存在してない状態。
        # 渡すデータの更新と dirty の解消をする。
        if not self.aggrid_state.contains_key():
            self.aggrid_state.df = self.get_current_df()
            self.aggrid_state.is_dirty = False

        return self.aggrid_state.df


    def get_agrid_key(self) -> str:
        return self.aggrid_state.get_key()

    def is_aggird_dirty(self) -> bool:
        return self.aggrid_state.is_dirty

    def mark_aggrid_drity(self) -> None:
        self.aggrid_state.is_dirty = True

    def reload_aggrid(self) -> None:

        # 想定用途：
        # グリッドを dirty から clean にする。
        # グリッドの状態反映に再生成が必要。

        self.aggrid_state.change_key()


    # TODO: キャッシュのクリアってどうしよ。ここでやることではないか？
    #       そもそもキャッシュ事態いらんのか？

    def reload_all(self, *, clear_cache: bool = False):

        if clear_cache:
            repo.get_saved_df.clear()

        del self.state.df
        del self.aggrid_state.df

        self.aggrid_state.change_key()



    
