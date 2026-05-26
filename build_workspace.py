#!/usr/bin/env python3
"""
Next Layer Concepts — Notion Workspace Builder v1.0
Builds the complete AI Operations System workspace in Notion.

Usage:
    pip install notion-client
    export NOTION_TOKEN="ntn_your_token_here"
    python build_workspace.py <parent_page_id>

    <parent_page_id> is the ID of a Notion page you've shared
    with your integration. Get it from the page URL:
    notion.so/Your-Page-Title-{THIS_IS_THE_ID}
"""

import os
import sys
import time
import json

try:
    from notion_client import Client
except ImportError:
    print("ERROR: notion-client not installed. Run: pip install notion-client")
    sys.exit(1)


# ─── CONFIG ───────────────────────────────────────────────────────────────────

TOKEN = os.environ.get("NOTION_TOKEN")
if not TOKEN:
    print("ERROR: NOTION_TOKEN environment variable not set.")
    print("       export NOTION_TOKEN=your_token_here")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python build_workspace.py <parent_page_id>")
    print("       The parent page must be shared with your integration.")
    sys.exit(1)

ROOT_PARENT_ID = sys.argv[1].replace("-", "")

notion = Client(auth=TOKEN)
built = {}  # Stores created page/database IDs by key


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def log(msg):
    print(f"  {msg}")

def section(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")

def create_page(parent_id, title, emoji="📄", body_blocks=None):
    children = body_blocks or []
    page = notion.pages.create(
        parent={"type": "page_id", "page_id": parent_id},
        icon={"type": "emoji", "emoji": emoji},
        properties={
            "title": {"title": [{"text": {"content": title}}]}
        },
        children=children
    )
    time.sleep(0.35)
    return page["id"]

def heading(text, level=2):
    tag = f"heading_{level}"
    return {
        "object": "block",
        "type": tag,
        tag: {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }

def callout(text, emoji="💡"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"type": "emoji", "emoji": emoji}
        }
    }

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }

def bulleted(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }

def create_database(parent_id, title, emoji, properties):
    db = notion.databases.create(
        parent={"type": "page_id", "page_id": parent_id},
        icon={"type": "emoji", "emoji": emoji},
        title=[{"text": {"content": title}}],
        properties=properties
    )
    time.sleep(0.4)
    return db["id"]

def add_relation(database_id, property_name, target_db_id):
    notion.databases.update(
        database_id=database_id,
        properties={
            property_name: {
                "relation": {
                    "database_id": target_db_id,
                    "type": "single_property",
                    "single_property": {}
                }
            }
        }
    )
    time.sleep(0.35)

def create_record(database_id, properties):
    notion.pages.create(
        parent={"type": "database_id", "database_id": database_id},
        properties=properties
    )
    time.sleep(0.35)

def text_prop(value):
    return {"rich_text": [{"type": "text", "text": {"content": str(value)}}]}

def title_prop(value):
    return {"title": [{"type": "text", "text": {"content": str(value)}}]}

def select_prop(value):
    return {"select": {"name": value}}

def multi_prop(values):
    return {"multi_select": [{"name": v} for v in values]}

def date_prop(value):
    return {"date": {"start": value}}

def checkbox_prop(value):
    return {"checkbox": value}

def number_prop(value):
    return {"number": value}


# ─── COLOUR PALETTE FOR SELECTS ───────────────────────────────────────────────

STATUS_COLOURS = {
    "Draft": "gray", "Testing": "yellow", "Active": "green",
    "Paused": "orange", "Archived": "purple", "Deprecated": "purple",
    "Pilot": "blue", "Scaled": "green",
    "Queued": "gray", "In Progress": "yellow", "Review": "blue",
    "Complete": "green",
    "Pending": "gray", "In Review": "yellow", "Approved": "green",
    "Revision Needed": "orange", "Rejected": "red",
    "New": "gray", "Planned": "blue", "Done": "green",
    "Idea": "gray", "In Build": "yellow", "Live": "green",
    "Prospect": "blue", "Archived_client": "purple",
}

def sel(name, colour=None):
    colour = colour or STATUS_COLOURS.get(name, "default")
    return {"name": name, "color": colour}

def select_options(*names):
    return {"select": {"options": [sel(n) for n in names]}}

def multi_options(*names):
    return {"multi_select": {"options": [sel(n) for n in names]}}


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — PAGE HIERARCHY
# ═══════════════════════════════════════════════════════════════════════════════

section("PHASE 1 — Building Page Hierarchy")

# Root hub page
log("Creating root hub page...")
hub_id = create_page(ROOT_PARENT_ID, "Next Layer Concepts — AI Operations Hub", "🧠", [
    callout(
        "Next Layer Concepts AI Operations System v1.0 — Built with Claude Code. "
        "Navigate using the sidebar sections 00–09.",
        "🚀"
    ),
    divider(),
    heading("Quick Navigation", 2),
    bulleted("00 — Home Dashboard"),
    bulleted("01 — Command Centre"),
    bulleted("02 — Workflows"),
    bulleted("03 — Prompt Library"),
    bulleted("04 — Clients"),
    bulleted("05 — Knowledge Base"),
    bulleted("06 — SOPs & Documentation"),
    bulleted("07 — Automations"),
    bulleted("08 — Improvements & Changelog"),
    bulleted("09 — Settings & Meta"),
])
built["hub"] = hub_id
log(f"  Hub created: {hub_id}")

# Top-level sections
sections_def = [
    ("00 — Home Dashboard",          "🏠", "home"),
    ("01 — Command Centre",          "🎯", "command"),
    ("02 — Workflows",               "⚙️",  "workflows"),
    ("03 — Prompt Library",          "💬", "prompts"),
    ("04 — Clients",                 "🤝", "clients"),
    ("05 — Knowledge Base",          "📚", "knowledge"),
    ("06 — SOPs & Documentation",    "📋", "sops"),
    ("07 — Automations",             "⚡", "automations"),
    ("08 — Improvements & Changelog","🔄", "improvements"),
    ("09 — Settings & Meta",         "⚙️",  "settings"),
]

for title, emoji, key in sections_def:
    log(f"Creating section: {title}")
    built[key] = create_page(hub_id, title, emoji)

# Sub-pages under Command Centre (01)
log("Creating Command Centre sub-pages...")
built["cmd_active"]   = create_page(built["command"], "Active Projects Dashboard", "📊")
built["cmd_weekly"]   = create_page(built["command"], "Weekly Review", "📅")
built["cmd_priority"] = create_page(built["command"], "Priorities Board", "🎯")

