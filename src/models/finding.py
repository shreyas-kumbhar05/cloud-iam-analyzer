from dataclasses import dataclass


@dataclass
class Finding:
    """Represents a security finding detected by an IAM analysis rule."""

    rule_name: str
    severity: str
    reason: str
    resource: str
    remediation: str = ""
