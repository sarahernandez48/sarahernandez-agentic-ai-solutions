# Prompt Playbook v1

## Objective
Capture empirical observations comparing prompt variants and model behaviors. Use this as a living artifact you will refine in future weeks.

## How to Use This File
1. After each script run, append rows to the Results Table.
2. Tag failure modes (see legend) so patterns emerge quickly.
3. Summarize insights after completing stretch assignments.

## Scoring Rubric (1–5)
| Score | Instruction Adherence | Reasoning Depth | Style / Persona | Format Fidelity |
|-------|-----------------------|-----------------|-----------------|-----------------|
| 1 | Misses key directives | Single sentence | Ignores persona | Broken / ignores |
| 3 | Mostly follows | Some steps implicit | Partial persona | Minor drift |
| 5 | Precise & complete | Clear multi-step chain | Fully consistent | Exact, parsable |

## Failure Mode Tags
hallucination, verbosity, shallow, drift (format), persona-loss, json-break, constraint-fail

## Results Table (Populate During Lab)
| Prompt Pattern | Example Used | Model | Adherence (1–5) | Reasoning (1–5) | Style (1–5) | Format (1–5) | Failure Modes | Notes | Reuse? (Y/N) |
|-------|------|------|-------|-------|-------|-------|-------|-------|-------|
|Simple|Explain photosynthesis|Llama3|5|5|5|3|shallow|Explains basic concepts, however does not explain the process|Y|
|Simple|Explain photosynthesis|Mistral|3|5|5|3|shallow|The explanation is very technical, little natural language|N|
|Simple|Explain photosynthesis|OpenAI (gpt-5-mini)|5|5|5|5|constraint-fail|More detail about the process, the explanation is more clear|Y|
|Simple|Explain photosynthesis|Gemini(gemini-2.5-flash)|5|5|5|5|---|The examples were provided in natural language to understand the concept, the process is much more detailed, it explains the phosynthesis formula|Y|
|Role|You are a biology professor. Explain photosynthesis to a high school student.|Llama3|3|5|3|5|The information is concise, however the role is not taken into account|-------|Y|
|Role|You are a biology professor. Explain photosynthesis to a high school student.|Mistral|3|3|5|3|shallow|The information is also concise, the role was taken into account, without technical details.|N|
|Role|You are a biology professor. Explain photosynthesis to a high school student.|OpenAI (gpt-5-mini)|5|5|3|5|information in greater detail, the process is explained in detail|-------|Y|
|Role|You are a biology professor. Explain photosynthesis to a high school student.|Gemini(gemini-2.5-flash)|5|5|5|5|The role is taken into account, explanation with practical exercise, as teachers do, detailed information|-------|Y|
|Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs.|Llama3|5|5|5|5|The inputs and the step-by-step explanation are great, explaining all the variables involved and the results.|-------|Y|
|Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs.|Mistral|5|5|5|5|shallow|The explanation of the inputs is good, however the results are very concise.|Y|
|Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs.|OpenAI (gpt-5-mini)|3|3|3|3|drift (format)|The inputs are not understood, the role of each variable is not explained correctly, and the results are not consistent.|N|
|Chain-of-Thought|Explain photosynthesis step-by-step, start with inputs (what plants need) and end with outputs.|Gemini(gemini-2.5-flash)|5|5|5|5|The inputs are explained in detail, concepts are clear, the step-by-step process is clear, and the results are consistent.|-------|Y|


## Model Summary (After Initial Pass)
| Capability | Best Model(s) | Evidence Snippet | Notes |
|------------|---------------|------------------|-------|
| Explanatory Clarity |Gemini(gemini-2.5-flash) | 2.  Water (H2O): Source: Absorbed from the soil by the plant's roots. How it travels:Transported up to the leaves through specialized vascular tissues called **xylem**. **Role:** Provides the electrons and protons (hydrogen ions, H+) needed for the light-dependent reactions, and is the source of the oxygen gas released during photosynthesis. |Technical concepts explained in detail, in natural language, and easy to understand |
| Chain-of-Thought |Llama3 | 1. **Light absorption**: Chlorophyll molecules absorb light energy from the sun, exciting electrons and initiating the photosynthetic process. 2. **Water splitting**: Plants use water (H2O) to produce hydrogen ions (H+) and oxygen (O2). This process is called photolysis. * H2O → 2H+ + O2 | The step-by-step instructions are concise and explained in a simple, easy-to-understand way.|
| JSON Adherence | Gemini(gemini-2.5-flash), Llama3, OpenAI (gpt-5-mini), Mistral |  | All models generated results correctly in JSON format without parsing issues.|
| Persona Control | Mistral and Gemini(gemini-2.5-flash)| Mistral: Photosynthesis! It's one of the coolest processes in biology, and it's essential for life on Earth. So, let me break it down for you in a way that's easy to understand. What is photosynthesis? Photosynthesis is the process by which plants, algae, and some bacteria convert light energy from the sun into chemical energy in the form of glucose (a type of sugar). This process occurs in specialized organelles called chloroplasts within plant cells.How does it work?|These two models better took into account the role, taking into account techniques that a teacher uses to make himself understood. |
| Instruction Strictness | Gemini(gemini-2.5-flash) | 2) Water splitting (photolysis) and O2 release (thylakoid lumen), - The oxygen-evolving complex associated with PSII splits water: H2O → 2 H+ + 2 e− + 1/2 O2.- Electrons from water replace those lost by PSII; O2 is produced and released to the atmosphere.| This model seems less friendly to me, more direct, and goes to the specific point. |

## Insight Log
Record notable surprises, regressions, or improvements.
- Day 1:
- Day 2:
- Day 3:

---

### 1. Role Prompting

*   **Best Practice:**
    *   Clearly define the persona or role you want the AI to adopt. This helps to set the context, tone, and level of detail in the response.
*   **Example:**
    *   Instead of "Explain black holes," use "You are an astrophysicist. Explain the concept of a black hole to a curious 10-year-old."

---

### 2. Few-Shot Learning

*   **Best Practice:**
    *   Provide a few examples of the desired input and output format. This is especially useful for tasks like classification, summarization, or code generation.
*   **Example:**
    *   When asking for a summary, provide one or two examples of a text and its corresponding summary before providing the text you want to be summarized.

---

### 3. Chain-of-Thought (CoT)

*   **Best Practice:**
    *   Encourage the model to "think step by step" or to "show its work." This is particularly effective for complex reasoning tasks, such as math problems or logic puzzles.
*   **Example:**
    *   Append "Let's think step by step" to your prompt when you need the model to reason through a problem.

---

### 4. Anti-Patterns to Avoid
## Reflection (End of Week)
Answer briefly:
1. Which two prompt patterns yielded the largest delta between models?
2. Which failure mode was most frequent? Root cause?
3. Default model choice for: explanation / reasoning / structure.
4. Open questions heading into Week 2.
*   **Ambiguity:**
    *   Avoid vague or open-ended questions. Be as specific as possible.
*   **Leading Questions:**
    *   Don't phrase your prompt in a way that suggests a desired answer.
*   **Overly Complex Prompts:**
    *   Break down complex tasks into smaller, more manageable prompts.

---
