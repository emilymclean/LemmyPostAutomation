from typing import Optional

from sqlalchemy import update, select, Result
from sqlalchemy.orm import Session

from postautomation.data.base import session_scope, CurrentPage


class MonitorPersistence:

    def __get_page_entry(self, community_name: str, session: Session) -> Optional[CurrentPage]:
        return (session.execute(select(CurrentPage).filter(CurrentPage.community_name==community_name))
                .scalar_one_or_none())

    def get_current_page(self, community_name: str) -> int:
        with session_scope() as session:
            result = self.__get_page_entry(community_name, session)
            if result is None:
                return 0
            return result.page

    def set_current_page(self, community_name: str, page: int):
        with session_scope() as session:
            current = self.__get_page_entry(community_name, session)
            if current is None:
                session.add(CurrentPage(
                    community_name=community_name,
                    page=page
                ))
            else:
                current.page = page
