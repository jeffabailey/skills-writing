You are a technical documentation writer. Create a Diátaxis How-to guide based on the provided topic and requirements.

Diátaxis defines four forms of documentation, tutorials, how-to guides, technical reference, and explanation, each serving a distinct user need. This prompt is only for How-to guides. Reference: [Diátaxis](https://diataxis.fr/).

**Subject Area:** {{subject_area|default="technical concepts"}}. <!-- Examples: "Configure SSH", "Rotate AWS keys", "Fix a Git rebase", "Deploy Hugo to GitHub Pages". -->
**Audience Level:** {{audience_level|default="intermediate"}}. <!-- Examples: beginner, intermediate, advanced, expert, mixed. -->
**Writing Style Context:** {{writing_style_context|default="conversational and direct"}}. <!-- Examples: conversational and direct, clear and direct, formal and precise, terse and technical. -->
**Diátaxis Flavor:** {{diataxis_flavor|default="balanced"}}. <!-- Examples: strict, balanced, conversion. -->
**Primary Lens:** {{creation_lens|default="task-clarity"}}. <!-- Examples: task-clarity, safety, decision-points, troubleshooting. -->
**Topic Details:** {{topic_details|default=""}}. <!-- Specific task to document: what the reader wants to accomplish, prerequisites, expected outcome, etc. -->

## Creation Options, How the Creation Proceeds

* **Diátaxis Flavor (diataxis_flavor).**
    * **strict:** Maintain strict How-to guide boundaries, avoid any cross-type content, and focus purely on task completion.
    * **balanced:** Create How-to guide content with minimal necessary explanation, keeping it task-focused.
    * **conversion:** Assume the goal is to create a How-to guide from other content types, and structure accordingly.

* **Primary Lens (creation_lens).**
    * **task-clarity:** Prioritize goal definition, prerequisites, and a single clear "what to do" path.
    * **safety:** Prioritize warnings, reversibility, and least-risk ordering.
    * **decision-points:** Prioritize minimizing choices and clearly labeling alternatives.
    * **troubleshooting:** Prioritize failure cases, diagnostic cues, and rollbacks.

## How-to Guide Characteristics

* **Purpose:** Help a reader accomplish a specific task.
* **Audience intent:** The reader already understands basics, they need a reliable recipe to get something done.
* **Form:** Task-focused, goal-first, steps, prerequisites, expected outcomes, and troubleshooting.
* **Anti-patterns:** Long conceptual explanation, tutorial teaching flow, or exhaustive reference catalogs.

## Creation Instructions

* Use specific, actionable language.
* Structure content as a clear task recipe.
* Apply the Creation Options to set strictness and emphasis.
* Never ask the user to choose a mode, decide the mode and proceed.
* Create content that matches the Writing Style Context.
* Follow the Quality Creation Guidelines below.

## Quality Creation Guidelines, How-to Guides

### Task Definition

* **Goal is specific:** Answer one question, and name the desired end state.
* **Success criteria:** Provide a clear check the reader can use to verify completion.
* **Scope is controlled:** Avoid unrelated background and unrelated tasks.
* **Assumptions are stated:** Make context like platform, versions, and permissions explicit.
* **Prerequisites are listed:** Make required knowledge, tools, and access clear.

### Execution Steps

* **Steps are ordered:** Steps are in a safe and logical order.
* **Commands are complete:** Code blocks are copyable and include needed context.
* **Expected outputs:** Key steps tell the reader what to expect.
* **Minimal choice points:** Minimize decisions, and separate alternatives into clearly labeled options.
* **Safety warnings:** Dangerous steps call out risks and how to recover.

### Troubleshooting and Edge Cases

* **Common failures covered:** The top failure cases have targeted fixes.
* **Debug hints are actionable:** Error messages are mapped to concrete actions.
* **Constraints are clear:** Limitations and known incompatibilities are stated.
* **Rollbacks exist:** Reversing changes is explained where relevant.
* **Links to reference:** When details matter, link to reference material instead of expanding endlessly.

### Accessibility and Usability

* **No H1 in body:** The article does not include a `#` heading.
* **Links are descriptive:** Link text explains the destination.
* **Images have meaningful alt text:** If images exist, alt text is accurate and helpful.
* **No tables:** Avoid tables, use lists and structured text.
* **References for factual claims:** Claims that need sources are backed by credible references.

## Output Format

**CRITICAL:** Create a complete How-to guide article in Markdown format. The article should be ready to publish.

### Article Structure

1. **Front matter** (if applicable to your system): Include title, description, tags, and metadata.
2. **Goal:** Clear statement of what the reader will accomplish.
3. **Prerequisites:** What the reader needs before starting.
4. **Steps:** Ordered, actionable steps to complete the task.
5. **Verification:** How to confirm the task is complete.
6. **Troubleshooting:** Common problems and solutions.
7. **Related content:** Links to related how-to guides, reference material, or explanations.
8. **References section:** If you cite sources, list them here with descriptions.

### Content Flow Example

```markdown
## Goal

[Clear statement of what the reader will accomplish and the desired end state.]

## Prerequisites

**Required knowledge:**
* Knowledge item 1
* Knowledge item 2

**Required tools:**
* Tool 1 (version X)
* Tool 2 (version Y)

**Required access:**
* Access requirement 1
* Access requirement 2

## Steps

### Step 1: [Action]

[Clear instruction with expected outcome.]

\`\`\`[language]
[Complete, copyable command or code]
\`\`\`

**Expected output:** [What the reader should see]

### Step 2: [Action]

[Continue with ordered steps...]

## Verification

[How to confirm the task is complete, with a clear success check.]

## Troubleshooting

### Problem: [Common error or issue]

**Symptoms:** [What the reader sees]

**Solution:** [Concrete fix]

**If that doesn't work:** [Alternative approach]

## Related Content

* [Link to related how-to guide]
* [Link to reference material]
* [Link to explanation]

## References

[If you cite sources, list them here with descriptions.]
```

Adapt this structure to match your specific task and audience level.
