# Memory System Reference

Schemas, update rules, and initialization protocol for project memory, plus guidance on separating reusable skill behavior from project-specific product memory. New projects should use `ai-agent-workspace/product/`; existing projects may keep compatible `docs/` paths as the confirmed source of truth.

---

## Layer 1 — Personal Or Cross-Project Preferences

Layer 1 contains the user's reusable working style and cross-project product methodology. It is outside this skill and outside the current project's product memory unless the user explicitly asks to store it in a project document.

Do not assume a host-specific global path. If a Layer 1 change is proposed, first ask or infer from existing repository/user protocol where personal preferences should live, then state the target file and wait for confirmation before writing.

### Recommended Structure

```markdown
# Product Collaboration Preferences

## Working Style & Communication
- [e.g., I prefer to discuss ideal flow before touching entities]
- [e.g., Think in Chinese for strategy, English for technical specs]
- [e.g., Keep responses concise unless I ask for depth]
- [e.g., Always show the tradeoff, not just the recommendation]
- [e.g., Push back when feature list grows — I tend to over-scope]

## Cross-Project Methodology

### Validated Patterns
- **[Pattern name]** | Source: {project-id} | Confirmed: {date}
  - Context: when does this apply
  - Approach: what to do
  - Why it works: one sentence

### Anti-Patterns
- **[Anti-pattern name]** | Source: {project-id} | Confirmed: {date}
  - Context: what triggers this mistake
  - What goes wrong: one sentence

### Open Hypotheses
- **[Hypothesis]** | Source: {project-id} | Status: watching
  - Observation: what was noticed
  - Needs: one more project to confirm or refute
```

### Update rules

**Working Style** — update anytime via `[Meta]`. Low friction, high frequency.

**Cross-Project Methodology** — update only at two milestone moments:
1. When a Framework PRD is finalized
2. When a project phase closes

At these moments the AI scans `SESSION_MEMORY.md`, surfaces up to 3 candidate patterns, and writes only what the user confirms. Never auto-written.

### Write Threshold

Only write Layer 1 when the content is reusable across projects and the user confirms it should become a preference. Do not write one-off instructions, temporary project constraints, or ideas that were rejected in the same conversation.

---

## Layer 2 — Project Memory

**Location:** `{project_root}/ai-agent-workspace/product/memory/`
**Compatible legacy location:** `{project_root}/docs/00_MEMORY/`
**Visibility:** Visible to user, committed to git. This is the explicit memory of the project.

Project memory preserves evidence and history; it is not automatically the source of truth for final delivery. When memory is used to update a PRD, design artifact, handoff, title, or PR summary, apply `final-state-delivery.md`: current confirmed state wins, while rejected, superseded, and process-only entries stay in the history layer.

---

### ai-agent-workspace/product/memory/CONTEXT_SNAPSHOT.md

Compatible legacy path: `docs/00_MEMORY/CONTEXT_SNAPSHOT.md`.

**Role:** The "Evidence Locker". Records raw user inputs, constraints, and story samples that serve as the factual basis for decisions. **Append-only.**

```markdown
# Context Snapshots
> 事实快照库。记录关键的用户原始输入，作为决策依据。

## [CNT-001] 2026-03-05
> User: "我希望用户在断网时也能看到缓存的最近 5 条记录，但不能编辑。"
- **Tags**: #offline #constraint
- **Ref**: Session 2026-03-05 (Value Discovery)

## [CNT-002] 2026-03-06
> User: "这个流程太复杂了，我想要的是一键完成，不需要确认。"
- **Tags**: #ux #simplification
- **Ref**: Session 2026-03-06 (Logic Structuring)
```

**Update trigger:** 
- User tells a specific story (Scene 1).
- User sets a hard constraint.
- User explicitly corrects a misunderstanding.

Do not write:

- Casual brainstorming that the user has not endorsed.
- Temporary assumptions used only to explore an option.
- A rejected idea unless the rejection itself becomes an important constraint.

---

### ai-agent-workspace/product/memory/CONFIRMATIONS.md

Compatible legacy path: `docs/00_MEMORY/CONFIRMATIONS.md`.

**Role:** The append-only registry of explicit user confirmations. Each record is a complete post-change snapshot for one `Requirement ID + Scope/Version`; `CONTEXT_SNAPSHOT.md` preserves evidence, while `DECISIONS.md` records the resulting business judgment.

Source resolution is exclusive. New projects use `ai-agent-workspace/product/memory/CONFIRMATIONS.md`; an existing project may keep `docs/00_MEMORY/CONFIRMATIONS.md`. If both files exist, the state is split-brain and final delivery stops until one source is migrated or removed. Resolve and validate the source from the project root with `scripts/validate-confirmations.py --project <project-root> --scope <scope_id@version> --json`.

