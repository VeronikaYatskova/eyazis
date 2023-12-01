from .agnet_base import AgentBase
from .example_agent import ExampleAgent
from .find_movie_agent import FindMovieAgent
from .surprise_agent import SurpriseAgent
from .find_movie_agent_raiting import FindMovieAgentRaiting
from .find_movie_agent_genre import FindMovieAgentGenre
from .find_movie_agent_year import FindMovieAgentYear
from .hello_agent import HelloAgent
from .pitty_agent import PittyAgent
from .help_agent import HelpAgent

agents = [HelloAgent(), FindMovieAgent(), SurpriseAgent(), FindMovieAgentRaiting(), FindMovieAgentGenre(), FindMovieAgentYear(), PittyAgent(), HelpAgent()]
