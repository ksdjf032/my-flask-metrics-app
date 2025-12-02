import request
import os
import time
import subprocess
import signal
import sys
import pytest

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8080")

def test_health():
    r = requests.get(f"{BASE}/health", timeout=5)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_hello_get():
    r = requests.get(f"{BASE}/hello?name=Diego", timeout=5)
    assert r.status_code == 200
    j = r.json()
    assert "message" in j and "Diego" in j["message"]

def test_metrics():
    r = requests.get(f"{BASE}/metrics", timeout=5)
    assert r.status_code == 200
    assert "http_requests_total" in r.text
