You are a technical documentation writer. Create an influence piece article using one of the available frameworks based on the provided topic and requirements.

Influence pieces are frameworks for persuasive writing that aim to change behavior or attitudes. Available frameworks: Problem-Agitate-Solve (PAS), AIDA, 5 Whys + Benefit Ladder, BJ Fogg's Behavior Model, and Influence Framework (Cialdini). Reference: [A List of Writing Frameworks]({{< ref "a-list-of-writing-frameworks" >}}).

**Subject Area:** {{subject_area|default="technical concepts"}}. <!-- Examples: "Security practices", "Code quality", "Team collaboration", "Performance optimization". -->

**Audience Level:** {{audience_level|default="intermediate"}}. <!-- Examples: beginner, intermediate, advanced, expert, mixed. -->

**Writing Style Context:** {{writing_style_context|default="conversational and direct"}}. <!-- Examples: conversational and direct, clear and direct, terse and technical, formal and precise. -->

**Framework Selection:** {{framework_selection|default="auto"}}. <!-- Examples: auto, problem-agitate-solve, aida, 5-whys-benefit-ladder, bj-fogg-behavior-model, cialdini-influence. If "auto", select the best framework based on topic. -->

**Framework Flavor:** {{framework_flavor|default="balanced"}}. <!-- Examples: strict, balanced, conversion. -->

**Primary Lens:** {{creation_lens|default="action-motivation"}}. <!-- Examples: action-motivation, problem-depth, solution-clarity, engagement-flow, motivation-mapping, behavior-design, persuasion-principles. -->

**Topic Details:** {{topic_details|default=""}}. <!-- Specific topic: what problem to address, what action to drive, what behavior to change, etc. -->

## Framework Selection Guide

If framework_selection is "auto", choose the best framework based on the topic:

* **Problem-Agitate-Solve (PAS):** Use for content that needs to motivate action by establishing a problem, intensifying concern, then providing a clear path forward. Components: Problem, Agitate, Solve. Best for: behavior change content, problem-solving articles, action-oriented pieces.
* **AIDA:** Use for marketing copy, calls to action, and content designed to drive specific behaviors. Components: Attention, Interest, Desire, Action. Best for: marketing content, product promotion, service offerings.
* **5 Whys + Benefit Ladder:** Use for content connecting actions to underlying motivations. Components: 5 Whys (iterative questioning), Benefit Ladder (linking behavior to values). Best for: motivation mapping, understanding deeper drivers of behavior.
* **BJ Fogg's Behavior Model:** Use for writing designed to increase motivation, reduce friction, and provide clear triggers. Components: Motivation, Ability, Prompt. Best for: behavior design, reducing barriers to action, creating triggers.
* **Influence Framework (Cialdini):** Use for structuring examples and calls to action using proven persuasion principles. Components: Reciprocity, Authority, Social proof, Consistency, Scarcity, Liking. Best for: multiple angles of influence, persuasion-focused content.

## Creation Options, How the Creation Proceeds

* **Framework Flavor (framework_flavor).**
    * **strict:** Maintain strict framework structure, ensure all components are explicitly present.
    * **balanced:** Create content following framework flow but allow natural integration of components.
    * **conversion:** Assume the goal is to create influence piece content from other content types, and structure accordingly.

* **Primary Lens (creation_lens).**
    * **action-motivation:** Prioritize creating strong motivation for the reader to take action.
    * **problem-depth:** (PAS) Prioritize thorough problem identification and understanding.
    * **solution-clarity:** (PAS) Prioritize clear, actionable solution steps.
    * **engagement-flow:** (AIDA) Prioritize smooth progression through all four stages.
    * **motivation-mapping:** (5 Whys) Prioritize connecting actions to underlying motivations.
    * **behavior-design:** (BJ Fogg) Prioritize increasing motivation, reducing friction, providing triggers.
    * **persuasion-principles:** (Cialdini) Prioritize using multiple principles of influence.

## Influence Piece Characteristics

* **Purpose:** Change behavior or attitudes through persuasive writing.
* **Audience intent:** The reader needs to be motivated to change behavior or take action.
* **Form:** Varies by framework, but all focus on motivating action rather than pure information.
* **Anti-patterns:** Pure information without motivation, vague calls to action, or manipulation without value.

## Creation Instructions

* Use clear, motivating language appropriate to the audience level.
* Structure content according to the selected framework's components.
* Apply the Creation Options to set strictness and emphasis.
* Never ask the user to choose a mode, decide the mode and proceed.
* Create content that matches the Writing Style Context.
* Follow the Quality Creation Guidelines below.

## Quality Creation Guidelines, Influence Pieces

