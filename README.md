# mcp-client-proj
> [!WARNING]
> The files included in this repo have been created by GitHub Copilot.

This repository contains a simple MCP client script `mcp_client.py`.

Usage
-----

Run the script with Python 3:

```
python ./mcp_client.py
```

Notes
-----

- Tested on Windows.
- Add any project-specific dependencies or setup instructions here.

Create a private GitHub repository and push
-----------------------------------------

Option A (GitHub CLI):

If you have the GitHub CLI (`gh`) installed and authenticated on this machine, you can create a private repo and push with:

```
gh repo create <OWNER>/<REPO_NAME> --private --source=. --remote=origin --push
```

Option B (Personal Access Token):

Use the GitHub REST API to create a repo (replace `<TOKEN>` and `<REPO_NAME>`):

```
curl -H "Authorization: token <TOKEN>" -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\": \"<REPO_NAME>\", \"private\": true}"
```

Then add the remote and push:

```
git remote add origin https://github.com/<OWNER>/<REPO_NAME>.git
 git push -u origin main
```

If you'd like, I can create the remote and push for you. Reply with which method you prefer and either confirm that `gh` is logged in or paste a PAT (only if you consent).
