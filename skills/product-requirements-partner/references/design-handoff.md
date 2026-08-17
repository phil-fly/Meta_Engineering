# Design & Handoff Reference

Conventions for visual mockups, design tokens, iteration workflow, and development handoff. New projects use `ai-agent-workspace/product/design/`; existing projects may keep compatible `docs/03_DESIGN/` as the confirmed source of truth.

---

## Core Principle: Physical Isolation

Design files and production code are always separate artifacts:

```
ai-agent-workspace/product/design/  ← visual iteration happens here
  design-tokens.md
  screens/
    home.html
    detail.html
    settings.html
  handoff/
    home.md
    detail.md

src/                     ← only touched after design is confirmed
```

Visual changes → edit the product design directory only.
Production implementation → only after the screen's handoff note exists and is confirmed.

---

## Design Tokens

Only require `design-tokens.md` when the target repository already contains a real frontend implementation or the current work will introduce the first frontend implementation. A `package.json`, design file, prototype, or product document alone is not frontend implementation evidence. When no frontend implementation exists and none will be introduced, do not create the file.

When the condition applies, locate and read the single editable `ai-agent-workspace/product/design/design-tokens.md` or compatible `docs/03_DESIGN/design-tokens.md` before frontend design or development. If an existing frontend has no file, create it and backfill it from production Token, Theme, component, layout, and responsive sources before producing mockups. Do not create a parallel token set. Missing values remain explicit `pending`, `not found`, or `not applicable` entries until confirmed.

The file must contain actual detail rather than route links. At minimum it records document status; production source-of-truth and derivation relationships; Color; Typography; Spacing; Size/Density; Radius; Border; Shadow/Elevation; Layout/Grid; Breakpoint/Responsive behavior; z-index; Motion; Icon; Component Token; Theme; exceptions; maintenance rules; and long-lived changes. Each applicable domain records the semantic name, current value or formula, production definition, consumers, override priority, status, and exceptions.

```markdown
# Design Tokens

## Source Of Truth
| Domain | Production source | Derived consumers | Priority | Status | Exceptions |
| --- | --- | --- | --- | --- | --- |
| Color | pending | pending | pending | pending | pending |

## Color
| Semantic name | Token | Light | Dark | Usage | Status |
| --- | --- | --- | --- | --- | --- |
| primary | pending | pending | pending | pending | pending |

## Typography
## Spacing
## Size And Density
## Radius
## Border
## Shadow And Elevation
## Layout And Grid
## Breakpoints And Responsive Behavior
## Z-index And Layering
## Motion
## Icons
## Component Tokens
## Theme And Brand Modes
## Exceptions And Debt
## Maintenance Contract
## Change Log
```

---

## Design Artifact Levels

Choose the lightest artifact that can answer the current question:

| Level | Use When | Artifact | Notes |
| --- | --- | --- | --- |
| Static visual mockup | Layout, hierarchy, visual tone, stakeholder review | Self-contained HTML in `ai-agent-workspace/product/design/screens/` or compatible `docs/03_DESIGN/screens/` | No production code changes |
| Interactive prototype | Flow, transitions, conditional states, form behavior | HTML prototype or component demo in `ai-agent-workspace/product/design/prototypes/` or compatible `docs/03_DESIGN/prototypes/` | May include lightweight JS for prototype-only behavior |
| Development handoff | Design is confirmed and engineering needs build details | Handoff note in `ai-agent-workspace/product/design/handoff/` or compatible `docs/03_DESIGN/handoff/` | Must reference entities, states, edge cases |

Do not use a high-fidelity mockup to hide unresolved flow or entity questions.

---

## Screen Mockup Format

Each screen is one self-contained HTML file. Rules:

- **All styles inline** — no external CSS, no build tools
- **Static by default** — interactions described in text comments, not implemented in JS unless the artifact is explicitly an interactive prototype
- **Opens in any browser** — no dependencies
- **References tokens** — use CSS variables at the top of the `<style>` block

