import logging

from src.models.normalized_policy import NormalizedPolicy

logger = logging.getLogger(__name__)


def _to_list(value):
    """Normalize a string or list into a list."""
    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def parse_aws_policy(policy: dict) -> list[NormalizedPolicy]:
    """
    Convert an AWS IAM policy document into normalized policies.

    Each AWS statement becomes one NormalizedPolicy object.
    """

    statements = policy.get("Statement", [])

    if isinstance(statements, dict):
        statements = [statements]

    if not isinstance(statements, list):
        raise TypeError("AWS policy Statement must be a dictionary or list")

    normalized_policies = []

    for statement in statements:
        if not isinstance(statement, dict):
            raise TypeError("Each AWS policy statement must be a dictionary")

        effect = statement.get("Effect")

        if effect not in ("Allow", "Deny"):
            raise ValueError(f"Unsupported AWS policy Effect: {effect}")

        permissions = {
            "allow": [],
            "deny": [],
            "exclusions": [],
        }

        actions = _to_list(statement.get("Action"))
        not_actions = _to_list(statement.get("NotAction"))

        if effect == "Allow":
            permissions["allow"] = actions
        else:
            permissions["deny"] = actions

        permissions["exclusions"] = not_actions

        principal = statement.get("Principal")

        if isinstance(principal, dict):
            subjects = [
                f"{principal_type}:{subject}"
                for principal_type, values in principal.items()
                for subject in _to_list(values)
            ]
        else:
            subjects = _to_list(principal)

        normalized_policy = NormalizedPolicy(
            provider="aws",
            subjects=subjects,
            resources=_to_list(statement.get("Resource")),
            conditions=statement.get("Condition"),
            raw_source=statement,
        )

        normalized_policy.permissions.allow = permissions["allow"]
        normalized_policy.permissions.deny = permissions["deny"]
        normalized_policy.permissions.exclusions = permissions["exclusions"]

        normalized_policies.append(normalized_policy)

    logger.info(
        "Parsed AWS IAM policy containing %d statements",
        len(normalized_policies),
    )

    return normalized_policies
