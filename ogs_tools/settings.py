import pprint

import requests
from traitlets import HasTraits, Int, Unicode, Float
from traitlets.config import Application
from traitlets.config.configurable import Configurable
import pyperclip

pp = pprint.PrettyPrinter(indent=4)


def ogs_games():
    games = 'https://online-go.com/api/v1/players1084709/games?ended__isnull=0&ordering=-ended&page_size=5&format=json'
    last_five = requests.get(games)
    return last_five.json()


def players_and_rankings(game_players):
    result = dict()
    for color in 'black white'.split():
        p = Player(color=color, rank=game_players[color]['ranking'], username=game_players[color]['username'])
        result[color] = p
    return result


def game_title(game_players):
    _ = players_and_rankings(game_players)
    result = dict()
    for color in 'black white'.split():
        result[color] = f"{_[color].username} ({_[color].human_rank()})"
    return f"{result['black']} vs {result['white']}"


class Player(HasTraits):
    username = Unicode()
    color = Unicode()
    rank = Float()

    def human_rank(self):
        """Only works for kyu for now."""
        r = 30 - int(self.rank)
        return f"{r}k"


class User(Configurable):
    """OGS user.
    """
    id = Int(default_value=1084709, config=True)

    def game_color(self, game):
        for color in 'black white'.split():
            if game[color] == self.id:
                return color.capitalize()


class App(Application):
    game = Int(default_value=0, config=True)

    def start(self):
        u = User()
        g = ogs_games()
        game = g['results'][self.game]
        self.log.warning(pp.pformat(game))
        title = game_title(game['players'])
        post_title = f"{title} - please review."
        game_url = f"https://online-go.com/game/{game['id']}"
        post_content = f"""
        Hello, I played as {u.game_color(game)} and lost this game. I would appreciate a review:
        
        {game_url}
        """
        total_content = f"{post_title}\n{post_content}\n\n"
        pyperclip.copy(total_content)
        self.log.warning(total_content)



if __name__ == '__main__':
    App.launch_instance()
