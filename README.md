# LLM Workflow Prototype: Sales Follow-Up Email Drafting

## Overview
This project prototypes an LLM-assisted workflow for drafting sales follow-up emails after discovery calls.

## Workflow Definition
- **Workflow chosen:** Writing sales follow-up emails
- **User:** Account Executive (AE) at a B2B SaaS company
- **Input received by system:** Structured notes from a sales call (pain points, stakeholder roles, budget, timeline, objections, next steps)
- **Output produced by system:** A concise, personalized follow-up email draft with recap, value mapping, and clear next step CTA
- **Why valuable:** AEs spend significant time writing repetitive follow-ups. Partial automation can improve speed and consistency while keeping a human in review.

## Repository Contents
- `app.py` - command-line prototype that calls an LLM API
- `prompts.md` - initial prompt + two revisions and observations
- `eval_set.json` - small stable evaluation set (normal, edge, and likely-failure cases)
- `report.md` - 1-2 page summary of approach, results, and recommendation

## How to Run
1. Create and activate a Python 3.10+ environment.
2. Install dependency:
   - `pip install openai`
3. Set environment variable:
   - `export OPENAI_API_KEY="your_api_key_here"`
4. Run:
   - `python app.py --input examples/input_normal.json --prompt-version v3`

If no `--input` is passed, the script runs built-in sample data.

## CLI Options
- `--input`: path to JSON file containing sales call notes
- `--prompt-version`: `v1`, `v2`, or `v3` (default: `v3`)
- `--model`: model name (default: `gpt-4.1-mini`)
- `--output`: optional output file path

## Reproducibility Notes
- Prompt versions are fixed in `app.py` and documented in `prompts.md`.
- Evaluation inputs are fixed in `eval_set.json`.
- Outputs are printed in structured sections and can also be saved to file.
