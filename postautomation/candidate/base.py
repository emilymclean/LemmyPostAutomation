from abc import ABC
from typing import List

from postautomation import PostCandidate

class CandidateProvider(ABC):

    def list_candidates(self, page_token: str) -> List[PostCandidate]:
        pass
