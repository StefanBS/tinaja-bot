import asyncio
import socket
from types import SimpleNamespace

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from tinaja_bot.cogs.exercism import Exercism


class FakeContext:
    def __init__(self):
        self.author = SimpleNamespace(mention='@member')
        self.sent = []

    async def send(self, message):
        self.sent.append(message)


@pytest.fixture
async def exercism_org():
    """A stand-in for exercism.org: 'alice' is a public profile, 'broken' fails, 'slow' hangs, and /about exists"""

    async def profile(request):
        name = request.match_info['name']
        if name == 'slow':
            await asyncio.sleep(0.5)
        if name == 'alice':
            return web.Response(status=200)
        if name == 'broken':
            return web.Response(status=500)
        return web.Response(status=404)

    async def about(request):
        return web.Response(status=200)

    app = web.Application()
    app.router.add_get('/profiles/{name}', profile)
    app.router.add_get('/about', about)
    async with TestServer(app) as server:
        yield str(server.make_url('')).rstrip('/')


async def run_exercism(base_url, *args, timeout=10):
    cog = Exercism(base_url=base_url, timeout=timeout)
    ctx = FakeContext()
    await cog.cog_load()
    try:
        await cog.exercism.callback(cog, ctx, *args)
    finally:
        await cog.cog_unload()
    return ctx.sent


def closed_port_url():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    return f'http://127.0.0.1:{port}'


async def test_asks_for_a_profile_name(exercism_org):
    assert await run_exercism(exercism_org) == ['@member you must provide an exercism profile name']


async def test_shares_link_to_public_profile(exercism_org):
    assert await run_exercism(exercism_org, 'alice') == [f'{exercism_org}/profiles/alice']


async def test_rejects_unknown_profile(exercism_org):
    assert await run_exercism(exercism_org, 'nobody') == [
        'nobody does not appear to be a valid exercism public profile'
    ]


async def test_cannot_be_pointed_at_other_pages(exercism_org):
    assert await run_exercism(exercism_org, '../../about') == [
        '../../about does not appear to be a valid exercism public profile'
    ]


async def test_reports_unexpected_status(exercism_org):
    assert await run_exercism(exercism_org, 'broken') == [
        'An error occurred while checking the profile. Status code: 500'
    ]


async def test_reports_unreachable_site():
    assert await run_exercism(closed_port_url(), 'alice') == ['An error occurred while checking the profile.']


async def test_gives_up_on_slow_site(exercism_org):
    assert await run_exercism(exercism_org, 'slow', timeout=0.05) == ['An error occurred while checking the profile.']
