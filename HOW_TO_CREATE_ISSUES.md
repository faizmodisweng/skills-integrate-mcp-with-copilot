# Creating GitHub Issues from ISSUES_TO_CREATE.md

This guide explains how to create GitHub issues from the `ISSUES_TO_CREATE.md` file.

## Overview

The repository contains:
- **`ISSUES_TO_CREATE.md`**: Original document with 10 proposed issues for SLIIT RSVP feature set
- **`issues_data.json`**: Structured JSON file with all issue data (titles, descriptions, labels, acceptance criteria)
- **`create_issues.py`**: Python script to automatically create the issues via GitHub API

## Quick Start

### Option 1: Using the Python Script (Recommended)

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Create a GitHub Personal Access Token:**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a name like "Create Issues Script"
   - Select scope: `repo` (full control of private repositories)
   - Click "Generate token" and copy the token

3. **Run the script with dry-run to preview:**
   ```bash
   python create_issues.py --token YOUR_TOKEN --repo faizmodisweng/skills-integrate-mcp-with-copilot --dry-run
   ```

4. **Create the issues:**
   ```bash
   python create_issues.py --token YOUR_TOKEN --repo faizmodisweng/skills-integrate-mcp-with-copilot
   ```

### Option 2: Using Environment Variables

```bash
export GITHUB_TOKEN="your_github_token_here"
export GITHUB_REPOSITORY="faizmodisweng/skills-integrate-mcp-with-copilot"
python create_issues.py
```

### Option 3: Using GitHub CLI (gh)

If you have the GitHub CLI installed and authenticated:

```bash
# Loop through each issue in the JSON file
cat issues_data.json | jq -c '.[]' | while read issue; do
  title=$(echo $issue | jq -r '.title')
  body=$(echo $issue | jq -r '.body')
  labels=$(echo $issue | jq -r '.labels | join(",")')
  
  gh issue create --title "$title" --body "$body" --label "$labels"
done
```

## Issues to be Created

The following 10 issues will be created:

1. **Scaffold React SPA and routing** (enhancement, frontend, setup)
   - Estimate: 3-5 points

2. **Implement Events page and `EventCard` component** (enhancement, frontend, api-integration)
   - Estimate: 5-8 points

3. **Add Ticket component for printable tickets** (feature, frontend, ux)
   - Estimate: 3-5 points

4. **Clubs directory page** (enhancement, frontend)
   - Estimate: 3 points

5. **Add React Query and replace manual fetches** (improvement, frontend, tech-debt)
   - Estimate: 2-4 points

6. **Add Login UI (Google button + email form)** (feature, frontend, auth)
   - Estimate: 2-3 points

7. **Contact page and contact form submission** (enhancement, frontend, api-integration)
   - Estimate: 2-4 points

8. **Move static frontend assets into `frontend/` and update FastAPI static mount** (maintenance, infra)
   - Estimate: 1-2 points

9. **Persist activities to a simple database (SQLite)** (backend, database, enhancement)
   - Estimate: 5-8 points

10. **Protect signup/unregister endpoints with basic auth or token** (security, backend)
    - Estimate: 2-4 points

## Script Features

- **Dry-run mode**: Preview issues before creating them
- **Error handling**: Reports which issues were created successfully and which failed
- **Detailed output**: Shows issue numbers and URLs after creation
- **Environment variable support**: Can use `GITHUB_TOKEN` and `GITHUB_REPOSITORY` env vars
- **Label support**: Automatically applies labels to created issues

## Troubleshooting

### Authentication Errors

If you get a 401 Unauthorized error:
- Verify your token is valid and has `repo` scope
- Make sure the token hasn't expired
- Check that you have write access to the repository

### Rate Limiting

If you hit GitHub's rate limit:
- Wait for the rate limit to reset (check the `X-RateLimit-Reset` header)
- Or authenticate with a token (authenticated requests have higher limits)

### Missing Dependencies

If you get `ModuleNotFoundError: No module named 'requests'`:
```bash
pip install requests
```

## Manual Creation

If you prefer to create issues manually, you can:
1. Open `issues_data.json` to see the structured data
2. Navigate to https://github.com/faizmodisweng/skills-integrate-mcp-with-copilot/issues/new
3. Copy the title, body, and labels from each entry in the JSON file

## Example Output

```
Loaded 10 issues from issues_data.json

Creating issues in repository: faizmodisweng/skills-integrate-mcp-with-copilot
================================================================================

[1/10] Creating: Scaffold React SPA and routing
✓ Created: https://github.com/faizmodisweng/skills-integrate-mcp-with-copilot/issues/2

[2/10] Creating: Implement Events page and `EventCard` component
✓ Created: https://github.com/faizmodisweng/skills-integrate-mcp-with-copilot/issues/3

...

================================================================================

Summary:
  Total issues: 10
  Successfully created: 10
  Failed: 0

✓ All issues created successfully!
```

## Notes

- The script creates issues sequentially to avoid overwhelming the GitHub API
- Each issue includes properly formatted markdown with acceptance criteria as checklists
- Labels are automatically applied (make sure these labels exist in your repository)
- The script reports the issue number and URL for each created issue
