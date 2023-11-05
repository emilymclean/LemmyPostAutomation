from typing import List, Optional

import pandas
from pandas import DataFrame

from postautomation import PostCandidate
from postautomation.candidate import CandidateProvider


class CSVCandidateProvider(CandidateProvider):
    file_name: str
    df: DataFrame

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.refresh_candidates()

    def list_candidates(self, page_token: Optional[str]) -> (List[PostCandidate], Optional[str]):
        return [PostCandidate.from_dataframe(row) for row in self.df.to_dict(orient="records")], None

    def remove_candidate(self, candidate: PostCandidate):
        self.df = self.df[self.df["url"] != candidate.url]
        with open(self.file_name, "w") as f:
            f.write(self.df.to_csv(index=False))

    def refresh_candidates(self):
        self.df = pandas.read_csv(self.file_name, header=0)


