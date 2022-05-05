from pydantic import validator
from pydantic.main import BaseModel
from controllers_files.result import Result
from controllers_files.player_manager import player_manager as pm


class Match(BaseModel):

    id_player_1: int
    id_player_2: int
    score_player_1: Result = None

    @property  # Défini le score du joueur 2 par rapport au joueur 1
    def score_player_2(self):
        return Result(1.0 - self.score_player_1.value)\
            if self.score_player_1 else None

    @validator('id_player_2')
    def check_id_player(cls, value, values):
        assert value != values['id_player_1']
        return value

    def __eq__(self, other) -> bool:
        return min(self.id_player_1, self.id_player_2) == min(other.id_player_1, other.id_player_2) and \
            max(self.id_player_1, self.id_player_2) == max(
                other.id_player_1, other.id_player_2)

    @property
    def is_played(self):
        return self.score_player_1 is not None

    def play(self, pick_winner_view_class):  # Permet de jouer un match ainsi le vainqueur
        if not self.is_played:
            self.score_player_1 = Result(pick_winner_view_class(
                player_1=pm.search_by_id(self.id_player_1),
                player_2=pm.search_by_id(self.id_player_2)).display())

    def has_player(self, player_id):
        return player_id in (self.id_player_1, self.id_player_2)

    def get_player_score(self, player_id):  # Récupère le score du joueur voulu
        if self.id_player_1 == player_id:
            return self.score_player_1
        elif self.id_player_2 == player_id:
            return self.score_player_2

    def __str__(self) -> str:
        res = 'égalité'
        if self.score_player_1 == Result.Win:
            res = "1 a gagné"
        elif self.score_player_2 == Result.Win:
            res = '2 a gagné'
        return f'{str(pm.search_by_id(self.id_player_1))} VS {str(pm.search_by_id(self.id_player_2))} ({res})'
