from abc import ABC
from typing import List, Optional

from postautomation import PostCandidate


class CandidateProvider(ABC):

    def list_candidates(self, page_token: Optional[str]) -> (List[PostCandidate], Optional[str]):
        pass

    def remove_candidate(self, candidate: PostCandidate):
        pass