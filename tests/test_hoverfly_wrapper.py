import json
import os
from textwrap import dedent

import pytest
import requests

from pytest_hoverfly_wrapper.plugin import TEST_DATA_DIR, generate_logs, template_block_domain_json
from pytest_hoverfly_wrapper.simulations import StaticSimulation


# foobar.json is a simple simulation which fakes a request to https://google.com. Note the scheme.
@pytest.mark.simulated(StaticSimulation(files=["foobar.json"]))
def test_1(setup_hoverfly, journal_api):
    proxy_port = setup_hoverfly[1]
    proxies = {
        "http": "http://localhost:{}".format(proxy_port),
        "https": "http://localhost:{}".format(proxy_port),
    }
    r = requests.get("http://google.com", proxies=proxies)
    assert not r.headers.get("Hoverfly-Cache-Served")
