from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class CompetitorAnalysisParams:
    #duration: datetime
    location: List[str]
    demographics: List[str]
    competitors: List[str]
    timelineidentifier: str
    min_required_date: datetime