# Workflows sub-pages
log("Creating Workflow sub-pages...")
built["wfl_registry_page"] = create_page(built["workflows"], "Workflow Registry", "📁")
built["credit_risk_folder"] = create_page(built["workflows"], "UK Credit Risk Analysis", "🏦", [
    callout(
        "Pilot Workflow — UK Companies House Full Accounts → AI Credit Risk Report. "
        "Status: PILOT. Owner: Next Layer Concepts.",
        "🏦"
    ),
    divider(),
    heading("Workflow Overview", 2),
    paragraph(
        "This workflow takes UK Companies House Full Accounts PDFs as input and "
        "produces structured credit risk analysis reports with risk ratings and recommendations."
    ),
    divider(),
    heading("Phase Process", 2),
    bulleted("Phase 1: Intake — create analysis record, link PDF"),
    bulleted("Phase 2: Extraction — run 5 extraction prompts (P01–P05)"),
    bulleted("Phase 3: Analysis — run 4 risk analysis prompts (P06–P09)"),
    bulleted("Phase 4: Scoring — run overall risk score prompt (P10)"),
    bulleted("Phase 5: Summary — run 3 summary prompts (P11–P13)"),
    bulleted("Phase 6: Review — analyst reviews all outputs"),
    bulleted("Phase 7: Report — assemble and deliver final report"),
    bulleted("Phase 8: Archive — complete record, log improvements"),
])

# Prompt Library sub-pages
log("Creating Prompt Library sub-pages...")
built["prompt_categories"] = create_page(built["prompts"], "Prompt Categories Guide", "🗂️", [
    heading("Prompt Categories", 2),
    bulleted("Extraction — pulls specific data from a document"),
    bulleted("Analysis — interprets financial or operational data"),
    bulleted("Scoring — generates a numerical or categorical risk score"),
    bulleted("Summary — condenses information into a brief"),
    bulleted("Generation — creates new content from instructions"),
    bulleted("Classification — categorises input data"),
    bulleted("Validation — checks output quality or consistency"),
    bulleted("Component — reusable prompt fragments (system prompts, format rules)"),
])
built["prompt_testing"] = create_page(built["prompts"], "Prompt Testing Log", "🧪")

# Clients sub-pages
log("Creating Clients sub-pages...")
built["client_projects_page"] = create_page(built["clients"], "Client Projects", "📁")
built["client_deliverables"]  = create_page(built["clients"], "Client Deliverables", "📦")

# Knowledge Base sub-pages
log("Creating Knowledge Base sub-pages...")
built["kb_ai_tools"]    = create_page(built["knowledge"], "AI Tools & Models", "🤖", [
    heading("AI Model Notes", 2),
    bulleted("GPT-4o — Strong at structured extraction, handles long documents well"),
    bulleted("Claude Opus — Excellent reasoning, strong for complex analysis tasks"),
    bulleted("Claude Sonnet — Balanced speed/quality for production workflows"),
    bulleted("Gemini — Strong multimodal capabilities, useful for document parsing"),
    divider(),
    heading("Selection Criteria", 2),
    bulleted("Extraction tasks → GPT-4o or Claude Sonnet"),
    bulleted("Complex analysis → Claude Opus"),
    bulleted("High-volume automation → Claude Sonnet (cost efficiency)"),
    bulleted("Document OCR/parsing → Gemini or GPT-4o Vision"),
])
built["kb_research"]    = create_page(built["knowledge"], "Industry Research", "🔬")
built["kb_frameworks"]  = create_page(built["knowledge"], "Frameworks & Methodologies", "🏗️", [
    heading("Credit Risk Analysis Framework", 2),
    bulleted("Profitability — Revenue trends, margin analysis, YoY changes"),
    bulleted("Liquidity — Current ratio, quick ratio, working capital"),
    bulleted("Solvency — Debt-to-equity, interest coverage, net debt"),
    bulleted("Cash Flow — Operating cash flow, free cash flow, cash conversion"),
    bulleted("Red Flags — Director loans, related party transactions, qualified audits"),
    divider(),
    heading("Risk Scoring Guide", 2),
    bulleted("0–20: Very Low Risk"),
    bulleted("21–40: Low Risk"),
    bulleted("41–60: Medium Risk"),
    bulleted("61–80: High Risk"),
    bulleted("81–100: Critical Risk"),
])
built["kb_reference"]   = create_page(built["knowledge"], "Reference Documents", "📄")

# SOPs sub-pages
log("Creating SOP sub-pages...")
built["sop_templates"] = create_page(built["sops"], "Templates Library", "📝")
built["sop_internal"]  = create_page(built["sops"], "Internal Processes", "🔧")

# Automations sub-pages
log("Creating Automation sub-pages...")
built["auto_blueprints"] = create_page(built["automations"], "Zapier & Make Blueprints", "🔌", [
    heading("Priority Automations to Build", 2),
    bulleted("1. New Analysis → Create Output placeholder records (Make)"),
    bulleted("2. Analysis status → Review: notify reviewer via email (Zapier)"),
    bulleted("3. New Client → Create onboarding checklist (Make)"),
    bulleted("4. Prompt Active/Deprecated → Log to Change Log (Zapier)"),
    bulleted("5. Risk score updated → Alert if > threshold (Zapier)"),
    bulleted("6. Weekly digest → Open items summary email (Make, scheduled)"),
    bulleted("7. PDF upload → Trigger analysis workflow (Make + AI model)"),
    bulleted("8. Report Issued → Archive analysis record (Zapier)"),
])
built["auto_api_docs"]   = create_page(built["automations"], "API Documentation", "📡")

# Improvements sub-pages
log("Creating Improvements sub-pages...")
built["retros"] = create_page(built["improvements"], "Retrospectives", "🪞", [
    callout("Run a retrospective at the end of each month. Use the template below.", "📅"),
    divider(),
    heading("Monthly Retrospective Template", 2),
    bulleted("What worked well this month?"),
    bulleted("What didn't work or caused friction?"),
    bulleted("Prompt improvements made"),
    bulleted("Workflow improvements made"),
    bulleted("Automations built or planned"),
    bulleted("Ideas for next month"),
    divider(),
    heading("Metrics to Record", 2),
    bulleted("Analyses completed:"),
    bulleted("Prompts updated:"),
    bulleted("Client reports delivered:"),
    bulleted("Automations live:"),
])

