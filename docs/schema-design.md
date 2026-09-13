# Normalized Policy Schema

## Purpose

The normalized policy schema provides one common representation for authorization statements from different cloud providers.

Each provider can represent policies differently, so the parser for each provider converts its native policy structure into the same `NormalizedPolicy` structure. This allows the rule engine and the components that come after it to work with one common representation instead of needing separate logic for AWS, Azure, GCP, and other providers.

The schema is designed to preserve the important security semantics of the original policy. Provider-specific information that cannot be represented directly in the common schema should not be silently discarded.

## Statement-Level Normalization

A `NormalizedPolicy` represents **one authorization statement**, not an entire policy document.

A policy document can contain multiple statements, and each statement can have different subjects, permissions, resources, and conditions. Therefore, the parser converts each statement into its own `NormalizedPolicy` object.

For example:

```text
Policy document
├── Statement 1 → NormalizedPolicy
├── Statement 2 → NormalizedPolicy
└── Statement 3 → NormalizedPolicy
```

This gives the rule engine a single, well-defined authorization unit to analyze.

## Fields

### `provider`

Identifies which cloud provider produced the normalized policy.

```python
provider: str
```

This is part of the normalized model so that downstream components, especially the rule engine, can determine which provider a policy came from without inspecting provider-specific structures.

### `subjects`

Represents **who** the statement applies to.

```python
subjects: list[str]
```

The name `subjects` is intentionally provider-neutral. Different providers may use different terminology or structures for identities, so the provider-specific parser converts those representations into the common concept of subjects.

### `permissions`

Represents **what** actions are allowed, denied, or excluded by the statement.

```python
permissions: PermissionRepresentation
```

The permission representation contains:

```text
allow
deny
exclusions
```

where:

- `allow` contains permitted actions.
- `deny` contains explicitly denied actions.
- `exclusions` preserves exclusion semantics where a provider represents permissions using exceptions or exclusions.

Keeping these separately is important because reducing a policy to only allowed actions could lose security-relevant authorization semantics such as explicit deny rules or exclusions.

### `resources`

Represents **where** the permissions apply.

```python
resources: list[str]
```

Permissions and resources are kept separate because they describe different parts of authorization:

```text
permissions → WHAT can be done
resources   → WHERE it can be done
```

This also allows the rule engine to reason directly about the scope of a permission without having to parse a combined representation.

### `conditions`

Represents any conditions under which the statement applies.

```python
conditions: dict | None
```

`None` means that the statement does not contain a condition.

A dictionary contains the actual provider-normalized condition information when a condition is present.

Keeping the absence of a condition explicit is important because some security rules may need to distinguish between a statement that has no condition and one that is conditionally restricted.

### `metadata`

Stores provider-specific information that is meaningful but cannot be represented cleanly in the common normalized fields.

```python
metadata: dict
```

The purpose of `metadata` is not to store everything from the provider's policy. Information that can be represented by the common schema should be normalized into the appropriate field.

Provider-specific information should remain in `metadata` when removing it would otherwise lose useful security semantics.

### `raw_source`

Stores the original provider policy representation from which the normalized statement was created.

```python
raw_source: dict
```

This preserves the original source for traceability.

For example, if the normalized object contains an unexpected permission, `raw_source` allows us to compare the normalized result with the original provider statement and determine whether the unexpected value came from the original policy or from a parser error.

## Design Principles

### Provider-Neutral Representation

All provider parsers convert their native policy structures into one common normalized schema.

The normalized schema therefore uses concepts such as:

```text
provider
subjects
permissions
resources
conditions
metadata
raw_source
```

rather than adopting the field names and structures of one particular provider.

### Preserve Security Semantics

Normalization must not silently discard security-relevant information.

When a provider has semantics that fit the common schema, they should be represented directly. When they do not fit, the relevant provider-specific information should be retained through `metadata` or `raw_source` rather than being lost.

### One Normalized Object per Statement

Each authorization statement becomes one `NormalizedPolicy` object. This keeps the unit analyzed by the rule engine small and well defined while preserving the different semantics of individual statements.
