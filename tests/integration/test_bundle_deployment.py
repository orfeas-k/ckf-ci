import subprocess
import json

import aiohttp
import pytest
import requests
from pytest_operator.plugin import OpsTest

BUNDLE_PATH = "./releases/1.7/edge/kubeflow/bundle.yaml"

class TestCharm:
    @pytest.mark.abort_on_fail
    async def test_bundle_deployment_works(self, ops_test: OpsTest):
        subprocess.Popen(["juju", "deploy", f"{BUNDLE_PATH}", "--trust"])

        await ops_test.model.wait_for_idle(
            apps=["istio-ingressgateway"],
            status="active",
            raise_on_blocked=False,
            raise_on_error=False,
            timeout=1500,
        )

        await ops_test.model.wait_for_idle(
            apps=["oidc-gatekeeper"],
            status="blocked",
            raise_on_blocked=False,
            raise_on_error=False,
            timeout=1500,
        )
        
        url = get_public_url()
        subprocess.Popen(["juju", "config", "dex-auth", f"public-url={url}"])
        subprocess.Popen(["juju", "config", "oidc-gatekeeper", f"public-url={url}"])


        applications = ops_test.model.applications
        await ops_test.model.wait_for_idle(apps=list(applications.keys()),
            raise_on_blocked=False,
            raise_on_error=False,
            timeout=1500
        )
        
        result_status, result_text = await fetch_response(url)
        assert result_status == 200
        assert "Log in to Your Account" in result_text
        assert "Email Address" in result_text
        assert "Password" in result_text

def get_public_url():
    """ Extracts public url from service istio-ingressgateway-workload for EKS deployment.
    As a next step, this could be generalized in order for the above test to run in MicroK8s as well.
    """
    p = subprocess.Popen(["kubectl", "-n", "kubeflow", "get", "svc", "istio-ingressgateway-workload", "-o", "jsonpath={.status.loadBalancer.ingress[0].hostname}"], stdout=subprocess.PIPE, text=True)
    url, err = p.communicate()
    url = "http://" + url
    return url

async def fetch_response(url, headers = None):
    """Fetch provided URL and return pair - status and text (int, string)."""
    result_status = 0
    result_text = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            result_status = response.status
            result_text = await response.text()
    return result_status, str(result_text)