```markdown
# User Confirmations — {project_id}

## CONF-001 · {Short object title}
- **Confirmed at:** 2026-03-06T10:30:00+08:00
- **Source:** Session 2026-03-06, message/turn {stable reference}
- **Object:** {human-readable requirement, decision, screen, flow, or scope title}
- **Requirement ID:** REQ-XXX {stable ID; Object is display text only}
- **Scope/Version:** {stable scope_id@version token, or scope_id@N/A}
- **Decision state:** confirmed | deferred | rejected
- **Change type:** add | patch | replace | remove
- **Affected fields:** {field.path, field.path} | N/A (required for patch; descriptive only)
- **Accepted conclusion:** {complete current conclusion after this event}
- **User quote:** "{exact confirmation wording}"
- **Status:** active | superseded | withdrawn (record lifecycle)
- **Supersedes:** CONF-XXX | N/A (required for replace/remove or a patch of an existing active record)
- **Related decision:** DEC-XXX | N/A

---
```

Every new or changed user-confirmed conclusion persisted for later delivery uses one `CONF-*` record. `proposed` and `pending` stay in the working layer or TODO until the user decides. All displayed fields except `Related decision` are required; `Affected fields` may be `N/A` except for `patch`, and `Supersedes` may be `N/A` only for the initial `add`. A missing field, duplicate ID, invalid timestamp, broken chain, non-latest active record, or active count other than one makes that reconstruction key `unresolved`.

`Status` describes record lifecycle; `Decision state` describes the accepted requirement outcome. Records for one exact `Requirement ID + Scope/Version` form a linear snapshot chain:

1. The first record is `add` and has `Supersedes: N/A`.
2. Every later `patch`, `replace`, or `remove` points to the immediately previous record.
3. Every record carries the complete current `Accepted conclusion`. A `patch` lists changed fields for review, but no consumer is expected to merge free-form fragments.
4. Earlier records are `superseded` or `withdrawn`; the latest record is the only `active` record.
5. `remove` records an explicit `rejected` or `deferred` current outcome.

Append corrections as new snapshots; do not rewrite history. The validator projects the unique active snapshot and can filter it by target `Scope/Version`.

**Update trigger:** An explicit user confirmation, version deferral, withdrawal, or supersession that must persist beyond the current conversation. A current explicit instruction is already authoritative for the current response; persistence is required only when project memory mode is active and a durable product artifact is being updated. If the user forbids memory writes, do not update this registry and report that persistence was not recorded. Short acknowledgements such as “好” or “提 PR” are recorded only when they answer one uniquely identified conclusion under `final-state-delivery.md`.

---

### ai-agent-workspace/product/memory/SESSION_MEMORY.md

Compatible legacy path: `docs/00_MEMORY/SESSION_MEMORY.md`.

**Role:** The "Narrative Log". Records what happened, connecting facts (Context) to conclusions (Decisions). **Append-only.**

```markdown
# Project Session Log

## 2026-03-05 · 离线模式讨论
- **Discussion**: 确认了离线缓存策略。
- **Evidence**: 基于 [CNT-001] 的用户约束。
- **Outcome**: 
  - 决定采用 LocalStorage 缓存方案 (见 DECISIONS.md -> DEC-005)
  - 拒绝了 SQLite 方案 (太重)
  - 新增 TODO: "验证 LocalStorage 容量限制"

## 2026-03-06 · 交互简化
- **Discussion**: 优化下单流程。
- **Evidence**: [CNT-002] 用户反馈。
- **Outcome**: 移除确认弹窗，改为 Toast 撤回机制。
```

**Update trigger:** End of a meaningful discussion loop or session.

Write only when there is a meaningful change in understanding, a decision draft, a resolved conflict, or a new product direction. Do not append a session entry after every small exchange.

---

### ai-agent-workspace/product/memory/TODO.md

Compatible legacy path: `docs/TODO.md`.

**Role:** The "Action List". Single source of truth for tasks.

```markdown
# TODO — {project_id}

## Open
- [ ] **TODO-001** `[value]` Description of what needs to be resolved
  - Trigger: "user's exact words"
  - Linked to: entity / flow step / screen / feature name
  - Added: 2026-03-01

## In Progress
- [ ] **TODO-002** `[flow]` Currently being worked on

## Done
- [x] **TODO-003** `[entity]` Resolved item — brief resolution note
  - Resolved: 2026-03-02

## Dropped
- [-] **TODO-004** `[value]` Item no longer relevant
  - Reason: scope cut in MVP decision DEC-003
```

**Dimension tags:** `[value]` `[flow]` `[entity]` `[interaction]` `[design]`

**Update triggers:**
- User signals uncertainty → append to Open
- Decision resolves a pending item → move to Done with resolution note
- Item becomes irrelevant → move to Dropped with reason

Only create TODOs that have an owner-worthy next action or decision. Do not create TODOs for vague curiosity unless the user wants to track it.

---

### ai-agent-workspace/product/strategy/DECISIONS.md

Compatible legacy path: `docs/01_STRATEGY/DECISIONS.md`.

**Role:** The "Rule Book". Human-readable record of business judgments.

