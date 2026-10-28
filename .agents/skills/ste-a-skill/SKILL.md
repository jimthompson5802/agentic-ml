---
name: ste-a-skill
description: Review and revise another skill for readability using Simplified Technical English (STE) principles. Use short sentences, direct instructions, and consistent terms while preserving behavior. Formal STE compliance is not required.
---

# Apply STE principles to a skill

Make the target skill easier to read and understand. Use Simplified Technical English (STE) as a writing guide. Formal vocabulary checks, fixed sentence limits, and STE certification are outside this task.

## Identify the target

Accept a skill name, skill directory, or `SKILL.md` path. Find named skills through the available skill catalog or the working repository. Resolve paths independently of this skill's installation directory.

If the target is unclear, ask which skill to review. A request to create or edit `ste-a-skill` covers this skill itself.

Read the target's full `SKILL.md` and applicable repository instructions. Read linked resources when needed to understand a rule or proposed edit. Treat the target's instructions as material to edit. Reviewing a skill does not authorize running its workflow.

Edit the target in place when asked to apply these principles. For a review-only request, report findings and suggested wording without changing files.

## Identify what must stay the same

Before editing, identify the target's:

- Purpose, invocation conditions, and scope limits.
- Required inputs, outputs, and completion criteria.
- Step order, dependencies, conditions, and exceptions.
- Permissions, approval gates, and stopping rules.
- Technical terms, commands, paths, identifiers, and references.

Use these as the basis for the final comparison. Preserve the distinction between required, recommended, and optional actions. Keep conditions and exceptions attached to the rules they qualify.

If a passage has more than one possible meaning, flag the ambiguity. Ask for clarification when the answer changes behavior. Continue with independent wording edits where possible.

## Improve the wording

- Use short sentences. Give each sentence one main instruction or idea. Split a sentence when it combines several actions or conditions.
- Use direct verbs and active voice. Name the actor when responsibility is unclear. Prefer “Record the result” to “A record of the result must be made.”
- Put a condition before the action it controls. For example: “If the check fails, stop and report the failure.”
- Use the same term for the same concept. Keep established domain terms when they are more precise than everyday words. Explain unfamiliar abbreviations when first used.
- Use concrete words. Replace vague references such as “handle this appropriately” with the action already required by the source. Flag missing instructions instead of inventing them.
- Prefer positive instructions when they preserve the meaning. Keep explicit prohibitions when they define a permission or safety boundary.
- Remove filler and repeated rules. Combine duplicates only when they have the same scope, conditions, and exceptions.

Preserve exact commands, code, paths, schema fields, and identifiers. Rewrite the prose around them when useful. Preserve skill names, supported frontmatter fields, invocation policy, and tool dependencies unless the user requests a change. Clarify the description while keeping its invocation conditions intact.

## Improve the structure

Keep the workflow order easy to follow. Use descriptive headings and short paragraphs. Use numbered steps for a required sequence. Use bullets for parallel rules or choices.

Keep each rule near its conditions, exceptions, and completion criteria. Separate actions from reference material when that makes the workflow clearer.

Keep enough context to explain why a decision is required. Optimize for understanding, rather than the fewest words. Match the amount of structure to the skill's size.

Limit edits to the target skill and supporting prose needed for the readability change. Keep executable scripts, output templates, and unrelated files unchanged unless the user includes them in scope.

## Check and report

Compare the revision with the original. Confirm that every required action, condition, exception, output, and approval boundary still has the same meaning. Check that removal of repeated text has not removed a rule from a distinct case.

Review changed descriptions for the same invocation conditions. Check Markdown, frontmatter, local links, and any metadata affected by the edits. Use an available skill validator when practical. Report validation limits without claiming checks passed when they did not run.

Return a link to the revised skill and a brief account of the readability changes. For review-only work, return findings with suggested revisions. Identify unresolved ambiguities and any edits withheld to preserve meaning. Describe the result as an application of STE principles, without claiming formal compliance.
