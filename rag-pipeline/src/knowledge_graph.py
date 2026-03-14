"""Kùzu Knowledge Graph for structured disability scheme eligibility queries.

Uses the same Cypher query language as Neo4j — skills transfer directly.
Kùzu is embedded (pip install kuzu), so no Docker/server needed.
"""

import kuzu
from pathlib import Path
from src.config import KUZU_DIR


def get_db() -> kuzu.Database:
    """Get or create the Kùzu database."""
    KUZU_DIR.parent.mkdir(parents=True, exist_ok=True)
    return kuzu.Database(str(KUZU_DIR))


def create_schema(conn: kuzu.Connection) -> None:
    """Create node and relationship tables if they don't exist."""
    # ── Node tables ────────────────────────────────────────────────
    node_tables = {
        "Scheme": (
            "id STRING, name STRING, full_name STRING, ministry STRING, "
            "level STRING, benefit_type STRING, benefit_value_inr STRING, "
            "frequency STRING, source_pdf STRING, PRIMARY KEY (id)"
        ),
        "DisabilityCategory": (
            "id STRING, name STRING, description STRING, PRIMARY KEY (id)"
        ),
        "State": "id STRING, name STRING, code STRING, PRIMARY KEY (id)",
        "AgeGroup": (
            "id STRING, label STRING, min_age INT64, max_age INT64, PRIMARY KEY (id)"
        ),
        "IncomeLevel": (
            "id STRING, label STRING, max_income_inr INT64, PRIMARY KEY (id)"
        ),
        "DocumentType": (
            "id STRING, name STRING, description STRING, PRIMARY KEY (id)"
        ),
    }
    existing = {t.strip() for t in _list_tables(conn, "NODE")}
    for table_name, cols in node_tables.items():
        if table_name not in existing:
            conn.execute(f"CREATE NODE TABLE {table_name}({cols})")

    # ── Relationship tables ────────────────────────────────────────
    rel_tables = {
        "COVERS": ("Scheme", "DisabilityCategory", "min_disability_pct INT64"),
        "AVAILABLE_IN": ("Scheme", "State", ""),
        "FOR_AGE_GROUP": ("Scheme", "AgeGroup", ""),
        "HAS_INCOME_LIMIT": ("Scheme", "IncomeLevel", ""),
        "REQUIRES_DOCUMENT": ("Scheme", "DocumentType", ""),
    }
    existing_rels = {t.strip() for t in _list_tables(conn, "REL")}
    for rel_name, (src, dst, props) in rel_tables.items():
        if rel_name not in existing_rels:
            prop_clause = f", {props}" if props else ""
            conn.execute(
                f"CREATE REL TABLE {rel_name}(FROM {src} TO {dst}{prop_clause})"
            )


def _list_tables(conn: kuzu.Connection, table_type: str) -> list[str]:
    """List existing table names of given type."""
    try:
        result = conn.execute(f"CALL show_tables() RETURN name, type")
        names = []
        while result.has_next():
            row = result.get_next()
            if row[1] == table_type:
                names.append(row[0])
        return names
    except Exception:
        return []


# ── Reference data ─────────────────────────────────────────────────
DISABILITY_CATEGORIES = [
    ("visual", "Visual Impairment", "Blindness and low vision"),
    ("hearing", "Hearing Impairment", "Deaf and hard of hearing"),
    ("locomotor", "Locomotor Disability", "Physical disability affecting movement"),
    ("intellectual", "Intellectual Disability", "Mental retardation, learning disabilities"),
    ("mental_illness", "Mental Illness", "Psychiatric conditions"),
    ("cerebral_palsy", "Cerebral Palsy", "Neurological condition affecting movement and posture"),
    ("autism", "Autism Spectrum", "Autism spectrum disorder"),
    ("multiple", "Multiple Disabilities", "Two or more disabilities combined"),
    ("speech", "Speech and Language", "Speech and language disability"),
    ("specific_learning", "Specific Learning Disabilities", "Dyslexia, dyscalculia, dysgraphia"),
    ("acid_attack", "Acid Attack Victims", "Survivors of acid attacks"),
    ("muscular_dystrophy", "Muscular Dystrophy", "Progressive muscle weakness"),
    ("chronic_neurological", "Chronic Neurological Conditions", "Parkinson's, multiple sclerosis"),
    ("thalassemia", "Blood Disorders", "Thalassemia, hemophilia, sickle cell"),
]

