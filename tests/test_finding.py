from src.models.finding import Finding


def test_finding_stores_all_required_fields():
    finding = Finding(
        rule_name="wildcard_action",
        severity="High",
        reason="Policy allows all actions.",
        resource="*",
        remediation="Replace wildcard permissions with specific actions.",
    )

    assert finding.rule_name == "wildcard_action"
    assert finding.severity == "High"
    assert finding.reason == "Policy allows all actions."
    assert finding.resource == "*"
    assert finding.remediation == (
        "Replace wildcard permissions with specific actions."
    )


def test_remediation_defaults_to_empty_string():
    finding = Finding(
        rule_name="wildcard_resource",
        severity="High",
        reason="Policy allows access to all resources.",
        resource="*",
    )

    assert finding.remediation == ""
