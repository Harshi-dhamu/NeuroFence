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
## Day 3 Progress

- Added Prompt Manager
- Implemented prompt filtering
- Added category support
- Added random prompt selection
- Expanded prompt dataset
## Day 4 Progress

- Added Fuzz Engine
- Added Prompt Generator
- Implemented batch generation
- Added sequential prompt retrieval
- Prepared the module for future scan integration
## Day 5 Progress

- Added prompt categorization
- Implemented High Risk prompts
- Implemented Medium Risk prompts
- Implemented Low Risk prompts
- Successfully tested risk categorization