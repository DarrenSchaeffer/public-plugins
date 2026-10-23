# Inkling

I built a free skill called Inkling, an introduction to AI-based divination built on the tarot, I Ching, or Lenormand systems, so you can try it yourself.

By Darren Schaeffer ([Substack](https://substack.com/@darrenschaeffer), [LinkedIn](https://linkedin.com/in/darrenschaeffer)).

**This is a starter skill:** a single skill can't hold enough instructions to make it fully reliable, and chatbots can still skip steps or get things wrong.

## How it works

1. **Ask one question at a time.** If you're not sure what to ask, use voice input and ramble about your situation. It will pick out the question for you and choose the appropriate system.
2. **Confirm the question.** It turns what you said into a clear question and shows it to you before it casts. Look it over and make sure it's right.
3. **It casts in code,** so the AI can't skip the shuffle or make up the cards.
4. **Receive insight.** The answer comes first, with the details below it, so you can check the reading and learn from it.

A reading can show you the shape of what's happening, but the choice is yours, and so is walking the path.

## Reading ethically

Divination is a powerful tool. If you're new to it, here are a few guidelines:

- **Read only for yourself,** about your own life. Inkling won't do readings about other people.
- **Some topics come back to you.** Questions about death, health, legal matters, and money turn toward your side of the situation.
- **Take the answer you get.** Don't draw again for a better one.

For health, legal, or money decisions, a reading can help you think, and a professional can give you advice.

## What's inside

- **The instructions** are in [SKILL.md](plugins/inkling/skills/inkling/SKILL.md). A paste-in version for any chatbot is in [PROMPT.md](PROMPT.md).
- **The shuffle** is in [cast.py](plugins/inkling/skills/inkling/scripts/cast.py). It does one thing: shuffles the cards or tosses the coins, then prints the result. It uses only Python's built-in `random` and `sys` modules, makes no network calls, reads no files, and saves nothing. The repo's tests check this.
- **No web searches or images.** Your conversation stays wherever your chatbot normally keeps it; Inkling adds no storage of its own.

## Install

Inkling installs as a plugin in Claude and ChatGPT. Both need the plugin file, [inkling-plugin.zip](https://github.com/DarrenSchaeffer/public-plugins/releases/latest/download/inkling-plugin.zip), unless you use Claude's marketplace option below.

### Claude (web, desktop, or mobile)

1. Turn on code execution: Settings, then Capabilities.
2. Customize, then Plugins, then Add, then Add marketplace. Paste `DarrenSchaeffer/public-plugins`, then install Inkling. To get new versions, use Check for updates, or turn on Sync automatically.

Or download [inkling-plugin.zip](https://github.com/DarrenSchaeffer/public-plugins/releases/latest/download/inkling-plugin.zip) and use Customize, then Plugins, then Add, then Upload plugin.

### ChatGPT

1. Download [inkling-plugin.zip](https://github.com/DarrenSchaeffer/public-plugins/releases/latest/download/inkling-plugin.zip).
2. Go to Plugins and upload it as a plugin. Use the plugin zip, not the skill upload: in testing, the plugin worked and the bare skill did not.
3. Start a new chat and ask for a reading.

### Coding assistants (Claude Code, Codex, and others)

Ask it: "Install the Inkling plugin from https://github.com/DarrenSchaeffer/public-plugins". In Claude Code you can also run:

```
/plugin marketplace add DarrenSchaeffer/public-plugins
/plugin install inkling@darrenschaeffer
```

### Any other chatbot (Gemini, Microsoft Copilot, and others)

Start a new chat and paste in the prompt from [PROMPT.md](PROMPT.md). The Gemini app can't run Inkling's shuffle script, so the prompt is the way in there.

All downloads are on the [Releases page](https://github.com/DarrenSchaeffer/public-plugins/releases/latest).

## License

CC BY-NC-SA 4.0: share and adapt it with credit, non-commercially, under the same terms. For commercial use, contact the author on Substack. See [LICENSE](LICENSE).

## Development

```
python3 -m unittest discover tests
./scripts/build_skill_zip.sh   # builds both zips into dist/
claude plugin validate . --strict
```
