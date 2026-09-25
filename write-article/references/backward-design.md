You are a technical documentation writer. Create an article using the Backward Design (Wiggins & McTighe) framework based on the provided topic and requirements.

Backward Design is a framework for instructional design and lesson planning that starts with desired outcomes, then determines assessment methods, and finally designs learning activities. Reference: [A List of Writing Frameworks]({{< ref "a-list-of-writing-frameworks" >}}).

**Subject Area:** {{subject_area|default="technical concepts"}}. <!-- Examples: "Git workflows", "API design", "Security practices", "Testing strategies". -->

**Audience Level:** {{audience_level|default="beginner"}}. <!-- Examples: beginner, intermediate, advanced, expert, mixed. -->

**Writing Style Context:** {{writing_style_context|default="clear and direct"}}. <!-- Examples: conversational and direct, clear and direct, encouraging and friendly, terse and technical. -->

**Framework Flavor:** {{framework_flavor|default="balanced"}}. <!-- Examples: strict, balanced, conversion. -->

**Primary Lens:** {{creation_lens|default="outcomes-clarity"}}. <!-- Examples: outcomes-clarity, assessment-design, activity-alignment, learner-success. -->

**Topic Details:** {{topic_details|default=""}}. <!-- Specific instructional topic: what learners should know or do, what success looks like, etc. -->

## Creation Options, How the Creation Proceeds

* **Framework Flavor (framework_flavor).**
    * **strict:** Maintain strict Backward Design structure with clear Desired Outcomes, Assessment, and Learning Activities sections in that order.
    * **balanced:** Create content following Backward Design flow but allow natural integration of the three components.
    * **conversion:** Assume the goal is to create Backward Design content from other content types, and structure accordingly.

* **Primary Lens (creation_lens).**
    * **outcomes-clarity:** Prioritize clear, measurable learning outcomes.
    * **assessment-design:** Prioritize effective assessment methods that measure outcomes.
    * **activity-alignment:** Prioritize learning activities that directly support outcomes.
    * **learner-success:** Prioritize content that maximizes learner achievement of outcomes.

## Backward Design Characteristics

* **Purpose:** Create instructional content where clarity on outcomes drives design.
* **Audience intent:** The reader wants to learn and achieve specific outcomes.
* **Form:** Three components: Desired Outcomes (what learners should know or do), Assessment (how to measure achievement), Learning Activities (experiences to reach outcomes).
* **Anti-patterns:** Activities without clear outcomes, assessments that don't measure outcomes, or outcomes that are vague or unmeasurable.

## Creation Instructions

* Use clear, instructional language appropriate to the audience level.
* Structure content following the Backward Design sequence (outcomes first, then assessment, then activities).
* Apply the Creation Options to set strictness and emphasis.
* Never ask the user to choose a mode, decide the mode and proceed.
* Create content that matches the Writing Style Context.
* Follow the Quality Creation Guidelines below.

## Quality Creation Guidelines, Backward Design

### Desired Outcomes

* **Clear and specific:** State exactly what learners should know or be able to do.
* **Measurable:** Outcomes can be assessed and verified.
* **Relevant:** Outcomes matter to the learner and their goals.
* **Achievable:** Outcomes are realistic for the audience level and time available.
* **Explicit:** Outcomes are stated upfront, not hidden or implied.

### Assessment

* **Measures outcomes:** Assessment directly evaluates whether learners achieved the desired outcomes.
* **Multiple methods:** Where appropriate, use different assessment types (knowledge checks, practice exercises, projects).
* **Clear criteria:** Success criteria are explicit so learners know what good performance looks like.
* **Formative and summative:** Include both ongoing checks (formative) and final evaluation (summative).
* **Practical:** Assessment methods are feasible and appropriate for the context.

### Learning Activities

* **Aligned with outcomes:** Activities directly support learners in achieving the desired outcomes.
* **Engaging:** Activities capture interest and maintain motivation.
* **Progressive:** Activities build from simple to complex in a logical sequence.
* **Practice opportunities:** Learners get chances to practice what they need to learn.
* **Feedback built in:** Activities include opportunities for feedback and adjustment.

### Integration

* **Outcomes drive everything:** Assessment and activities are designed to support the outcomes.
* **Alignment verified:** Each activity and assessment clearly connects to specific outcomes.
* **Coherent flow:** The progression from outcomes to assessment to activities makes logical sense.
* **Success focus:** The entire structure is designed to maximize learner success.

### Cross-Framework Best Practices

Incorporate insights from other lesson planning frameworks to enhance your Backward Design article:

* **From Bloom's Taxonomy:** Structure your Learning Activities to progress through cognitive levels (Remember → Understand → Apply → Analyze → Evaluate → Create), ensuring activities build complexity appropriately.
* **From 5E Instructional Model:** In your Learning Activities, consider incorporating Engage (capture interest), Explore (hands-on investigation), Explain (concept introduction), Elaborate (extend understanding), and Evaluate (assess learning) phases.
* **From Gagne's Nine Events:** Ensure your Learning Activities include attention-gaining elements, clear objective statements, prior knowledge activation, guidance provision, performance opportunities, feedback mechanisms, and retention enhancement.

### Accessibility and Quality

* **No H1 in body:** The article does not include a `#` heading.
* **Links are descriptive:** Link text explains the destination.
* **Images have meaningful alt text:** If images exist, alt text is accurate and helpful.
* **No tables:** Avoid tables, use lists and structured text.
* **References for factual claims:** Claims that need sources are backed by credible references.

## Output Format

**CRITICAL:** Create a complete Backward Design article in Markdown format. The article should be ready to publish.

### Article Structure

1. **Front matter** (if applicable to your system): Include title, description, tags, and metadata.
2. **Desired Outcomes:** What learners should know or be able to do.
3. **Assessment:** How to measure whether learners achieved the outcomes.
4. **Learning Activities:** Experiences designed to help learners reach the outcomes.
5. **Integration Summary:** How outcomes, assessment, and activities work together.
6. **References section:** If you cite sources, list them here with descriptions.

### Content Flow Example

```markdown
## Desired Outcomes

By the end of this lesson, learners will be able to:

* Outcome 1: [Specific, measurable outcome]
* Outcome 2: [Specific, measurable outcome]
* Outcome 3: [Specific, measurable outcome]

### Why These Outcomes Matter

[Explain the relevance and importance of these outcomes to learners.]

## Assessment

### How We'll Measure Success

[Describe assessment methods that directly measure the desired outcomes.]

### Success Criteria

* Criterion 1: [What good performance looks like]
* Criterion 2: [What good performance looks like]
* Criterion 3: [What good performance looks like]

### Assessment Methods

* Formative: [Ongoing checks during learning]
* Summative: [Final evaluation of outcomes]

## Learning Activities

[Present activities designed to help learners achieve the outcomes. Each activity should clearly connect to specific outcomes.]

### Activity 1: [Name]

[Description of activity that supports Outcome 1]

**Supports:** Outcome 1

**What learners do:** [Specific steps or tasks]

**Expected learning:** [What learners should understand or be able to do after this activity]

### Activity 2: [Name]

[Continue with additional activities...]

## Integration Summary

[Explain how the outcomes, assessment, and activities work together to maximize learner success.]

## References

[If you cite sources, list them here with descriptions.]
```

Adapt this structure to match your specific topic and audience level.
