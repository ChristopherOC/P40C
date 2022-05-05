from random import choice

from controllers_files.player_manager import player_manager as pm


class Matchmaking:

    def __init__(self, players):
        self.players = players
        self.tournament_matchs = []
        self.tournament_scores = []

    def gen_turn_one(self):  # Divise la liste des joueurs par deux

        turn_players = [pm.search_by_id(player.id) for player in self.players]
        turn_players.sort(key=lambda x: -x.rank)

        return [sorted((p1.id, p2.id)) for p1, p2 in zip(turn_players[:4], turn_players[4:])]

    def gen_scores(self, turn_matchs):  # Affecte une valeur au score d'un joueur et du second par analogie

        scores = []

        for p_id1, p_id2 in turn_matchs:
            s1 = choice((0.0, 0.5, 1.0))
            s2 = 1 - s1
            scores.append((p_id1, s1, p_id2, s2))
        return scores

    def get_player_score(self, player_id):  # fixe le score du joueur
        score = 0
        for p_id1, s1, p_id2, s2 in self.tournament_scores:
            if p_id1 == player_id:
                score += s1
            elif p_id2 == player_id:
                score += s2
        return score

    def gen_next_turn(self):  # Divise les joueurs en deux listes en fonction de leur score et de leur rang si égalité
        turn_matchs = []
        turn_players = [pm.search_by_id(player.id) for player in self.players]
        turn_players.sort(key=lambda x: ((-self.get_player_score(x.id), x.rank)))
        while turn_players:

            p1 = turn_players.pop(0)
            p2 = self.find_opponent(turn_players, p1)
            turn_players.pop(turn_players.index(p2))
            match = sorted((p1.id, p2.id))

            self.tournament_matchs.append(match)
            turn_matchs.append(match)
        return turn_matchs

    def find_opponent(self, turn_players, p1):  # Recherche l'adversaire dans la liste opposée pour jouer le match
        for p2 in turn_players:

            if sorted((p1.id, p2.id)) not in self.tournament_matchs:

                return p2

        return turn_players[0]
