from unittest.mock import Mock

import pytest

from app.agents.model_utils import invoke_llm_with_retry


def test_successful_response():
    """Successful model call should execute only once."""

    fake_llm = Mock()
    fake_llm.invoke.return_value = "Success"

    result = invoke_llm_with_retry(fake_llm, [])

    assert result == "Success"
    assert fake_llm.invoke.call_count == 1


def test_retry_on_temporary_error():
    """HTTP 503 should trigger retries."""

    fake_llm = Mock()

    fake_llm.invoke.side_effect = [
        Exception("503 Service Unavailable"),
        Exception("503 Service Unavailable"),
        "Success",
    ]

    result = invoke_llm_with_retry(fake_llm, [])

    assert result == "Success"
    assert fake_llm.invoke.call_count == 3


def test_no_retry_on_quota_error():
    """HTTP 429 should stop immediately."""

    fake_llm = Mock()
    fake_llm.invoke.side_effect = Exception("429 RESOURCE_EXHAUSTED")

    with pytest.raises(Exception, match="429"):
        invoke_llm_with_retry(fake_llm, [])

    assert fake_llm.invoke.call_count == 1