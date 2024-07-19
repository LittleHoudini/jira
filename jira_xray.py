import contextlib
from jira import JIRA
import logging
from enum import Enum
# Set up logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)
logger = logging.getLogger('jira_xray')
logger.setLevel(logging.DEBUG)

script_version=1.0


# Set up Atlasian connection
url = 'url'
username = "username"
password = 'password'
jira_project_name = 'jira_project_name'

class Members(Enum):
    YANIV_COHEN = "Yaniv Cohen"


class IssueTypes(Enum):
    STORY = 'Story'
    TASK = 'Task'
    BUG = 'Bug'
    EPIC = 'Epic'
    SUB_TASK = 'Sub-task'
    TEST = 'Test'
    XRAY_TEST = 'Xray Test'

    

class JiraXray(contextlib.ContextDecorator):
    def __init__(self, jira_project_name: str, url: str, username: str, password:str):
        self.jira = JIRA(server=url, basic_auth=(username, password))
        self.jira_project_name = jira_project_name
        self.porject_key = self.get_project().key
    ### GETTERS ###
    def get_project(self):
        projects = self.jira.projects()
        for project in projects:
            if project.key == self.jira_project_name:
                logger.info(f'Found project {project.key}')
                return project
        logger.error(f'Project {self.jira_project_name} not found')
        raise Exception(f'Project {self.jira_project_name} not found')
    
    
    def get_test_plans(self):
        test_plans = self.jira.search_issues(f'project = {self.jira_project_name} AND issuetype = {IssueTypes.TEST.value}')
        return test_plans

    def get_test_plan(self, test_plan_key: str):
        test_plan = self.jira.issue(test_plan_key)
        return test_plan

    def get_test_plan_tests(self, test_plan_key: str):
        test_plan = self.get_test_plan(test_plan_key)
        if test_plan is None:
            logger.error(f'Test plan {test_plan_key} not found')
            return None
        tests = self.jira.search_issues(f'project = {self.jira_project_name} AND "Test Plan" = {test_plan_key}')
        return tests

    def get_issue(self, issue_key: str):
        test = self.jira.issue(issue_key)
        return test

    def get_test_steps(self, test_key: str):
        test = self.get_test(test_key)
        if test is None:
            logger.error(f'Test {test_key} not found')
            return None
        test_steps = test.fields.customfield_10100
        return test_steps
    
    
    def update_issue(self, issue_key: str, fields: dict):
        issue = self.get_issue(issue_key)
        if issue is not None:
            res = issue.update(fields=fields)
            logger.debug(f'Updated issue, {res=}')
            return res
        return None
    

    def create_xray_issue(self, summary: str, description: str,  test_steps: list = [], test_plan_key: str="YANSB-20"):
        xray_test = self.jira.create_issue(project=self.jira_project_name, summary=summary, description=description, issuetype={'name': IssueTypes.XRAY_TEST.value}, 
                                           #customfield_10101=test_plan_key,
                                           #customfield_10100=test_steps
                                           )
        # res = xray_test.update(fields={'customfield_10101': test_plan_key, 'customfield_10100': test_steps})
        # logger.debug(f'Updated issue, {res=}')
        return xray_test

    def create_issue(self, summary: str, description: str, issuetype: IssueTypes, assignee: Members):
        # TODO: check why I cant update assignee
        issue = self.jira.create_issue(project=self.porject_key, summary=summary, description=description, issuetype={'name': issuetype},  assignee={'name': assignee})
        # res = issue.update(assignee={'name': assignee})
        # logger.debug(f'Updated issue, {res=}')
        logger.debug(f'Created issue, {issue=}, {issue.fields.assignee=}')
        logger.info(f'Created issue, {issue=},')
        return issue


class CreateXrayTest(JiraXray):
    def __init__(self, summary: str, description: str, test_steps: list = [], test_plan_key: str="YANSB-20", issuetype: IssueTypes=IssueTypes.XRAY_TEST, assignee:Members=Members.YANIV_COHEN, issue_key:str=None):
        super().__init__(jira_project_name=jira_project_name, url=url, username=username, password=password)
        self.summary = summary
        self.description = description
        self.test_steps = test_steps
        self.test_plan_key = test_plan_key
        self.issuetype = issuetype
        self.assignee = assignee
        self.issue_key = issue_key

    def __enter__(self):
        issue = self.get_issue(self.issue_key)
        if issue is None:
            self.issue = self.jira.create_issue(project=self.porject_key, summary=self.summary, description=self.description, issuetype={'name': self.issuetype},  assignee={'name': self.assignee})
            logger.info(f'Created New Issue, {self.issue=}')
        else:
            self.issue = self.update_issue(issue_key=self.issue_key, fields={'summary': self.summary, 'description': self.description, 'issuetype': {'name': self.issuetype}, 'assignee': {'name': self.assignee}})
            logger.info(f'Updated Existing Issue, {self.issue=}')
            
        

    def __exit__(self, *exc ):
        logger.info(f'Finished Xray test, {self.issue=}')


if __name__ == '__main__':
    jira_xray = JiraXray(jira_project_name=jira_project_name, url=url, username=username, password=password)
    # jira_xray.update_issue("issue_key":"YANSB-28", fields={"summary":"Hello World TEST TEST TEST HELLO", 
    #                                                        "description":"This is a test", 
    #                                                        "issuetype":IssueTypes.XRAY_TEST.value, 
    #                                                        "assignee":Members.YANIV_COHEN.value}
    #                        )
    # create_xray_issue = jira_xray.create_xray_test(summary='Test 16', description='Test 12 description', test_steps=['Step 1', 'Step 2', 'Step 3'])