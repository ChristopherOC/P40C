from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, constr

from model.match import Match


class Round(BaseModel):  # Défini des règles pour créer un round

    name: constr(strict=True, min_length=1, max_length=15)
    begin_date: Optional[datetime] = datetime.today()
    end_date: datetime = None
    matchs: List[Match] = []

    def play(self, pick_winner_view_class):
        if not self.end_date:
            for match in self.matchs:
                print("Round :", self.name)
                match.play(pick_winner_view_class)

                self.end_date = datetime.today()
