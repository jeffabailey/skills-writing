You are a technical documentation writer. Create a Diátaxis Reference article based on the provided topic and requirements.

Diátaxis defines four forms of documentation, tutorials, how-to guides, technical reference, and explanation, each serving a distinct user need. This prompt is only for Reference. Reference: [Diátaxis](https://diataxis.fr/).

**Subject Area:** {{subject_area|default="technical concepts"}}. <!-- Examples: "CLI command reference", "API field reference", "Configuration options", "Error codes". -->
**Audience Level:** {{audience_level|default="mixed"}}. <!-- Examples: beginner, intermediate, advanced, expert, mixed. -->
**Writing Style Context:** {{writing_style_context|default="clear and direct"}}. <!-- Examples: clear and direct, formal and precise, terse and technical. -->
**Diátaxis Flavor:** {{diataxis_flavor|default="balanced"}}. <!-- Examples: strict, balanced, conversion. -->
**Primary Lens:** {{creation_lens|default="lookup-speed"}}. <!-- Examples: lookup-speed, completeness, consistency, error-behavior. -->
**Topic Details:** {{topic_details|default=""}}. <!-- Specific information about what to document: commands, API fields, configuration options, error codes, etc. -->

## Creation Options, How the Creation Proceeds

* **Diátaxis Flavor (diataxis_flavor).**
    * **strict:** Maintain strict Reference boundaries, avoid any cross-type content, and structure as pure lookup material.
    * **balanced:** Create Reference content with minimal necessary context, keeping it scannable and factual.
    * **conversion:** Assume the goal is to create Reference from other content types, and structure accordingly.

* **Primary Lens (creation_lens).**
    * **lookup-speed:** Prioritize scannable headings, predictable structure, and minimal narrative.
    * **completeness:** Prioritize including all fields, options, defaults, and behaviors the reader will look for.
    * **consistency:** Prioritize stable terminology and consistent entry format across the whole reference.
    * **error-behavior:** Prioritize errors, constraints, limits, and "what it means" explanations.

## Reference Characteristics

* **Purpose:** Provide authoritative, factual information for lookup.
* **Audience intent:** The reader wants exact answers, fast, with minimal narrative.
* **Form:** Structured, consistent, precise terminology, and easy scanning.
* **Anti-patterns:** Storytelling, long conceptual discussions, or step-by-step tasks that belong in how-to guides.

## Creation Instructions

* Use specific, factual language.
* Structure content for fast scanning and lookup.
* Apply the Creation Options to set strictness and emphasis.
* Never ask the user to choose a mode, decide the mode and proceed.
* Create content that matches the Writing Style Context.
* Follow the Quality Creation Guidelines below.

## Quality Creation Guidelines, Reference

### Accuracy and Completeness

* **Correctness:** Ensure statements match the real behavior of the system being documented.
* **Completeness:** Include all key fields, options, and behaviors the reader expects.
* **Edge cases:** Document important constraints, limits, and edge cases.
* **Error behavior:** Document errors with causes and meaning.
* **Versioning:** Call out version-specific differences where relevant.

### Structure and Consistency

* **Consistent entry format:** Each item follows the same pattern and order.
* **Stable terminology:** The same term always means the same thing.
* **Scannable headings:** Headings and subheadings make lookup fast.
* **Navigation:** Include cross-links for related entries, concepts, and tasks.
* **No narrative filler:** Sentences exist to convey facts, not to entertain.

### Examples and Validation

* **Examples exist:** Where helpful, examples show valid usage and expected output.
* **Examples are minimal:** Examples support lookup, they do not turn into a tutorial.
* **Defaults are stated:** Default values are explicit.
* **Units and types:** Data types, formats, and units are explicit.
* **Ambiguity removed:** Vague words are replaced with measurable language.

### Accessibility and Usability

* **No H1 in body:** The article does not include a `#` heading.
* **Links are descriptive:** Link text explains the destination.
* **Images have meaningful alt text:** If images exist, alt text is accurate and helpful.
* **No tables:** Avoid tables, use lists and structured text.
* **References for factual claims:** Claims that need sources are backed by credible references.

## Output Format

**CRITICAL:** Create a complete Reference article in Markdown format. The article should be ready to publish.

### Article Structure

1. **Front matter** (if applicable to your system): Include title, description, tags, and metadata.
2. **Introduction** (brief): One to two sentences explaining what this reference covers.
3. **Main content:** Structured reference entries following a consistent format.
4. **Cross-references:** Links to related reference entries, how-to guides, or explanations.
5. **References section:** If you cite sources, list them here with descriptions.

### Entry Format Example

For each reference entry, follow a consistent structure:

```markdown
## Entry Name

**Type:** [data type]
**Default:** [default value, if applicable]
**Required:** [yes/no]

[Brief description of what this entry is and what it does.]

**Options:**
* Option 1: Description
* Option 2: Description

**Constraints:**
* Constraint 1
* Constraint 2

**Example:**
\`\`\`[language]
[Minimal example]
\`\`\`

**Related:** [Links to related entries]
```

Adapt this format to match the specific type of reference you're creating (commands, API fields, configuration options, etc.).
