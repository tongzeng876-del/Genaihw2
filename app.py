#!/usr/bin/env python3
"""Small CLI prototype for drafting sales follow-up emails with an LLM."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

from openai import OpenAI

PROMPTS: Dict[str, str] = {
    "v1": (
        "You are a helpful sales assistant. Write a follow-up email based on call notes. "
        "Include thank-you, short recap, benefits, and next step."
    ),
    "v2": (
        "You are an assistant helping B2B SaaS account executives draft post-call follow-up emails.\n\n"
        "Rules:\n"
        "1. Use only facts present in the notes.\n"
        "2. If key information is missing, use neutral language and mark with [NEEDS HUMAN INPUT].\n"
        "3. Keep email between 120 and 180 words.\n"
        "4. Include sections in this order: Subject line, Greeting, Recap, Value mapping, CTA, Sign-off.\n"
        "5. Tone: professional, concise, and collaborative."
    ),
    "v3": (
        "You are an assistant helping B2B SaaS account executives draft post-call follow-up emails.\n\n"
        "Hard constraints:\n"
        "1. Never invent names, numbers, timelines, integrations, or commitments not explicitly in the input.\n"
        "2. If any of the following are missing, include one concise placeholder question in CTA and tag [NEEDS HUMAN INPUT]: "
        "decision process, timeline, or confirmed next meeting.\n"
        "3. Keep body length between 110 and 160 words.\n"
        "4. Preserve uncertainty exactly as given (e.g., 'tentative,' 'not confirmed').\n"
        "5. Avoid hype and superlatives.\n\n"
        "Output format:\n"
        "- SUBJECT: <one line>\n"
        "- EMAIL:\n"
        "  <plain text body in 2 to 3 short paragraphs>\n"
        "- REVIEW_FLAGS:\n"
        "  - <bullet list of possible risk points requiring human review, or 'none'>"
    ),
}

DEFAULT_INPUT: Dict[str, Any] = {
    "company": "Northbeam Logistics",
    "contact_name": "Elena Ruiz",
    "role": "Director of Operations",
    "summary": "They want better visibility into shipment delays and weekly exception reporting.",
    "pain_points": [
        "Manual status updates across 4 systems",
        "Late identification of delayed shipments",
    ],
    "desired_outcomes": [
        "Single dashboard for delay alerts",
        "Weekly automated exception report",
    ],
    "timeline": "Pilot in Q3",
    "next_step": "Share sample dashboard and schedule technical validation next Tuesday",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Draft sales follow-up emails with an LLM")
    parser.add_argument("--input", type=str, help="Path to JSON input notes")
    parser.add_argument("--prompt-version", default="v3", choices=sorted(PROMPTS.keys()))
    parser.add_argument("--model", default="gpt-4.1-mini", help="Model name")
    parser.add_argument("--output", type=str, help="Optional output file path")
    return parser.parse_args()


def load_input(path: str | None) -> Dict[str, Any]:
    if not path:
        return DEFAULT_INPUT

    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object/dictionary.")

    return data


def build_user_prompt(notes: Dict[str, Any]) -> str:
    return (
        "Draft a follow-up email from these sales call notes:\n\n"
        f"{json.dumps(notes, indent=2, ensure_ascii=True)}"
    )


def run_generation(model: str, system_prompt: str, user_prompt: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.output_text.strip()


def main() -> int:
    args = parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY is not set.", file=sys.stderr)
        return 1

    notes = load_input(args.input)
    system_prompt = PROMPTS[args.prompt_version]
    user_prompt = build_user_prompt(notes)

    output_text = run_generation(args.model, system_prompt, user_prompt)

    structured = (
        "=== CONFIG ===\n"
        f"model: {args.model}\n"
        f"prompt_version: {args.prompt_version}\n\n"
        "=== INPUT NOTES ===\n"
        f"{json.dumps(notes, indent=2, ensure_ascii=True)}\n\n"
        "=== GENERATED EMAIL ===\n"
        f"{output_text}\n"
    )

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(structured, encoding="utf-8")
        print(f"Saved output to: {output_path}")
    else:
        print(structured)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
