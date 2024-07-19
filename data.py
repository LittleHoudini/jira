xray_json_template = {
    "tests": [
        {
            "start" : "2021-08-30T11:47:35+01:00",
            "finish" : "2021-08-30T11:50:56+01:00",
            "status" : "PASSED",
            "testKey" : "YANSB-74",
            "testInfo": {
                "summary": "Strong password validation",
                "type": "Automation",
                "projectKey": "YANSB",
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
                    }
                ]
            },
        }
    ]
}


template = {
    "tests": [
        {
            "status" : "",
            "testInfo": {
                "summary": "",
                "type": "Automation",
                "projectKey": "YANSB",
                "steps": ""
            },
        }
    ]
}