# Settings sub-pages
log("Creating Settings sub-pages...")
built["settings_conventions"] = create_page(built["settings"], "Workspace Conventions", "📐", [
    heading("Naming Conventions", 2),
    bulleted("Title Case for all database records and page titles"),
    bulleted("Dates always YYYY-MM-DD format"),
    bulleted("IDs always included for automation-readiness"),
    divider(),
    heading("ID Format", 2),
    paragraph("NLC — [AREA CODE] — [YEAR] — [SEQUENCE]"),
    bulleted("WFL = Workflow"),
    bulleted("PRO = Prompt"),
    bulleted("CRA = Credit Risk Analysis"),
    bulleted("OUT = Output"),
    bulleted("REV = Review"),
    bulleted("CLI = Client"),
    bulleted("PRJ = Project"),
    bulleted("SOP = Standard Operating Procedure"),
    bulleted("AUT = Automation"),
    bulleted("CHG = Change Log"),
    divider(),
    heading("Status Rules", 2),
    bulleted("Draft → Testing → Active → Paused → Archived (lifecycle)"),
    bulleted("Queued → In Progress → Review → Complete → Archived (tasks)"),
    bulleted("Pending → In Review → Approved → Revision Needed (reviews)"),
    bulleted("Never delete records — always set to Archived or Deprecated"),
    divider(),
    heading("File Naming (External Files)", 2),
    paragraph("NLC — [Client] — [Type] — [Date]"),
    bulleted("Example: NLC — Acme Ltd — Credit Risk Report — 2024-12-01"),
    bulleted("Example: NLC — Acme Ltd — Full Accounts PDF — 2024-03-31"),
])
built["settings_access"] = create_page(built["settings"], "Access & Permissions Notes", "🔐")

log("✓ Page hierarchy complete")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — DATABASES
# ═══════════════════════════════════════════════════════════════════════════════

section("PHASE 2 — Building Databases")

# ── WORKFLOW REGISTRY ──────────────────────────────────────────────────────────
log("Creating Workflow Registry database...")
built["db_workflows"] = create_database(
    built["wfl_registry_page"],
    "Workflow Registry",
    "⚙️",
    {
        "Workflow Name":      {"title": {}},
        "Status":             select_options("Draft", "Pilot", "Active", "Scaled", "Paused", "Archived"),
        "Department":         select_options("Finance", "Marketing", "Operations", "Consulting", "Research"),
        "Owner":              {"people": {}},
        "Version":            {"rich_text": {}},
        "Last Reviewed":      {"date": {}},
        "Automation Status":  select_options("Manual", "Partial", "Fully Automated"),
        "Tags":               multi_options("AI", "Finance", "Reporting", "Marketing", "Content",
                                            "Operations", "Consulting", "Automation", "Template"),
        "Notes":              {"rich_text": {}},
        "Workflow ID":        {"rich_text": {}},
    }
)
log(f"  Workflow Registry: {built['db_workflows']}")

# ── MASTER PROMPT DATABASE ─────────────────────────────────────────────────────
log("Creating Master Prompt Database...")
built["db_prompts"] = create_database(
    built["prompts"],
    "Master Prompt Database",
    "💬",
    {
        "Prompt Name":        {"title": {}},
        "Prompt ID":          {"rich_text": {}},
        "Category":           select_options("Extraction", "Analysis", "Scoring", "Summary",
                                             "Generation", "Classification", "Validation", "Component"),
        "AI Model":           select_options("GPT-4o", "Claude Opus", "Claude Sonnet",
                                             "Claude Haiku", "Gemini", "Llama", "Custom"),
        "Status":             select_options("Draft", "Testing", "Active", "Deprecated"),
        "Version":            {"rich_text": {}},
        "Prompt Body":        {"rich_text": {}},
        "Input Required":     {"rich_text": {}},
        "Expected Output":    {"rich_text": {}},
        "Performance Notes":  {"rich_text": {}},
        "Created":            {"date": {}},
        "Last Modified":      {"date": {}},
        "Owner":              {"people": {}},
        "Tags":               multi_options("Credit Risk", "Balance Sheet", "P&L", "Cash Flow",
                                            "Solvency", "Liquidity", "Risk Score", "Executive Summary",
                                            "Red Flags", "Recommendations", "Extraction",
                                            "Marketing", "Content", "Operations"),
    }
)
log(f"  Master Prompt Database: {built['db_prompts']}")

# ── PROMPT TESTING LOG ─────────────────────────────────────────────────────────
log("Creating Prompt Testing Log database...")
built["db_prompt_tests"] = create_database(
    built["prompt_testing"],
    "Prompt Testing Log",
    "🧪",
    {
        "Test Name":          {"title": {}},
        "Test Date":          {"date": {}},
        "Tester":             {"people": {}},
        "AI Model Used":      select_options("GPT-4o", "Claude Opus", "Claude Sonnet",
                                             "Claude Haiku", "Gemini", "Custom"),
        "Input Summary":      {"rich_text": {}},
        "Output Quality":     select_options("Poor", "Fair", "Good", "Excellent"),
        "Issues Found":       {"rich_text": {}},
        "Action Taken":       {"rich_text": {}},
        "Result":             select_options("Passed", "Failed", "Revised"),
    }
)
log(f"  Prompt Testing Log: {built['db_prompt_tests']}")

# ── ANALYSIS TRACKER ───────────────────────────────────────────────────────────
log("Creating Analysis Tracker database...")
built["db_analyses"] = create_database(
    built["credit_risk_folder"],
    "Analysis Tracker",
    "📊",
    {
        "Analysis Name":      {"title": {}},
        "Analysis ID":        {"rich_text": {}},
        "Company Name":       {"rich_text": {}},
        "Companies House No": {"rich_text": {}},
        "Filing Period":      {"date": {}},
        "Date Initiated":     {"date": {}},
        "Analyst":            {"people": {}},
        "Status":             select_options("Queued", "In Progress", "Review", "Complete", "Archived"),
        "Priority":           select_options("Low", "Medium", "High", "Urgent"),
        "PDF Source":         {"url": {}},
        "Notes":              {"rich_text": {}},
    }
)
log(f"  Analysis Tracker: {built['db_analyses']}")

# ── OUTPUT ARCHIVE ─────────────────────────────────────────────────────────────
log("Creating Output Archive database...")
built["db_outputs"] = create_database(
    built["credit_risk_folder"],
    "Output Archive",
    "📄",
    {
        "Output Name":        {"title": {}},
        "Output ID":          {"rich_text": {}},
        "Section Type":       select_options("Profitability", "Liquidity", "Solvency",
                                             "Cash Flow", "Risk Score", "Executive Summary",
                                             "Red Flags", "Recommendations", "Director Analysis",
                                             "Related Parties"),
        "AI Model":           select_options("GPT-4o", "Claude Opus", "Claude Sonnet",
                                             "Claude Haiku", "Gemini", "Custom"),
        "Raw Output":         {"rich_text": {}},
        "Quality Rating":     select_options("Poor", "Acceptable", "Good", "Excellent"),
        "Reviewed":           {"checkbox": {}},
        "Review Notes":       {"rich_text": {}},
        "Date Generated":     {"date": {}},
        "Version":            {"rich_text": {}},
        "Included in Report": {"checkbox": {}},
    }
)
log(f"  Output Archive: {built['db_outputs']}")

