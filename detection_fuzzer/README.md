# Detection & Fuzzing

Assigned Member: Dhruti

This module is responsible for:
- Generating adversarial prompts
- Executing fuzz tests
- Detecting anomalous model behavior
## Day 2 Progress

- Created `loader.py` to load prompts from `prompts/prompts.json`
- Added exception handling for:
  - FileNotFoundError
  - JSONDecodeError
- Successfully tested the prompt loader.