```markdown
# Business Decisions — {project_id}

## DEC-001 · {Short decision title}
- **Date:** 2026-03-01
- **Status:** active | superseded
- **Supersedes:** DEC-XXX | N/A
- **Confirmation:** CONF-XXX
- **Context:** Based on [CNT-001]
- **Decision:** One sentence summary of what was decided
- **Rationale:** Why this direction, not alternatives
- **Trade-offs accepted:** What was explicitly de-prioritized
- **Residual risk:** Known open questions from this decision

---
```

**Written when:** Consensus Detection fires — user signals agreement on a business judgment.

**Critical rule:** DECISIONS are **never written without explicit user confirmation**. The AI may draft a decision, but it must present the draft and wait for the user to approve before writing to `DECISIONS.md`. Each new decision must reference a `CONF-*` record; the confirmation registry carries the object, scope/version, accepted conclusion, exact quote, timestamp, and source. If a later confirmation replaces an older decision in the same scope, write the new decision as `active`, mark the older decision `superseded`, and link both records. If the decision overrides or conflicts with an existing Context entry, it must explicitly reference the affected `[CNT-XXX]` and state the override reason.

**Legacy compatibility:** Existing decision entries without a `Status` field are treated as `active` only when they are covered by an explicit legacy-current marker and no later explicit confirmation, explicit supersession, or same-scope contradiction exists. The marker must be present in the authoritative document frontmatter and include exactly one entry for the scope:

```yaml
product_state: legacy-current
legacy_scope: {stable scope ID}
legacy_version: {version ID}
effective_at: {ISO-8601 timestamp with timezone}
```

The marker is evidence of an unchanged baseline, not a user confirmation, and cannot establish a new “latest” confirmation. Entries without the marker, with multiple markers for one scope, or with a marker that conflicts with another authoritative artifact are `unresolved`; ask the user or migrate the state into `CONFIRMATIONS.md`. New or edited entries must use `Status` and `Confirmation`.

Before relying on legacy compatibility, run `scripts/validate-legacy-current.py --path <authoritative-document> [<other-document> ...]`; duplicate scopes or malformed markers fail closed.

Decision threshold:

- Stable business judgment.
- Changes scope, user promise, pricing, permission, data retention, or core flow.
- Will be useful to future collaborators.

Do not write DECISIONS for wording choices, early hypotheses, or low-impact UI preferences.

---

## Project Initialization Protocol

When a new `project_id` is mentioned for the first time, create this skeleton in one step:

```
{project_root}/
├── docs/
├── ai-agent-workspace/
│   └── product/
│       ├── memory/
│       │   ├── CONTEXT_SNAPSHOT.md  ← Header + "事实快照库..."
│       │   ├── CONFIRMATIONS.md     ← Header + "User Confirmations"
│       │   ├── SESSION_MEMORY.md    ← Header + "Project Session Log"
│       │   └── TODO.md              ← initialized with empty sections
│       ├── strategy/
│       │   └── DECISIONS.md         ← empty, filled as business judgments are made
│       ├── prd/
│       │   ├── README.md            ← 目录与各 PRD 文件用途说明（不再承载 Framework PRD 正文）
│       │   └── framework-prd.md     ← 默认的 Framework PRD 主文档（可按项目约定更名）
│       ├── design/
│       │   ├── design-tokens.md     ← placeholder
│       │   ├── screens/
│       │   ├── handoff/
│       │   ├── ui_ux/
│       │   ├── prototypes/
│       │   ├── ai_prompts/
│       │   └── tech_design/
│       └── resources/               ← competitor research, raw inputs
```

**No .gitignore changes needed** (docs are meant to be committed).

Confirm to user: `"Project '{project_id}' initialized. Product workspace ready in ai-agent-workspace/product/. Memory includes CONTEXT_SNAPSHOT.md, CONFIRMATIONS.md, SESSION_MEMORY.md, and TODO.md; PRD docs initialized in product/prd/ (README + framework-prd.md)."`

---

## Two-Layer Principle Within Layer 2

| Sub-layer | Records | Files |
|-----------|---------|-------|
| **Objective facts** | What happened & User's raw input | `ai-agent-workspace/product/memory/SESSION_MEMORY.md`, `ai-agent-workspace/product/memory/CONTEXT_SNAPSHOT.md` |
| **Confirmation authority** | Explicit accepted state and ordering | `ai-agent-workspace/product/memory/CONFIRMATIONS.md` |
| **Logic assets** | Conclusions — decisions, flows, specs | `ai-agent-workspace/product/strategy/DECISIONS.md`, other product workspace docs |

Facts layer = history. Logic layer = conclusions. Final delivery is a current-state projection from the active conclusions, not a summary of both layers.

**When they conflict:**
1. If the confirmation registry contains a later `active` confirmation for the same object and scope, treat it as the current state and record the supersession without asking for the same decision again.
2. If the object, scope, condition, or replacement relationship is ambiguous, surface the conflict and wait for the user's judgment.
3. If the user decides to override, record a new active decision in `DECISIONS.md`, mark the older decision superseded when applicable, and explicitly reference the affected `[CNT-XXX]`.
4. The original Context and Session entries are never deleted or modified; they remain historical evidence and are not copied into final delivery unless `final-state-delivery.md` explicitly admits them.
