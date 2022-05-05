from views import views
from controllers_files.player_manager import player_manager as pm
from controllers_files.router import router
from controllers_files.tournament_manager import tournament_manager as tm


def main_controller():
    router.navigate(views.MainMenu().display())


# For the players
def players_controller():
    router.navigate(views.PlayerMenu().display())


def player_form():  # Formulaire de création d'un joueur
    form_data = views.FormPlayer().display()
    pm.create(save=True, **form_data)
    router.navigate("/players")


def list_players_by_name():  # Liste les joueurs par ordre alphabétique
    views.ListView("Players", pm.search(sort_key=lambda x: x.lastname)).display()
    router.navigate("/players")


def list_players_by_rank():  # Liste les joueurs par rang
    views.ListView("Players", pm.search(sort_key=lambda x: -x.rank)).display()
    router.navigate("/players")


def update_player_rank():  # Modifie le rang d'un joueur
    player_id = views.PickPlayer(pm.search(sort_key=lambda x: x.rank)).display()
    player = pm.search_by_id(player_id)
    form_data = views.UpdatePlayer().display()
    player.rank = form_data["rank"]
    pm.save_item(player_id)
    router.navigate("/players")


# For the tournament
def tournaments_controller():
    router.navigate(views.TournamentMenu().display())


def create_tournament():  # Permet de créer un tournoi
    form_data = views.FormTournament().display()
    print(tm.create(save=True, **form_data))
    router.navigate("/tournaments")


def tournament_list():  # Permet d'accéder à la liste des tournois en cours
    views.ListView("Tournament", tm.search(lambda x: x.end_date == None)).display()
    router.navigate("/tournaments")


def pending_tournament():  # Permet d'accéder aux tournois en cours afin de les jouer
    tournament_id = views.PickTournament("Pending Tournament",
                                         tm.search(filter_key=lambda x: x.end_date == None)).display()
    tournament = tm.search_by_id(tournament_id)
    tournament.play(pick_winner_view_class=views.PickWinner)
    tm.save_item(tournament.id)
    router.navigate("/tournaments")


def tournament_report():  # Génère un rapport du tournoi
    tournamernt_id = views.PickTournament("Rapport des tournois", tm.all()).display()
    tournament = tm.search_by_id(tournamernt_id)
    views.TournamentReport(tournament).display()
    router.navigate("/tournaments")
