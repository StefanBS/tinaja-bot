import discord
from prometheus_client.core import GaugeMetricFamily


class ServerCensus:
    """Prometheus collector that counts Members and Online members per Server at scrape time"""

    def __init__(self, servers):
        self._servers = servers

    def collect(self):
        members = GaugeMetricFamily(
            'discord_server_members',
            'Number of Members (people, not bots) in the Server',
            labels=['server_id', 'server_name'],
        )
        online_members = GaugeMetricFamily(
            'discord_server_online_members',
            'Number of Members who are online, idle or do-not-disturb',
            labels=['server_id', 'server_name'],
        )
        for server in self._servers():
            # Until chunked, the member cache is partial and would undercount
            if not server.chunked:
                continue
            people = [m for m in server.members if not m.bot]
            labels = [str(server.id), server.name]
            members.add_metric(labels, len(people))
            online_members.add_metric(labels, len([m for m in people if m.status != discord.Status.offline]))
        yield members
        yield online_members
