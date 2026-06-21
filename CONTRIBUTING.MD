# Contributing to carb-trak

Want to add new emission parameters or refine calculation constants? Here is the flow:
1. Open `data/emission_factors.py`.
2. Append your items directly to the `FACTORS` dictionary.
3. Track and verify your adjustments by running the automated suite:
```bash
   uv run pytest test_app.py -v```
Open a pull request against the main branch.
