from src.models.normalized_policy import NormalizedPolicy
from src.parsers.aws_parser import parse_aws_policy


def test_parse_single_statement_policy():
    policy = {
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::example-bucket/*",
        },
    }

    result = parse_aws_policy(policy)

    assert len(result) == 1
    assert isinstance(result[0], NormalizedPolicy)
    assert result[0].provider == "aws"
    assert result[0].subjects == ["*"]
    assert result[0].permissions.allow == ["s3:GetObject"]
    assert result[0].resources == ["arn:aws:s3:::example-bucket/*"]


def test_parse_multiple_statements():
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::example-bucket/*",
            },
            {
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:DeleteObject",
                "Resource": "arn:aws:s3:::example-bucket/*",
            },
        ],
    }

    result = parse_aws_policy(policy)

    assert len(result) == 2
    assert result[0].permissions.allow == ["s3:GetObject"]
    assert result[1].permissions.deny == ["s3:DeleteObject"]


def test_parse_multiple_actions():
    policy = {
        "Statement": {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
            ],
            "Resource": "arn:aws:s3:::example-bucket/*",
        }
    }

    result = parse_aws_policy(policy)

    assert result[0].permissions.allow == [
        "s3:GetObject",
        "s3:PutObject",
    ]


def test_parse_deny_statement():
    policy = {
        "Statement": {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:DeleteObject",
            "Resource": "*",
        }
    }

    result = parse_aws_policy(policy)

    assert result[0].permissions.deny == ["s3:DeleteObject"]
    assert result[0].permissions.allow == []


def test_parse_policy_with_condition():
    condition = {"Bool": {"aws:SecureTransport": "true"}}

    policy = {
        "Statement": {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::example-bucket/*",
            "Condition": condition,
        }
    }

    result = parse_aws_policy(policy)

    assert result[0].conditions == condition


def test_parse_not_action():
    policy = {
        "Statement": {
            "Effect": "Allow",
            "Principal": "*",
            "NotAction": "iam:DeleteUser",
            "Resource": "*",
        }
    }

    result = parse_aws_policy(policy)

    assert result[0].permissions.exclusions == ["iam:DeleteUser"]


def test_parse_missing_condition():
    policy = {
        "Statement": {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "*",
        }
    }

    result = parse_aws_policy(policy)

    assert result[0].conditions is None


def test_preserve_raw_statement():
    statement = {
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "*",
    }

    policy = {"Statement": statement}

    result = parse_aws_policy(policy)

    assert result[0].raw_source == statement


def test_parse_empty_statement_list():
    policy = {
        "Version": "2012-10-17",
        "Statement": [],
    }

    result = parse_aws_policy(policy)

    assert result == []
