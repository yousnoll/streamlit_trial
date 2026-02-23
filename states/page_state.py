from .session_state_wrapper import SessionStateWrapper


class PageState(SessionStateWrapper):
    def __init__(self):
        super().__init__("page")
    
    #region: page_id property

    @property
    def page_id(self) -> str | None:
        return self._get_val("page_id")

    @page_id.setter
    def page_id(self, value: str | None) -> None:
        self._set_val("page_id", value)

    @page_id.deleter
    def page_id(self) -> None:
        self._del_val("page_id")

    #endregion

    def first_time(self, id: str, no_update: bool = False) -> bool:

        if self.page_id == id:
            return False

        print(f"First time page(id={id})")

        if not no_update:
            self.page_id = id

        return True