# ── RISK REVIEW BOARD ──────────────────────────────────────────────────────────
log("Creating Risk Review Board database...")
built["db_reviews"] = create_database(
    built["credit_risk_folder"],
    "Risk Review Board",
    "🔍",
    {
        "Review Name":        {"title": {}},
        "Reviewer":           {"people": {}},
        "Review Date":        {"date": {}},
        "Status":             select_options("Pending", "In Review", "Approved",
                                             "Revision Needed", "Rejected"),
        "Overall Risk Rating":select_options("Very Low", "Low", "Medium",
                                             "High", "Very High", "Critical"),
        "Risk Score":         {"number": {"format": "number"}},
        "Key Findings":       {"rich_text": {}},
        "Red Flags":          {"rich_text": {}},
        "Recommendations":    {"rich_text": {}},
        "Report Issued":      {"checkbox": {}},
        "Report File":        {"files": {}},
    }
)
log(f"  Risk Review Board: {built['db_reviews']}")

# ── CLIENT REGISTRY ────────────────────────────────────────────────────────────
log("Creating Client Registry database...")
built["db_clients"] = create_database(
    built["clients"],
    "Client Registry",
    "🤝",
    {
        "Client Name":        {"title": {}},
        "Client ID":          {"rich_text": {}},
        "Status":             select_options("Active", "Prospect", "Paused", "Archived"),
        "Industry":           select_options("Finance", "Property", "Retail", "Manufacturing",
                                             "Technology", "Healthcare", "Legal", "Construction",
                                             "Hospitality", "Other"),
        "Contact Name":       {"rich_text": {}},
        "Contact Email":      {"email": {}},
        "Onboarded":          {"date": {}},
        "Account Manager":    {"people": {}},
        "Notes":              {"rich_text": {}},
    }
)
log(f"  Client Registry: {built['db_clients']}")

# ── CLIENT PROJECTS ────────────────────────────────────────────────────────────
log("Creating Client Projects database...")
built["db_projects"] = create_database(
    built["client_projects_page"],
    "Client Projects",
    "📁",
    {
        "Project Name":       {"title": {}},
        "Project ID":         {"rich_text": {}},
        "Status":             select_options("Scoping", "Active", "Review", "Delivered", "Archived"),
        "Start Date":         {"date": {}},
        "Target Date":        {"date": {}},
        "Project Manager":    {"people": {}},
        "Brief":              {"rich_text": {}},
        "Deliverables":       {"rich_text": {}},
        "Budget":             {"number": {"format": "pound"}},
        "Invoiced":           {"checkbox": {}},
        "Notes":              {"rich_text": {}},
    }
)
log(f"  Client Projects: {built['db_projects']}")

# ── SOP REGISTRY ───────────────────────────────────────────────────────────────
log("Creating SOP Registry database...")
built["db_sops"] = create_database(
    built["sops"],
    "SOP Registry",
    "📋",
    {
        "SOP Name":           {"title": {}},
        "SOP ID":             {"rich_text": {}},
        "Status":             select_options("Draft", "Active", "Needs Review", "Archived"),
        "Owner":              {"people": {}},
        "Last Reviewed":      {"date": {}},
        "Version":            {"rich_text": {}},
        "Department":         select_options("Operations", "Finance", "Consulting",
                                             "Marketing", "Technology"),
        "Tags":               multi_options("Onboarding", "Process", "Technical", "Client",
                                            "Credit Risk", "Automation", "Quality Control"),
    }
)
log(f"  SOP Registry: {built['db_sops']}")

# ── AUTOMATION REGISTRY ────────────────────────────────────────────────────────
log("Creating Automation Registry database...")
built["db_automations"] = create_database(
    built["automations"],
    "Automation Registry",
    "⚡",
    {
        "Automation Name":    {"title": {}},
        "Automation ID":      {"rich_text": {}},
        "Tool":               select_options("Zapier", "Make", "Power Automate", "n8n",
                                             "API", "Python Script", "Other"),
        "Status":             select_options("Idea", "Planned", "In Build", "Live",
                                             "Paused", "Deprecated"),
        "Trigger":            {"rich_text": {}},
        "Action":             {"rich_text": {}},
        "Priority":           select_options("Low", "Medium", "High"),
        "Owner":              {"people": {}},
        "Live Date":          {"date": {}},
        "Notes":              {"rich_text": {}},
    }
)
log(f"  Automation Registry: {built['db_automations']}")

# ── CHANGE LOG ─────────────────────────────────────────────────────────────────
log("Creating Change Log database...")
built["db_changelog"] = create_database(
    built["improvements"],
    "Change Log",
    "🔄",
    {
        "Change Title":       {"title": {}},
        "Change ID":          {"rich_text": {}},
        "Change Type":        select_options("Prompt Update", "Workflow Change", "Database Update",
                                             "Process Change", "Fix", "New Feature", "Deprecation"),
        "Area":               select_options("Prompt Library", "Workflow", "Client",
                                             "Automation", "Workspace", "Database", "SOP"),
        "Changed By":         {"people": {}},
        "Date":               {"date": {}},
        "Version Before":     {"rich_text": {}},
        "Version After":      {"rich_text": {}},
        "Reason":             {"rich_text": {}},
        "Impact":             select_options("Low", "Medium", "High"),
    }
)
log(f"  Change Log: {built['db_changelog']}")

# ── IDEAS BACKLOG ──────────────────────────────────────────────────────────────
log("Creating Ideas Backlog database...")
built["db_ideas"] = create_database(
    built["improvements"],
    "Ideas Backlog",
    "💡",
    {
        "Idea Title":         {"title": {}},
        "Area":               select_options("Workflow", "Prompt", "Automation", "Client",
                                             "Workspace", "Database", "SOP", "Reporting"),
        "Status":             select_options("New", "Reviewed", "Planned",
                                             "In Progress", "Done", "Rejected"),
        "Priority":           select_options("Low", "Medium", "High"),
        "Submitted By":       {"people": {}},
        "Submitted Date":     {"date": {}},
        "Notes":              {"rich_text": {}},
        "Effort Estimate":    select_options("Small", "Medium", "Large"),
    }
)
log(f"  Ideas Backlog: {built['db_ideas']}")

log("✓ All databases created")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — RELATIONS
# ═══════════════════════════════════════════════════════════════════════════════

section("PHASE 3 — Wiring Up Relations")

relations = [
    # (source_db_key, property_name, target_db_key)
    ("db_workflows",   "Linked SOPs",       "db_sops"),
    ("db_workflows",   "Linked Prompts",     "db_prompts"),
    ("db_workflows",   "Linked Clients",     "db_clients"),
    ("db_workflows",   "Linked Automations", "db_automations"),
    ("db_prompts",     "Workflow",           "db_workflows"),
    ("db_prompts",     "Linked Tests",       "db_prompt_tests"),
    ("db_prompt_tests","Prompt",             "db_prompts"),
    ("db_analyses",    "Prompts Used",       "db_prompts"),
    ("db_analyses",    "Output Records",     "db_outputs"),
    ("db_analyses",    "Risk Review",        "db_reviews"),
    ("db_analyses",    "Client",             "db_clients"),
    ("db_outputs",     "Analysis",           "db_analyses"),
    ("db_outputs",     "Prompt Used",        "db_prompts"),
    ("db_reviews",     "Analysis",           "db_analyses"),
    ("db_reviews",     "Client",             "db_clients"),
    ("db_clients",     "Projects",           "db_projects"),
    ("db_clients",     "Workflows Used",     "db_workflows"),
    ("db_clients",     "Analyses",           "db_analyses"),
    ("db_projects",    "Client",             "db_clients"),
    ("db_sops",        "Workflow",           "db_workflows"),
    ("db_automations", "Workflow",           "db_workflows"),
    ("db_changelog",   "Linked Prompt",      "db_prompts"),
    ("db_changelog",   "Linked Workflow",    "db_workflows"),
    ("db_ideas",       "Linked Workflow",    "db_workflows"),
]

