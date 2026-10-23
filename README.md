# Inkling

Clarity on your own life, through divination. Inkling reads tarot (Celtic Cross), Lenormand (3x3 grid), and the I Ching (one hexagram) inside your AI chatbot. The cards and coins come from a small script that ships with the skill, so every cast is random and checkable.

By Darren Schaeffer ([Substack](https://substack.com/@darrenschaeffer), [LinkedIn](https://linkedin.com/in/darrenschaeffer), X [@dasc8079](https://x.com/dasc8079)). Free for personal use under CC BY-NC-SA 4.0.

You can read exactly what it does: the skill's instructions are in [SKILL.md](plugins/inkling/skills/inkling/SKILL.md), the shuffle is in [cast.py](plugins/inkling/skills/inkling/scripts/cast.py), and a paste-in version for any chatbot is in [PROMPT.md](PROMPT.md).

## How to use

- Ask one question at a time. Ramble or use voice input if you like; Inkling works out what's worth asking.
- It picks tarot, Lenormand, or the I Ching to fit the question, then shows you the refined question. Reply Y to confirm, and it casts.
- The answer comes first. Below it are the details of the cast, for checking and learning.
- You're still responsible for your choices.

## Install

Download files are on the [Releases page](https://github.com/dasc8079/public-plugins/releases/latest).

### Claude (web, desktop, or mobile)

1. Turn on code execution: Settings, then Capabilities.
2. Download `inkling-plugin.zip`.
3. Customize, then Plugins, then Add, then Upload plugin. Pick the zip.

No Plugins option on your plan? Download `inkling-skill.zip` instead, then Customize, then Skills, then "+", then Upload a skill.

### Claude Code

```
/plugin marketplace add dasc8079/public-plugins
/plugin install inkling@darrenschaeffer
```

### ChatGPT

If your plan lets you add skills, upload `inkling-skill.zip` as a skill. Otherwise, start a new chat and paste in the prompt from [PROMPT.md](PROMPT.md). Not yet tested in ChatGPT.

### Gemini

If your account has skills, create one and upload `inkling-skill.zip`. Otherwise, start a new chat and paste in the prompt from [PROMPT.md](PROMPT.md). Not yet tested in Gemini.

### Microsoft Copilot

Copilot doesn't take skills. Start a new chat and paste in the prompt from [PROMPT.md](PROMPT.md).

## License

CC BY-NC-SA 4.0: share and adapt it with credit, non-commercially, under the same terms. For commercial use, contact the author on Substack. See [LICENSE](LICENSE).

## Development

```
python3 -m unittest discover tests
./scripts/build_skill_zip.sh   # builds both zips into dist/
claude plugin validate . --strict
```
