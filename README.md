# Megabuyte for Claude

Connect Claude to Megabuyte's UK technology sector intelligence.

This repository is a plugin marketplace with one plugin, **megabuyte**, which adds:

- **megabuyte-mcp**, an MCP server that gives Claude access to Megabuyte data
- Skills for company briefs, peer benchmarks, deal precedents, buyer and target screens, market maps and daily briefings

You'll need a Megabuyte account. Sign-in happens in your browser.

Follow the section for the app you use: [Claude desktop app](#claude-desktop-app-cowork) or [Claude Code](#claude-code).

---

## Claude desktop app (Cowork)

### Install

1. Open **Customize** in the left sidebar, then **Plugins**.
2. Click **+ Add** → **Add marketplace**.
3. Enter `https://github.com/megabuyte-git/megabuyte-plugins` and confirm.
4. Find **megabuyte** and click **Install**.

> **Can't see "Add marketplace"?** On Team and Enterprise plans, your Claude admin may need to allow it, or add the Megabuyte marketplace for your organization under **Organization settings → Plugins** on claude.ai.

### Sign in

1. In **Customize**, open the **megabuyte** plugin, then **Connectors**.
2. Next to **megabuyte-mcp**, click **Connect**.
3. Sign in to Megabuyte in the browser window and approve access.

To use it in a chat, switch on **megabuyte-mcp** in the **+** menu under **Connectors**.

---

## Claude Code

Requires a recent version of Claude Code with plugin support.

### Install

In a Claude Code session:

```
/plugin marketplace add https://github.com/megabuyte-git/megabuyte-plugins
/plugin install megabuyte@megabuyte-plugins
```

Or from your shell:

```bash
claude plugin marketplace add https://github.com/megabuyte-git/megabuyte-plugins
claude plugin install megabuyte@megabuyte-plugins
```

### Sign in (once)

The server shows as **needs authentication** until you sign in.

1. Run `/mcp` and select **plugin:megabuyte:megabuyte-mcp**. If it's disabled, choose **Enable** first, then reopen it.
2. Choose **Authenticate**, then sign in to Megabuyte in the browser tab that opens.
3. Return to Claude Code. The server should show as connected.

Claude Code stores and refreshes your tokens, so you'll only need to repeat this if access is revoked or expires.

### Verify

```bash
claude plugin list   # megabuyte should be listed and enabled
claude mcp list      # megabuyte-mcp should show as connected
```

### Update and uninstall

```
/plugin marketplace update megabuyte-plugins
/plugin uninstall megabuyte@megabuyte-plugins
```

To clear stored credentials: `/mcp` → **plugin:megabuyte:megabuyte-mcp** → **Clear authentication**.

---

## Try it

Ask Claude something like:

> "Give me a company brief on [company], including recent deals and its closest peers."

## Troubleshooting

- **Still says "needs authentication" (Claude Code):** run `/mcp`, select **plugin:megabuyte:megabuyte-mcp**, and choose **Authenticate** or **Re-authenticate**.
- **Tools not available in a chat (desktop app):** check that **megabuyte-mcp** is switched on in the **+** menu under **Connectors**.
- **Headless use (`claude -p`, Agent SDK):** sign-in can't happen there. Sign in once in an interactive session first.
- **Permission error on a tool call:** your Megabuyte subscription or role may not include that data. Contact your Megabuyte account manager.

## Support

[Contact Megabuyte](mailto:customersuccess@megabuyte.com)