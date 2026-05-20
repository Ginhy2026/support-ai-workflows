# Troubleshooting

## lark-cli Not Found

Cause:

- `@larksuite/cli` is not installed.
- npm global bin directory is not in PATH.

Next step:

```powershell
npm install -g @larksuite/cli
```

## PowerShell Blocks lark-cli.ps1

Error pattern:

```text
cannot be loaded because running scripts is disabled
```

Next step:

```powershell
lark-cli.cmd --version
```

Use the `.cmd` wrapper instead of changing execution policy.

## Not Logged In

Symptoms:

- `auth status` shows no user.
- token is missing or expired.

Next step:

```powershell
lark-cli auth login --domain search --recommend
```

## Missing search:docs:read

Symptoms:

- `auth check --scope "search:docs:read"` returns `ok: false`.
- Search returns `No permission`.

Next steps:

1. Ensure the Feishu app has the document search permission enabled.
2. Publish or approve the updated app permission.
3. Re-run user login:

```powershell
lark-cli auth login --domain search --recommend
```

## Search Returns Zero Results

Possible causes:

- Keywords are too specific.
- The current user cannot access the target knowledge base.
- The article uses different terminology.
- The target content is not indexed yet.

Try broader terms:

```text
CC1 噪音
CC1 异响
CC1 刮条
CC1 刮水
CT4
屏幕倒置
```

## User Has No Document Access

CLI authentication can be valid while search still cannot find internal documents. The user must have Feishu document or knowledge-base access through normal Feishu permissions.
