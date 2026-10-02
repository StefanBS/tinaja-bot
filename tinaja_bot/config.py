import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    token: str
    metrics_host: str = '0.0.0.0'
    metrics_port: int = 8000

    @classmethod
    def from_env(cls):
        token = os.getenv('DISCORD_BOT_TOKEN')
        if token is None:
            raise ValueError("No token found. Make sure to set the DISCORD_BOT_TOKEN environment variable.")
        return cls(
            token=token,
            metrics_host=os.getenv('METRICS_HOST', cls.metrics_host),
            metrics_port=int(os.getenv('METRICS_PORT', cls.metrics_port)),
        )
