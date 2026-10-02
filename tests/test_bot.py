import socket

import aiohttp
import pytest

from tinaja_bot.bot import TinajaBot
from tinaja_bot.config import Config


@pytest.fixture
async def bot():
    bot = TinajaBot(Config(token='unused', metrics_host='127.0.0.1', metrics_port=0))
    await bot.setup_hook()
    yield bot
    await bot.close()


async def test_registers_commands(bot):
    assert {'unexpo', 'exercism'} <= {c.name for c in bot.commands}


async def test_serves_census_metrics(bot):
    url = f"http://127.0.0.1:{bot.metrics_endpoint.port}/metrics"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            body = await response.text()
    assert response.status == 200
    assert 'discord_server_members' in body


async def test_close_frees_metrics_port():
    bot = TinajaBot(Config(token='unused', metrics_host='127.0.0.1', metrics_port=0))
    await bot.setup_hook()
    port = bot.metrics_endpoint.port
    await bot.close()

    with socket.socket() as s:
        s.bind(('127.0.0.1', port))


def test_config_requires_token(monkeypatch):
    monkeypatch.delenv('DISCORD_BOT_TOKEN', raising=False)
    with pytest.raises(ValueError):
        Config.from_env()


def test_config_reads_metrics_settings(monkeypatch):
    monkeypatch.setenv('DISCORD_BOT_TOKEN', 'abc')
    monkeypatch.setenv('METRICS_PORT', '9100')
    config = Config.from_env()
    assert config == Config(token='abc', metrics_host='0.0.0.0', metrics_port=9100)
