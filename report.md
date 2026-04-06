# Report: LLM Prototype for Sales Follow-Up Email Drafting

## Business Use Case
This prototype supports account executives who need to send timely and accurate follow-up emails after sales discovery calls. The workflow is high-frequency and writing-heavy: each email must recap pain points, reinforce business value, and propose next steps. In practice, this repetitive work can reduce selling time and produce uneven message quality across reps.

The intended user is an AE at a B2B SaaS company. The input is structured call notes (stakeholders, pain points, goals, timeline, objections, and next step). The output is a first-pass draft email that is concise, factual, and ready for quick human editing.

## Model Choice and Rationale
I used `gpt-4.1-mini` for the prototype because it balances quality and cost for repeated drafting tasks. This workflow is not a high-stakes autonomous decision task; it is a writing-assist workflow with human review. A smaller model keeps runtime and cost practical for frequent usage while still producing professional tone.

I briefly tested more open-ended prompts and observed fluent but occasionally overconfident text. The model quality was adequate, but prompt constraints were required to control factuality.

## Baseline vs Final Prompt Design
Baseline (v1) prompt asked for a generic follow-up email with recap and next step. It produced readable drafts quickly, but quality issues appeared:
- Generic wording with weak grounding in source notes
- Occasional invented details (for example, assumptions about timing or commitments)
- Inconsistent structure across outputs

Revision 1 (v2) added explicit rules: use only provided facts, add `[NEEDS HUMAN INPUT]` when key details are missing, enforce length, and standardize sections. This materially improved consistency and reduced obvious fabrication.

Revision 2 (v3, final) tightened constraints further by explicitly prohibiting invention of names/numbers/timelines/integrations, preserving uncertainty language, and requiring a `REVIEW_FLAGS` section. This improved reviewer visibility and made risky outputs easier to triage.

Overall, prompt iteration improved output reliability more than style tuning did. The best gains came from explicit constraints and review signaling, not from wording polish.

## Remaining Failure Modes / Human Review Needs
The prototype still requires human review before sending. In ambiguous notes, the model may produce wording that is technically safe but diplomatically suboptimal. It can also under-specify CTA language when timeline/ownership is missing. For compliance-sensitive domains, even implied claims can create risk if rep context is incomplete. Human checks are still needed for factual correctness, relationship tone, and legal/compliance-sensitive statements.

## Deployment Recommendation
I would recommend conditional deployment as a **drafting assistant**, not an autonomous sender. Suggested controls:
- Require human approval before outbound send
- Keep mandatory review for compliance/technical claims
- Log inputs/outputs for periodic quality audits
- Use stable evaluation cases (`eval_set.json`) to regress-test prompt changes

With these controls, the workflow can improve rep productivity while keeping risk manageable.
