from datetime import datetime
from typing import List

from controllers_files.player_manager import player_manager as pm
from pydantic import BaseModel, validator
from pydantic.types import PositiveInt, constr

from model.match import Match
from model.round import Round
from controllers_files.tournament_type import TournamentType


class Tournament(BaseModel):  # Paramètre générique des tournois

    name: constr(strict=True, regex="^[A-Za-z '\-éèàçê]{2,25}$")
    location: constr(strict=True, regex="^[A-Za-z '\-éèàçê]{2,25}$")
    begin_date: datetime = datetime.today()
    end_date: datetime = None
    rounds: List[Round] = []
    players: List[PositiveInt]
    id: PositiveInt
    tournament_type: TournamentType

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup()

    def setup(self):  # Création du round 1 par défaut lorsqu'un tournoi est créé
        if not self.rounds[0].matchs:
            players = [pm.search_by_id(player_id) for
                       player_id in self.players]
            players.sort(key=lambda x: -x.rank)
            group_1 = players[:len(players) // 2]
            group_2 = players[len(players) // 2:]
            self.rounds[0].matchs = [Match(id_player_1=player_1.id,
                                     id_player_2=player_2.id) for player_1,
                                     player_2 in zip(group_1, group_2)]

    @validator('players')  # Vérification des joueurs
    def check_players(cls, value):
        if not isinstance(value, list):
            raise ValueError("players don't match")
        for player_id in value:
            if not isinstance(player_id, int):
                raise ValueError('must be an int')
            try:
                pm.search_by_id(player_id)
            except ValueError:
                raise ValueError(f"This player(id:{player_id}) don't exist")
        return value

    @validator('id')
    def check_id(cls, value):
        if not isinstance(value, int):
            raise ValueError('wrong id')
        return value

    def play(self, pick_winner_view_class):  # Permet de jouer les rounds du tournoi
        for round_nb, round in enumerate(self.rounds):
            print("Match du round : ", round_nb + 1)
            round.play(pick_winner_view_class)
            if round_nb < len(self.rounds) - 1:
                self.setup_next_round(round_nb + 1)
        self.end_date = datetime.today()

    def setup_next_round(self, round_nb: int):  # Lorsqu'un round est fini le second est créé automatiquement
        players = [pm.search_by_id(player_id) for player_id in self.players]
        players.sort(key=lambda x: (self.get_player_score(x.id), -x.rank))
        while players:
            p1 = players.pop(0)
            for p2 in players:
                m = Match(id_player_1=p1.id, id_player_2=p2.id)
                if m not in self.matchs:
                    p2 = players.pop(0)
                    self.rounds[round_nb].matchs.append(m)
                    break
            else:
                p2 = players.pop(0)
                m = Match(id_player_1=p1.id, id_player_2=p2.id)
        self.rounds[round_nb].begin_date = datetime.today()

    def get_player_score(self, player_id):  # Récupère le score affecté à un joueur
        score = 0.0
        for round in self.rounds:
            for match in round.matchs:
                if match.is_played:
                    if match.has_player(player_id):
                        score += match.get_player_score(player_id).value
                        break
        return score

    @property
    def matchs(self):
        results = []
        for round in self.rounds:
            for match in round.matchs:
                results.append(match)
        return results

    def __str__(self) -> str:
        return f'{self.name} {self.begin_date} -> {self.end_date}'
