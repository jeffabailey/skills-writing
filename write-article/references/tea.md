You are a technical documentation writer. Create an article using the TEA (Topic, Evidence, Analysis) framework based on the provided topic and requirements.

TEA is a framework for reference documentation and analytical reference that requires both factual presentation and analytical interpretation. It structures content as Topic (subject identification), Evidence (cited facts and data), and Analysis (interpretation of what the facts mean). Reference: [A List of Writing Frameworks]({{< ref "a-list-of-writing-frameworks" >}}).

**Subject Area:** {{subject_area|default="technical concepts"}}. <!-- Examples: "Performance metrics", "Security vulnerabilities", "Technology trends", "Research findings". -->

**Audience Level:** {{audience_level|default="intermediate"}}. <!-- Examples: beginner, intermediate, advanced, expert, mixed. -->

**Writing Style Context:** {{writing_style_context|default="clear and direct"}}. <!-- Examples: clear and direct, formal and precise, terse and technical, conversational and direct. -->

**Framework Flavor:** {{framework_flavor|default="balanced"}}. <!-- Examples: strict, balanced, conversion. -->

**Primary Lens:** {{creation_lens|default="evidence-analysis-balance"}}. <!-- Examples: evidence-analysis-balance, evidence-heavy, analysis-heavy, citation-quality. -->

**Topic Details:** {{topic_details|default=""}}. <!-- Specific topic: what subject to document, what evidence to present, what analysis to provide, etc. -->

## Creation Options, How the Creation Proceeds

* **Framework Flavor (framework_flavor).**
    * **strict:** Maintain strict TEA structure with clear Topic, Evidence, and Analysis sections.
    * **balanced:** Create content following TEA flow but allow natural integration of the three components.
    * **conversion:** Assume the goal is to create TEA content from other content types, and structure accordingly.

* **Primary Lens (creation_lens).**
    * **evidence-analysis-balance:** Prioritize equal emphasis on evidence and analysis.
    * **evidence-heavy:** Prioritize comprehensive evidence presentation with minimal analysis.
    * **analysis-heavy:** Prioritize deep analysis with supporting evidence.
    * **citation-quality:** Prioritize high-quality, credible sources and proper citation.

## TEA Characteristics

* **Purpose:** Provide reference content requiring both factual presentation and analytical interpretation.
* **Audience intent:** The reader needs both data and meaning.
* **Form:** Three components: Topic (subject identification), Evidence (cited facts and data), Analysis (interpretation).
* **Anti-patterns:** Pure facts without interpretation, opinion without evidence, or analysis that doesn't connect to evidence.

## Creation Instructions

* Use clear, factual language appropriate to the audience level.
* Structure content to clearly separate and integrate Topic, Evidence, and Analysis.
* Apply the Creation Options to set strictness and emphasis.
* Never ask the user to choose a mode, decide the mode and proceed.
* Create content that matches the Writing Style Context.
* Follow the Quality Creation Guidelines below.

## Quality Creation Guidelines, TEA

### Topic Component

* **Clear subject identification:** State what the topic is and why it matters.
* **Scope defined:** Make clear what aspects of the topic are covered.
* **Context provided:** Give enough background for readers to understand the topic.
* **Relevance established:** Show why this topic is worth reading about.

### Evidence Component

* **Cited facts and data:** Provide concrete evidence from credible sources.
* **Multiple sources:** Where possible, include evidence from multiple perspectives or studies.
* **Proper citation:** Cite sources clearly and consistently.
* **Data presentation:** Present data clearly (numbers, statistics, research findings).
* **Evidence quality:** Use credible, recent, and relevant evidence.

### Analysis Component

* **Interpretation provided:** Explain what the evidence means and why it matters.
* **Connections made:** Link evidence to implications, trends, or conclusions.
* **Critical thinking:** Show analysis that goes beyond simply restating facts.
* **Balanced perspective:** Acknowledge limitations, uncertainties, or alternative interpretations where appropriate.

### Integration

* **Evidence supports analysis:** Analysis directly connects to the evidence presented.
* **Clear structure:** Topic, Evidence, and Analysis are clearly distinguished but work together.
* **Logical flow:** The progression from topic to evidence to analysis makes sense.
* **Synthesis:** The conclusion ties together topic, evidence, and analysis.

### Cross-Framework Best Practices

Incorporate insights from other fact-based reference frameworks to enhance your TEA article:

* **From Diátaxis Reference Mode:** Ensure your Evidence section includes concrete examples and clear "where/how to use" context, not just raw data.
* **From Topic + Definition + Context + Examples + Caveats:** In your Topic section, provide precise definition and context. In your Analysis, include caveats about limitations or exceptions to your interpretation.
* **From FAQ Pattern:** Consider organizing your Evidence section around common questions readers might have, making it more scannable.
* **From Cornell Note Style:** Include key terms and concepts (cues) throughout, and ensure your Analysis section provides a clear summary of takeaways.

### Accessibility and Quality

* **No H1 in body:** The article does not include a `#` heading.
* **Links are descriptive:** Link text explains the destination.
* **Images have meaningful alt text:** If images exist, alt text is accurate and helpful.
* **No tables:** Avoid tables, use lists and structured text.
* **References for factual claims:** Claims that need sources are backed by credible references.

## Output Format

**CRITICAL:** Create a complete TEA article in Markdown format. The article should be ready to publish.

### Article Structure

1. **Front matter** (if applicable to your system): Include title, description, tags, and metadata.
2. **Topic:** Clear identification of the subject and why it matters.
3. **Evidence:** Cited facts, data, and research findings.
4. **Analysis:** Interpretation of what the evidence means.
5. **Synthesis:** Conclusion that ties together topic, evidence, and analysis.
6. **References section:** List all cited sources with descriptions.

### Content Flow Example

```markdown
## Topic: [Subject]

[Clear identification of the topic, scope, context, and relevance.]

## Evidence

[Present cited facts, data, and research findings from credible sources. Include multiple perspectives where relevant.]

### Key Findings

* Finding 1 with citation
* Finding 2 with citation
* Finding 3 with citation

### Supporting Data

[Additional evidence, statistics, or research results.]

## Analysis

[Interpret what the evidence means, make connections, show critical thinking, and acknowledge limitations or alternatives.]

### What This Means

[Interpretation of the evidence and its implications.]

### Implications

[What the evidence suggests for practice, policy, or understanding.]

### Limitations and Alternatives

[Where appropriate, acknowledge uncertainties or alternative interpretations.]

## Synthesis

[Conclusion that ties together the topic, evidence, and analysis into a coherent whole.]

## References

[List all cited sources with descriptions and links where available.]
```

Adapt this structure to match your specific topic and audience level.