for src_key, prop_name, tgt_key in relations:
    log(f"  {src_key} → [{prop_name}] → {tgt_key}")
    try:
        add_relation(built[src_key], prop_name, built[tgt_key])
    except Exception as e:
        log(f"  WARNING: Could not add relation {prop_name}: {e}")

log("✓ Relations wired")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — SAMPLE RECORDS
# ═══════════════════════════════════════════════════════════════════════════════

section("PHASE 4 — Creating Sample Records")

# ── Workflow Registry: UK Credit Risk Analysis ─────────────────────────────────
log("Adding workflow record: UK Credit Risk Analysis...")
create_record(built["db_workflows"], {
    "Workflow Name":     title_prop("UK Credit Risk Analysis"),
    "Workflow ID":       text_prop("NLC-WFL-2024-001"),
    "Status":            select_prop("Pilot"),
    "Department":        select_prop("Finance"),
    "Version":           text_prop("v1.0"),
    "Automation Status": select_prop("Manual"),
    "Tags":              multi_prop(["AI", "Finance", "Reporting"]),
    "Notes":             text_prop(
        "Pilot workflow. Analyses UK Companies House Full Accounts PDFs "
        "and generates professional credit risk reports. Target: fully "
        "automated Phase 2 (extraction) by Q2 2025."
    ),
})

