
# Normalized Policy Schema

  

## Purpose

  

Different cloud providers represent policies in different ways. Therefore, there is a need for one common way to show what's allowed and what is not across AWS, Azure, GCP, and others cloud platforms.

  

Each provider has its own format, the parser for each one converts that native structure into `NormalizedPolicy`. Since all formats are converted into one Normalized form, the rule engine and everything downstream work with one representation instead of needing separate logic for every provider.

Also, provider-specific information that cannot be fit into the common schema does not disappear but is preserved   


## Statement-Level Normalization

  

One `NormalizedPolicy` equals one authorisation statement. Not an entire policy document.

  

Policy documents contain multiple statements. Each one might have different subjects, permissions, resources, and conditions. 

So the parser takes each statement and converts it into its own `NormalizedPolicy` object.

  

### Example:

  

```text

Policy document

├── Statement 1 → NormalizedPolicy

├── Statement 2 → NormalizedPolicy

└── Statement 3 → NormalizedPolicy

```

  

Rule engine gets a single, clear unit to analyze.

  

## Fields

  

### `provider`

  

**Type:**  `str`

Gives information about which cloud provider created this normalized policy. Downstream components, including the rule engine, must know where this policy came from without needing to know provider-specific structure  

  

### `subjects`

  

**Type:**  `list[str]`

Subject is used to indicate the entities the statement applies to. There can be more than 1 subject in the list.

In the normalised schema, I am intentionally calling this subjects and not principal, as principle is AWS terminology


### `permissions`

  

**Type:**  `PermissionRepresentation`

  

Indicates what actions are allowed, denied, or excluded.

Permission representation has three parts:

-  `allow` - permitted actions

-  `deny` - explicitly denied actions

-  `exclusions` - preserves exclusion semantics where a provider uses exceptions or exclusions

 
 From my perspective, separating these 3 matters, as I cannot store them in a list because it will convey different meanings in different scenarios.  


### `resources`

  
**Type:**  `list[str]`

  

Where the permissions apply. Permissions and resources stay separate because they describe different parts:

  

- permissions → what can be done

- resources → where it can be done

  

The rule engine reasons about permission scope without parsing a combined representation.

  

### `conditions`

  

**Type:**  `dict or None`

  

Any conditions under which the statement applies.

  

`None` means no condition exists.

  

Dictionary contains the actual provider-normalised condition information when one is present. Absence of condition needs to be explicit. 

  

### `metadata`

  

**Type:**  `dict`

  

Will contain provider-specific information that's meaningful but doesn't fit cleanly into common normalized fields.

  

Not a dumping ground for everything in the provider policy. Information that fits the common schema gets normalised into the right field.

The Provider-specific information stays in metadata when removing it would lose useful security semantics.

  

### `raw_source`

  

**Type:**  `dict`

  
This will include the original provider policy which is unmodified. This is preserved for traceability 

If normalized object has an unexpected permission, `raw_source` helps compare the normalized result with the original provider statement.

This will help in understanding whether the unexpected value came from the original policy or is from a parser error
 

## Design Principles

  

### Provider-Neutral Representation

All provider parsers convert native policy structures into one common normalized schema.

Normalized schema uses concepts like:

-  `provider`

-  `subjects`

-  `permissions`

-  `resources`

-  `conditions`

-  `metadata`

-  `raw_source`

  
Since the schema is supposed to be normalized, the field names and structure of one particular provider is not used
 

### Preserve Security Semantics
Normalization doesn't discard security-relevant information.

When a provider has semantics that fit the common schema, it is represented directly. When they don't, I can retain the relevant provider-specific information through `metadata` or `raw_source`. 

### One Normalized Object per Statement

Each authorization statement becomes one `NormalizedPolicy` object. 

This keeps the unit analyzed by the rule engine small and well-defined while preserving the different semantics of individual statements.
