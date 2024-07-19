import pytest

@pytest.mark.parametrize('create_jira_ticket', [{
                                                "summary": "Strong password validation",
                                                "testKey": "YANSB-805",
                                                "steps": [
                                                    {
                                                        "action": "Open the Change Password screen by selecting option \"My Profile > Password\"",
                                                        "data": "test data",
                                                        "result": "status code 200"
                                                    },
                                                    {
                                                        "action": "Fill the password fields with data",
                                                        "data": "Current Password: ${Password}\nNew Password: ${Password}\nConfirm New Password: ${Password}",
                                                        "result": "The new password is: ${Valid}\nError:\n${Message}"
                                                    },
                                                    {
                                                        "action": "step3",
                                                        "data": "Current Password: ${Password}\nNew Password: ${Password}\nConfirm New Password: ${Password}",
                                                        "result": "The new password is: ${Valid}\nError:\n${Message}"
                                                    },
                                                    {
                                                        "action": "adding another step to existing steps - step4 -",
                                                        "data": "Current Password: ${Password}\nNew Password: ${Password}\nConfirm New Password: ${Password}",
                                                        "result": "The new password is: ${Valid}\nError:\n${Message}"
                                                    }
                                                ]
                                                }], indirect=True)
def test_example_pass(create_jira_ticket):
    assert 1 == 1

@pytest.mark.parametrize('create_jira_ticket', [{
                                                "summary": "this fails on purpose",
                                                "testKey": "YANSB-104",
                                                "steps": [
                                                    {
                                                        "action": "action 1",
                                                        "data": "test data 1",
                                                        "result": "something"
                                                    },
                                                    {
                                                        "action": "action 2",
                                                        "data": "no data",
                                                        "result": "who knows"
                                                    }
                                                ]
                                                }], indirect=True)
def test_example_fail(create_jira_ticket):
    assert 1 == 2