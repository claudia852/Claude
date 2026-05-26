#!/usr/bin/env python3
"""
Next Layer Concepts — Notion Workspace Builder v1.0
"""

import os
import sys
import time

try:
    from notion_client import Client
except ImportError:
    print("ERROR: notion-client not installed. Run: pip install notion-client")
    sys.exit(1)

TOKEN = os.environ.get("NOTION_TOKEN")
if not TOKEN:
    print("ERROR: NOTION_TOKEN environment variable not set.")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python build_workspace.py <parent_page_id>")
    sys.exit(1)

ROOT_PARENT_ID = sys.argv[1].replace("-", "")
notion = Client(auth=TOKEN)
built = {}

def log(msg): print(f"  {msg}")
def section(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")

def create_page(parent_id, title, emoji="📄", body_blocks=None):
    children = body_blocks or []
    page = notion.pages.create(
        parent={"page_id": parent_id},
        icon={"type": "emoji", "emoji": emoji},
        properties={"title": {"title": [{"text": {"content": title}}]}},
        children=children
    )
    time.sleep(0.35)
    return page["id"]

def heading(text, level=2):
    tag = f"heading_{level}"
    return {"object": "block", "type": tag, tag: {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def callout(text, emoji="💡"):
    return {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": text}}], "icon": {"type": "emoji", "emoji": emoji}}}

def divider(): return {"object": "block", "type": "divider", "divider": {}}

def paragraph(text):
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def bulleted(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def create_database(parent_id, title, emoji, properties):
    db = notion.databases.create(
        parent={"page_id": parent_id},
        icon={"type": "emoji", "emoji": emoji},
        title=[{"text": {"content": title}}],
        properties=properties
    )
    time.sleep(0.4)
    return db["id"]

def add_relation(database_id, property_name, target_db_id):
    try:
        notion.databases.update(
            database_id=database_id,
            properties={property_name: {"relation": {"database_id": target_db_id, "type": "single_property", "single_property": {}}}}
        )
        time.sleep(0.35)
    except Exception as e:
        log(f"WARNING: Could not add relation {property_name}: {e}")

def create_record(database_id, properties):
    notion.pages.create(parent={"database_id": database_id}, properties=properties)
    time.sleep(0.35)

def text_prop(v): return {"rich_text": [{"type": "text", "text": {"content": str(v)}}]}
def title_prop(v): return {"title": [{"type": "text", "text": {"content": str(v)}}]}
def select_prop(v): return {"select": {"name": v}}
def multi_prop(vs): return {"multi_select": [{"name": v} for v in vs]}
def date_prop(v): return {"date": {"start": v}}
def number_prop(v): return {"number": v}

STATUS_COLOURS = {
    "Draft": "gray", "Testing": "yellow", "Active": "green", "Paused": "orange",
    "Archived": "purple", "Deprecated": "purple", "Pilot": "blue", "Scaled": "green",
    "Queued": "gray", "In Progress": "yellow", "Review": "blue", "Complete": "green",
    "Pending": "gray", "In Review": "yellow", "Approved": "green",
    "Revision Needed": "orange", "Rejected": "red", "New": "gray", "Planned": "blue",
    "Done": "green", "Idea": "gray", "In Build": "yellow", "Live": "green",
    "Prospect": "blue",
}
def sel(name, colour=None): return {"name": name, "color": colour or STATUS_COLOURS.get(name, "default")}
def select_options(*names): return {"select": {"options": [sel(n) for n in names]}}
def multi_options(*names): return {"multi_select": {"options": [sel(n) for n in names]}}

# PHASE 1
section("PHASE 1 — Building Page Hierarchy")
log("Creating root hub page...")
hub_id = create_page(ROOT_PARENT_ID, "Next Layer Concepts — AI Operations Hub", "🧠", [
    callout("Next Layer Concepts AI Operations System v1.0. Navigate using sections 00–09.", "🚀"),
    divider(), heading("Quick Navigation", 2),
    bulleted("00 — Home Dashboard"), bulleted("01 — Command Centre"), bulleted("02 — Workflows"),
    bulleted("03 — Prompt Library"), bulleted("04 — Clients"), bulleted("05 — Knowledge Base"),
    bulleted("06 — SOPs & Documentation"), bulleted("07 — Automations"),
    bulleted("08 — Improvements & Changelog"), bulleted("09 — Settings & Meta"),
])
built["hub"] = hub_id
log(f"Hub: {hub_id}")

for title, emoji, key in [
    ("00 — Home Dashboard","🏠","home"),("01 — Command Centre","🎯","command"),
    ("02 — Workflows","⚙️","workflows"),("03 — Prompt Library","💬","prompts"),
    ("04 — Clients","🤝","clients"),("05 — Knowledge Base","📚","knowledge"),
    ("06 — SOPs & Documentation","📋","sops"),("07 — Automations","⚡","automations"),
    ("08 — Improvements & Changelog","🔄","improvements"),("09 — Settings & Meta","⚙️","settings"),
]:
    log(f"Creating: {title}")
    built[key] = create_page(hub_id, title, emoji)

built["cmd_active"] = create_page(built["command"], "Active Projects Dashboard", "📊")
built["cmd_weekly"] = create_page(built["command"], "Weekly Review", "📅")
built["cmd_priority"] = create_page(built["command"], "Priorities Board", "🎯")
built["wfl_registry_page"] = create_page(built["workflows"], "Workflow Registry", "📁")
built["credit_risk_folder"] = create_page(built["workflows"], "UK Credit Risk Analysis", "🏦", [
    callout("Pilot Workflow — UK Companies House Full Accounts → AI Credit Risk Report.", "🏦"),
    divider(), heading("Phase Process", 2),
    bulleted("Phase 1: Intake"), bulleted("Phase 2: Extraction (P01–P05)"),
    bulleted("Phase 3: Analysis (P06–P09)"), bulleted("Phase 4: Scoring (P10)"),
    bulleted("Phase 5: Summary (P11–P13)"), bulleted("Phase 6: Review"),
    bulleted("Phase 7: Report"), bulleted("Phase 8: Archive"),
])
built["prompt_categories"] = create_page(built["prompts"], "Prompt Categories Guide", "🗂️")
built["prompt_testing"] = create_page(built["prompts"], "Prompt Testing Log", "🧪")
built["client_projects_page"] = create_page(built["clients"], "Client Projects", "📁")
built["client_deliverables"] = create_page(built["clients"], "Client Deliverables", "📦")
built["kb_ai_tools"] = create_page(built["knowledge"], "AI Tools & Models", "🤖")
built["kb_research"] = create_page(built["knowledge"], "Industry Research", "🔬")
built["kb_frameworks"] = create_page(built["knowledge"], "Frameworks & Methodologies", "🏗️")
built["kb_reference"] = create_page(built["knowledge"], "Reference Documents", "📄")
built["sop_templates"] = create_page(built["sops"], "Templates Library", "📝")
built["sop_internal"] = create_page(built["sops"], "Internal Processes", "🔧")
built["auto_blueprints"] = create_page(built["automations"], "Zapier & Make Blueprints", "🔌")
built["auto_api_docs"] = create_page(built["automations"], "API Documentation", "📡")
built["retros"] = create_page(built["improvements"], "Retrospectives", "🪞")
built["settings_conventions"] = create_page(built["settings"], "Workspace Conventions", "📐")
built["settings_access"] = create_page(built["settings"], "Access & Permissions Notes", "🔐")
log("✓ Page hierarchy complete")

# PHASE 2
section("PHASE 2 — Building Databases")

built["db_workflows"] = create_database(built["wfl_registry_page"], "Workflow Registry", "⚙️", {
    "Workflow Name": {"title": {}}, "Status": select_options("Draft","Pilot","Active","Scaled","Paused","Archived"),
    "Department": select_options("Finance","Marketing","Operations","Consulting","Research"),
    "Owner": {"people": {}}, "Version": {"rich_text": {}}, "Last Reviewed": {"date": {}},
    "Automation Status": select_options("Manual","Partial","Fully Automated"),
    "Tags": multi_options("AI","Finance","Reporting","Marketing","Content","Operations","Consulting","Automation","Template"),
    "Notes": {"rich_text": {}}, "Workflow ID": {"rich_text": {}},
})
log(f"Workflow Registry: {built['db_workflows']}")

built["db_prompts"] = create_database(built["prompts"], "Master Prompt Database", "💬", {
    "Prompt Name": {"title": {}}, "Prompt ID": {"rich_text": {}},
    "Category": select_options("Extraction","Analysis","Scoring","Summary","Generation","Classification","Validation","Component"),
    "AI Model": select_options("GPT-4o","Claude Opus","Claude Sonnet","Claude Haiku","Gemini","Llama","Custom"),
    "Status": select_options("Draft","Testing","Active","Deprecated"),
    "Version": {"rich_text": {}}, "Prompt Body": {"rich_text": {}}, "Input Required": {"rich_text": {}},
    "Expected Output": {"rich_text": {}}, "Performance Notes": {"rich_text": {}},
    "Created": {"date": {}}, "Last Modified": {"date": {}}, "Owner": {"people": {}},
    "Tags": multi_options("Credit Risk","Balance Sheet","P&L","Cash Flow","Solvency","Liquidity",
                          "Risk Score","Executive Summary","Red Flags","Recommendations",
                          "Extraction","Marketing","Content","Operations"),
})
log(f"Master Prompt Database: {built['db_prompts']}")

built["db_prompt_tests"] = create_database(built["prompt_testing"], "Prompt Testing Log", "🧪", {
    "Test Name": {"title": {}}, "Test Date": {"date": {}}, "Tester": {"people": {}},
    "AI Model Used": select_options("GPT-4o","Claude Opus","Claude Sonnet","Claude Haiku","Gemini","Custom"),
    "Input Summary": {"rich_text": {}}, "Output Quality": select_options("Poor","Fair","Good","Excellent"),
    "Issues Found": {"rich_text": {}}, "Action Taken": {"rich_text": {}},
    "Result": select_options("Passed","Failed","Revised"),
})

built["db_analyses"] = create_database(built["credit_risk_folder"], "Analysis Tracker", "📊", {
    "Analysis Name": {"title": {}}, "Analysis ID": {"rich_text": {}}, "Company Name": {"rich_text": {}},
    "Companies House No": {"rich_text": {}}, "Filing Period": {"date": {}}, "Date Initiated": {"date": {}},
    "Analyst": {"people": {}}, "Status": select_options("Queued","In Progress","Review","Complete","Archived"),
    "Priority": select_options("Low","Medium","High","Urgent"), "PDF Source": {"url": {}}, "Notes": {"rich_text": {}},
})
log(f"Analysis Tracker: {built['db_analyses']}")

built["db_outputs"] = create_database(built["credit_risk_folder"], "Output Archive", "📄", {
    "Output Name": {"title": {}}, "Output ID": {"rich_text": {}},
    "Section Type": select_options("Profitability","Liquidity","Solvency","Cash Flow","Risk Score",
                                   "Executive Summary","Red Flags","Recommendations","Director Analysis","Related Parties"),
    "AI Model": select_options("GPT-4o","Claude Opus","Claude Sonnet","Claude Haiku","Gemini","Custom"),
    "Raw Output": {"rich_text": {}}, "Quality Rating": select_options("Poor","Acceptable","Good","Excellent"),
    "Reviewed": {"checkbox": {}}, "Review Notes": {"rich_text": {}}, "Date Generated": {"date": {}},
    "Version": {"rich_text": {}}, "Included in Report": {"checkbox": {}},
})

built["db_reviews"] = create_database(built["credit_risk_folder"], "Risk Review Board", "🔍", {
    "Review Name": {"title": {}}, "Reviewer": {"people": {}}, "Review Date": {"date": {}},
    "Status": select_options("Pending","In Review","Approved","Revision Needed","Rejected"),
    "Overall Risk Rating": select_options("Very Low","Low","Medium","High","Very High","Critical"),
    "Risk Score": {"number": {"format": "number"}}, "Key Findings": {"rich_text": {}},
    "Red Flags": {"rich_text": {}}, "Recommendations": {"rich_text": {}},
    "Report Issued": {"checkbox": {}}, "Report File": {"files": {}},
})

built["db_clients"] = create_database(built["clients"], "Client Registry", "🤝", {
    "Client Name": {"title": {}}, "Client ID": {"rich_text": {}},
    "Status": select_options("Active","Prospect","Paused","Archived"),
    "Industry": select_options("Finance","Property","Retail","Manufacturing","Technology",
                               "Healthcare","Legal","Construction","Hospitality","Other"),
    "Contact Name": {"rich_text": {}}, "Contact Email": {"email": {}}, "Onboarded": {"date": {}},
    "Account Manager": {"people": {}}, "Notes": {"rich_text": {}},
})
log(f"Client Registry: {built['db_clients']}")

built["db_projects"] = create_database(built["client_projects_page"], "Client Projects", "📁", {
    "Project Name": {"title": {}}, "Project ID": {"rich_text": {}},
    "Status": select_options("Scoping","Active","Review","Delivered","Archived"),
    "Start Date": {"date": {}}, "Target Date": {"date": {}}, "Project Manager": {"people": {}},
    "Brief": {"rich_text": {}}, "Deliverables": {"rich_text": {}},
    "Budget": {"number": {"format": "pound"}}, "Invoiced": {"checkbox": {}}, "Notes": {"rich_text": {}},
})

built["db_sops"] = create_database(built["sops"], "SOP Registry", "📋", {
    "SOP Name": {"title": {}}, "SOP ID": {"rich_text": {}},
    "Status": select_options("Draft","Active","Needs Review","Archived"),
    "Owner": {"people": {}}, "Last Reviewed": {"date": {}}, "Version": {"rich_text": {}},
    "Department": select_options("Operations","Finance","Consulting","Marketing","Technology"),
    "Tags": multi_options("Onboarding","Process","Technical","Client","Credit Risk","Automation","Quality Control"),
})

built["db_automations"] = create_database(built["automations"], "Automation Registry", "⚡", {
    "Automation Name": {"title": {}}, "Automation ID": {"rich_text": {}},
    "Tool": select_options("Zapier","Make","Power Automate","n8n","API","Python Script","Other"),
    "Status": select_options("Idea","Planned","In Build","Live","Paused","Deprecated"),
    "Trigger": {"rich_text": {}}, "Action": {"rich_text": {}},
    "Priority": select_options("Low","Medium","High"),
    "Owner": {"people": {}}, "Live Date": {"date": {}}, "Notes": {"rich_text": {}},
})

built["db_changelog"] = create_database(built["improvements"], "Change Log", "🔄", {
    "Change Title": {"title": {}}, "Change ID": {"rich_text": {}},
    "Change Type": select_options("Prompt Update","Workflow Change","Database Update","Process Change","Fix","New Feature","Deprecation"),
    "Area": select_options("Prompt Library","Workflow","Client","Automation","Workspace","Database","SOP"),
    "Changed By": {"people": {}}, "Date": {"date": {}},
    "Version Before": {"rich_text": {}}, "Version After": {"rich_text": {}},
    "Reason": {"rich_text": {}}, "Impact": select_options("Low","Medium","High"),
})

built["db_ideas"] = create_database(built["improvements"], "Ideas Backlog", "💡", {
    "Idea Title": {"title": {}},
    "Area": select_options("Workflow","Prompt","Automation","Client","Workspace","Database","SOP","Reporting"),
    "Status": select_options("New","Reviewed","Planned","In Progress","Done","Rejected"),
    "Priority": select_options("Low","Medium","High"),
    "Submitted By": {"people": {}}, "Submitted Date": {"date": {}},
    "Notes": {"rich_text": {}}, "Effort Estimate": select_options("Small","Medium","Large"),
})
log("✓ All databases created")

# PHASE 3 - Relations
section("PHASE 3 — Wiring Relations")
relations = [
    ("db_workflows","Linked SOPs","db_sops"),("db_workflows","Linked Prompts","db_prompts"),
    ("db_workflows","Linked Clients","db_clients"),("db_workflows","Linked Automations","db_automations"),
    ("db_prompts","Workflow","db_workflows"),("db_prompts","Linked Tests","db_prompt_tests"),
    ("db_prompt_tests","Prompt","db_prompts"),("db_analyses","Prompts Used","db_prompts"),
    ("db_analyses","Output Records","db_outputs"),("db_analyses","Risk Review","db_reviews"),
    ("db_analyses","Client","db_clients"),("db_outputs","Analysis","db_analyses"),
    ("db_outputs","Prompt Used","db_prompts"),("db_reviews","Analysis","db_analyses"),
    ("db_reviews","Client","db_clients"),("db_clients","Projects","db_projects"),
    ("db_clients","Workflows Used","db_workflows"),("db_clients","Analyses","db_analyses"),
    ("db_projects","Client","db_clients"),("db_sops","Workflow","db_workflows"),
    ("db_automations","Workflow","db_workflows"),("db_changelog","Linked Prompt","db_prompts"),
    ("db_changelog","Linked Workflow","db_workflows"),("db_ideas","Linked Workflow","db_workflows"),
]
for src, prop, tgt in relations:
    log(f"  {src} → [{prop}] → {tgt}")
    add_relation(built[src], prop, built[tgt])
log("✓ Relations wired")

# PHASE 4 - Sample Records
section("PHASE 4 — Creating Sample Records")

create_record(built["db_workflows"], {
    "Workflow Name": title_prop("UK Credit Risk Analysis"), "Workflow ID": text_prop("NLC-WFL-2024-001"),
    "Status": select_prop("Pilot"), "Department": select_prop("Finance"), "Version": text_prop("v1.0"),
    "Automation Status": select_prop("Manual"), "Tags": multi_prop(["AI","Finance","Reporting"]),
    "Notes": text_prop("Pilot workflow for UK Companies House Full Accounts credit risk analysis."),
})
log("Added workflow record")

prompts = [
    ("CRA — Component — System Context — v1.0","NLC-PRO-2024-001","Component","You are a UK-qualified financial analyst specialising in credit risk assessment for SMEs.","N/A","N/A","Credit Risk|Component"),
    ("CRA — Extraction — Revenue & Profitability — v1.0","NLC-PRO-2024-002","Extraction","Extract all revenue and profitability figures from the P&L.","Full Accounts PDF","9 profitability metrics","Credit Risk|P&L|Extraction"),
    ("CRA — Extraction — Balance Sheet Assets — v1.0","NLC-PRO-2024-003","Extraction","Extract all asset figures from the Balance Sheet.","Full Accounts PDF","Balance sheet assets","Credit Risk|Balance Sheet|Extraction"),
    ("CRA — Extraction — Balance Sheet Liabilities — v1.0","NLC-PRO-2024-004","Extraction","Extract all liability and equity figures from the Balance Sheet.","Full Accounts PDF","Balance sheet liabilities & equity","Credit Risk|Balance Sheet|Extraction"),
    ("CRA — Extraction — Cash Flow — v1.0","NLC-PRO-2024-005","Extraction","Extract all cash flow figures.","Full Accounts PDF","Cash flow statement","Credit Risk|Cash Flow|Extraction"),
    ("CRA — Extraction — Director & Related Parties — v1.0","NLC-PRO-2024-006","Extraction","Extract director remuneration, loans and related party transactions.","Full Accounts PDF - Notes","Director disclosures","Credit Risk|Director Analysis|Extraction|Red Flags"),
    ("CRA — Analysis — Profitability Risk — v1.0","NLC-PRO-2024-007","Analysis","Conduct profitability risk analysis from extraction data.","Output from PRO-002","Profitability risk rating","Credit Risk|P&L|Analysis"),
    ("CRA — Analysis — Liquidity Risk — v1.0","NLC-PRO-2024-008","Analysis","Conduct liquidity risk analysis from balance sheet data.","Outputs from PRO-003 and PRO-004","Liquidity ratios and risk rating","Credit Risk|Liquidity|Analysis"),
    ("CRA — Analysis — Solvency Risk — v1.0","NLC-PRO-2024-009","Analysis","Conduct solvency risk analysis from balance sheet data.","Outputs from PRO-003 and PRO-004","Solvency ratios and risk rating","Credit Risk|Solvency|Analysis"),
    ("CRA — Analysis — Cash Flow Risk — v1.0","NLC-PRO-2024-010","Analysis","Conduct cash flow risk analysis.","Output from PRO-005","Cash flow risk rating","Credit Risk|Cash Flow|Analysis"),
    ("CRA — Scoring — Overall Risk Score — v1.0","NLC-PRO-2024-011","Scoring","Calculate overall credit risk score 0-100.","Outputs from PRO-007 to PRO-010","Risk score 0-100","Credit Risk|Risk Score|Scoring"),
    ("CRA — Summary — Executive Risk Brief — v1.0","NLC-PRO-2024-012","Summary","Write professional executive risk brief.","All analysis outputs","Executive summary","Credit Risk|Executive Summary|Summary"),
    ("CRA — Summary — Red Flags & Recommendations — v1.0","NLC-PRO-2024-013","Summary","Identify red flags and produce recommendations.","All analysis outputs","Red flags and recommendations","Credit Risk|Red Flags|Recommendations|Summary"),
]
for name, pid, cat, body, inp, exp, tags_str in prompts:
    create_record(built["db_prompts"], {
        "Prompt Name": title_prop(name), "Prompt ID": text_prop(pid), "Category": select_prop(cat),
        "AI Model": select_prop("GPT-4o"), "Status": select_prop("Active"), "Version": text_prop("v1.0"),
        "Prompt Body": text_prop(body), "Input Required": text_prop(inp), "Expected Output": text_prop(exp),
        "Tags": multi_prop([t.strip() for t in tags_str.split("|")]), "Created": date_prop("2024-11-01"),
    })
    log(f"  + {name}")

create_record(built["db_clients"], {
    "Client Name": title_prop("Acme Manufacturing Ltd"), "Client ID": text_prop("NLC-CLI-2024-001"),
    "Status": select_prop("Active"), "Industry": select_prop("Manufacturing"),
    "Contact Name": text_prop("James Thornton"), "Contact Email": {"email": "j.thornton@acme-manufacturing.co.uk"},
    "Onboarded": date_prop("2024-11-01"),
    "Notes": text_prop("First pilot client for UK Credit Risk Analysis workflow."),
})

create_record(built["db_analyses"], {
    "Analysis Name": title_prop("Acme Manufacturing Ltd — Full Accounts 2024"),
    "Analysis ID": text_prop("NLC-CRA-2024-001"), "Company Name": text_prop("Acme Manufacturing Ltd"),
    "Companies House No": text_prop("04521890"), "Filing Period": date_prop("2024-03-31"),
    "Date Initiated": date_prop("2024-11-15"), "Status": select_prop("Queued"), "Priority": select_prop("High"),
    "Notes": text_prop("Credit facility renewal Q1 2025."),
})

create_record(built["db_sops"], {
    "SOP Name": title_prop("How to Run a UK Credit Risk Analysis"), "SOP ID": text_prop("NLC-SOP-2024-001"),
    "Status": select_prop("Active"), "Version": text_prop("v1.0"), "Department": select_prop("Finance"),
    "Last Reviewed": date_prop("2024-11-01"), "Tags": multi_prop(["Credit Risk","Process","Technical"]),
})

for name, aid, tool, trigger, action, priority in [
    ("Auto-Create Output Records","NLC-AUT-2024-001","Make","New Analysis record","Create 13 Output Archive records","High"),
    ("Review Notification","NLC-AUT-2024-002","Zapier","Status changes to Review","Email reviewer","High"),
    ("Client Delivery","NLC-AUT-2024-003","Zapier","Risk Review approved","Send report to client","High"),
    ("Weekly Digest","NLC-AUT-2024-004","Make","Every Monday 8AM","Email open items summary","Medium"),
    ("Prompt Deprecation Logger","NLC-AUT-2024-005","Zapier","Prompt set to Deprecated","Create Change Log entry","Medium"),
    ("New Client Onboarding","NLC-AUT-2024-006","Make","New Client Registry record","Create onboarding checklist","Medium"),
]:
    create_record(built["db_automations"], {
        "Automation Name": title_prop(name), "Automation ID": text_prop(aid), "Tool": select_prop(tool),
        "Status": select_prop("Idea"), "Trigger": text_prop(trigger), "Action": text_prop(action),
        "Priority": select_prop(priority),
    })

for t, cid, ct, area, before, after, reason, impact in [
    ("Workspace v1.0 Created","NLC-CHG-2024-001","New Feature","Workspace","","v1.0","Initial build","High"),
    ("UK Credit Risk Workflow v1.0","NLC-CHG-2024-002","New Feature","Workflow","","v1.0","Pilot launch with 13 prompts","High"),
]:
    create_record(built["db_changelog"], {
        "Change Title": title_prop(t), "Change ID": text_prop(cid), "Change Type": select_prop(ct),
        "Area": select_prop(area), "Date": date_prop("2024-11-01"),
        "Version Before": text_prop(before), "Version After": text_prop(after),
        "Reason": text_prop(reason), "Impact": select_prop(impact),
    })

for idea, area, status, priority, notes, effort in [
    ("Build Make automation for output records","Automation","New","High","Auto-create 13 Output Archive records per analysis","Small"),
    ("Sector-specific benchmarks in scoring","Prompt","New","Medium","Use sector-specific benchmarks for more accurate scoring","Medium"),
    ("Client-facing report template","Workflow","New","Medium","Exportable Notion report template","Large"),
    ("Altman Z-Score in solvency analysis","Prompt","New","Low","Add Altman Z-Score calculation to solvency prompt","Small"),
]:
    create_record(built["db_ideas"], {
        "Idea Title": title_prop(idea), "Area": select_prop(area), "Status": select_prop(status),
        "Priority": select_prop(priority), "Notes": text_prop(notes),
        "Effort Estimate": select_prop(effort), "Submitted Date": date_prop("2024-11-01"),
    })

log("✓ All sample records created")

section("BUILD COMPLETE")
print(f"""
  Next Layer Concepts — AI Operations System v1.0
  ═══════════════════════════════════════════════
  Hub ID:    {built['hub']}
  Relations: {len(relations)}
  Databases: {len([k for k in built if k.startswith('db_')])}
  ═══════════════════════════════════════════════
  Workspace built successfully!
""")
for k, v in built.items():
    if k.startswith("db_"):
        print(f"  {k:<25} {v}")
