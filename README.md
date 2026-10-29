# Wisdom Tools

Public tools by Darren Schaeffer to help you live your most authentic life.

[Substack](https://substack.com/@darrenschaeffer) · [LinkedIn](https://linkedin.com/in/darrenschaeffer)

## Tools

| Tool | What it does |
|---|---|
| [Inkling](plugins/inkling) | Try AI divination using tarot, Lenormand, or the I Ching. |

Each tool has its own page with install steps and instructions.

## Get every tool in Claude

Turn on code execution (Settings, then Capabilities). Then go to Customize, then Plugins, then Add, then Add marketplace, and type `DarrenSchaeffer/wisdom-tools`. Every tool here shows up in the list, and new ones appear as they're added.

## License

Free for personal use. All rights reserved: don't change, share, or republish these tools without permission. For commercial use, contact the author on Substack. See [LICENSE](LICENSE).

## Development

```
python3 -m unittest discover tests
./scripts/build_plugin_zip.sh   # builds dist/inkling-plugin.zip
claude plugin validate . --strict
```