File naming: `{screen-name}.html`
Examples: `home.html`, `onboarding-step-1.html`, `settings-notifications.html`

### HTML template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Screen Name} — {Project}</title>
  <style>
    /* Design tokens */
    :root {
      --color-primary: #_____;
      --color-surface: #_____;
      --color-text-primary: #_____;
      --color-text-secondary: #_____;
      --color-border: #_____;
      --radius-md: ___px;
      --space-4: 4px;
      --space-8: 8px;
      --space-16: 16px;
      --space-24: 24px;
    }

    /* Screen styles */
    body { margin: 0; font-family: ____; background: var(--color-surface); }
    /* ... */
  </style>
</head>
<body>
  <!-- Screen content -->

  <!-- INTERACTION NOTES:
    - Tapping [X] opens the detail sheet
    - Pull-to-refresh triggers data reload
    - Long-press on list item reveals delete action
  -->
</body>
</html>
```

---

## Visual Quality Standard

Mockups should be **opinionated and specific** — not wireframes, not generic UI. Apply a clear aesthetic direction:

- Choose a visual tone and commit to it (minimal / editorial / utilitarian / etc.)
- Typography choices should inherit the confirmed project standard. For a new project, choose an intentional family and record loading, fallback, and performance implications instead of rejecting system fonts by default.
- Color usage should create hierarchy, not just fill space
- Spacing should feel designed, not default

The goal: a stakeholder looking at the mockup should immediately understand what the product feels like, not just what it contains.

---

## Iteration Workflow

```
1. Scene 3 (Interaction Design) + Scene 4 (Entity Definition) produce: page list, information hierarchy, entity model
        ↓
2. Scene 5 reads the single design-tokens.md when frontend implementation exists; it backfills a missing file from production or creates one before the first frontend implementation, then creates first-pass HTML mockups
        ↓
3. Visual review: open in browser, discuss, edit HTML only
        ↓
4. Design confirmed: write handoff note in `ai-agent-workspace/product/design/handoff/` or compatible `docs/03_DESIGN/handoff/`
        ↓
5. Development: dev agent reads handoff note + mockup, implements in src/
        ↓
6. If visual tweaks needed post-implementation: update mockup first, then src/
```

Never jump from step 3 to step 5 without a handoff note.

---

## Handoff Note Format

File: `ai-agent-workspace/product/design/handoff/{screen-name}.md` or compatible `docs/03_DESIGN/handoff/{screen-name}.md`

```markdown
# Handoff: {Screen Name}

**Mockup:** `ai-agent-workspace/product/design/screens/{screen-name}.html`
**Status:** Ready for development / Needs revision

## Components
- [ ] {Component name}: {brief description}
- [ ] {Component name}: {brief description}

## Key Interactions
- {Trigger} → {Result}: {any relevant state change}
- {Trigger} → {Result}: {any relevant state change}

## Entities & State Changes
- {EntityName}.{field} changes from {A} to {B} when {action}
- Reads: {list of entities/fields displayed}
- Writes: {list of entities/fields modified}

## Edge Cases
- {Condition}: {how to handle}
- {Condition}: {how to handle}

## Open Questions
- [ ] {Question that needs resolution before or during development}
```

---

## Scene 3/4 → Scene 5 Transition

Before starting mockups, confirm this checklist is complete from Scene 3 (Interaction Design) and Scene 4 (Entity Definition):

- [ ] Screen list defined (from Screen Tree in Framework PRD)
- [ ] Each screen's information hierarchy described
- [ ] Primary interactions per screen listed
- [ ] Entity model defined and validated against page structure
- [ ] Existing frontend implementation: the single `design-tokens.md` was read, or a missing file was backfilled from production Token/Theme, component, layout, responsive, and design-artifact sources
- [ ] First frontend implementation: the detailed `design-tokens.md` was created before UI code; repositories without frontend implementation and without frontend scope did not create it
- [ ] Component states, long-text behavior, permissions, and applicable responsive behavior described for handoff

If any item is missing, return to the relevant scene before generating HTML.
