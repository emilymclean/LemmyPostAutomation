import os.path
from pathlib import Path
from typing import List, Optional

import pandas
from pandas import DataFrame

from postautomation import PostCandidate
from postautomation.candidate import CandidateProvider


class CSVCandidateProvider(CandidateProvider):
    file_name: str
    unsuitable_file_name: str
    df: DataFrame
    unsuitable_df: DataFrame

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.unsuitable_file_name = str(Path(file_name).with_suffix(".unsuitable.csv"))
        self._setup_files()
        self.refresh_candidates()

    def list_candidates(self, page_token: Optional[str]) -> (List[PostCandidate], Optional[str]):
        return [PostCandidate.from_dataframe(row) for row in self.df.to_dict(orient="records")], None

    def remove_candidate(self, candidate: PostCandidate, unsuitable: bool = False):
        removed = self.df[self.df["url"] == candidate.url]
        self.unsuitable_df = pandas.concat([self.unsuitable_df, removed], ignore_index=True)
        self.df = pandas.concat([self.df, removed], ignore_index=True).drop_duplicates(keep=False)

        with open(self.file_name, "w") as f:
            f.write(self.df.to_csv(index=False))
        if unsuitable:
            with open(self.unsuitable_file_name, "w") as uf:
                uf.write(self.unsuitable_df.to_csv(index=False))

    def refresh_candidates(self):
        dtype = {
            'url': 'string',
            'title': 'string',
            'content_warnings': 'string'
        }

        self.df = pandas.read_csv(self.file_name, header=0, dtype=dtype)
        self.unsuitable_df = pandas.read_csv(self.unsuitable_file_name, header=0, dtype=dtype)

    def _setup_files(self):
        dummy_file = "url,title,content_warnings"
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w") as f:
                f.write(dummy_file)

        if not os.path.exists(self.unsuitable_file_name):
            with open(self.unsuitable_file_name, "w") as f:
                f.write(dummy_file)

