# Deck JSON

Use this intermediate format between text planning and PPTX generation.

```json
{
  "title": "Deck title",
  "subtitle": "Optional subtitle",
  "theme": "light",
  "source": "Source: user-provided text",
  "slides": [
    {
      "section": "Optional section",
      "title": "Insight title",
      "bullets": ["One idea", "Second idea"],
      "notes": "Speaker notes"
    }
  ]
}
```

Rules:

- Keep titles under 90 characters.
- Use 2-5 bullets per slide.
- Keep bullets under 120 characters when possible.
- Put paragraphs, quotes, and narration into `notes`.
- Preserve Korean text unless improving clarity is part of the task.
- Use `theme: "dark"` only when the user asks for it.
- Use `source` for a short footer; include `Source:` in the value.

Example:

```json
{
  "title": "AI Workflow Adoption",
  "subtitle": "From experiments to operating cadence",
  "theme": "light",
  "source": "Source: user-provided notes",
  "slides": [
    {
      "section": "KEY MESSAGE",
      "title": "AI work is moving from prompt craft to workflow design",
      "bullets": [
        "Teams get more value from repeatable systems than one-off answers",
        "Context selection and evaluation now drive output quality",
        "Reusable workflows make quality easier to audit"
      ],
      "notes": "Use this slide to frame the main shift."
    }
  ]
}
```
