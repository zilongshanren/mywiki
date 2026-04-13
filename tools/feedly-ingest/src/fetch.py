"""Rate-limited HTTP client.

Previous versions used tenacity to retry transport errors — but SSL handshake
failures and connection timeouts against dead/misconfigured blogs never
recover, they just burn wall-clock time (3 × 30s per URL). We now fail fast:
one attempt, short timeout, move on. The seen.sqlite dedupe means the next
run will retry the URL anyway.
"""
from __future__ import annotations

import logging
import time
from collections import defaultdict
from urllib.parse import urlparse

import httpx

log = logging.getLogger(__name__)


class Fetcher:
    """Thin wrapper over httpx.Client with per-domain throttling."""

    def __init__(self, cfg: dict):
        self.cfg = cfg
        timeout = httpx.Timeout(
            cfg.get("timeout_seconds", 10),
            connect=min(cfg.get("timeout_seconds", 10), 5),  # fail connect fast
        )
        self.client = httpx.Client(
            headers={"User-Agent": cfg["user_agent"]},
            timeout=timeout,
            follow_redirects=True,
            verify=True,
        )
        self._last_hit: dict[str, float] = defaultdict(float)
        rate = max(float(cfg.get("rate_limit_per_domain", 1.0)), 0.01)
        self._min_interval = 1.0 / rate

    def _throttle(self, url: str) -> None:
        domain = urlparse(url).netloc
        gap = time.monotonic() - self._last_hit[domain]
        if gap < self._min_interval:
            time.sleep(self._min_interval - gap)
        self._last_hit[domain] = time.monotonic()

    def get_html(self, url: str) -> str | None:
        self._throttle(url)
        log.debug("GET %s", url)
        try:
            r = self.client.get(url)
        except httpx.HTTPError as e:
            log.warning("GET failed %s: %s", url, e)
            return None
        except Exception as e:  # noqa: BLE001 — catches ssl.SSLError etc.
            log.warning("GET crashed %s: %s", url, e)
            return None
        if r.status_code != 200:
            log.warning("HTTP %s for %s", r.status_code, url)
            return None
        return r.text

    def get_bytes(self, url: str) -> bytes | None:
        self._throttle(url)
        try:
            r = self.client.get(url)
        except httpx.HTTPError as e:
            log.warning("GET bytes failed %s: %s", url, e)
            return None
        except Exception as e:  # noqa: BLE001
            log.warning("GET bytes crashed %s: %s", url, e)
            return None
        return r.content if r.status_code == 200 else None

    def get_json(self, url: str):
        self._throttle(url)
        try:
            r = self.client.get(url)
        except httpx.HTTPError as e:
            log.warning("GET json failed %s: %s", url, e)
            return None
        except Exception as e:  # noqa: BLE001
            log.warning("GET json crashed %s: %s", url, e)
            return None
        if r.status_code != 200:
            return None
        try:
            return r.json()
        except ValueError:
            return None

    def close(self) -> None:
        self.client.close()
