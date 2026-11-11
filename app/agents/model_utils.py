from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)


def should_retry(exception):
    """
    Decide whether an exception is temporary and worth retrying.
    """

    error_message = str(exception).lower()

    # Do not retry quota or billing errors
    if "429" in error_message or "resource_exhausted" in error_message:
        return False

    if "402" in error_message or "payment required" in error_message:
        return False

    # Retry temporary server errors
    if any(code in error_message for code in ["500", "503", "504"]):
        return True

    # Retry temporary network errors
    if any(
        keyword in error_message
        for keyword in [
            "timeout",
            "timed out",
            "connection error",
            "connection reset",
        ]
    ):
        return True

    # Do not retry unknown errors
    return False


@retry(
    retry=retry_if_exception(should_retry),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=10),
    reraise=True,
)
def invoke_llm_with_retry(llm, messages):
    """
    Invoke the configured LLM with automatic retries for temporary errors.
    """

    return llm.invoke(messages)