"""The feed registry — one entry per sellable weekly feed.

Every feed is a *change feed over a public government registry*, sold to the
vendors who serve the businesses in it (pick-and-shovel, DEVELOP.md #5).
Rules for an entry (CLAUDE.md #8/#9/#10):
  - the source is a free, keyless public open-data portal (Socrata), pulled weekly;
  - rows describe BUSINESSES / licensed premises, never private individuals —
    personal-name and personal-contact columns are left out on purpose;
  - a feed is information (public records, as published), never a
    determination or advice; the buyer is responsible for how they use it.

Entry fields:
  id            stable kebab handle (also the URL path feeds/<id>/)
  title/short   product copy                buyers/why  who pays and why (honest)
  price         USD per month
  source        domain, dataset, date_field, date_format ("iso" timestamp |
                "yyyymmdd" text | "mmddyyyy" text | "isodate" text | "mixed"),
                optional where (SoQL), order, id_field (export column to dedupe on)
  columns       [(source_field, export_name), ...] in export order
  derive        fn(raw_row, rec) to normalise values in place (optional)
  enrich        joins from a second dataset (optional): domain, dataset,
                key_src (export col), key_field (remote col), key_transform,
                columns [(remote_field, export_name)]
  contact       {export_name: "phone"|"email"} — masked in the free sample
  group_by      export column summarised in stats (state / county / category)
  attribution   source name for the page footer; source_url the public page
  window_days   trailing window (default 7)
"""
import re

# --- helpers -----------------------------------------------------------------

def _yyyymmdd(v):
    v = (v or "").strip()
    return f"{v[:4]}-{v[4:6]}-{v[6:8]}" if len(v) == 8 and v.isdigit() else v


def _mdy(v):
    v = (v or "").strip()
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})", v)
    return f"{m.group(3)}-{m.group(1)}-{m.group(2)}" if m else v[:10]


def _day(v):
    return (v or "")[:10]


def _pest_snippet(text, words=("RODENT", "MICE", "RAT ", "RATS", "ROACH", "INSECT", "FLIES", "PEST", "VERMIN")):
    """Keep only the violation segments that mention pests (Chicago packs every
    violation into one long text field)."""
    parts = [p.strip() for p in (text or "").split("|")]
    hits = [p for p in parts if any(w in p.upper() for w in words)]
    return " | ".join(hits)[:600]


PEST_NYC = ("upper(violation_description) like '%RATS%' OR upper(violation_description) like '%MICE%' "
            "OR upper(violation_description) like '%ROACH%' OR upper(violation_description) like '%FLIES%' "
            "OR upper(violation_description) like '%VERMIN%'")

FMCSA = "data.transportation.gov"
LI_CARRIER = {  # FMCSA Licensing & Insurance carrier master, joined by docket number
    "domain": FMCSA, "dataset": "6eyk-hxee", "key_src": "docket", "key_field": "docket_number",
    "columns": [("legal_name", "legal_name"), ("dba_name", "dba_name"), ("bus_street_po", "street"),
                ("bus_city", "city"), ("bus_state_code", "state"), ("bus_zip_code", "zip"),
                ("bus_telno", "phone"), ("common_stat", "common_authority"), ("contract_stat", "contract_authority"),
                ("broker_stat", "broker_authority"), ("bipd_file", "bipd_on_file"), ("cargo_file", "cargo_on_file")],
}
CENSUS_EMAIL = {  # FMCSA census, joined by USDOT number (L&I pads it with zeros)
    "domain": FMCSA, "dataset": "az4n-8mr2", "key_src": "usdot", "key_field": "dot_number", "key_transform": "lstrip0",
    "columns": [("email_address", "email"), ("power_units", "power_units"), ("total_drivers", "drivers"),
                ("add_date", "usdot_registered")],
}
TRUCK_DISCLAIMER = ("Rows are FMCSA public records as published (registration, licensing and insurance filings). "
                    "A filing is not a finding of fraud, non-compliance or bad faith.")

