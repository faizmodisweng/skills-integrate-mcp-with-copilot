#!/usr/bin/env python3
"""
Script to create GitHub issues from issues_data.json

This script reads the issues_data.json file and creates GitHub issues
using the GitHub API. It requires a GitHub personal access token with
'repo' scope.

Usage:
    python create_issues.py --token YOUR_GITHUB_TOKEN --repo OWNER/REPO

Example:
    python create_issues.py --token ghp_xxxx --repo faizmodisweng/skills-integrate-mcp-with-copilot

Environment Variables:
    GITHUB_TOKEN: GitHub personal access token (alternative to --token)
    GITHUB_REPOSITORY: Repository in format OWNER/REPO (alternative to --repo)
"""

import json
import os
import sys
import argparse
import requests
from typing import List, Dict, Any


def load_issues_data(file_path: str = "issues_data.json") -> List[Dict[str, Any]]:
    """Load issues data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        sys.exit(1)


def create_github_issue(
    token: str,
    repo: str,
    title: str,
    body: str,
    labels: List[str]
) -> Dict[str, Any]:
    """
    Create a GitHub issue using the GitHub API.
    
    Args:
        token: GitHub personal access token
        repo: Repository in format 'owner/repo'
        title: Issue title
        body: Issue body (description)
        labels: List of label names
    
    Returns:
        Response data from GitHub API
    """
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "body": body,
        "labels": labels
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error creating issue '{title}': {response.status_code}")
        print(f"Response: {response.text}")
        return None


def main():
    """Main function to create all issues."""
    parser = argparse.ArgumentParser(
        description="Create GitHub issues from issues_data.json"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token",
        default=os.environ.get("GITHUB_TOKEN")
    )
    parser.add_argument(
        "--repo",
        help="Repository in format OWNER/REPO",
        default=os.environ.get("GITHUB_REPOSITORY")
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print issues without creating them"
    )
    parser.add_argument(
        "--file",
        default="issues_data.json",
        help="Path to issues data JSON file (default: issues_data.json)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.dry_run and not args.token:
        print("Error: GitHub token is required. Provide via --token or GITHUB_TOKEN env var")
        sys.exit(1)
    
    if not args.repo:
        print("Error: Repository is required. Provide via --repo or GITHUB_REPOSITORY env var")
        sys.exit(1)
    
    # Load issues data
    issues = load_issues_data(args.file)
    print(f"Loaded {len(issues)} issues from {args.file}")
    
    if args.dry_run:
        print("\nDRY RUN - Issues that would be created:")
        print("=" * 80)
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['title']}")
            print(f"   Labels: {', '.join(issue['labels'])}")
            print(f"   Body preview: {issue['body'][:100]}...")
        print("\n" + "=" * 80)
        print(f"\nTo create these issues, run without --dry-run flag")
        return
    
    # Create issues
    created_issues = []
    failed_issues = []
    
    print(f"\nCreating issues in repository: {args.repo}")
    print("=" * 80)
    
    for i, issue_data in enumerate(issues, 1):
        print(f"\n[{i}/{len(issues)}] Creating: {issue_data['title']}")
        
        result = create_github_issue(
            token=args.token,
            repo=args.repo,
            title=issue_data['title'],
            body=issue_data['body'],
            labels=issue_data['labels']
        )
        
        if result:
            created_issues.append(result)
            print(f"✓ Created: {result['html_url']}")
        else:
            failed_issues.append(issue_data['title'])
            print(f"✗ Failed to create issue")
    
    # Summary
    print("\n" + "=" * 80)
    print(f"\nSummary:")
    print(f"  Total issues: {len(issues)}")
    print(f"  Successfully created: {len(created_issues)}")
    print(f"  Failed: {len(failed_issues)}")
    
    if created_issues:
        print(f"\n✓ Created issues:")
        for issue in created_issues:
            print(f"  - #{issue['number']}: {issue['title']}")
            print(f"    {issue['html_url']}")
    
    if failed_issues:
        print(f"\n✗ Failed issues:")
        for title in failed_issues:
            print(f"  - {title}")
        sys.exit(1)
    
    print("\n✓ All issues created successfully!")


if __name__ == "__main__":
    main()
