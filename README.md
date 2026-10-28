# Megabuyte Plugins

Connect Claude (as well as ChatGPT and GitHub Copilot) to Megabuyte's UK technology sector intelligence.

This repository is a plugin marketplace with one plugin, **megabuyte**, which adds:

- **megabuyte-mcp**, an MCP server that gives Claude access to Megabuyte data
- Skills for company briefs, peer benchmarks, deal precedents, buyer and target screens, market maps and daily briefings

You'll need a Megabuyte account. Sign-in happens in your browser.

Follow the section for the app you use: [Claude desktop app](#claude-desktop-app-cowork), [Claude Code](#claude-code), [ChatGPT and Codex](#chatgpt-and-codex) or [GitHub Copilot](#github-copilot).

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

## ChatGPT and Codex

The same plugin works in the ChatGPT desktop app and Codex.

### Install

1. In the ChatGPT desktop app, open the **Plugins Directory**.
2. Add `https://github.com/megabuyte-git/megabuyte-plugins` as a marketplace.
3. Find **megabuyte** and click **Install**.

> **Can't add a marketplace?** In a ChatGPT workspace, your admin may need to publish the plugin to the workspace for you.

### Sign in

When you install, you'll be asked to connect **megabuyte-mcp**. Sign in to Megabuyte in the browser window and approve access.

---

## GitHub Copilot

The same plugin works in GitHub Copilot CLI and in Copilot Chat in VS Code.

### Install (Copilot CLI)

In a Copilot CLI session:

```
/plugin marketplace add megabuyte-git/megabuyte-plugins
/plugin install megabuyte@megabuyte-plugins
```

Or from your shell:

```bash
copilot plugin marketplace add megabuyte-git/megabuyte-plugins
copilot plugin install megabuyte@megabuyte-plugins
```

### Install (VS Code)

1. Open your user settings (JSON) and add the Megabuyte marketplace:

   ```json
   "chat.plugins.enabled": true,
   "chat.plugins.marketplaces": ["https://github.com/megabuyte-git/megabuyte-plugins.git"]
   ```

2. Run **Developer: Reload Window** from the Command Palette.
3. In the Chat view, select the cog, open **Agent Customizations**, then **Plugins**.
4. Find **megabuyte** and click **Install**.

### Sign in

1. In Copilot CLI, run `/mcp` and select **megabuyte-mcp**. In VS Code, run **MCP: List Servers**, select **megabuyte-mcp**, then **Start Server**.
2. Sign in to Megabuyte in the browser window that opens and approve access.

### Update and uninstall

```bash
copilot plugin update megabuyte
copilot plugin uninstall megabuyte
```

In VS Code, manage the plugin from **Agent Plugins - Installed** in the Extensions view.

---

## Try it

Ask Claude something like:

> "Give me a company brief on [company], including recent deals and its closest peers."

## Troubleshooting

- **Still says "needs authentication" (Claude Code):** run `/mcp`, select **plugin:megabuyte:megabuyte-mcp**, and choose **Authenticate** or **Re-authenticate**.
- **Tools not available in a chat (desktop app):** check that **megabuyte-mcp** is switched on in the **+** menu under **Connectors**.
- **Headless use (`claude -p`, Agent SDK):** sign-in can't happen there. Sign in once in an interactive session first.
- **Tools not available (ChatGPT or Codex):** open the **megabuyte** plugin in the Plugins Directory and check that **megabuyte-mcp** is connected. Reconnect it if sign-in has expired.
- **Tools not available (GitHub Copilot):** run `/mcp` in Copilot CLI, or **MCP: List Servers** in VS Code, and check that **megabuyte-mcp** is running and signed in. Restart it to sign in again.
- **Permission error on a tool call:** your Megabuyte subscription or role may not include that data. Contact your Megabuyte account manager.

## Support

[Contact Megabuyte](mailto:customersuccess@megabuyte.com)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how the skills are built and released.