FEEDS = [
    # ------------------------------------------------------------------ trucking
    {
        "id": "us-new-trucking-carriers",
        "search_terms": ['new trucking company leads', 'new DOT number list', 'new MC authority leads', 'FMCSA new registrations weekly'],
        "category": "trucking",
        "title": "New trucking companies registered with FMCSA this week",
        "short": "Every new USDOT registration from the past 7 days — company, address, phone, email, fleet size — as a clean weekly CSV.",
        "buyers": "Truck-insurance agents, factoring companies, ELD/dashcam and dispatch vendors, fuel-card and load-board sales teams — the services a new carrier has to buy in its first weeks.",
        "why": "A new carrier must show insurance, an ELD and (usually) factoring before its first load; whoever reaches it first wins the account. FMCSA publishes the registration the day after it happens.",
        "price": 29,
        "source": {"domain": FMCSA, "dataset": "az4n-8mr2", "date_field": "add_date", "date_format": "yyyymmdd",
                   "order": "add_date DESC, dot_number DESC", "id_field": "usdot"},
        "columns": [
            ("dot_number", "usdot"), ("legal_name", "legal_name"), ("dba_name", "dba_name"),
            ("add_date", "registered"), ("status_code", "status"), ("carrier_operation", "operation"),
            ("classdef", "class"), ("phy_street", "street"), ("phy_city", "city"), ("phy_state", "state"),
            ("phy_zip", "zip"), ("phone", "phone"), ("email_address", "email"),
            ("power_units", "power_units"), ("total_drivers", "drivers"), ("business_org_desc", "entity_type"),
            ("mcs150_date", "mcs150_date"),
        ],
        "derive": lambda raw, rec: rec.update(registered=_yyyymmdd(rec["registered"]), mcs150_date=_yyyymmdd(rec["mcs150_date"])),
        "contact": {"phone": "phone", "email": "email"},
        "group_by": "state",
        "attribution": "FMCSA Motor Carrier Census (US DOT open data, updated daily)",
        "source_url": "https://data.transportation.gov/Trucking-and-Motorcoaches/Company-Census-File/az4n-8mr2",
        "disclaimer": TRUCK_DISCLAIMER,
        "faq": [
            ("Is this the same as a 'new MC authority' list?", "It is earlier and broader: every new USDOT registration (for-hire carriers, private fleets, brokers) in the week it was added to the FMCSA census. Authority grants follow days to weeks later; the 'operation' and 'class' columns tell you which rows are for-hire carriers."),
            ("Do rows include phone and email?", "Yes — the phone and email the company filed with FMCSA, exactly as published in the public census. The free sample masks them; the paid CSV does not."),
        ],
    },
    # ------------------------------------------------------------- restaurants
    {
        "id": "nyc-restaurant-pest-violations",
        "search_terms": ['NYC restaurant pest violation list', 'restaurant health inspection leads NYC', 'pest control leads restaurants'],
        "category": "restaurants",
        "title": "NYC restaurants cited for rats, mice, roaches or flies this week",
        "short": "Every NYC food establishment written up for a vermin violation in the past 7 days — name, address, phone, cuisine, the exact violation — weekly CSV.",
        "buyers": "Commercial pest-control companies selling to restaurants: a health-inspection vermin citation is the moment an owner needs an exterminator, and the city publishes it within days.",
        "why": "A rodent or roach citation costs points, a possible re-inspection and a letter grade. The owner is looking for a pest company that week — and the inspection record is public.",
        "price": 19,
        "source": {"domain": "data.cityofnewyork.us", "dataset": "43nn-pn8j", "date_field": "inspection_date", "date_format": "iso",
                   "where": PEST_NYC, "order": "inspection_date DESC, camis", "id_field": "camis"},
        "columns": [("camis", "camis"), ("dba", "restaurant"), ("cuisine_description", "cuisine"),
                    ("building", "building"), ("street", "street"), ("boro", "borough"), ("zipcode", "zip"),
                    ("phone", "phone"), ("inspection_date", "inspected"), ("inspection_type", "inspection_type"),
                    ("violation_code", "violation_code"), ("violation_description", "violation"),
                    ("critical_flag", "critical"), ("action", "action"), ("score", "score"), ("grade", "grade")],
        "derive": lambda raw, rec: rec.update(inspected=_day(rec["inspected"])),
        "contact": {"phone": "phone"},
        "group_by": "borough",
        "attribution": "NYC DOHMH Restaurant Inspection Results (NYC Open Data, updated daily)",
        "source_url": "https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j",
        "faq": [("Which violations are included?", "Any inspection line from the past 7 days whose violation text mentions rats, mice, roaches, flies or vermin (codes 04K, 04L, 04M, 04N, 08A and similar). One row per establishment per week, carrying its most recent matching violation.")],
    },
    {
        "id": "nyc-new-restaurants",
        "search_terms": ['new restaurant openings NYC list', 'restaurant opening leads NYC', 'pre-permit inspections NYC'],
        "category": "restaurants",
        "title": "New restaurants getting their first NYC health inspection this week",
        "short": "Every NYC food establishment that had a pre-permit (opening) inspection in the past 7 days — name, address, phone, cuisine — weekly CSV.",
        "buyers": "Restaurant suppliers and services selling into openings: POS and payments, linen and uniforms, food and beverage distributors, pest control, insurance, signage, delivery platforms.",
        "why": "A pre-permit inspection happens weeks before the doors open — while the owner is still choosing vendors. The Health Department publishes it within days.",
        "price": 19,
        "source": {"domain": "data.cityofnewyork.us", "dataset": "43nn-pn8j", "date_field": "inspection_date", "date_format": "iso",
                   "where": "inspection_type like 'Pre-permit%'", "order": "inspection_date DESC, camis", "id_field": "camis"},
        "columns": [("camis", "camis"), ("dba", "restaurant"), ("cuisine_description", "cuisine"),
                    ("building", "building"), ("street", "street"), ("boro", "borough"), ("zipcode", "zip"),
                    ("phone", "phone"), ("inspection_date", "inspected"), ("inspection_type", "inspection_type"),
                    ("action", "action")],
        "derive": lambda raw, rec: rec.update(inspected=_day(rec["inspected"])),
        "contact": {"phone": "phone"},
        "group_by": "borough",
        "attribution": "NYC DOHMH Restaurant Inspection Results (NYC Open Data, updated daily)",
        "source_url": "https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j",
    },
    {
        "id": "chicago-restaurant-pest-violations",
        "search_terms": ['Chicago restaurant rodent violations list', 'pest control leads Chicago restaurants'],
        "category": "restaurants",
        "title": "Chicago food establishments cited for rodents or insects this week",
        "short": "Every Chicago food inspection in the past 7 days that cited the pest violation (rodents, insects, animals present) — name, address, result, the inspector's note — weekly CSV.",
        "buyers": "Commercial pest-control companies in the Chicago area. The citation is public within a day or two of the inspection.",
        "why": "A pest citation on a Chicago inspection can mean a failed result and a re-inspection; the operator needs a licensed exterminator now.",
        "price": 19,
        "source": {"domain": "data.cityofchicago.org", "dataset": "4ijn-s7e5", "date_field": "inspection_date", "date_format": "iso",
                   "where": "upper(violations) like '%RODENT%' OR upper(violations) like '%ROACH%' OR upper(violations) like '%MICE%'",
                   "order": "inspection_date DESC, inspection_id DESC", "id_field": "license"},
        "columns": [("license_", "license"), ("dba_name", "establishment"), ("aka_name", "aka"), ("facility_type", "facility_type"),
                    ("risk", "risk"), ("address", "address"), ("zip", "zip"), ("inspection_date", "inspected"),
                    ("inspection_type", "inspection_type"), ("results", "result"), ("violations", "pest_violation")],
        "derive": lambda raw, rec: rec.update(inspected=_day(rec["inspected"]), pest_violation=_pest_snippet(raw.get("violations"))),
        "group_by": "facility_type",
        "attribution": "City of Chicago Food Inspections (Chicago Data Portal, updated daily)",
        "source_url": "https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5",
    },
    # ------------------------------------------------------------------ liquor
    {
        "id": "ny-new-liquor-license-applications",
        "search_terms": ['new liquor license applications New York', 'NY SLA pending applications list', 'bar and restaurant opening leads NY'],
        "category": "liquor",
        "title": "New liquor license applications filed in New York this week",
        "short": "Every application the NY State Liquor Authority received in the past 7 days — trade name, legal name, premises address, county, license class — weekly CSV.",
        "buyers": "Vendors selling into bars and restaurants before they open: POS, payments, beverage distributors, insurance, security, linen, signage, and licensing consultants.",
        "why": "An SLA application lands months before opening night — the window when a new venue chooses its vendors. The SLA publishes pending applications daily.",
        "price": 19,
        "source": {"domain": "data.ny.gov", "dataset": "f8i8-k2gm", "date_field": "received_date", "date_format": "iso",
                   "order": "received_date DESC, application_id", "id_field": "application_id"},
        "columns": [("application_id", "application_id"), ("received_date", "received"), ("status", "status"),
                    ("description", "license_class"), ("legalname", "legal_name"), ("dba", "trade_name"),
                    ("actual_address_of_premises", "premises_address"), ("city", "city"), ("zip_code", "zip"),
                    ("premises_county", "county")],
        "derive": lambda raw, rec: rec.update(received=_day(rec["received"])),
        "group_by": "county",
        "attribution": "NY State Liquor Authority — Current Pending Licenses (data.ny.gov, updated daily)",
        "source_url": "https://data.ny.gov/Economic-Development/Current-SLA-Pending-Licenses/f8i8-k2gm",
    },
    {
        "id": "ny-newly-issued-liquor-licenses",
        "search_terms": ['newly issued liquor licenses New York', 'new bars and restaurants NY weekly'],
        "category": "liquor",
        "title": "Liquor licenses newly issued in New York this week",
        "short": "Every non-temporary license the NY State Liquor Authority issued for the first time in the past 7 days — trade name, legal name, premises address, county, class — weekly CSV.",
        "buyers": "Beverage distributors, POS and payments, insurance, security and hospitality-supply vendors: a newly issued license means the venue is opening now.",
        "why": "Issuance is the green light to sell alcohol; it usually lands days before opening. The SLA publishes it the next day.",
        "price": 19,
        "source": {"domain": "data.ny.gov", "dataset": "9s3h-dpkz", "date_field": "originalissuedate", "date_format": "iso",
                   "where": "description not like 'Temporary%'", "order": "originalissuedate DESC, licensepermitid", "id_field": "license_id"},
        "columns": [("licensepermitid", "license_id"), ("originalissuedate", "issued"), ("effectivedate", "effective"),
                    ("expirationdate", "expires"), ("description", "license_class"), ("legalname", "legal_name"),
                    ("dba", "trade_name"), ("actualaddressofpremises", "premises_address"), ("city", "city"),
                    ("zipcode", "zip"), ("premisescounty", "county")],
        "derive": lambda raw, rec: rec.update(issued=_day(rec["issued"]), effective=_day(rec["effective"]), expires=_day(rec["expires"])),
        "group_by": "county",
        "attribution": "NY State Liquor Authority — Current Active Licenses (data.ny.gov, updated daily)",
        "source_url": "https://data.ny.gov/Economic-Development/Current-Liquor-Authority-Active-Licenses/9s3h-dpkz",
    },
    {
        "id": "texas-new-liquor-license-applications",
        "search_terms": ['TABC pending applications list', 'new liquor license applications Texas', 'Texas bar opening leads'],
        "category": "liquor",
        "title": "New TABC liquor license applications filed in Texas this week",
        "short": "Every original license application the Texas Alcoholic Beverage Commission received in the past 7 days — trade name, owner, address, county, license type, phone — weekly CSV.",
        "buyers": "Vendors selling into new Texas bars, restaurants and stores: POS, payments, distributors, insurance, security, signage, and TABC licensing consultants.",
        "why": "A TABC original application is filed weeks to months before opening, while vendors are being chosen. TABC publishes pending applications daily.",
        "price": 19,
        "source": {"domain": "data.texas.gov", "dataset": "mxm5-tdpj", "date_field": "submission_date", "date_format": "iso",
                   "order": "submission_date DESC, applicationid", "id_field": "application_id"},
        "columns": [("applicationid", "application_id"), ("submission_date", "submitted"), ("applicationstatus", "status"),
                    ("license_type", "license_type"), ("trade_name", "trade_name"), ("owner", "owner"),
                    ("address", "address"), ("city", "city"), ("zip", "zip"), ("county", "county"), ("phone", "phone")],
        "derive": lambda raw, rec: rec.update(submitted=_day(rec["submitted"]), application_id=rec["application_id"].replace(".0", ""), zip=rec["zip"][:5]),
        "contact": {"phone": "phone"},
        "group_by": "county",
        "attribution": "Texas Alcoholic Beverage Commission — Pending Original License Applications (data.texas.gov, updated daily)",
        "source_url": "https://data.texas.gov/dataset/Pending-Original-New-Primary-and-Subordinate-Licen/mxm5-tdpj",
    },
    {
        "id": "texas-newly-issued-liquor-licenses",
        "search_terms": ['new TABC licenses issued', 'new Texas liquor licenses this week'],
        "category": "liquor",
        "title": "TABC liquor licenses newly issued in Texas this week",
        "short": "Every license TABC originally issued in the past 7 days — trade name, owner, address, county, license type and tier, phone — weekly CSV.",
        "buyers": "Beverage distributors, POS and payments, insurance, security and restaurant-supply vendors: an original issue means the location is opening now.",
        "why": "Issuance is the go-live signal for a Texas bar or restaurant; TABC publishes its license file daily.",
        "price": 19,
        "source": {"domain": "data.texas.gov", "dataset": "7hf9-qc9f", "date_field": "original_issue_date", "date_format": "iso",
                   "order": "original_issue_date DESC, license_id", "id_field": "license_id"},
        "columns": [("license_id", "license_id"), ("original_issue_date", "issued"), ("license_type", "license_type"),
                    ("tier", "tier"), ("license_status", "status"), ("trade_name", "trade_name"), ("owner", "owner"),
                    ("address", "address"), ("city", "city"), ("zip", "zip"), ("county", "county"), ("phone", "phone")],
        "derive": lambda raw, rec: rec.update(issued=_day(rec["issued"]), license_id=rec["license_id"].replace(".0", ""), zip=rec["zip"][:5]),
        "contact": {"phone": "phone"},
        "group_by": "county",
        "attribution": "Texas Alcoholic Beverage Commission — License Information (data.texas.gov, updated daily)",
        "source_url": "https://data.texas.gov/dataset/TABC-License-Information/7hf9-qc9f",
    },
    # ------------------------------------------------------- business registries
    {
        "id": "chicago-new-business-licenses",
        "search_terms": ['new Chicago business licenses list', 'new business leads Chicago'],
        "category": "business",
        "title": "New business licenses issued in Chicago this week",
        "short": "Every newly issued (not renewed) City of Chicago business license that started in the past 7 days — business name, DBA, address, license type, business activity, neighborhood — weekly CSV.",
        "buyers": "Anyone selling to brand-new Chicago businesses: merchant services, insurance, payroll, signage, cleaning, security, local marketing.",
        "why": "A new license means a business opening its doors in Chicago this month; the city posts it within days.",
        "price": 19,
        "source": {"domain": "data.cityofchicago.org", "dataset": "r5kz-chrr", "date_field": "license_start_date", "date_format": "iso",
                   "where": "application_type = 'ISSUE'", "order": "license_start_date DESC, license_id", "id_field": "license_id"},
        "columns": [("license_id", "license_id"), ("license_start_date", "license_start"), ("license_description", "license_type"),
                    ("business_activity", "business_activity"), ("legal_name", "legal_name"), ("doing_business_as_name", "dba_name"),
                    ("address", "address"), ("city", "city"), ("state", "state"), ("zip_code", "zip"),
                    ("community_area_name", "community_area"), ("neighborhood", "neighborhood"), ("license_status", "status")],
        "derive": lambda raw, rec: rec.update(license_start=_day(rec["license_start"])),
        "group_by": "license_type",
        "attribution": "City of Chicago Business Licenses (Chicago Data Portal, updated daily)",
        "source_url": "https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr",
    },
    {
        "id": "connecticut-new-business-registrations",
        "search_terms": ['new business registrations Connecticut', 'new Connecticut LLC list', 'new business leads CT'],
        "category": "business",
        "title": "New businesses registered in Connecticut this week",
        "short": "Every business the Connecticut Secretary of the State registered in the past 7 days — name, entity type, business email, billing address, NAICS, formation state — weekly CSV.",
        "buyers": "Banks and merchant services, insurance agents, payroll and bookkeeping firms, web and marketing agencies — the first vendors a new Connecticut company buys from.",
        "why": "Connecticut publishes the registration (with the business email on file) the next morning — earlier than any list broker.",
        "price": 19,
        "source": {"domain": "data.ct.gov", "dataset": "n7gp-d28j", "date_field": "date_registration", "date_format": "iso",
                   "where": "upper(status) not in ('REJECTED', 'EXPIRED RESERVATION', 'RESERVED', 'CANCELLED', 'WITHDRAWN')",
                   "order": "date_registration DESC, accountnumber", "id_field": "account_number"},
        "columns": [("accountnumber", "account_number"), ("name", "name"), ("business_type", "entity_type"), ("status", "status"),
                    ("date_registration", "registered"), ("citizenship", "domestic_or_foreign"), ("formation_place", "formation_place"),
                    ("naics_code", "naics"), ("billingstreet", "street"), ("billingcity", "city"), ("billingstate", "state"),
                    ("billingpostalcode", "zip"), ("business_email_address", "email")],
        "derive": lambda raw, rec: rec.update(registered=_day(rec["registered"])),
        "contact": {"email": "email"},
        "group_by": "entity_type",
        "attribution": "Connecticut Business Registry — Business Master (data.ct.gov, updated daily)",
        "source_url": "https://data.ct.gov/Business/Connecticut-Business-Registry-Business-Master/n7gp-d28j",
    },
    {
        "id": "new-york-new-business-entities",
        "search_terms": ['new LLCs New York this week', 'NY new corporation filings list', 'new business leads New York'],
        "category": "business",
        "title": "New corporations and LLCs filed in New York this week",
        "short": "Every entity whose initial filing with the NY Department of State landed in the past 7 days — name, entity type, county, jurisdiction, service-of-process address — weekly CSV.",
        "buyers": "Banks, merchant services, insurance agents, payroll and bookkeeping firms, registered-agent and compliance services selling to new New York companies.",
        "why": "New York files roughly 3,000 new entities a week and publishes them daily; the filing address is where the founder receives mail.",
        "price": 19,
        "source": {"domain": "data.ny.gov", "dataset": "n9v6-gdp6", "date_field": "initial_dos_filing_date", "date_format": "iso",
                   "order": "initial_dos_filing_date DESC, dos_id", "id_field": "dos_id"},
        "columns": [("dos_id", "dos_id"), ("current_entity_name", "name"), ("initial_dos_filing_date", "filed"), ("entity_type", "entity_type"),
                    ("county", "county"), ("jurisdiction", "jurisdiction"), ("dos_process_name", "process_name"),
                    ("dos_process_address_1", "process_address"), ("dos_process_address_2", "process_address_2"),
                    ("dos_process_city", "process_city"), ("dos_process_state", "process_state"), ("dos_process_zip", "process_zip")],
        "derive": lambda raw, rec: rec.update(filed=_day(rec["filed"])),
        "group_by": "county",
        "attribution": "NY Department of State — Active Corporations (data.ny.gov, updated daily)",
        "source_url": "https://data.ny.gov/Economic-Development/Active-Corporations-Beginning-1800/n9v6-gdp6",
    },
    {
        "id": "colorado-new-business-entities",
        "search_terms": ['new Colorado business entities', 'new LLC list Colorado', 'new business leads Colorado'],
        "category": "business",
        "title": "New business entities formed in Colorado this week",
        "short": "Every entity formed with the Colorado Secretary of State in the past 7 days — name, entity type, status, principal address, registered-agent organization — weekly CSV.",
        "buyers": "Banks, merchant services, insurance agents, payroll and bookkeeping firms, and local service vendors selling to new Colorado companies.",
        "why": "Colorado forms about 3,000 entities a week and publishes each one the same day, with the principal office address.",
        "price": 19,
        "source": {"domain": "data.colorado.gov", "dataset": "4ykn-tg5h", "date_field": "entityformdate", "date_format": "iso",
                   "order": "entityformdate DESC, entityid", "id_field": "entity_id"},
        "columns": [("entityid", "entity_id"), ("entityname", "name"), ("entityformdate", "formed"), ("entitytype", "entity_type"),
                    ("entitystatus", "status"), ("jurisdictonofformation", "jurisdiction"), ("principaladdress1", "street"),
                    ("principaladdress2", "street_2"), ("principalcity", "city"), ("principalstate", "state"),
                    ("principalzipcode", "zip"), ("agentorganizationname", "agent_organization"), ("agentprincipalcity", "agent_city")],
        "derive": lambda raw, rec: rec.update(formed=_day(rec["formed"])),
        "group_by": "city",
        "attribution": "Colorado Secretary of State — Business Entities (data.colorado.gov, updated daily)",
        "source_url": "https://data.colorado.gov/Business/Business-Entities-in-Colorado/4ykn-tg5h",
    },
    # ------------------------------------------------------- permits & rentals
    {
        "id": "nyc-new-building-permits",
        "search_terms": ['NYC building permits issued this week', 'DOB NOW permits list', 'construction leads NYC'],
        "category": "permits",
        "title": "New building permits issued in NYC this week",
        "short": "Every initial (not renewal) DOB NOW work permit issued in the past 7 days — work type, job description, estimated cost, address, borough, owner business, contractor business — weekly CSV.",
        "buyers": "Building-material suppliers, dumpster and scaffold rental, equipment rental, insurance, and trades selling to general contractors with a job starting now.",
        "why": "An issued permit means work starts within weeks; the DOB publishes the permit, the owner and the permittee the next day.",
        "price": 19,
        "source": {"domain": "data.cityofnewyork.us", "dataset": "rbx6-tga4", "date_field": "issued_date", "date_format": "iso",
                   "where": "filing_reason like 'Initial%' AND work_permit not like 'Permit is no%'",
                   "order": "issued_date DESC, work_permit", "id_field": "permit"},
        "columns": [("work_permit", "permit"), ("job_filing_number", "job_filing"), ("filing_reason", "filing_reason"),
                    ("issued_date", "issued"), ("approved_date", "approved"), ("expired_date", "expires"),
                    ("work_type", "work_type"), ("job_description", "job_description"), ("estimated_job_costs", "estimated_cost"),
                    ("house_no", "house"), ("street_name", "street"), ("borough", "borough"), ("zip_code", "zip"),
                    ("permittee_s_license_type", "contractor_license_type"), ("applicant_business_name", "contractor_business"),
                    ("applicant_business_address", "contractor_address"), ("owner_business_name", "owner_business"),
                    ("owner_city", "owner_city"), ("owner_state", "owner_state"), ("permit_status", "status")],
        "derive": lambda raw, rec: rec.update(issued=_day(rec["issued"]), approved=_day(rec["approved"]), expires=_day(rec["expires"]),
                                              job_description=rec["job_description"][:240]),
        "group_by": "borough",
        "attribution": "NYC Department of Buildings — DOB NOW: Build, Approved Permits (NYC Open Data, updated daily)",
        "source_url": "https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Approved-Permits/rbx6-tga4",
        "faq": [("Why no owner or applicant names?", "By design: only business names are included. Owners who filed as private individuals appear with a blank owner_business column.")],
    },
    {
        "id": "new-orleans-str-permit-applications",
        "search_terms": ['New Orleans short-term rental permits', 'new STR permit applications New Orleans'],
        "category": "rentals",
        "title": "New short-term rental permit applications in New Orleans this week",
        "short": "Every STR permit application the City of New Orleans received in the past 7 days — property address, permit type, status, bedroom and guest limits — weekly CSV.",
        "buyers": "Co-hosts and property managers, STR cleaning and linen services, smart-lock and noise-monitor vendors, STR insurance — a permit application is a listing about to go live.",
        "why": "New Orleans requires a permit before listing; the application is public the day it is filed, weeks before the first guest.",
        "price": 19,
        "source": {"domain": "data.nola.gov", "dataset": "en36-xvxg", "date_field": "application_date", "date_format": "iso",
                   "order": "application_date DESC, reference_code", "id_field": "reference"},
        "columns": [("reference_code", "reference"), ("application_date", "applied"), ("address", "address"),
                    ("license_type", "permit_type"), ("residential_subtype", "subtype"), ("current_status", "status"),
                    ("bedroom_limit", "bedroom_limit"), ("guest_occupancy_limit", "guest_limit"), ("link", "city_record")],
        "derive": lambda raw, rec: rec.update(applied=_day(rec["applied"])),
        "group_by": "permit_type",
        "attribution": "City of New Orleans — Short-Term Rental Permit Applications (data.nola.gov, updated daily)",
        "source_url": "https://data.nola.gov/Housing-Land-Use-and-Blight/Short-Term-Rental-Permit-Applications/en36-xvxg",
        "faq": [("Why no host name or phone?", "By design. This feed lists licensed properties, not people; the city record link opens the full public permit.")],
    },
    {
        "id": "chicago-new-str-registrations",
        "search_terms": ['Chicago shared housing registrations', 'new short-term rental registrations Chicago'],
        "category": "rentals",
        "title": "Short-term rental registrations approved in Chicago this week",
        "short": "Every shared-housing (Airbnb-style) registration the City of Chicago approved in the past 7 days — unit address, registration number, ward, expiration — weekly CSV.",
        "buyers": "Co-hosts and property managers, STR cleaning services, smart-lock and noise-monitor vendors, STR insurance in the Chicago market.",
        "why": "Chicago requires registration before listing; an approval means a unit is about to start hosting.",
        "price": 19,
        "source": {"domain": "data.cityofchicago.org", "dataset": "qfyy-956j", "date_field": "current_status_date", "date_format": "iso",
                   "where": "current_status = 'APPROVED'", "order": "current_status_date DESC, registration_number", "id_field": "registration"},
        "columns": [("registration_number", "registration"), ("current_status_date", "approved"), ("street_address", "address"),
                    ("ward", "ward"), ("expiration_date", "expires")],
        "derive": lambda raw, rec: rec.update(approved=_day(rec["approved"]), expires=_day(rec["expires"])),
        "group_by": "ward",
        "attribution": "City of Chicago — Active Shared Housing Registrations (Chicago Data Portal, updated daily)",
        "source_url": "https://data.cityofchicago.org/Community-Economic-Development/Active-Shared-Housing-Registrations/qfyy-956j",
        "faq": [("Why no host name?", "By design. This feed lists registered units, not people.")],
    },
]