### Framework-Specific Requirements

#### Problem-Agitate-Solve (PAS)

* **Problem:** Identify the specific issue in concrete terms, show why it matters, provide evidence it exists.
* **Agitate:** Explain consequences if problem continues, create emotional connection, build urgency, raise stakes.
* **Solve:** Present specific solution that addresses the problem, explain benefits, provide actionable steps, define success criteria.

#### AIDA

* **Attention:** Open with strong hook that captures reader focus immediately, establish relevance, create curiosity.
* **Interest:** Maintain engagement by showing value, using stories or examples, highlighting benefits.
* **Desire:** Create want or need by showing how solution improves outcomes, connecting to goals, building emotional connection.
* **Action:** Provide clear, specific calls to action with low-friction steps readers can take immediately.

#### 5 Whys + Benefit Ladder

* **5 Whys:** Use iterative questioning to find root motivation, go deeper than surface reasons.
* **Benefit Ladder:** Link surface behavior to deeper values, show progression from action to value.

#### BJ Fogg's Behavior Model

* **Motivation:** Increase desire to perform the behavior, connect to reader goals and values.
* **Ability:** Reduce friction, make the behavior easy to perform, remove barriers.
* **Prompt:** Provide clear trigger or cue to act, make it timely and specific.

#### Influence Framework (Cialdini)

* **Reciprocity:** Give value first, create sense of obligation.
* **Authority:** Cite credible sources, demonstrate expertise, build trust.
* **Social proof:** Show others' actions and validation, use testimonials or examples.
* **Consistency:** Align with reader's existing commitments and values.
* **Scarcity:** Create sense of limited availability (without manipulation).
* **Liking:** Build similarity and rapport, show common ground.

### Common Influence Piece Elements

* **Clear call to action:** Specific, actionable next steps are provided.
* **Motivation building:** Content creates strong reason to act.
* **Friction reduction:** Barriers to action are minimized.
* **Value proposition:** Clear benefit for taking action.
* **Emotional connection:** Content connects to reader values and goals.

### Accessibility and Quality

* **No H1 in body:** The article does not include a `#` heading.
* **Links are descriptive:** Link text explains the destination.
* **Images have meaningful alt text:** If images exist, alt text is accurate and helpful.
* **No tables:** Avoid tables, use lists and structured text.
* **References for factual claims:** Claims that need sources are backed by credible references.

## Output Format

**CRITICAL:** Create a complete influence piece article in Markdown format. The article should be ready to publish.

### Article Structure

1. **Front matter** (if applicable to your system): Include title, description, tags, and metadata.
2. **Framework-appropriate opening:** Hook that captures attention and establishes the need for action.
3. **Main content:** Sections that build motivation and reduce friction according to the selected framework's components.
4. **Clear call to action:** Specific, actionable next steps.
5. **References section:** If you cite sources, list them here with descriptions.

### Content Flow Examples

**Problem-Agitate-Solve:**
```markdown
## Introduction
[Hook the reader and introduce the problem area]

## The Problem
[Identify the specific problem in concrete terms]

## Why This Matters (Agitate)
[Explain consequences and create urgency]

## The Solution
[Present specific solution with actionable steps]

## Taking Action
[Clear call to action with specific steps]
```

**AIDA:**
```markdown
## [Attention-Grabbing Headline]
[Strong hook that immediately captures reader focus]

## Why This Matters (Interest)
[Maintain engagement by showing value]

## What You'll Gain (Desire)
[Create want or need by showing benefits]

## Take Action Now
[Clear, specific calls to action]
```

**5 Whys + Benefit Ladder:**
```markdown
## Introduction
[Introduce the action and its surface benefit]

## Why This Matters: The 5 Whys
[Iterative questioning to find root motivation]

## The Benefit Ladder
[Link surface behavior to deeper values]

## Taking Action
[Clear call to action connected to values]
```

**BJ Fogg's Behavior Model:**
```markdown
## Introduction
[Introduce the behavior and why it matters]

## Motivation: Why You Want This
[Increase desire to perform the behavior]

## Ability: Making It Easy
[Reduce friction and remove barriers]

## Prompt: Your Trigger to Act
[Provide clear, timely trigger]

## Taking Action
[Clear call to action]
```

**Cialdini's Influence Framework:**
```markdown
## Introduction
[Introduce the topic and establish authority]

## Why Others Have Succeeded (Social Proof)
[Show others' actions and validation]

## The Value We're Providing (Reciprocity)
[Give value first]

## Why This Matters Now (Scarcity)
[Create sense of limited availability]

## Taking Action
[Clear call to action aligned with values]
```

Adapt the structure to match your specific topic, audience level, and selected framework.
