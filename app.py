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
    if not prs:
        return "NOT OK"
    full_prs = [repo.get_pull(int(pr)) for pr in prs]
    for pr in full_prs:
        add_comment(repo, pr, full_prs, request.query_string, request.args)
        
    return "OK"

def add_comment(repo, pr, full_prs, raw_data, req_args):
    print(f"raw_data: {raw_data}")

    round_id = req_args.get('roundId', '-1')
    unique_runtimes = req_args.get('uniqueRuntimes', '-1')
    total_runtimes = req_args.get('totalRuntimes', '-1')
    server_commit = req_args.get('commit', 'unknown')
    prs = req_args.get('prs', '').split(',')

    pr_list = [f"{pr.url} ({pr.title})" for pr in full_prs]

    message = f"""
Round {round_id} @ {commit}
=====
Runtimes: {unique_runtimes} ({total_runtimes} total)
- {pr_list.join('\n-')}
    """


    pr.create_issue_comment(message)