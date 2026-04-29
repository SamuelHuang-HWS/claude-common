#!/usr/bin/env python3
"""Static health checks for Sisyphus proj-* skills and contracts."""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Set, Tuple

try:
    import yaml
except ImportError:
    print(json.dumps({
        "status": "FAIL",
        "findings": [{
            "severity": "ERROR",
            "rule": "dependency",
            "path": "system",
            "message": "PyYAML is required but not installed."
        }]
    }, indent=2, ensure_ascii=False))
    sys.exit(1)


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_against_schema(data: Dict[str, Any], schema: Dict[str, Any], path: str) -> List[Dict[str, str]]:
    """Validate a small JSON-schema subset without adding jsonschema dependency."""
    findings: List[Dict[str, str]] = []
    properties = schema.get("properties", {})

    for field in schema.get("required", []):
        if field not in data:
            findings.append({
                "severity": "ERROR",
                "rule": "contract_required_fields",
                "path": path,
                "message": f"Missing required field: {field}"
            })

    type_map = {
        "string": str,
        "boolean": bool,
        "integer": int,
        "array": list,
        "object": dict,
    }

    for field, value in data.items():
        spec = properties.get(field)
        if not spec:
            if schema.get("additionalProperties") is False:
                findings.append({
                    "severity": "ERROR",
                    "rule": "contract_unknown_field",
                    "path": path,
                    "message": f"Unknown field: {field}"
                })
            continue

        expected_type = spec.get("type")
        if expected_type:
            py_type = type_map.get(expected_type)
            if py_type and not isinstance(value, py_type):
                findings.append({
                    "severity": "ERROR",
                    "rule": "contract_field_type",
                    "path": path,
                    "message": f"Field {field} must be {expected_type}"
                })
                continue

        if "enum" in spec and value not in spec["enum"]:
            findings.append({
                "severity": "ERROR",
                "rule": "contract_field_enum",
                "path": path,
                "message": f"Field {field} has invalid value {value!r}; expected one of {spec['enum']}"
            })

        if isinstance(value, str) and spec.get("minLength") and len(value) < spec["minLength"]:
            findings.append({
                "severity": "ERROR",
                "rule": "contract_field_min_length",
                "path": path,
                "message": f"Field {field} must not be empty"
            })

        if isinstance(value, list):
            min_items = spec.get("minItems")
            if min_items is not None and len(value) < min_items:
                findings.append({
                    "severity": "ERROR",
                    "rule": "contract_field_min_items",
                    "path": path,
                    "message": f"Field {field} must contain at least {min_items} item(s)"
                })
            item_type = (spec.get("items") or {}).get("type")
            py_item_type = type_map.get(item_type)
            if py_item_type:
                for idx, item in enumerate(value):
                    if not isinstance(item, py_item_type):
                        findings.append({
                            "severity": "ERROR",
                            "rule": "contract_item_type",
                            "path": path,
                            "message": f"Field {field}[{idx}] must be {item_type}"
                        })

    if data.get("role") == "deprecated" and not data.get("deprecated_by"):
        findings.append({
            "severity": "ERROR",
            "rule": "deprecated_contract_requires_replacement",
            "path": path,
            "message": "Contracts with role=deprecated must set deprecated_by"
        })

    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Sisyphus Skill Health Check")
    parser.add_argument("--skills-root", required=True, help="Path to the skills directory")
    parser.add_argument("--manifest", required=True, help="Path to skill-sync-manifest.json")
    parser.add_argument("--contracts", required=True, help="Path to the contracts directory")
    args = parser.parse_args()

    findings: List[Dict[str, str]] = []
    has_error = False

    def add_finding(severity: str, rule: str, path: str, message: str) -> None:
        nonlocal has_error
        if severity == "ERROR":
            has_error = True
        findings.append({
            "severity": severity,
            "rule": rule,
            "path": path,
            "message": message,
        })

    def add_many(new_findings: List[Dict[str, str]]) -> None:
        for finding in new_findings:
            add_finding(finding["severity"], finding["rule"], finding["path"], finding["message"])

    # 1. Skills root and SKILL.md frontmatter.
    if os.path.islink(args.skills_root) and not os.path.exists(os.path.realpath(args.skills_root)):
        add_finding("ERROR", "symlink_resolves", args.skills_root, "Broken skills root symlink")

    try:
        skill_dirs = sorted(d for d in os.listdir(args.skills_root) if d.startswith("proj-") or d == "cross-review")
    except Exception as e:
        add_finding("ERROR", "skills_root_access", args.skills_root, str(e))
        skill_dirs = []

    valid_skill_names: Set[str] = set()
    for skill_name in skill_dirs:
        dir_path = os.path.join(args.skills_root, skill_name)
        if not os.path.isdir(dir_path):
            continue

        if os.path.islink(dir_path) and not os.path.exists(os.path.realpath(dir_path)):
            add_finding("ERROR", "symlink_resolves", dir_path, "Broken skill symlink")
            continue

        skill_md_path = os.path.join(dir_path, "SKILL.md")
        if not os.path.exists(skill_md_path):
            add_finding("ERROR", "skill_md_exists", dir_path, "SKILL.md not found")
            continue

        valid_skill_names.add(skill_name)

        try:
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.splitlines()
            if not lines or lines[0].strip() != "---":
                add_finding("ERROR", "frontmatter_present", skill_md_path, "No frontmatter found")
                continue

            frontmatter_lines = []
            closed = False
            for line in lines[1:]:
                if line.strip() == "---":
                    closed = True
                    break
                frontmatter_lines.append(line)
            if not closed:
                add_finding("ERROR", "frontmatter_closed", skill_md_path, "Frontmatter closing marker not found")
                continue

            fm = yaml.safe_load("\n".join(frontmatter_lines)) or {}
            if not isinstance(fm, dict):
                add_finding("ERROR", "frontmatter_parse", skill_md_path, "Frontmatter is not a YAML object")
                continue

            if fm.get("name") != skill_name:
                add_finding("ERROR", "name_matches_directory", skill_md_path, f"name {fm.get('name')!r} != dir {skill_name!r}")

            description = fm.get("description")
            if not description:
                add_finding("ERROR", "description_present", skill_md_path, "Missing description in frontmatter")
            elif len(str(description)) > 1024:
                add_finding("WARN", "description_length", skill_md_path, "Description exceeds 1024 characters")

        except yaml.YAMLError as e:
            add_finding("ERROR", "frontmatter_parse", skill_md_path, str(e))
        except Exception as e:
            add_finding("ERROR", "skill_md_read", skill_md_path, str(e))

    # 2. Manifest JSON.
    try:
        manifest = load_json(args.manifest)
        if "generated_at" not in manifest:
            add_finding("WARN", "manifest_format", args.manifest, "Missing generated_at")
    except Exception as e:
        add_finding("ERROR", "manifest_json_valid", args.manifest, str(e))

    # 3. Contract schema and contracts.
    schema_path = os.path.join(args.contracts, "contract.schema.json")
    try:
        schema = load_json(schema_path)
    except Exception as e:
        add_finding("ERROR", "contract_schema_valid", schema_path, str(e))
        schema = {"required": [], "properties": {}}

    try:
        contract_files = sorted(f for f in os.listdir(args.contracts) if f.endswith(".contract.yaml"))
    except Exception as e:
        add_finding("ERROR", "contracts_dir_access", args.contracts, str(e))
        contract_files = []

    contract_names: Set[str] = set()
    contract_next_skills: Set[Tuple[str, str]] = set()
    contract_deprecated: Set[str] = set()

    for contract_file in contract_files:
        contract_path = os.path.join(args.contracts, contract_file)
        contract_name = contract_file.replace(".contract.yaml", "")
        contract_names.add(contract_name)
        try:
            data = load_yaml(contract_path)
            if not isinstance(data, dict):
                add_finding("ERROR", "contract_yaml_parse", contract_path, "Contract YAML is not an object")
                continue

            add_many(validate_against_schema(data, schema, contract_path))

            if data.get("name") != contract_name:
                add_finding("ERROR", "contract_name_matches_file", contract_path, f"name {data.get('name')!r} != file {contract_name!r}")

            if data.get("name") not in valid_skill_names:
                add_finding("ERROR", "contract_skill_exists", contract_path, f"Skill directory not found for contract: {data.get('name')}")

            if data.get("role") == "deprecated":
                contract_deprecated.add(contract_name)

            for next_skill in data.get("next_skills") or []:
                contract_next_skills.add((contract_name, next_skill))
        except yaml.YAMLError as e:
            add_finding("ERROR", "contract_yaml_parse", contract_path, str(e))
        except Exception as e:
            add_finding("ERROR", "contract_yaml_parse", contract_path, str(e))

    missing_contracts = sorted(valid_skill_names - contract_names)
    for skill_name in missing_contracts:
        add_finding("ERROR", "contract_coverage", args.contracts, f"Missing contract for active skill: {skill_name}")

    for skill_name in sorted(contract_names - valid_skill_names):
        add_finding("ERROR", "contract_orphan", args.contracts, f"Contract has no matching skill: {skill_name}")

    for source, target in sorted(contract_next_skills):
        if target not in valid_skill_names:
            add_finding("ERROR", "contract_next_skills_exist", source, f"Target skill does not exist: {target}")
        if target in contract_deprecated:
            add_finding("ERROR", "deprecated_not_main_route", source, f"Routes to deprecated skill: {target}")

    # 4. Review loop policy declaration.
    policy_path = os.path.join(os.path.dirname(args.contracts), "references", "review-loop-policy-v1.md")
    if os.path.exists(policy_path):
        try:
            with open(policy_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "max_rounds" not in content or "doom-loop" not in content:
                add_finding("WARN", "review_loop_policy", policy_path, "Missing max_rounds or doom-loop declaration")
        except Exception as e:
            add_finding("WARN", "review_loop_policy", policy_path, str(e))
    else:
        add_finding("WARN", "review_loop_policy", policy_path, "review-loop-policy-v1.md not found")

    output = {
        "status": "FAIL" if has_error else ("WARN" if findings else "PASS"),
        "summary": {
            "skills_checked": len(valid_skill_names),
            "contracts_checked": len(contract_files),
            "findings": len(findings),
        },
        "findings": findings,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
