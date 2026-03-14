#!/usr/bin/env python3.12
"""Download authentic Indian government disability-scheme PDFs."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMES_DIR = ROOT / "data" / "schemes"

# All URLs are official Indian government domains (gov.in, nic.in, s3waas.gov.in)
DOCUMENTS = [
    {
        "filename": "compendium_pwd_schemes_2023.pdf",
        "url": "https://cdnbbsr.s3waas.gov.in/s3e58aea67b01fa747687f038dfde066f6/uploads/2023/11/202311231014396043.pdf",
        "description": "Compendium of Schemes for Welfare of PwD (2023)",
    },
    {
        "filename": "adip_scheme_guidelines.pdf",
        "url": "https://socialjustice.gov.in/writereaddata/UploadFile/adipsch.pdf",
        "description": "ADIP Scheme Guidelines",
    },
    {
        "filename": "rpwd_act_2016.pdf",
        "url": "https://ssepd.odisha.gov.in/sites/default/files/2024-01/RPWD%20ACT.pdf",
        "description": "RPwD Act 2016 (full text)",
    },
    {
        "filename": "central_sector_umbrella_scheme_2024.pdf",
        "url": "https://cdnbbsr.s3waas.gov.in/s3e58aea67b01fa747687f038dfde066f6/uploads/2024/12/202412111222128691.pdf",
        "description": "Central Sector Umbrella Scheme (2024)",
    },
    {
        "filename": "niramaya_health_insurance_guidelines.pdf",
        "url": "http://esomsa.hp.gov.in/sites/default/files/Scheme%20Guidelines%20Niramaya%2007072015-47995315.pdf",
        "description": "Niramaya Health Insurance Guidelines",
    },
    {
        "filename": "social_welfare_statistics_2021.pdf",
        "url": "https://socialjustice.gov.in/writereaddata/UploadFile/HANDBOOKSocialWelfareStatistice2021.pdf",
        "description": "Social Welfare Statistics Handbook 2021",
    },
]


def download_all():
    SCHEMES_DIR.mkdir(parents=True, exist_ok=True)
    success, failed = 0, 0

    for doc in DOCUMENTS:
        dest = SCHEMES_DIR / doc["filename"]
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"  [skip] {doc['filename']} (already downloaded)")
            success += 1
            continue

        print(f"  [downloading] {doc['description']}")
        print(f"    URL: {doc['url']}")
        result = subprocess.run(
            [
                "curl", "-fSL",
                "--connect-timeout", "30",
                "--max-time", "120",
                "-o", str(dest),
                doc["url"],
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not dest.exists() or dest.stat().st_size < 1000:
            print(f"    FAILED: {result.stderr.strip()}")
            if dest.exists():
                dest.unlink()
            failed += 1
        else:
            size_mb = dest.stat().st_size / (1024 * 1024)
            print(f"    OK ({size_mb:.1f} MB)")
            success += 1

    print(f"\nDone: {success} downloaded, {failed} failed")
    if failed:
        print("Re-run this script to retry failed downloads.")
        sys.exit(1)


if __name__ == "__main__":
    download_all()