STATES = [
    ("all_india", "All India", "IN"),
    ("karnataka", "Karnataka", "KA"),
    ("maharashtra", "Maharashtra", "MH"),
    ("tamil_nadu", "Tamil Nadu", "TN"),
    ("delhi", "Delhi", "DL"),
    ("uttar_pradesh", "Uttar Pradesh", "UP"),
    ("west_bengal", "West Bengal", "WB"),
    ("rajasthan", "Rajasthan", "RJ"),
    ("madhya_pradesh", "Madhya Pradesh", "MP"),
    ("kerala", "Kerala", "KL"),
    ("odisha", "Odisha", "OD"),
    ("andhra_pradesh", "Andhra Pradesh", "AP"),
    ("telangana", "Telangana", "TG"),
    ("gujarat", "Gujarat", "GJ"),
    ("himachal_pradesh", "Himachal Pradesh", "HP"),
    ("bihar", "Bihar", "BR"),
    ("punjab", "Punjab", "PB"),
]

AGE_GROUPS = [
    ("child_0_5", "Early childhood (0-5)", 0, 5),
    ("child_6_14", "School age (6-14)", 6, 14),
    ("child_6_18", "Children (6-18)", 6, 18),
    ("youth_15_25", "Youth (15-25)", 15, 25),
    ("adult_18_60", "Working age (18-60)", 18, 60),
    ("all_ages", "All ages (0-100)", 0, 100),
]

INCOME_LEVELS = [
    ("bpl", "Below Poverty Line", 100000),
    ("low_income", "Low income (< Rs 1.5 lakh)", 150000),
    ("ews", "EWS (< Rs 2.5 lakh)", 250000),
    ("mid_income", "Middle income (< Rs 6 lakh)", 600000),
    ("no_limit", "No income limit", 0),
]

DOCUMENT_TYPES = [
    ("disability_cert", "Disability Certificate", "UDID or state disability certificate with ≥40% benchmark disability"),
    ("income_cert", "Income Certificate", "Certificate from tehsildar/revenue officer"),
    ("age_proof", "Age Proof", "Birth certificate, school certificate, or Aadhaar"),
    ("aadhaar", "Aadhaar Card", "12-digit unique identity number"),
    ("bank_account", "Bank Account Details", "Bank passbook or cancelled cheque"),
    ("photo", "Passport Photo", "Recent passport-size photographs"),
    ("residence_proof", "Residence Proof", "Proof of residence in applicable state"),
    ("bpl_card", "BPL Card", "Below Poverty Line ration card"),
    ("medical_cert", "Medical Certificate", "Certificate from government hospital or registered practitioner"),
]

