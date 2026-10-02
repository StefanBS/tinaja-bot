from types import SimpleNamespace

import discord
from prometheus_client import CollectorRegistry

from tinaja_bot.census import ServerCensus


def member(status, bot=False):
    return SimpleNamespace(status=status, bot=bot)


def server(id, name, members, chunked=True):
    return SimpleNamespace(id=id, name=name, members=members, chunked=chunked)


def census_of(*servers):
    registry = CollectorRegistry()
    registry.register(ServerCensus(lambda: servers))
    return registry


def sample(registry, metric, server_id):
    return registry.get_sample_value(metric, {'server_id': str(server_id), 'server_name': f'server-{server_id}'})


def test_counts_people_and_treats_idle_and_dnd_as_online():
    registry = census_of(
        server(
            1,
            'server-1',
            [
                member(discord.Status.online),
                member(discord.Status.idle),
                member(discord.Status.dnd),
                member(discord.Status.offline),
                member(discord.Status.online, bot=True),
            ],
        )
    )

    assert sample(registry, 'discord_server_members', 1) == 4
    assert sample(registry, 'discord_server_online_members', 1) == 3


def test_reports_each_server_separately():
    registry = census_of(
        server(1, 'server-1', [member(discord.Status.online)]),
        server(2, 'server-2', [member(discord.Status.offline), member(discord.Status.offline)]),
    )

    assert sample(registry, 'discord_server_members', 1) == 1
    assert sample(registry, 'discord_server_members', 2) == 2


def test_skips_servers_whose_members_are_not_cached_yet():
    registry = census_of(server(1, 'server-1', [member(discord.Status.online)], chunked=False))

    assert sample(registry, 'discord_server_members', 1) is None