# ── 13 Credit Risk Prompts ─────────────────────────────────────────────────────
credit_risk_prompts = [
    ("CRA — Component — System Context — v1.0", "NLC-PRO-2024-001", "Component",
     "You are a UK-qualified financial analyst specialising in credit risk assessment for SMEs. "
     "You are reviewing Companies House Full Accounts filed under FRS 102 or FRS 105. "
     "Your analysis is used by lenders, investors, and risk teams to assess creditworthiness. "
     "You are thorough, precise, and conservative in your risk assessments. "
     "You only state facts that are explicitly evidenced in the accounts. "
     "You flag uncertainty rather than making assumptions. "
     "Format all monetary figures in GBP with comma separators (£1,234,567).",
     "N/A — this is a system context component to prepend to other prompts",
     "N/A — sets AI persona and constraints",
     "Credit Risk | Component"),

    ("CRA — Extraction — Revenue & Profitability — v1.0", "NLC-PRO-2024-002", "Extraction",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Extract all revenue and profitability figures from the Profit and Loss account in the accounts provided.\n\n"
     "Return your output in exactly this format:\n"
     "REVENUE & PROFITABILITY EXTRACTION\n"
     "- Turnover / Revenue: £[X]\n"
     "- Cost of Sales: £[X]\n"
     "- Gross Profit: £[X] ([X]% gross margin)\n"
     "- Operating Profit / EBIT: £[X] ([X]% operating margin)\n"
     "- Net Profit Before Tax: £[X]\n"
     "- Net Profit After Tax: £[X] ([X]% net margin)\n"
     "- Prior Year Turnover: £[X]\n"
     "- Year-on-Year Revenue Change: [X]%\n"
     "- Year-on-Year Net Profit Change: [X]%\n\n"
     "If any figure is not disclosed, write: 'Not disclosed in accounts.'\n"
     "Do not estimate. Do not calculate from other figures unless explicitly stated.",
     "UK Companies House Full Accounts PDF (paste text or upload)",
     "Structured extraction of 9 profitability metrics with prior year comparison",
     "Credit Risk | P&L | Extraction"),

    ("CRA — Extraction — Balance Sheet Assets — v1.0", "NLC-PRO-2024-003", "Extraction",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Extract all asset figures from the Balance Sheet in the accounts provided.\n\n"
     "Return your output in exactly this format:\n"
     "BALANCE SHEET — ASSETS EXTRACTION\n"
     "FIXED / NON-CURRENT ASSETS\n"
     "- Tangible Fixed Assets: £[X]\n"
     "- Intangible Assets: £[X]\n"
     "- Investments: £[X]\n"
     "- Total Fixed Assets: £[X]\n\n"
     "CURRENT ASSETS\n"
     "- Stock / Inventory: £[X]\n"
     "- Debtors / Trade Receivables: £[X]\n"
     "- Cash and Cash Equivalents: £[X]\n"
     "- Other Current Assets: £[X]\n"
     "- Total Current Assets: £[X]\n\n"
     "TOTAL ASSETS: £[X]\n\n"
     "If any figure is not disclosed, write: 'Not disclosed in accounts.'",
     "UK Companies House Full Accounts PDF (paste text or upload)",
     "Structured extraction of all balance sheet asset lines",
     "Credit Risk | Balance Sheet | Extraction"),

    ("CRA — Extraction — Balance Sheet Liabilities — v1.0", "NLC-PRO-2024-004", "Extraction",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Extract all liability and equity figures from the Balance Sheet in the accounts provided.\n\n"
     "Return your output in exactly this format:\n"
     "BALANCE SHEET — LIABILITIES & EQUITY EXTRACTION\n"
     "CURRENT LIABILITIES\n"
     "- Trade Creditors / Payables: £[X]\n"
     "- Bank Overdraft: £[X]\n"
     "- Short-term Borrowings: £[X]\n"
     "- Other Current Liabilities: £[X]\n"
     "- Total Current Liabilities: £[X]\n\n"
     "NON-CURRENT LIABILITIES\n"
     "- Long-term Borrowings: £[X]\n"
     "- Deferred Tax: £[X]\n"
     "- Other Long-term Liabilities: £[X]\n"
     "- Total Non-Current Liabilities: £[X]\n\n"
     "TOTAL LIABILITIES: £[X]\n\n"
     "EQUITY\n"
     "- Share Capital: £[X]\n"
     "- Retained Earnings / Reserves: £[X]\n"
     "- Total Equity: £[X]\n\n"
     "NET ASSETS / (LIABILITIES): £[X]",
     "UK Companies House Full Accounts PDF (paste text or upload)",
     "Structured extraction of all balance sheet liability and equity lines",
     "Credit Risk | Balance Sheet | Extraction"),

    ("CRA — Extraction — Cash Flow — v1.0", "NLC-PRO-2024-005", "Extraction",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Extract all cash flow figures from the Cash Flow Statement in the accounts provided. "
     "If no formal cash flow statement is included (common in FRS 105 micro-entity accounts), "
     "state: 'No formal cash flow statement included in these accounts (micro-entity exemption likely applies).'\n\n"
     "CASH FLOW EXTRACTION\n"
     "- Net Cash from Operating Activities: £[X]\n"
     "- Net Cash from Investing Activities: £[X]\n"
     "- Net Cash from Financing Activities: £[X]\n"
     "- Net Change in Cash: £[X]\n"
     "- Opening Cash Balance: £[X]\n"
     "- Closing Cash Balance: £[X]\n"
     "- Capital Expenditure: £[X]\n"
     "- Free Cash Flow (Operating - Capex): £[X]",
     "UK Companies House Full Accounts PDF (paste text or upload)",
     "Structured extraction of cash flow statement",
     "Credit Risk | Cash Flow | Extraction"),

    ("CRA — Extraction — Director & Related Parties — v1.0", "NLC-PRO-2024-006", "Extraction",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Review the notes to the accounts and extract all director remuneration, director loan, "
     "and related party transaction disclosures.\n\n"
     "DIRECTOR & RELATED PARTY EXTRACTION\n"
     "- Director Remuneration (total): £[X]\n"
     "- Highest Paid Director: £[X]\n"
     "- Director Loan Account Balance (owed TO company): £[X]\n"
     "- Director Loan Account Balance (owed BY company): £[X]\n"
     "- Related Party Transactions: [describe each, with amounts]\n"
     "- Dividends Paid: £[X]\n"
     "- Auditor Remuneration: £[X]\n"
     "- Any other significant notes disclosures: [describe]\n\n"
     "Flag any director loans exceeding £10,000 or related party transactions "
     "that appear material relative to company turnover.",
     "UK Companies House Full Accounts PDF — Notes section (paste text or upload)",
     "Disclosure of director loans, remuneration, related party transactions",
     "Credit Risk | Director Analysis | Extraction | Red Flags"),

    ("CRA — Analysis — Profitability Risk — v1.0", "NLC-PRO-2024-007", "Analysis",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Using the profitability extraction data provided below, conduct a profitability risk analysis.\n\n"
     "INPUT: [Paste output from CRA-PRO-002 here]\n\n"
     "Analyse and return:\n"
     "PROFITABILITY RISK ANALYSIS\n"
     "- Revenue trend assessment: [growing/stable/declining — with commentary]\n"
     "- Gross margin assessment: [strong/acceptable/weak — with benchmark context for this sector]\n"
     "- Net margin assessment: [strong/acceptable/weak]\n"
     "- YoY trend assessment: [improving/stable/deteriorating]\n"
     "- Profitability Risk Rating: [Low / Medium / High / Critical]\n"
     "- Key profitability risk factors: [bullet list]\n"
     "- Positive indicators: [bullet list]",
     "Output from CRA — Extraction — Revenue & Profitability prompt",
     "Profitability risk rating with supporting analysis",
     "Credit Risk | P&L | Analysis"),

    ("CRA — Analysis — Liquidity Risk — v1.0", "NLC-PRO-2024-008", "Analysis",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Using the balance sheet data provided, conduct a liquidity risk analysis.\n\n"
     "INPUT: [Paste outputs from CRA-PRO-003 and CRA-PRO-004 here]\n\n"
     "Calculate and analyse:\n"
     "LIQUIDITY RISK ANALYSIS\n"
     "- Current Ratio: [Total Current Assets / Total Current Liabilities = X.XX]\n"
     "- Quick Ratio: [(Current Assets - Stock) / Current Liabilities = X.XX]\n"
     "- Cash Ratio: [Cash / Current Liabilities = X.XX]\n"
     "- Working Capital: £[Current Assets - Current Liabilities]\n"
     "- Days Cash Cover: [Cash / (Annual Turnover / 365) = X days]\n"
     "- Liquidity Risk Rating: [Low / Medium / High / Critical]\n"
     "- Benchmark: Current ratio > 1.5 = healthy; 1.0–1.5 = acceptable; < 1.0 = concern\n"
     "- Key liquidity risk factors: [bullet list]\n"
     "- Positive indicators: [bullet list]",
     "Outputs from Balance Sheet Assets and Liabilities extraction prompts",
     "Liquidity ratios, working capital analysis, liquidity risk rating",
     "Credit Risk | Liquidity | Analysis"),

    ("CRA — Analysis — Solvency Risk — v1.0", "NLC-PRO-2024-009", "Analysis",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Using the balance sheet data provided, conduct a solvency risk analysis.\n\n"
     "INPUT: [Paste outputs from CRA-PRO-003 and CRA-PRO-004 here]\n\n"
     "Calculate and analyse:\n"
     "SOLVENCY RISK ANALYSIS\n"
     "- Debt-to-Equity Ratio: [Total Liabilities / Total Equity = X.XX]\n"
     "- Net Debt: [(Short + Long-term borrowings) - Cash = £X]\n"
     "- Gearing Ratio: [Net Debt / (Net Debt + Equity) = X%]\n"
     "- Equity Ratio: [Total Equity / Total Assets = X%]\n"
     "- Net Asset Position: [Positive / Negative — £X]\n"
     "- Solvency Risk Rating: [Low / Medium / High / Critical]\n"
     "- Benchmark: D/E < 1.0 = low leverage; 1.0–2.0 = moderate; > 2.0 = high\n"
     "- Key solvency risk factors: [bullet list]\n"
     "- Positive indicators: [bullet list]",
     "Outputs from Balance Sheet Assets and Liabilities extraction prompts",
     "Solvency ratios, gearing analysis, solvency risk rating",
     "Credit Risk | Solvency | Analysis"),

    ("CRA — Analysis — Cash Flow Risk — v1.0", "NLC-PRO-2024-010", "Analysis",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Using the cash flow data provided, conduct a cash flow risk analysis.\n\n"
     "INPUT: [Paste output from CRA-PRO-005 here]\n\n"
     "Analyse and return:\n"
     "CASH FLOW RISK ANALYSIS\n"
     "- Operating cash flow quality: [strong/acceptable/weak — with commentary]\n"
     "- Free cash flow assessment: [positive/negative — sustainability comment]\n"
     "- Cash trend: [building/stable/depleting]\n"
     "- Capex investment level: [high/moderate/low — growth signal?]\n"
     "- Financing activity assessment: [debt increasing/decreasing/stable]\n"
     "- Cash Flow Risk Rating: [Low / Medium / High / Critical]\n"
     "- Key cash flow risk factors: [bullet list]\n"
     "- Note: If no cash flow statement available, assess liquidity from balance sheet cash position.\n"
     "- Positive indicators: [bullet list]",
     "Output from Cash Flow extraction prompt",
     "Cash flow quality assessment and risk rating",
     "Credit Risk | Cash Flow | Analysis"),

    ("CRA — Scoring — Overall Risk Score — v1.0", "NLC-PRO-2024-011", "Scoring",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Using all four risk analysis outputs provided, calculate an overall credit risk score.\n\n"
     "INPUT: [Paste outputs from CRA-PRO-007, 008, 009, 010 here]\n\n"
     "SCORING METHODOLOGY:\n"
     "Score each dimension 0–25 (0 = minimal risk, 25 = maximum risk):\n"
     "- Profitability Risk Score: [0–25]\n"
     "- Liquidity Risk Score: [0–25]\n"
     "- Solvency Risk Score: [0–25]\n"
     "- Cash Flow Risk Score: [0–25]\n\n"
     "OVERALL CREDIT RISK SCORE\n"
     "- Total Score: [sum of 4 dimensions] / 100\n"
     "- Risk Category:\n"
     "  0–20: Very Low Risk\n"
     "  21–40: Low Risk\n"
     "  41–60: Medium Risk\n"
     "  61–80: High Risk\n"
     "  81–100: Critical Risk\n"
     "- Overall Risk Category: [Very Low / Low / Medium / High / Critical]\n"
     "- Score Rationale: [2–3 sentence explanation of the score]",
     "Outputs from all four risk analysis prompts (PRO-007 to PRO-010)",
     "Numeric risk score 0-100 with risk category and rationale",
     "Credit Risk | Risk Score | Scoring"),

    ("CRA — Summary — Executive Risk Brief — v1.0", "NLC-PRO-2024-012", "Summary",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Using all analysis and scoring outputs, write a professional executive risk brief.\n\n"
     "INPUT: [Paste all analysis and scoring outputs here]\n\n"
     "EXECUTIVE RISK BRIEF\n"
     "Company: [Name] | Companies House No: [X] | Accounts Period: [X]\n"
     "Analysis Date: [Date] | Analyst: Next Layer Concepts\n\n"
     "OVERALL RISK RATING: [Very Low / Low / Medium / High / Critical]\n"
     "RISK SCORE: [X / 100]\n\n"
     "EXECUTIVE SUMMARY\n"
     "[3–4 sentences summarising the company's overall financial position and credit risk profile. "
     "Professional, factual, suitable for a credit committee or senior decision-maker.]\n\n"
     "FINANCIAL HIGHLIGHTS\n"
     "- [Key metric 1 with brief commentary]\n"
     "- [Key metric 2 with brief commentary]\n"
     "- [Key metric 3 with brief commentary]\n\n"
     "RISK ASSESSMENT SUMMARY\n"
     "- Profitability: [rating + 1-sentence commentary]\n"
     "- Liquidity: [rating + 1-sentence commentary]\n"
     "- Solvency: [rating + 1-sentence commentary]\n"
     "- Cash Flow: [rating + 1-sentence commentary]",
     "All analysis outputs from PRO-007 through PRO-011",
     "Professional executive summary suitable for a credit committee",
     "Credit Risk | Executive Summary | Summary"),

    ("CRA — Summary — Red Flags & Recommendations — v1.0", "NLC-PRO-2024-013", "Summary",
     "[PREPEND SYSTEM CONTEXT PROMPT]\n\n"
     "Using all analysis outputs provided, identify critical red flags and produce actionable recommendations.\n\n"
     "INPUT: [Paste all analysis outputs including director/related party extraction]\n\n"
     "RED FLAGS\n"
     "[List each red flag as a bullet point. Include the source (e.g., 'Balance Sheet:', 'Notes:'). "
     "Only include genuine concerns — do not pad with minor issues. "
     "If no red flags exist, state: 'No material red flags identified in these accounts.']\n\n"
     "RECOMMENDATIONS\n"
     "[List actionable recommendations as bullet points. "
     "Be specific — e.g., 'Request interim management accounts for the 6 months to [date]' "
     "rather than 'monitor performance'. "
     "Recommendations should be proportionate to the risk level.]\n\n"
     "NEXT REVIEW\n"
     "- Recommended next review date: [X]\n"
     "- Trigger conditions for earlier review: [list any conditions that should prompt early review]",
     "All analysis outputs including director/related party data",
     "Bulleted red flags list and specific actionable recommendations",
     "Credit Risk | Red Flags | Recommendations | Summary"),
]

