# Akinator Automation API

A simple tool to enable automation of Akinator games using an LLM.

## Installation

Install directly from GitHub (branch `akinator-api`):

```bash
pip install git+https://github.com/Varker00/akinator-automation.git@akinator-api
```

## Usage

```python
from akinator-api import AkinatorGame, AkiCategories

# Specify game category, function that will provide the answers (eg. input). Enable debug prints if needed (optional).
game = AkinatorGame(AkiCategories.CHARACTERS, input, debug_print=True
game.start_game()
```

That's it!

Results will be saved to ./results/{date_and_time}.json
