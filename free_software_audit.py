#!/usr/bin/env python3
"""Utility to inventory installed Python packages and flag non-free licenses.

The audit runs entirely offline using ``importlib.metadata`` so it can be shipped
with the project without introducing new dependencies. Results help Rahbar AI
Developer keep the stack free and open source.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from importlib import metadata
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

APPROVED_LICENSE_KEYWORDS = {
    "mit",
    "apache",
    "bsd",
    "lgpl",
    "gpl",
    "mpl",
    "isc",
    "zlib",
    "artistic",
    "public domain",
    "cc0",
    "wtfpl",
}

REVIEW_LICENSE_KEYWORDS = {
    "proprietary",
    "commercial",
    "all rights reserved",
    "non-commercial",
    "nonfree",
    "evaluation",
}

DEFAULT_IGNORE = {
    "pip",
    "setuptools",
    "wheel",
}


@dataclass
class PackageInfo:
    name: str
    version: str
    license: str
    summary: str
    url: Optional[str]
    classifier: str
    reason: str


def normalise_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return " ".join(value.strip().split())


def read_license(meta) -> Tuple[str, str]:
    raw_licenses = meta.get_all("License") or []
    license_text = normalise_text("; ".join(raw_licenses))

    if not license_text:
        for field in ("Classifier", "license", "License-File"):
            values = meta.get_all(field) or []
            if values:
                license_text = normalise_text("; ".join(values))
                if license_text:
                    break

    if not license_text:
        return ("unknown", "license metadata missing")

    lower = license_text.lower()

    if any(keyword in lower for keyword in REVIEW_LICENSE_KEYWORDS):
        return ("review", "license marked non-free or restricted")

    if any(keyword in lower for keyword in APPROVED_LICENSE_KEYWORDS):
        return ("approved", "recognized free/open license")

    return ("review", "license not recognised, manual check required")


def gather_packages(ignore: Iterable[str]) -> List[PackageInfo]:
    ignore_set = {pkg.lower() for pkg in ignore}
    results: List[PackageInfo] = []

    for dist in metadata.distributions():
        name = dist.metadata.get("Name") or dist.metadata.get("Summary") or dist.metadata.get("Home-page")
        if not name:
            continue
        normalized_name = name.lower().strip()
        if normalized_name in ignore_set:
            continue
        version = dist.version or "unknown"
        summary = normalise_text(dist.metadata.get("Summary"))
        url = normalise_text(dist.metadata.get("Home-page")) or None

        classification, reason = read_license(dist.metadata)
        license_text = normalise_text(dist.metadata.get("License"))
        if not license_text:
            license_text = normalise_text("; ".join(dist.metadata.get_all("License") or []))
        if not license_text and classification != "approved":
            license_text = "unknown"

        results.append(
            PackageInfo(
                name=name,
                version=version,
                license=license_text or "unknown",
                summary=summary,
                url=url,
                classifier=classification,
                reason=reason,
            )
        )

    results.sort(key=lambda pkg: pkg.name.lower())
    return results


def filter_packages(packages: Iterable[PackageInfo], names: Iterable[str]) -> List[PackageInfo]:
    wanted = {name.lower() for name in names if name}
    if not wanted:
        return list(packages)
    output: List[PackageInfo] = []
    for pkg in packages:
        if pkg.name.lower() in wanted:
            output.append(pkg)
    return output


def print_table(packages: Iterable[PackageInfo]) -> None:
    rows = list(packages)
    if not rows:
        print("No packages matched the audit criteria.")
        return

    name_width = max(len(pkg.name) for pkg in rows)
    version_width = max(len(pkg.version) for pkg in rows)
    license_width = max(len(pkg.license) for pkg in rows)

    header = f"{'NAME'.ljust(name_width)}  {'VERSION'.ljust(version_width)}  {'LICENSE'.ljust(license_width)}  CLASS"  # noqa: E501
    print(header)
    print("-" * len(header))
    for pkg in rows:
        print(
            f"{pkg.name.ljust(name_width)}  "
            f"{pkg.version.ljust(version_width)}  "
            f"{pkg.license.ljust(license_width)}  "
            f"{pkg.classifier.upper()}"
        )

    reviews = [pkg for pkg in rows if pkg.classifier != "approved"]
    if reviews:
        print()
        print("Packages needing manual review:")
        for pkg in reviews:
            print(f" - {pkg.name} ({pkg.version}): {pkg.reason}")


def export_json(packages: Iterable[PackageInfo], path: Path) -> None:
    data = [asdict(pkg) for pkg in packages]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"JSON report saved to {path}")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit installed Python packages for free software compliance")
    parser.add_argument(
        "--packages",
        nargs="*",
        help="Optional list of package names to inspect (default: audit everything)",
    )
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=sorted(DEFAULT_IGNORE),
        help="Packages to skip during audit",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional output path for JSON report",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    packages = gather_packages(ignore=args.ignore)
    filtered = filter_packages(packages, args.packages or [])

    print_table(filtered)

    if args.json:
        export_json(filtered, args.json)

    issues = [pkg for pkg in filtered if pkg.classifier != "approved"]
    if issues:
        print()
        print(f"Audit complete with {len(issues)} package(s) requiring review.")
        return 1

    print()
    print("Audit complete. All packages show approved free/open licenses.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
