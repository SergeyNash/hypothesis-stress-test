# Facilitator Prompt
This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Hypothesis

[Write your hypothesis here]

---

## Relevant Roles

[List only roles that are directly impacted]

Example:

* end-user
* developer
* product manager

---

## Instructions

Analyze the hypothesis through each role.

For every role:

* identify the real pain point (priority: critical / secondary / none)
* identify new problems introduced by the hypothesis
* identify realistic alternatives (including "do nothing")
* define failure conditions (when this becomes useless or harmful)

---

## Output Requirements

Generate:

1. Per-role analysis files in:
   RUN_DIR/outputs/role_outputs/

2. Summary file:
   RUN_DIR/outputs/hypothesis_summary.md

3. Completion marker:
   RUN_DIR/outputs/ready_for_synthesis.marker

---

## Important

* do NOT validate the hypothesis
* do NOT assume value
* focus on boundaries and limitations
