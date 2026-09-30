import json
from pathlib import Path
from typing import Any
import requests

class APIClient:
    def __init__(self, url: str, timeout: int = 10, cache_path: Path | None = None) -> None:
        self.url = url
        self.timeout = timeout
        self.cache_path = cache_path

    def fetch(self) -> dict[str, Any]:
        try:
            response = requests.get(self.url, timeout=self.timeout)
            if response.status_code not in {200, 201}:
                response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError('Expected a JSON object from API.')
            result = {'status_code': response.status_code, 'source_url': self.url, 'data': data}
            self._cache(result)
            return result
        except requests.exceptions.Timeout:
            return {'status_code': None, 'source_url': self.url, 'error': 'API request timed out', 'data': {}}
        except requests.exceptions.RequestException as exc:
            return {'status_code': None, 'source_url': self.url, 'error': f'Network error: {exc}', 'data': {}}
        except (ValueError, json.JSONDecodeError) as exc:
            return {'status_code': None, 'source_url': self.url, 'error': f'Invalid JSON response: {exc}', 'data': {}}
        finally:
            pass

    def _cache(self, result: dict[str, Any]) -> None:
        if self.cache_path:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(json.dumps(result, indent=4), encoding='utf-8')