log(f"Adding {len(credit_risk_prompts)} credit risk prompts...")
for name, pid, category, body, inp, expected, tags_str in credit_risk_prompts:
    tag_list = [t.strip() for t in tags_str.split("|")]
    create_record(built["db_prompts"], {
        "Prompt Name":     title_prop(name),
        "Prompt ID":       text_prop(pid),
        "Category":        select_prop(category),
        "AI Model":        select_prop("GPT-4o"),
        "Status":          select_prop("Active"),
        "Version":         text_prop("v1.0"),
        "Prompt Body":     text_prop(body),
        "Input Required":  text_prop(inp),
        "Expected Output": text_prop(expected),
        "Tags":            multi_prop(tag_list),
        "Created":         date_prop("2024-11-01"),
    })
    log(f"  + {name}")

# ── Sample Client ──────────────────────────────────────────────────────────────
log("Adding sample client: Acme Manufacturing Ltd...")
create_record(built["db_clients"], {
    "Client Name":    title_prop("Acme Manufacturing Ltd"),
    "Client ID":      text_prop("NLC-CLI-2024-001"),
    "Status":         select_prop("Active"),
    "Industry":       select_prop("Manufacturing"),
    "Contact Name":   text_prop("James Thornton"),
    "Contact Email":  {"email": "j.thornton@acme-manufacturing.co.uk"},
    "Onboarded":      date_prop("2024-11-01"),
    "Notes":          text_prop("First pilot client for UK Credit Risk Analysis workflow. "
                                "Credit facility renewal meeting scheduled Q1 2025."),
})

# ── Sample Analysis ────────────────────────────────────────────────────────────
log("Adding sample analysis record...")
create_record(built["db_analyses"], {
    "Analysis Name":      title_prop("Acme Manufacturing Ltd — Full Accounts 2024"),
    "Analysis ID":        text_prop("NLC-CRA-2024-001"),
    "Company Name":       text_prop("Acme Manufacturing Ltd"),
    "Companies House No": text_prop("04521890"),
    "Filing Period":      date_prop("2024-03-31"),
    "Date Initiated":     date_prop("2024-11-15"),
    "Status":             select_prop("Queued"),
    "Priority":           select_prop("High"),
    "Notes":              text_prop("Client has credit facility renewal Q1 2025. "
                                    "Full accounts for year ending 31 March 2024."),
})

