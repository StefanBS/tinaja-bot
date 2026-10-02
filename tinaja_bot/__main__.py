from dotenv import load_dotenv

from tinaja_bot.bot import TinajaBot
from tinaja_bot.config import Config

load_dotenv()
config = Config.from_env()
TinajaBot(config).run(config.token)
