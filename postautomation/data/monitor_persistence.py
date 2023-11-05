from typing import Optional

from sqlalchemy import update, select, Result, and_
from sqlalchemy.orm import Session

from postautomation.data.base import session_scope, CurrentPage, PhashHistory, PostPhashHistory


class MonitorPersistence:

    def __get_page_entry(self, community_name: str, session: Session) -> CurrentPage:
        return (session.execute(select(CurrentPage).filter(CurrentPage.community_name == community_name))
                .scalar_one_or_none())

    def get_current_page(self, community_name: str) -> Optional[int]:
        with session_scope() as session:
            result = self.__get_page_entry(community_name, session)
            if result is None:
                return 1
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

    def __get_phash(self, community_name: str, phash: str, session: Session) -> Optional[PhashHistory]:
         return (session.execute(select(PhashHistory)
                                    .filter(
                and_(PhashHistory.community_name == community_name, PhashHistory.phash == phash)))
                    .scalar_one_or_none())

    def phash_exists(self, community_name: str, phash: str) -> bool:
        with session_scope() as session:
            return self.__get_phash(community_name, phash, session) is not None

    def record_phash(self, community_name: str, phash: str, url: str, post_id: int):
        with session_scope() as session:
            current_phash = self.__get_phash(community_name, phash, session)
            if current_phash is None:
                current_phash = PhashHistory(
                    community_name=community_name,
                    phash=phash
                )
                session.add(current_phash)
                session.commit()

            session.add(PostPhashHistory(
                post_id=post_id,
                community_name=community_name,
                phash_id=current_phash.id,
                url=url
            ))

    def has_processed(self, post_id: int) -> bool:
        with session_scope() as session:
            existing = session.execute(select(PostPhashHistory).filter(PostPhashHistory.post_id == post_id)).scalar_one_or_none()
            return existing is not None