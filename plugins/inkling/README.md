# Inkling

Inkling is a free plugin that lets you try AI divination using tarot, Lenormand, or the I Ching.

By Darren Schaeffer ([Substack](https://substack.com/@darrenschaeffer), [LinkedIn](https://linkedin.com/in/darrenschaeffer)).

**This is a starter plugin:** a single plugin can't hold enough instructions to make it fully reliable, and chatbots can still skip steps or get things wrong.

## How it works

1. **Start with "Use Inkling":** "Use Inkling to give me a reading on [your question]."
2. **Ask one question at a time.** If you're not sure what to ask, use voice input and ramble about your situation. It will pick out the question for you and choose the appropriate system.
3. **Confirm the question.** It turns what you said into a clear question and shows it to you before it casts. Look it over and make sure it's right.
4. **It shuffles in code,** so the AI can't skip it or make up the cards.
5. **Receive insight.** The answer comes first, with the details below it, so you can check the reading and learn from it.

A reading can show you the shape of what's happening, but the choice is yours, and so is walking the path.

## Reading ethically

Divination is a powerful tool. If you're new to it, here are a few guidelines:

- **Read only for yourself,** about your own life. Inkling won't do readings about other people.
- **Some topics come back to you.** Questions about death, health, legal matters, and money turn toward your side of the situation.
- **Take the answer you get.** Don't draw again for a better one.

For health, legal, or money decisions, a reading can help you think, and a professional can give you advice.

## What's inside

- **The instructions** are in [SKILL.md](skills/inkling/SKILL.md). A paste-in version for any chatbot is in [PROMPT.md](PROMPT.md).
- **The shuffle** is in [cast.py](skills/inkling/scripts/cast.py). It does one thing: shuffles the cards or tosses the coins, then prints the result. It uses only Python's built-in `random` and `sys` modules, makes no network calls, reads no files, and saves nothing. The repo's tests check this.
- **No web searches or images.** Your conversation stays wherever your chatbot normally keeps it; Inkling adds no storage of its own.

## Install

Inkling installs as a plugin in Claude and ChatGPT.

### Claude (web, desktop, or mobile)

1. Turn on code execution: Settings, then Capabilities.
2. Go to Customize, then Plugins, then Add, then Add marketplace. Type `DarrenSchaeffer/wisdom-tools` (this GitHub page, not Anthropic's store).
3. Install Inkling from the list. When a new version comes out, use Check for updates.

Or upload it instead:

1. Download [inkling-plugin.zip](https://github.com/DarrenSchaeffer/wisdom-tools/releases/latest/download/inkling-plugin.zip).
2. Go to Customize, then Plugins, then Add, then Upload plugin. Pick the zip.

### ChatGPT

1. Download [inkling-plugin.zip](https://github.com/DarrenSchaeffer/wisdom-tools/releases/latest/download/inkling-plugin.zip).
2. Go to Plugins, then Add, then Upload a plugin from archive. Pick the zip.
3. On the next screen, click Install. Uploading alone doesn't turn it on.
4. Start a new chat.

### Coding assistants (Claude Code, Codex, GitHub Copilot, and others)

Paste this in:

```
Install the Inkling plugin from https://github.com/DarrenSchaeffer/wisdom-tools
```

In Claude Code you can also run:

```
/plugin marketplace add DarrenSchaeffer/wisdom-tools
/plugin install inkling@darrenschaeffer
```

To get new versions automatically in Claude Code: run `/plugin`, open the Marketplaces tab, select this marketplace, and choose Enable auto-update. Otherwise, update by hand: `/plugin`, then Installed, then Inkling, then Update now.

### Any other chatbot (Gemini, Microsoft Copilot, and others)

Start a new chat and paste in [the prompt](PROMPT.md).

All downloads are on the [Releases page](https://github.com/DarrenSchaeffer/wisdom-tools/releases/latest).

## Example prompts

- "Use Inkling to give me a reading on my creative work."
- "Use Inkling to cast the I Ching: should I start writing every morning?"
- "Use Inkling with Lenormand: what's going on with my job search?"

## Support

Questions and feedback: [Substack](https://substack.com/@darrenschaeffer) or [GitHub issues](https://github.com/DarrenSchaeffer/wisdom-tools/issues).

## License

Free for personal use. All rights reserved: don't change, share, or republish it without permission. For commercial use, contact the author on Substack. See [LICENSE](LICENSE).