# ── Scheme metadata (extracted from actual government PDFs) ────────
# Each entry maps to real content in the downloaded documents.
SCHEMES_DATA = [
    {
        "id": "adip",
        "name": "ADIP Scheme",
        "full_name": "Assistance to Disabled Persons for Purchase/Fitting of Aids/Appliances",
        "ministry": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "benefit_type": "equipment",
        "benefit_value_inr": "Up to Rs 10,000 per aid/appliance",
        "frequency": "as-needed",
        "source_pdf": "adip_scheme_guidelines.pdf",
        "disabilities": ["visual", "hearing", "locomotor", "intellectual", "cerebral_palsy", "multiple"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["all_ages"],
        "income_levels": ["low_income"],
        "documents": ["disability_cert", "income_cert", "aadhaar", "photo"],
    },
    {
        "id": "ddrs",
        "name": "DDRS",
        "full_name": "Deendayal Disabled Rehabilitation Scheme",
        "ministry": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "benefit_type": "service",
        "benefit_value_inr": "Varies by project",
        "frequency": "annual",
        "source_pdf": "compendium_pwd_schemes_2023.pdf",
        "disabilities": ["visual", "hearing", "locomotor", "intellectual", "cerebral_palsy", "autism", "multiple"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["all_ages"],
        "income_levels": ["no_limit"],
        "documents": ["disability_cert", "aadhaar"],
    },
    {
        "id": "niramaya",
        "name": "Niramaya Health Insurance",
        "full_name": "Niramaya Health Insurance Scheme for Persons with Disabilities",
        "ministry": "National Trust (under MoSJE)",
        "level": "central",
        "benefit_type": "insurance",
        "benefit_value_inr": "Rs 1,00,000 annual health cover",
        "frequency": "annual",
        "source_pdf": "niramaya_health_insurance_guidelines.pdf",
        "disabilities": ["autism", "cerebral_palsy", "intellectual", "multiple"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["all_ages"],
        "income_levels": ["no_limit"],
        "documents": ["disability_cert", "aadhaar", "photo", "bank_account"],
    },
    {
        "id": "scholarship_pre_matric",
        "name": "Pre-Matric Scholarship",
        "full_name": "Pre-Matric Scholarship for Students with Disabilities",
        "ministry": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "benefit_type": "financial",
        "benefit_value_inr": "Rs 700-1,000/month + book allowance",
        "frequency": "monthly",
        "source_pdf": "compendium_pwd_schemes_2023.pdf",
        "disabilities": ["visual", "hearing", "locomotor", "intellectual", "cerebral_palsy", "autism", "multiple", "speech", "specific_learning"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["child_6_14"],
        "income_levels": ["ews"],
        "documents": ["disability_cert", "income_cert", "age_proof", "aadhaar", "bank_account"],
    },
    {
        "id": "scholarship_post_matric",
        "name": "Post-Matric Scholarship",
        "full_name": "Post-Matric Scholarship for Students with Disabilities",
        "ministry": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "benefit_type": "financial",
        "benefit_value_inr": "Rs 1,100-1,600/month + fees + book allowance",
        "frequency": "monthly",
        "source_pdf": "compendium_pwd_schemes_2023.pdf",
        "disabilities": ["visual", "hearing", "locomotor", "intellectual", "cerebral_palsy", "autism", "multiple", "speech", "specific_learning"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["youth_15_25"],
        "income_levels": ["mid_income"],
        "documents": ["disability_cert", "income_cert", "age_proof", "aadhaar", "bank_account"],
    },
    {
        "id": "nhfdc_loan",
        "name": "NHFDC Loan Scheme",
        "full_name": "National Handicapped Finance and Development Corporation Loan Scheme",
        "ministry": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "benefit_type": "financial",
        "benefit_value_inr": "Loans up to Rs 25 lakh at concessional rates",
        "frequency": "one-time",
        "source_pdf": "compendium_pwd_schemes_2023.pdf",
        "disabilities": ["visual", "hearing", "locomotor", "intellectual", "cerebral_palsy", "multiple"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["adult_18_60"],
        "income_levels": ["mid_income"],
        "documents": ["disability_cert", "income_cert", "aadhaar", "bank_account", "residence_proof"],
    },
    {
        "id": "sipda",
        "name": "SIPDA",
        "full_name": "Scheme for Implementation of Persons with Disabilities Act",
        "ministry": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "benefit_type": "service",
        "benefit_value_inr": "Barrier-free access, UDID issuance, awareness",
        "frequency": "as-needed",
        "source_pdf": "central_sector_umbrella_scheme_2024.pdf",
        "disabilities": ["visual", "hearing", "locomotor", "intellectual", "cerebral_palsy", "autism", "multiple", "speech", "specific_learning", "mental_illness", "acid_attack", "muscular_dystrophy", "chronic_neurological", "thalassemia"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["all_ages"],
        "income_levels": ["no_limit"],
        "documents": ["disability_cert", "aadhaar"],
    },
    {
        "id": "early_intervention",
        "name": "Early Intervention Centres",
        "full_name": "District Early Intervention Centres under Central Sector Umbrella Scheme",
        "ministry": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "benefit_type": "service",
        "benefit_value_inr": "Free therapy and rehabilitation services",
        "frequency": "as-needed",
        "source_pdf": "central_sector_umbrella_scheme_2024.pdf",
        "disabilities": ["cerebral_palsy", "autism", "intellectual", "multiple", "speech", "specific_learning"],
        "disability_pct": 40,
        "states": ["all_india"],
        "age_groups": ["child_0_5", "child_6_14"],
        "income_levels": ["no_limit"],
        "documents": ["disability_cert", "age_proof", "aadhaar"],
    },
]


def populate_reference_data(conn: kuzu.Connection) -> None:
    """Insert reference data (disability categories, states, etc.)."""
    for id_, name, desc in DISABILITY_CATEGORIES:
        conn.execute(
            "CREATE (d:DisabilityCategory {id: $id, name: $name, description: $descr})",
            {"id": id_, "name": name, "descr": desc},
        )
    for id_, name, code in STATES:
        conn.execute(
            "CREATE (s:State {id: $id, name: $name, code: $code})",
            {"id": id_, "name": name, "code": code},
        )
    for id_, label, min_a, max_a in AGE_GROUPS:
        conn.execute(
            "CREATE (a:AgeGroup {id: $id, label: $label, min_age: $min_a, max_age: $max_a})",
            {"id": id_, "label": label, "min_a": min_a, "max_a": max_a},
        )
    for id_, label, max_inc in INCOME_LEVELS:
        conn.execute(
            "CREATE (i:IncomeLevel {id: $id, label: $label, max_income_inr: $max_inc})",
            {"id": id_, "label": label, "max_inc": max_inc},
        )
    for id_, name, desc in DOCUMENT_TYPES:
        conn.execute(
            "CREATE (d:DocumentType {id: $id, name: $name, description: $descr})",
            {"id": id_, "name": name, "descr": desc},
        )


def populate_schemes(conn: kuzu.Connection) -> None:
    """Insert scheme nodes and their relationships."""
    for s in SCHEMES_DATA:
        conn.execute(
            "CREATE (s:Scheme {"
            "id: $id, name: $name, full_name: $full_name, ministry: $ministry, "
            "level: $level, benefit_type: $benefit_type, "
            "benefit_value_inr: $benefit_value_inr, frequency: $frequency, "
            "source_pdf: $source_pdf})",
            {
                "id": s["id"], "name": s["name"], "full_name": s["full_name"],
                "ministry": s["ministry"], "level": s["level"],
                "benefit_type": s["benefit_type"],
                "benefit_value_inr": s["benefit_value_inr"],
                "frequency": s["frequency"], "source_pdf": s["source_pdf"],
            },
        )
        # Disability relationships
        for dis_id in s["disabilities"]:
            conn.execute(
                "MATCH (s:Scheme {id: $sid}), (d:DisabilityCategory {id: $did}) "
                "CREATE (s)-[:COVERS {min_disability_pct: $pct}]->(d)",
                {"sid": s["id"], "did": dis_id, "pct": s["disability_pct"]},
            )
        # State relationships
        for st_id in s["states"]:
            conn.execute(
                "MATCH (s:Scheme {id: $sid}), (st:State {id: $stid}) "
                "CREATE (s)-[:AVAILABLE_IN]->(st)",
                {"sid": s["id"], "stid": st_id},
            )
        # Age group relationships
        for ag_id in s["age_groups"]:
            conn.execute(
                "MATCH (s:Scheme {id: $sid}), (a:AgeGroup {id: $agid}) "
                "CREATE (s)-[:FOR_AGE_GROUP]->(a)",
                {"sid": s["id"], "agid": ag_id},
            )
        # Income level relationships
        for inc_id in s["income_levels"]:
            conn.execute(
                "MATCH (s:Scheme {id: $sid}), (i:IncomeLevel {id: $incid}) "
                "CREATE (s)-[:HAS_INCOME_LIMIT]->(i)",
                {"sid": s["id"], "incid": inc_id},
            )
        # Document requirements
        for doc_id in s["documents"]:
            conn.execute(
                "MATCH (s:Scheme {id: $sid}), (d:DocumentType {id: $did}) "
                "CREATE (s)-[:REQUIRES_DOCUMENT]->(d)",
                {"sid": s["id"], "did": doc_id},
            )


def populate_graph() -> tuple[int, int]:
    """Build the full knowledge graph. Returns (node_count, rel_count)."""
    import shutil
    # Start fresh — remove file or directory
    if KUZU_DIR.exists():
        if KUZU_DIR.is_dir():
            shutil.rmtree(KUZU_DIR)
        else:
            KUZU_DIR.unlink()
    # Also clean lock/WAL files Kùzu may create alongside
    for suffix in [".lock", ".wal"]:
        p = KUZU_DIR.with_suffix(suffix)
        if p.exists():
            p.unlink()
    db = get_db()
    conn = kuzu.Connection(db)
    create_schema(conn)
    populate_reference_data(conn)
    populate_schemes(conn)
    # Count
    nodes = _count(conn, "MATCH (n) RETURN count(n)")
    rels = _count(conn, "MATCH ()-[r]->() RETURN count(r)")
    return nodes, rels


def _count(conn: kuzu.Connection, query: str) -> int:
    result = conn.execute(query)
    if result.has_next():
        return result.get_next()[0]
    return 0


def query_eligible_schemes(
    conn: kuzu.Connection,
    disability: str | None = None,
    age: int | None = None,
    state: str | None = None,
    max_income: int | None = None,
) -> list[dict]:
    """Query KG for eligible schemes based on structured criteria.

    All parameters are optional — omitted criteria are not filtered.
    Returns list of dicts with scheme info.
    """
    conditions = []
    params = {}

    # Build MATCH clause dynamically
    match_parts = ["(s:Scheme)"]
    if disability:
        match_parts.append("(s)-[:COVERS]->(d:DisabilityCategory)")
        # Match on id or name — try both underscore and space forms
        dis_normalized = disability.replace("_", " ")
        conditions.append(
            "(lower(d.name) CONTAINS lower($disability) OR "
            "lower(d.id) CONTAINS lower($disability_raw))"
        )
        params["disability"] = dis_normalized
        params["disability_raw"] = disability

    if state:
        match_parts.append("(s)-[:AVAILABLE_IN]->(st:State)")
        conditions.append(
            "(lower(st.name) CONTAINS lower($state) OR st.id = 'all_india')"
        )
        params["state"] = state

    if age is not None:
        match_parts.append("(s)-[:FOR_AGE_GROUP]->(ag:AgeGroup)")
        conditions.append("ag.min_age <= $age AND ag.max_age >= $age")
        params["age"] = age

    if max_income is not None:
        match_parts.append("(s)-[:HAS_INCOME_LIMIT]->(il:IncomeLevel)")
        conditions.append(
            "(il.max_income_inr >= $income OR il.max_income_inr = 0)"
        )
        params["income"] = max_income

    match_clause = "MATCH " + ", ".join(match_parts)
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    query = (
        f"{match_clause}{where_clause} "
        "RETURN DISTINCT s.id, s.name, s.full_name, s.benefit_type, "
        "s.benefit_value_inr, s.ministry"
    )

    result = conn.execute(query, params)
    schemes = []
    while result.has_next():
        row = result.get_next()
        schemes.append({
            "id": row[0],
            "name": row[1],
            "full_name": row[2],
            "benefit_type": row[3],
            "benefit_value_inr": row[4],
            "ministry": row[5],
        })
    return schemes


def get_scheme_details(conn: kuzu.Connection, scheme_id: str) -> dict | None:
    """Get full scheme info including all relationships."""
    # Base scheme
    result = conn.execute(
        "MATCH (s:Scheme {id: $id}) RETURN s.*", {"id": scheme_id}
    )
    if not result.has_next():
        return None
    row = result.get_next()
    scheme = dict(zip(
        ["id", "name", "full_name", "ministry", "level", "benefit_type",
         "benefit_value_inr", "frequency", "source_pdf"],
        row,
    ))
    # Disabilities
    r = conn.execute(
        "MATCH (s:Scheme {id: $id})-[c:COVERS]->(d:DisabilityCategory) "
        "RETURN d.name, c.min_disability_pct",
        {"id": scheme_id},
    )
    scheme["disabilities"] = []
    while r.has_next():
        row = r.get_next()
        scheme["disabilities"].append({"name": row[0], "min_pct": row[1]})
    # States
    r = conn.execute(
        "MATCH (s:Scheme {id: $id})-[:AVAILABLE_IN]->(st:State) RETURN st.name",
        {"id": scheme_id},
    )
    scheme["states"] = [row[0] for row in _iter_results(r)]
    # Age groups
    r = conn.execute(
        "MATCH (s:Scheme {id: $id})-[:FOR_AGE_GROUP]->(ag:AgeGroup) "
        "RETURN ag.label, ag.min_age, ag.max_age",
        {"id": scheme_id},
    )
    scheme["age_groups"] = [
        {"label": row[0], "min": row[1], "max": row[2]} for row in _iter_results(r)
    ]
    # Documents
    r = conn.execute(
        "MATCH (s:Scheme {id: $id})-[:REQUIRES_DOCUMENT]->(d:DocumentType) "
        "RETURN d.name, d.description",
        {"id": scheme_id},
    )
    scheme["required_documents"] = [
        {"name": row[0], "description": row[1]} for row in _iter_results(r)
    ]
    return scheme


def _iter_results(result):
    while result.has_next():
        yield result.get_next()
