from typing import Literal

import pandas as pd
import streamlit as st

import data.df_repository as repo
import states


# TODO: 良い名前を思いついてない。
#       多分データフレーム管理に特化するイメージなんだけど、単純に RunListのデータフレームだと内を指してるのかわかんねぇよなぁ
#       UIも扱うしデータも扱うしで困るな
#       これこそ component なのか？

# それとも各 state を更にラップする？
# ん？ ViewModel なのでは？
# Presenter
# Proxy とかもあり？
# Manager
# Facade
# Facade は結構いい感じ？あとは無難に Manager か

class RunListContext:
    def __init__(self):
        self.state = states.RunListState()
        self.aggrid_state = states.AgGridState()
        pass


    def get_current_df(self, refresh: bool = False) -> pd.DataFrame:

        if self.state.df is None or refresh:
            self.state.df = repo.get_saved_df()

        return self.state.df


    def get_aggrid_df(self) -> pd.DataFrame:

        if self.aggrid_state.df is None:
            self.aggrid_state.df = self.get_current_df()

        # グリッド生成時に現在のデータグリッドに反映させる。
        # 
        if not self.aggrid_state.contains_key():
            self.aggrid_state.df = self.get_current_df()

        return self.aggrid_state.df


    def reload_aggrid(self):

        # 想定用途：
        # グリッドを dirty から clean にする。
        # グリッドの状態反映に再生成が必要。
        
        # NOTE: get_aggrid_df に反映処理があるから、触らなくても問題はないはず
        # self.aggrid_state.df = self.get_current_df()
        # del self.aggrid_state.df
        self.aggrid_state.change_key()


    # TODO: キャッシュのクリアってどうしよ。ここでやることではないか？
    #       そもそもキャッシュ事態いらんのか？

    def reload_all(self):

        del self.state.df
        del self.aggrid_state.df

        self.aggrid_state.change_key()


    # TODO: 引数でcsvのみか、各パラメーターファイルも保存するとか？
    #      
    def save_current_df(self, force: bool = False) -> bool:

        # 強制 or 変更フラグが立っているとき保存する
        need_save = force or self.state.is_df_changed
        if not need_save:
            return False
        
        repo.save_df(self.get_current_df())
        
        print("df_changed_reasons = ", self.state.df_changed_reasons)

        self.state.is_df_changed = False
        self.state.df_changed_reasons = None
        return True
