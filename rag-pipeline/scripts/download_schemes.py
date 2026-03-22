#!/usr/bin/env python3.12
"""Download authentic Indian government disability-scheme PDFs."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMES_DIR = ROOT / "data" / "schemes"

# All URLs are official Indian government domains (gov.in, nic.in, s3waas.gov.in)
# or verified mirrors. These are REAL government documents — no synthetic data.
DOCUMENTS = [
    # ── Compendium & Overview Documents ─────────────────────────
    {
        "filename": "compendium_pwd_schemes_2023.pdf",
        "url": "https://cdnbbsr.s3waas.gov.in/s3e58aea67b01fa747687f038dfde066f6/uploads/2023/11/202311231014396043.pdf",
        "description": "Compendium of Schemes for Welfare of PwD (2023) — covers 50+ central schemes",
    },
    {
        "filename": "central_sector_umbrella_scheme_2024.pdf",
        "url": "https://cdnbbsr.s3waas.gov.in/s3e58aea67b01fa747687f038dfde066f6/uploads/2024/12/202412111222128691.pdf",
        "description": "Central Sector Umbrella Scheme for PwD (2024)",
    },
    {
        "filename": "social_welfare_statistics_2021.pdf",
        "url": "https://socialjustice.gov.in/writereaddata/UploadFile/HANDBOOKSocialWelfareStatistice2021.pdf",
        "description": "Social Welfare Statistics Handbook 2021 — disability data and scheme budgets",
    },
    # ── RPwD Act (Legal Foundation) ─────────────────────────────
    {
        "filename": "rpwd_act_2016.pdf",
        "url": "https://ssepd.odisha.gov.in/sites/default/files/2024-01/RPWD%20ACT.pdf",
        "description": "Rights of Persons with Disabilities Act, 2016 (full text)",
    },
    # ── ADIP Scheme (Assistive Devices) ─────────────────────────
    {
        "filename": "adip_scheme_guidelines.pdf",
        "url": "https://socialjustice.gov.in/writereaddata/UploadFile/adipsch.pdf",
        "description": "ADIP Scheme — Assistance to Disabled Persons for Aids/Appliances",
    },
    # ── DDRS (Rehabilitation) ───────────────────────────────────
    {
        "filename": "ddrs_revised_scheme.pdf",
        "url": "https://disabilityaffairs.gov.in/upload/uploadfiles/files/Revised%20DDRS%20Scheme.pdf",
        "description": "DDRS — Deendayal Disabled Rehabilitation Scheme (Revised)",
    },
    {
        "filename": "ddrs_original_scheme.pdf",
        "url": "http://disabilityaffairs.gov.in/upload/uploadfiles/files/Scheme_DDRS%20(1).pdf",
        "description": "DDRS — Original Scheme Document",
    },
    # ── Niramaya Health Insurance ───────────────────────────────
    {
        "filename": "niramaya_health_insurance_guidelines.pdf",
        "url": "http://esomsa.hp.gov.in/sites/default/files/Scheme%20Guidelines%20Niramaya%2007072015-47995315.pdf",
        "description": "Niramaya Health Insurance Scheme Guidelines (National Trust)",
    },
    # ── Scholarship Schemes (DEPwD) ─────────────────────────────
    {
        "filename": "scholarship_pre_matric_pwd_guidelines.pdf",
        "url": "https://scholarships.gov.in/public/schemeGuidelines/DEPDGuidelines.pdf",
        "description": "Pre-Matric Scholarship for Students with Disabilities — DEPwD Guidelines",
    },
    {
        "filename": "scholarship_post_matric_pwd_guidelines.pdf",
        "url": "https://scholarships.gov.in/public/schemeGuidelines/DEPDGuidelines_1.pdf",
        "description": "Post-Matric Scholarship for Students with Disabilities — DEPwD Guidelines",
    },
    # ── SIPDA (Implementation of PwD Act) ───────────────────────
    {
        "filename": "sipda_scheme_guidelines.pdf",
        "url": "https://socialjustice.gov.in/writereaddata/UploadFile/18721740858722.pdf",
        "description": "SIPDA — Scheme for Implementation of Persons with Disabilities Act",
    },
    # ── NHFDC (Loans & Finance) ─────────────────────────────────
    {
        "filename": "nhfdc_annual_report.pdf",
        "url": "https://socialjustice.gov.in/writereaddata/UploadFile/63491659437974.pdf",
        "description": "NHFDC — National Handicapped Finance & Development Corporation guidelines",
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