# Parked — not built weekly. FMCSA's Licensing & Insurance "All With History"
# files (AuthHist 9mw4-x3tu, ActPendInsur qh9u-swkp) are periodic snapshots
# whose newest rows lag months (probe 2026-09-12: latest grants dated May), so a
# trailing-7-day window returns nothing. Revive as a *diff* feed over the daily
# L&I Carrier file (6eyk-hxee: pending/active authority flags) if the trucking
# census feed shows demand.
PARKED = [
    {
        "id": "us-new-mc-authority-grants",
        "category": "trucking",
        "title": "MC operating authorities granted by FMCSA this week",
        "short": "Every carrier, broker or freight-forwarder authority FMCSA granted in the past 7 days, joined to the company's name, address, phone and email — weekly CSV.",
        "buyers": "Truck-insurance agents, factoring companies, ELD and dispatch vendors, load boards and freight-broker bond agents — a granted authority means the company is about to haul (or broker) its first load.",
        "why": "The grant is the moment a carrier becomes bookable and a broker becomes bondable. FMCSA's licensing system publishes the disposition the next day.",
        "price": 29,
        "source": {"domain": FMCSA, "dataset": "9mw4-x3tu", "date_field": "disp_served_date", "date_format": "mmddyyyy",
                   "where": "upper(disp_action_desc) like '%GRANT%'", "order": "docket_number", "id_field": "docket"},
        "columns": [("docket_number", "docket"), ("dot_number", "usdot"), ("mod_col_1", "authority_type"),
                    ("original_action_desc", "application"), ("orig_served_date", "applied"),
                    ("disp_action_desc", "disposition"), ("disp_served_date", "granted")],
        "derive": lambda raw, rec: rec.update(applied=_mdy(rec["applied"]), granted=_mdy(rec["granted"])),
        "enrich": [LI_CARRIER, CENSUS_EMAIL],
        "contact": {"phone": "phone", "email": "email"},
        "group_by": "state",
        "attribution": "FMCSA Licensing & Insurance — Authority History, Carrier and Census files (US DOT open data)",
        "source_url": "https://data.transportation.gov/Trucking-and-Motorcoaches/AuthHist-All-With-History/9mw4-x3tu",
        "disclaimer": TRUCK_DISCLAIMER,
        "faq": [("What is 'authority type'?", "FMCSA's own label for the docket: motor property common/contract carrier, broker, freight forwarder, household goods, passenger. Filter the column to the segment you sell to.")],
    },
    {
        "id": "us-mc-authority-revocations",
        "category": "trucking",
        "title": "MC operating authorities revoked by FMCSA this week",
        "short": "Every carrier or broker authority FMCSA revoked in the past 7 days (most for lapsed insurance or BOC-3), with company name, address, phone and email — weekly CSV.",
        "buyers": "Truck-insurance agents (a revoked-for-insurance carrier needs a policy to reinstate), compliance services that handle reinstatement, and brokers keeping a do-not-book list.",
        "why": "Revocation follows a 30-day insurance-cancellation notice; the carrier is parked until it fixes it. That is a buying moment for insurance and reinstatement services.",
        "price": 29,
        "source": {"domain": FMCSA, "dataset": "9mw4-x3tu", "date_field": "disp_served_date", "date_format": "mmddyyyy",
                   "where": "upper(disp_action_desc) like '%REVO%'", "order": "docket_number", "id_field": "docket"},
        "columns": [("docket_number", "docket"), ("dot_number", "usdot"), ("mod_col_1", "authority_type"),
                    ("disp_action_desc", "disposition"), ("disp_served_date", "revoked")],
        "derive": lambda raw, rec: rec.update(revoked=_mdy(rec["revoked"])),
        "enrich": [LI_CARRIER, CENSUS_EMAIL],
        "contact": {"phone": "phone", "email": "email"},
        "group_by": "state",
        "attribution": "FMCSA Licensing & Insurance — Authority History, Carrier and Census files (US DOT open data)",
        "source_url": "https://data.transportation.gov/Trucking-and-Motorcoaches/AuthHist-All-With-History/9mw4-x3tu",
        "disclaimer": TRUCK_DISCLAIMER,
    },
    {
        "id": "us-trucking-insurance-cancellations",
        "category": "trucking",
        "title": "Trucking insurance cancellation notices filed with FMCSA this week",
        "short": "Every BMC-91/34 insurance cancellation an insurer filed in the past 7 days — carrier, docket, policy, insurer, cancellation-effective date — joined to the carrier's name, phone and email. Weekly CSV.",
        "buyers": "Truck-insurance agents and MGAs: a cancellation notice means the carrier has ~30 days to replace its liability or cargo policy or lose its authority. Brokers use the same list as a risk watchlist.",
        "why": "Insurers must notify FMCSA before cancelling; FMCSA publishes the filing. It is the earliest public signal that a carrier is shopping for insurance.",
        "price": 29,
        "source": {"domain": FMCSA, "dataset": "qh9u-swkp", "date_field": "trans_date", "date_format": "mmddyyyy",
                   "where": "cancl_effective_date IS NOT NULL", "order": "docket_number", "id_field": "policy_key"},
        "columns": [("docket_number", "docket"), ("dot_number", "usdot"), ("mod_col_1", "coverage"),
                    ("ins_form_code", "form"), ("name_company", "insurer"), ("policy_no", "policy"),
                    ("underl_lim_amount", "underlying_limit"), ("max_cov_amount", "max_coverage"),
                    ("effective_date", "effective"), ("cancl_effective_date", "cancellation_effective"),
                    ("trans_date", "filed")],
        "derive": lambda raw, rec: rec.update(effective=_mdy(rec["effective"]), cancellation_effective=_mdy(rec["cancellation_effective"]),
                                              filed=_mdy(rec["filed"]), policy_key=rec["docket"] + "|" + rec["policy"] + "|" + rec["coverage"]),
        "extra_key": "policy_key",
        "enrich": [LI_CARRIER, CENSUS_EMAIL],
        "contact": {"phone": "phone", "email": "email"},
        "group_by": "state",
        "attribution": "FMCSA Licensing & Insurance — Active & Pending Insurance, Carrier and Census files (US DOT open data)",
        "source_url": "https://data.transportation.gov/Trucking-and-Motorcoaches/ActPendInsur-All-With-History/qh9u-swkp",
        "disclaimer": TRUCK_DISCLAIMER + " A cancellation notice can be withdrawn or replaced before its effective date.",
    },
]

BY_ID = {f["id"]: f for f in FEEDS}

CATEGORIES = [  # hub order + labels
    ("trucking", "Trucking & freight", "New FMCSA carrier registrations, nationwide, with the phone and email on file."),
    ("restaurants", "Restaurants", "Health-inspection pest citations and pre-opening inspections."),
    ("liquor", "Bars & liquor licenses", "Liquor-license applications and new issuances — the earliest public sign of a venue opening."),
    ("business", "New businesses", "New entities and business licenses from state and city registries."),
    ("permits", "Building permits", "Newly issued construction permits."),
    ("rentals", "Short-term rentals", "New STR permits and registrations."),
]
