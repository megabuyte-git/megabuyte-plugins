# Megabuyte Plugins

Connect Claude (as well as ChatGPT and GitHub Copilot) to Megabuyte's UK technology sector intelligence.

This repository is a plugin marketplace with one plugin, **megabuyte**, which adds skills for company briefs, peer benchmarks, deal precedents, buyer and target screens, market maps and daily briefings.

## Before you start

The plugin does **not** include the Megabuyte MCP server. The skills rely on it for data, so you must already have installed the Megabuyte MCP server in your app and signed in, following its own install instructions. You'll need a Megabuyte account for this.

Follow the section for the app you use: [Claude desktop app](#claude-desktop-app-cowork), [Claude Code](#claude-code), [ChatGPT and Codex](#chatgpt-and-codex) or [GitHub Copilot](#github-copilot).

---

## Claude desktop app (Cowork)

### Install

1. Open **Customize** in the left sidebar, then **Plugins**.
2. Click **+ Add** → **Add marketplace**.
3. Enter `https://github.com/megabuyte-git/megabuyte-plugins` and confirm.
4. Find **megabuyte** and click **Install**.

> **Can't see "Add marketplace"?** On Team and Enterprise plans, your Claude admin may need to allow it, or add the Megabuyte marketplace for your organization under **Organization settings → Plugins** on claude.ai.

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

### Verify

```bash
claude plugin list   # megabuyte should be listed and enabled
```

### Update and uninstall

```
/plugin marketplace update megabuyte-plugins
/plugin uninstall megabuyte@megabuyte-plugins
```

---

## ChatGPT and Codex

The same plugin works in the ChatGPT desktop app and Codex.

### Install

1. In the ChatGPT desktop app, open the **Plugins Directory**.
2. Add `https://github.com/megabuyte-git/megabuyte-plugins` as a marketplace.
3. Find **megabuyte** and click **Install**.

> **Can't add a marketplace?** In a ChatGPT workspace, your admin may need to publish the plugin to the workspace for you.

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

- **Skills run but return no Megabuyte data:** the plugin doesn't include the MCP server. Check that the Megabuyte MCP server is installed, switched on and signed in, following its own install instructions.
- **Permission error on a tool call:** your Megabuyte subscription or role may not include that data. Contact your Megabuyte account manager.

## Support

[Contact Megabuyte](mailto:customersuccess@megabuyte.com)