import os
from github import Github


from flask import Flask, request
app = Flask(__name__)

repo_org = os.getenv('REPO_ORG')
repo_name = os.getenv('REPO_NAME')
gh_token = os.getenv('GITHUB_TOKEN')

@app.route('/')
def index():
    g = Github(gh_token)
    repo = g.get_repo(f'{repo_org}/{repo_name}')
    prs = request.args.get('prs','').split(',')
    for pr in prs:
        if not pr or not request.query_string:
            continue
        add_comment(repo, pr, request.query_string)
        
    return "OK"

def add_comment(repo, pr_number, data):
    print(f"repo: {repo}, pr: {pr_number}, data: {data}")
    pr = repo.get_pull(int(pr_number))
    pr.create_issue_comment(f'Test Comment, raw data: {data}')