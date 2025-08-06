#!/usr/bin/env python3

import os
import uuid
import sqlite3
import requests
from github import Github
from datetime import datetime

# Basic configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite')
REPO_NAME = "Emmanuel-Odero/nilotic-network"
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')  # Set this in your environment

# Initialize GitHub API client
g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else None

def get_db():
    """Get a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_repo():
    """Fetch the Nilotic Network repository from GitHub"""
    if not g:
        print("GitHub token not provided. Please set GITHUB_TOKEN environment variable.")
        return None

    try:
        repo = g.get_repo(REPO_NAME)
        return repo
    except Exception as e:
        print(f"Error fetching repo: {str(e)}")
        return None

def get_file_content(repo, path):
    """Get the content of a file from the repository"""
    try:
        content = repo.get_contents(path)
        return content.decoded_content.decode('utf-8')
    except Exception as e:
        print(f"Error getting file content for {path}: {str(e)}")
        return None

def analyze_code(file_content, file_path):
    """Analyze code for issues and potential fixes"""
    issues = []

    # Example: Look for the supply calculation bug in main.cpp
    if 'main.cpp' in file_path and 'totalSupply = blockchain.getChain().size() * 10.0' in file_content:
        issue_id = str(uuid.uuid4())
        issues.append({
            'id': issue_id,
            'title': 'Incorrect supply calculation in /chain endpoint',
            'description': 'The total supply is incorrectly calculated using chain.size() * 10.0 instead of tracking the actual circulating supply',
            'severity': 'medium',
            'status': 'open',
            'file_path': file_path,
            'line_number': find_line_number(file_content, 'totalSupply = blockchain.getChain().size() * 10.0'),
            'suggested_fix': 'Replace with: totalSupply = blockchain.getCurrentSupply();'
        })

        # For this example, we'll also need to suggest adding the getCurrentSupply method
        if 'blockchain.cpp' in file_path and 'double getCurrentSupply() const' not in file_content:
            issue_id = str(uuid.uuid4())
            issues.append({
                'id': issue_id,
                'title': 'Missing getCurrentSupply() method in Blockchain class',
                'description': 'Need to implement a method to track and return the current supply of SLW tokens',
                'severity': 'medium',
                'status': 'open',
                'file_path': file_path,
                'line_number': 0,  # Would need to find the appropriate line in a real implementation
                'suggested_fix': '''
// Add to the Blockchain class in blockchain.h:
double getCurrentSupply() const;

// Add implementation in blockchain.cpp:
double Blockchain::getCurrentSupply() const {
    double supply = 0.0;
    // Add pre-mined supply (35% of 555M)
    supply += 555000000.0 * 0.35;
    // Add block rewards (5 SLW per block)
    supply += getChain().size() * 5.0;
    return supply;
}
'''
            })

    # In a real implementation, we'd have many more code analysis rules

    return issues

def find_line_number(content, search_string):
    """Find the line number of a string in the content"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if search_string in line:
            return i + 1
    return 0

def save_issues(issues):
    """Save identified issues to the database"""
    conn = get_db()
    cursor = conn.cursor()

    for issue in issues:
        # Check if issue already exists
        existing = cursor.execute(
            'SELECT id FROM issues WHERE title = ? AND file_path = ?',
            (issue['title'], issue['file_path'])
        ).fetchone()

        if not existing:
            cursor.execute('''
                INSERT INTO issues (id, title, description, severity, status, file_path, line_number, suggested_fix)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                issue['id'],
                issue['title'],
                issue['description'],
                issue['severity'],
                issue['status'],
                issue['file_path'],
                issue['line_number'],
                issue['suggested_fix']
            ))

    conn.commit()
    conn.close()

def create_pull_request(repo, issue):
    """Create a pull request to fix an issue"""
    if not repo:
        return None

    try:
        # Create a new branch for the PR
        base_branch = repo.default_branch
        branch_name = f"fix/{issue['id'][:8]}"

        # Get the content of the file to modify
        file_content = get_file_content(repo, issue['file_path'])
        if not file_content:
            return None

        # Apply the fix (in a real implementation, this would be more sophisticated)
        if 'totalSupply = blockchain.getChain().size() * 10.0' in file_content:
            new_content = file_content.replace(
                'totalSupply = blockchain.getChain().size() * 10.0',
                'totalSupply = blockchain.getCurrentSupply();'
            )

            # Create a new branch
            source_branch = repo.get_branch(base_branch)
            repo.create_git_ref(f"refs/heads/{branch_name}", source_branch.commit.sha)

            # Update the file
            repo.update_file(
                path=issue['file_path'],
                message=f"Fix: {issue['title']}",
                content=new_content,
                sha=repo.get_contents(issue['file_path']).sha,
                branch=branch_name
            )

            # Create the PR
            pr = repo.create_pull(
                title=f"Fix: {issue['title']}",
                body=f"""
This PR fixes issue {issue['id'][:8]}.

Problem:
{issue['description']}

Fix:
{issue['suggested_fix']}

Fixed by: Atim AI Assistant
""",
                head=branch_name,
                base=base_branch
            )

            # Save the PR info to database
            conn = get_db()
            cursor = conn.cursor()

            pr_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO pull_requests
                (id, github_id, title, description, status, diff, html_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                pr_id,
                pr.number,
                f"Fix: {issue['title']}",
                issue['description'],
                'open',
                f"Replaced 'totalSupply = blockchain.getChain().size() * 10.0' with 'totalSupply = blockchain.getCurrentSupply();'",
                pr.html_url
            ))

            # Update the issue status
            cursor.execute('''
                UPDATE issues SET status = ? WHERE id = ?
            ''', ('in-progress', issue['id']))

            conn.commit()
            conn.close()

            return pr
    except Exception as e:
        print(f"Error creating PR: {str(e)}")
        return None

def main():
    """Main function to run Atim's core code analysis"""
    print("Starting Atim - Nilotic Network AI Assistant")

    # Fetch repository
    repo = fetch_repo()
    if not repo:
        print("Failed to fetch repository.")
        return

    print(f"Analyzing repository: {REPO_NAME}")

    # Analyze important files
    target_files = [
        'src/main.cpp',
        'src/blockchain.cpp',
        'src/blockchain.h'
    ]

    all_issues = []
    for file_path in target_files:
        print(f"Analyzing {file_path}...")
        content = get_file_content(repo, file_path)
        if content:
            issues = analyze_code(content, file_path)
            all_issues.extend(issues)
            print(f"Found {len(issues)} issues in {file_path}")

    # Save issues to database
    save_issues(all_issues)
    print(f"Saved {len(all_issues)} issues to database")

    # Create pull requests for high-priority issues
    for issue in all_issues:
        if issue['status'] == 'open' and issue['severity'] in ['high', 'medium']:
            if 'totalSupply = blockchain.getChain().size() * 10.0' in issue['suggested_fix']:
                print(f"Creating PR for issue: {issue['title']}")
                pr = create_pull_request(repo, issue)
                if pr:
                    print(f"Created PR #{pr.number}: {pr.html_url}")
                    break  # Only create one PR for this example

if __name__ == "__main__":
    main()
