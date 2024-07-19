# conftest.py
import pytest
from create_xray_test import create_xray_test,post_test_result
import datetime
# Define a fixture to determine test result
@pytest.fixture(scope="function", autouse=False)
def create_jira_ticket(request):
    failed_count = request.session.testsfailed
    yield
    status = "FAILED" if request.session.testsfailed > failed_count else "PASSED"
    post_test_result(status=status, summary = request.param['summary'], steps = request.param['steps'])
        
