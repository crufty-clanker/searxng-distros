#!/usr/bin/env python3
"""
Validate SearXNG engine names in all distro settings.yml files.

Checks that all engines in enabled_engines and disabled_engines
are real SearXNG engines from the master branch.

Exit codes:
  0 - All engines valid
  1 - One or more invalid engines found
"""

import json
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple

SEARXNG_ENGINES_URL = (
    "https://api.github.com/repos/searxng/searxng/contents/searx/engines"
)


def fetch_real_engines() -> List[str]:
    """Fetch real SearXNG engine names from GitHub API."""
    req = urllib.request.Request(SEARXNG_ENGINES_URL, headers={"User-Agent": "Python"})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read())
        return sorted([item["name"].replace(".py", "") for item in data])


def parse_settings(filepath: Path) -> Dict[str, List[str]]:
    """Parse settings.yml and extract enabled_engines and disabled_engines."""
    result = {"enabled": [], "disabled": []}
    
    with open(filepath) as f:
        content = f.read()
    
    in_section = None
    current_section = None
    
    for line in content.split("\n"):
        stripped = line.strip()
        
        if stripped == "enabled_engines:":
            in_section = "enabled"
            current_section = result["enabled"]
        elif stripped == "disabled_engines:":
            in_section = "disabled"
            current_section = result["disabled"]
        elif in_section and stripped.startswith("- "):
            engine = stripped[2:].strip()
            if engine and not engine.startswith("#"):
                current_section.append(engine)
        elif in_section and not stripped.startswith("-") and not stripped.startswith("#"):
            in_section = None
            current_section = None
    
    return result


def validate_engines(
    engines: List[str], real_engines: List[str]
) -> Tuple[List[str], List[str]]:
    """Validate a list of engines against real engines."""
    invalid = [e for e in engines if e not in real_engines]
    valid = [e for e in engines if e in real_engines]
    return valid, invalid


def main():
    """Main validation function."""
    distros_dir = Path("distros")
    
    if not distros_dir.exists():
        print("❌ distros/ directory not found", file=sys.stderr)
        sys.exit(1)
    
    print("Fetching real SearXNG engines from GitHub...")
    try:
        real_engines = fetch_real_engines()
        print(f"✅ Loaded {len(real_engines)} real engines")
    except Exception as e:
        print(f"❌ Failed to fetch engines: {e}", file=sys.stderr)
        sys.exit(1)
    
    settings_files = list(distros_dir.glob("*/settings.yml"))
    
    if not settings_files:
        print("❌ No settings.yml files found in distros/", file=sys.stderr)
        sys.exit(1)
    
    print(f"\nValidating {len(settings_files)} distro(s):\n")
    
    all_valid = True
    issues = {}
    
    for settings_file in sorted(settings_files):
        distro_name = settings_file.parent.name
        print(f"🔍 {distro_name}/")
        
        try:
            parsed = parse_settings(settings_file)
        except Exception as e:
            print(f"  ❌ Error parsing: {e}", file=sys.stderr)
            all_valid = False
            continue
        
        distro_issues = []
        
        for section_name, engines in parsed.items():
            if not engines:
                print(f"  {section_name}: (empty)")
                continue
            
            valid, invalid = validate_engines(engines, real_engines)
            
            if invalid:
                print(f"  ❌ {section_name}: {len(invalid)} invalid engine(s)")
                for engine in invalid:
                    print(f"     - {engine}")
                distro_issues.append({
                    "section": section_name,
                    "invalid": invalid,
                    "valid_count": len(valid),
                    "total": len(engines),
                })
                all_valid = False
            else:
                print(f"  ✅ {section_name}: {len(engines)} engine(s) valid")
        
        if distro_issues:
            issues[distro_name] = {
                "file": str(settings_file),
                "issues": distro_issues,
            }
    
    print(f"\n{'='*60}")
    if all_valid:
        print("✅ All engines valid across all distros!")
        sys.exit(0)
    else:
        print(f"❌ Found issues in {len(issues)} distro(s):")
        for distro, data in issues.items():
            total_invalid = sum(len(i["invalid"]) for i in data["issues"])
            print(f"  - {distro}: {total_invalid} invalid engine(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