# ── Sample SOP ─────────────────────────────────────────────────────────────────
log("Adding SOP record: How to Run a Credit Risk Analysis...")
create_record(built["db_sops"], {
    "SOP Name":     title_prop("How to Run a UK Credit Risk Analysis"),
    "SOP ID":       text_prop("NLC-SOP-2024-001"),
    "Status":       select_prop("Active"),
    "Version":      text_prop("v1.0"),
    "Department":   select_prop("Finance"),
    "Last Reviewed":date_prop("2024-11-01"),
    "Tags":         multi_prop(["Credit Risk", "Process", "Technical"]),
})

# ── Sample Automations ─────────────────────────────────────────────────────────
log("Adding automation ideas...")
automation_ideas = [
    ("Auto-Create Output Records on New Analysis", "NLC-AUT-2024-001", "Make",
     "New record created in Analysis Tracker",
     "Create 13 Output Archive records linked to the analysis",
     "High", "Idea"),
    ("Review Notification on Status Change", "NLC-AUT-2024-002", "Zapier",
     "Analysis Tracker status changes to 'Review'",
     "Send email notification to designated reviewer",
     "High", "Idea"),
    ("Client Delivery on Report Approval", "NLC-AUT-2024-003", "Zapier",
     "Risk Review Board status changes to 'Approved'",
     "Send report email to client contact; set Report Issued = true",
     "High", "Idea"),
    ("Weekly Open Items Digest", "NLC-AUT-2024-004", "Make",
     "Every Monday 8:00 AM",
     "Email summary of open analyses, pending reviews, new ideas",
     "Medium", "Idea"),
    ("Prompt Deprecation Logger", "NLC-AUT-2024-005", "Zapier",
     "Prompt status changes to 'Deprecated'",
     "Create Change Log entry with version and date",
     "Medium", "Idea"),
    ("New Client Onboarding Checklist", "NLC-AUT-2024-006", "Make",
     "New record created in Client Registry",
     "Create onboarding task checklist linked to client",
     "Medium", "Idea"),
]
for name, aid, tool, trigger, action, priority, status in automation_ideas:
    create_record(built["db_automations"], {
        "Automation Name": title_prop(name),
        "Automation ID":   text_prop(aid),
        "Tool":            select_prop(tool),
        "Status":          select_prop(status),
        "Trigger":         text_prop(trigger),
        "Action":          text_prop(action),
        "Priority":        select_prop(priority),
    })
    log(f"  + {name}")

# ── Sample Change Log Entries ──────────────────────────────────────────────────
log("Adding initial change log entries...")
changelog_entries = [
    ("Workspace v1.0 Created", "NLC-CHG-2024-001", "New Feature", "Workspace",
     "", "v1.0",
     "Initial build of Next Layer Concepts AI Operations System", "High"),
    ("UK Credit Risk Workflow v1.0 Launched", "NLC-CHG-2024-002", "New Feature", "Workflow",
     "", "v1.0",
     "Pilot launch of UK Credit Risk Analysis workflow with 13 prompts", "High"),
]
for title, cid, ctype, area, before, after, reason, impact in changelog_entries:
    create_record(built["db_changelog"], {
        "Change Title":   title_prop(title),
        "Change ID":      text_prop(cid),
        "Change Type":    select_prop(ctype),
        "Area":           select_prop(area),
        "Date":           date_prop("2024-11-01"),
        "Version Before": text_prop(before),
        "Version After":  text_prop(after),
        "Reason":         text_prop(reason),
        "Impact":         select_prop(impact),
    })

# ── Sample Ideas ────────────────────────────────────────────────────────────────
log("Adding ideas backlog entries...")
ideas = [
    ("Build Make automation for output record creation", "Automation", "New", "High",
     "When a new Analysis Tracker record is created, automatically create placeholder Output Archive records for all 13 section types.", "Small"),
    ("Add sector-specific benchmarks to scoring prompt", "Prompt", "New", "Medium",
     "The current scoring prompt uses generic benchmarks. Improving it to use sector-specific benchmarks (e.g., manufacturing vs retail) would increase accuracy.", "Medium"),
    ("Create client-facing report template in Notion", "Workflow", "New", "Medium",
     "Build a Notion template that can be exported/printed as a professional client report. Would eliminate manual report assembly step.", "Large"),
    ("Add Altman Z-Score calculation to solvency analysis", "Prompt", "New", "Low",
     "The Altman Z-Score is a well-established insolvency predictor. Adding this calculation to the solvency prompt would add quantitative rigour.", "Small"),
]
for idea_title, area, status, priority, notes, effort in ideas:
    create_record(built["db_ideas"], {
        "Idea Title":     title_prop(idea_title),
        "Area":           select_prop(area),
        "Status":         select_prop(status),
        "Priority":       select_prop(priority),
        "Notes":          text_prop(notes),
        "Effort Estimate":select_prop(effort),
        "Submitted Date": date_prop("2024-11-01"),
    })

log("✓ All sample records created")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5 — BUILD REPORT
# ═══════════════════════════════════════════════════════════════════════════════

section("BUILD COMPLETE")
print(f"""
  Next Layer Concepts — AI Operations System v1.0
  ═══════════════════════════════════════════════

  Pages Created:
  ├── Root Hub Page
  ├── 10 Top-Level Sections (00–09)
  ├── Command Centre (3 sub-pages)
  ├── UK Credit Risk Analysis Folder
  ├── Knowledge Base (4 sub-pages)
  ├── SOPs (2 sub-pages)
  └── Various supporting pages

  Databases Created (12):
  ├── Workflow Registry
  ├── Master Prompt Database
  ├── Prompt Testing Log
  ├── Analysis Tracker
  ├── Output Archive
  ├── Risk Review Board
  ├── Client Registry
  ├── Client Projects
  ├── SOP Registry
  ├── Automation Registry
  ├── Change Log
  └── Ideas Backlog

  Relations Wired: {len(relations)}

  Sample Records Created:
  ├── 1 Workflow (UK Credit Risk Analysis)
  ├── 13 Credit Risk Prompts (P01–P13)
  ├── 1 Sample Client (Acme Manufacturing Ltd)
  ├── 1 Sample Analysis Record
  ├── 1 Sample SOP Record
  ├── 6 Automation Ideas
  ├── 2 Change Log Entries
  └── 4 Ideas Backlog Items

  IMPORTANT — Manual Steps Required in Notion:
  ─────────────────────────────────────────────
  1. Set up filtered VIEWS on each database (can't be done via API)
  2. Add linked database views to dashboard pages
  3. Create database TEMPLATES for new analyses, reviews, outputs
  4. Configure Notion AI (if on Plus plan) for prompt assistance
  5. Share relevant pages with team members

  Database IDs (save these for automations):
""")
for key, val in built.items():
    if key.startswith("db_"):
        print(f"  {key:<22} {val}")

print(f"""
  Root Hub ID: {built['hub']}
  ═══════════════════════════════════════════════
  Workspace built successfully. Open Notion to review.
""")
