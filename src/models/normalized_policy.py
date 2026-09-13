from dataclasses import dataclass, field


@dataclass
class PermissionRepresentation:
    allow: list[str] = field(default_factory=list)
    deny: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)


@dataclass
class NormalizedPolicy:
    provider: str
    subjects: list[str] = field(default_factory=list)
    permissions: PermissionRepresentation = field(
        default_factory=PermissionRepresentation
    )
    resources: list[str] = field(default_factory=list)
    conditions: dict | None = None
    metadata: dict = field(default_factory=dict)
    raw_source: dict = field(default_factory=dict)
