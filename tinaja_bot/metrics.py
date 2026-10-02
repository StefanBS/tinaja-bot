from aiohttp import web
from prometheus_client import generate_latest


class MetricsEndpoint:
    """HTTP server that publishes a Prometheus registry at /metrics"""

    def __init__(self, registry, host, port):
        self._registry = registry
        self._host = host
        self._port = port
        self._runner = None

    @property
    def port(self):
        """The bound port; differs from the configured one when that was 0"""
        return self._runner.addresses[0][1]

    async def start(self):
        app = web.Application()
        app.router.add_get('/metrics', self._handle)
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, self._host, self._port)
        await site.start()
        print(f'Metrics server started at http://{self._host}:{self.port}/metrics')

    async def stop(self):
        if self._runner is not None:
            await self._runner.cleanup()
            self._runner = None

    async def _handle(self, request):
        return web.Response(body=generate_latest(self._registry), content_type='text/plain')
