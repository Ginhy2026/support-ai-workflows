# Commands

## Check Node.js

```powershell
node --version
```

## Check lark-cli

```powershell
lark-cli --version
```

Windows PowerShell fallback:

```powershell
lark-cli.cmd --version
```

## Install lark-cli Manually

Do not run automatically unless the user explicitly chooses to do so.

```powershell
npm install -g @larksuite/cli
```

If PowerShell blocks `npm.ps1`, use:

```powershell
npm.cmd install -g @larksuite/cli
```

## Login

```powershell
lark-cli auth login --domain search --recommend
```

The command may open a browser authorization page. The user must complete the login.

## Check Status

```powershell
lark-cli auth status
```

Expected:

- `identity` is `user`
- `tokenStatus` is `valid`
- `scope` includes `search:docs:read`

## Check Scope

```powershell
lark-cli auth check --scope "search:docs:read"
```

Expected:

```json
{
  "ok": true,
  "granted": ["search:docs:read"]
}
```

## Search Feishu Documents

```powershell
lark-cli drive +search --query "CT4" --doc-types wiki,docx --page-size 10 --format json
```

## Search Through Repository Wrapper

```powershell
python tools\feishu_search_docs.py "CT4" --type wiki --type docx --count 5
```
