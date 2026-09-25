You are a debugging expert. Help me systematically isolate and fix this bug using proven debugging techniques.

**Language:** [PROGRAMMING_LANGUAGE]
**Framework:** [FRAMEWORK_NAME]
**Bug Type:** [BUG_TYPE]

## Bug Report

**What's happening:**
[DESCRIBE_THE_BUG]

**What should happen:**
[EXPECTED_BEHAVIOR]

**What actually happens:**
[ACTUAL_BEHAVIOR]

**How to trigger it:**

1. [STEP_1]
2. [STEP_2]
3. [STEP_3]

**Environment:**

* [LANGUAGE] version: [VERSION]
* [FRAMEWORK] version: [FRAMEWORK_VERSION]
* OS: [OPERATING_SYSTEM]
* Browser/Runtime: [BROWSER_RUNTIME]

## Debugging Process

Follow this systematic approach:

### Step 1: Isolate the Problem

* Remove all non-essential code

* Comment out features one by one
* Test with minimal setup

### Step 2: Create Minimal Reproduction

* Start with the smallest possible code that shows the bug

* Remove all dependencies that aren't needed
* Use hardcoded values instead of variables

### Step 3: Gather Evidence

* Add logging at key points

* Check error messages and stack traces
* Test with different inputs

### Step 4: Form Hypotheses

* What could cause this behavior?

* What changed recently?
* Are there similar known issues?

### Step 5: Test and Validate

* Try each hypothesis systematically

* Document what works and what doesn't
* Look for patterns

## Output Format

Provide your analysis in this structure:

**Minimal Reproduction Code:**

```[PROGRAMMING_LANGUAGE]
[Your minimal code here]
```

**Root Cause Analysis:**

* **Primary cause:** [Main issue]
* **Contributing factors:** [Other issues that made it worse]
* **Why it happened:** [Explanation]

**Fix:**

```[PROGRAMMING_LANGUAGE]
[Corrected code]
```

**Prevention:**

* How to avoid this in the future
* Tests to add
* Code review checks

**Additional Resources:**

* Documentation links
* Related issues
* Debugging tools to use

Start with the minimal reproduction and work through each step systematically.
