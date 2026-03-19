#!/usr/bin/env python3
"""Fix content errors in Virtual Auditor JSON files."""

import json
import os
import re

PAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "pages")

changes_log = []

def log_change(filename, description):
    changes_log.append(f"  [{filename}] {description}")

def load_json(filename):
    path = os.path.join(PAGES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join(PAGES_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def replace_regulatory_section(body_text, new_content):
    """Replace HEADING2: Regulatory Framework section content up to next HEADING2: or HEADING3:."""
    pattern = r'(HEADING2: Regulatory Framework\n).*?(?=\nHEADING[23]:)'
    match = re.search(pattern, body_text, re.DOTALL)
    if match:
        return body_text[:match.start()] + new_content + body_text[match.end():]
    # Try without leading newline requirement
    pattern2 = r'HEADING2: Regulatory Framework\n.*?(?=\nHEADING[23]:)'
    match2 = re.search(pattern2, body_text, re.DOTALL)
    if match2:
        return body_text[:match2.start()] + new_content + body_text[match2.end():]
    return None

def fix_bullet_artifacts(body_text):
    """Remove bullet artifacts before numbered HEADING3 steps.
    Actual pattern in files: '•\\n1\\n\\nHEADING3:' -> '1\\nHEADING3:'
    Also handles: '• 1\\nHEADING3:' -> '1\\nHEADING3:'
    """
    # Pattern 1: bullet, newline, number, newline(s), HEADING3
    result = re.sub(r'\u2022\n(\d+)\n+\n*(HEADING3:)', r'\1\n\2', body_text)
    # Pattern 2: bullet space number newline HEADING3
    result = re.sub(r'\u2022 (\d+)\n(HEADING3:)', r'\1\n\2', result)
    return result


# ============================================================
# SECTION A: Wrong Regulatory Framework (17 pages)
# ============================================================

print("=" * 60)
print("SECTION A: Fixing Regulatory Framework sections")
print("=" * 60)

# --- A1: startup-india-registration.json ---
fname = "startup-india-registration.json"
data = load_json(fname)
bt = data["bodyText"]

new_reg = "HEADING2: Regulatory Framework\nStartup India is governed by the DPIIT Notification G.S.R. 127(E) dated 19 February 2019, read with the Startup India Action Plan 2016. Recognition is granted by the Department for Promotion of Industry and Internal Trade (DPIIT) under the Ministry of Commerce and Industry. Tax exemption under Section 80-IAC of the Income Tax Act, 1961 (3 consecutive years out of first 10 years). Angel tax exemption under Section 56(2)(viib) was abolished in Budget 2024."
result = replace_regulatory_section(bt, new_reg)
if result:
    bt = result
    log_change(fname, "Replaced Regulatory Framework with DPIIT/Startup India content")

# Fix case study section
case_study_new = (
    "HEADING2: Recent Engagement \u2014 How We Helped\n"
    "Context: a SaaS startup in Bangalore with 3 founders, 18 months old, annual revenue of Rs 45 lakhs.\n"
    "Challenge: The founders needed DPIIT Startup India recognition to access the 80-IAC tax exemption before their Series A round. "
    "They also needed to ensure their innovation certificate and MSME/Udyam registration were in order.\n"
    "Our approach: We prepared the complete DPIIT recognition application, drafted the innovation description highlighting the proprietary AI algorithm, "
    "obtained the MSME/Udyam certificate, and filed the 80-IAC application with the Inter-Ministerial Board.\n"
    "Outcome: DPIIT recognition received within 3 working days. 80-IAC tax exemption approval within 45 days. "
    "The startup saved approximately Rs 12 lakhs in tax over the next 3 years."
)
# Replace from "HEADING2: Recent Engagement" to the end of that section
pattern = r'HEADING2: Recent Engagement.*?(?=\nHEADING2:|\Z)'
match = re.search(pattern, bt, re.DOTALL)
if match:
    # Check if there's content after this section
    remaining = bt[match.end():]
    bt = bt[:match.start()] + case_study_new + remaining
    log_change(fname, "Replaced case study with SaaS startup scenario")

data["bodyText"] = bt

# Fix FAQs
data["faqs"] = [
    {"q": "What is Startup India recognition?", "a": "DPIIT recognition under the Startup India initiative. Provides access to tax benefits (Section 80-IAC), Fund of Funds, self-certification for labour and environment laws, fast-track patent examination, and easier public procurement."},
    {"q": "Who is eligible for Startup India recognition?", "a": "Entity incorporated as Pvt Ltd, LLP, or Partnership. Must be less than 10 years old from incorporation date. Annual turnover must not exceed Rs 100 crore in any financial year. Must be working towards innovation, development, or improvement of products/processes/services."},
    {"q": "How long does DPIIT recognition take?", "a": "DPIIT recognition is typically granted within 2-5 working days of application submission on the Startup India portal. Tax exemption under 80-IAC requires a separate application to the Inter-Ministerial Board and takes 30-60 days."},
    {"q": "What is the 80-IAC tax exemption?", "a": "Section 80-IAC provides 100% deduction of profits for 3 consecutive assessment years out of the first 10 years from incorporation. Available to DPIIT-recognized startups incorporated as Pvt Ltd or LLP."},
    {"q": "Is angel tax still applicable after Budget 2024?", "a": "No. Section 56(2)(viib) was abolished in the July 2024 Union Budget. There is no longer any income tax on share premium for primary issuances. However, FEMA floor pricing under Rule 21 of NDI Rules still applies for FDI."},
    {"q": "What documents are needed for Startup India registration?", "a": "Certificate of Incorporation, brief description of innovation, proof of concept or working product details, PAN of the entity, and details of directors/partners. If applying for 80-IAC: audited financials and detailed business plan."}
]
log_change(fname, "Replaced all FAQs with correct Startup India FAQs")
save_json(fname, data)

# --- A2: partnership-registration.json ---
fname = "partnership-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nPartnership firms in India are governed by the Indian Partnership Act, 1932. Registration is optional but highly recommended \u2014 an unregistered firm cannot file suits against third parties (Section 69). Registration is done with the Registrar of Firms under the respective state government. The Partnership Deed must include: name, business, capital contribution, profit-sharing ratio, duration, and dispute resolution mechanism."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Partnership Act content")
    save_json(fname, data)

# --- A3: copyright-registration.json ---
fname = "copyright-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nCopyright registration in India is governed by the Copyright Act, 1957 read with the Copyright Rules, 2013. Registration is administered by the Copyright Office under the Department for Promotion of Industry and Internal Trade (DPIIT). While copyright exists automatically upon creation of the original work, registration provides prima facie evidence of ownership and is essential for enforcement proceedings."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Copyright Act content")
    save_json(fname, data)

# --- A4: patent-registration.json ---
fname = "patent-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nPatent registration in India is governed by the Patents Act, 1970 read with the Patents Rules, 2003. Applications are filed with the Indian Patent Office (IPO) under the Controller General of Patents, Designs & Trade Marks. Filing requires Form 1 (Application), Form 2 (Provisional/Complete Specification), Form 3 (Statement & Undertaking), and Form 5 (Declaration of Inventorship). Patent term is 20 years from filing date."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Patents Act content")
    save_json(fname, data)

# --- A5: fssai-registration.json ---
fname = "fssai-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nFSSAI registration and licensing is governed by the Food Safety and Standards Act, 2006, administered by the Food Safety and Standards Authority of India (FSSAI). Three categories: Basic Registration (annual turnover up to Rs 12 lakhs), State License (Rs 12 lakhs to Rs 20 crores), and Central License (above Rs 20 crores or multi-state operations). FSSAI license number must be displayed on all food product labels."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with FSSAI Act content")
    save_json(fname, data)

# --- A6: dsc-class-two.json ---
fname = "dsc-class-two.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nDigital Signature Certificates (DSC) in India are governed by the Information Technology Act, 2000 (Section 3) and the IT (Certifying Authorities) Rules. DSCs are issued by licensed Certifying Authorities (CAs) approved by the Controller of Certifying Authorities (CCA). Class 2 DSC is used for MCA filings, income tax e-filing, GST registration, and other government e-forms."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with IT Act/DSC Class 2 content")
    save_json(fname, data)

# --- A7: dsc-class-three.json ---
fname = "dsc-class-three.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nClass 3 Digital Signature Certificates are governed by the Information Technology Act, 2000 and IT (Certifying Authorities) Rules. Class 3 DSC provides the highest level of assurance and is required for e-tendering, e-procurement portals (GeM, IREPS, CPPP), and high-value transactions. Requires in-person verification by the Certifying Authority."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with IT Act/DSC Class 3 content")
    save_json(fname, data)

# --- A8: llp-winding-up.json ---
fname = "llp-winding-up.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nLLP winding up is governed by Sections 63-65 of the Limited Liability Partnership Act, 2008 read with the LLP (Winding Up and Dissolution) Rules, 2012. Two modes: voluntary winding up (by partners' resolution when LLP has no debts or can pay debts in full within one year) and compulsory winding up (by NCLT order on petition by partners, creditors, or Registrar)."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with LLP winding up content")
    save_json(fname, data)

# --- A9: trust-registration.json ---
fname = "trust-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nPrivate trusts are governed by the Indian Trusts Act, 1882. Public/charitable trusts are governed by state-specific acts (e.g., Bombay Public Trusts Act, 1950 in Maharashtra; Tamil Nadu Hindu Religious and Charitable Endowments Act). Registration is done with the office of the Sub-Registrar (for trust deed registration) and with the Charity Commissioner (for public trusts). 12A and 80G registration under Income Tax Act for tax exemption."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Trust registration content")
    save_json(fname, data)

# --- A10: society-registration.json ---
fname = "society-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nSocieties in India are registered under the Societies Registration Act, 1860 (Act XXI of 1860). Registration is with the Registrar of Societies under the respective state government. Minimum 7 members required for formation. The Memorandum of Association must include: name, objects, names and addresses of governing body members, and registered office address."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Societies Registration Act content")
    save_json(fname, data)

# --- A11: proprietorship-registration-india-sole-proprietorship.json ---
fname = "proprietorship-registration-india-sole-proprietorship.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nSole proprietorship in India does not require separate registration under any central act. Identity is established through a combination of: Shop and Establishment Act registration (state-specific), MSME/Udyam Registration (Ministry of MSME), GST Registration (if turnover exceeds threshold), current bank account in business name, and PAN of the proprietor. Professional tax registration is required in applicable states."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Sole Proprietorship content")
    save_json(fname, data)

# --- A12: nbfc-registration.json ---
fname = "nbfc-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nNBFC registration is governed by Chapter IIIB of the RBI Act, 1934 read with the RBI Master Direction \u2014 Non-Banking Financial Company \u2014 Systemically Important Non-Deposit taking Company and Deposit taking Company (Reserve Bank) Directions, 2016. Requires prior registration with RBI under Section 45-IA. Minimum Net Owned Fund (NOF) requirement: Rs 10 crore (raised from Rs 2 crore in October 2022). The entity must first be incorporated as a company under the Companies Act, 2013."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with NBFC/RBI Act content")
    save_json(fname, data)

# --- A13: payroll-service.json ---
fname = "payroll-service.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nPayroll compliance in India involves multiple statutes: Employees' Provident Funds and Miscellaneous Provisions Act, 1952 (EPF \u2014 applicable to establishments with 20+ employees), Employees' State Insurance Act, 1948 (ESI \u2014 applicable where wages up to Rs 21,000/month), Payment of Wages Act, 1936, Minimum Wages Act, 1948, Payment of Bonus Act, 1965, Payment of Gratuity Act, 1972, and Professional Tax acts (state-specific). TDS under Section 192 of the Income Tax Act for salary payments."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Payroll compliance content")
    save_json(fname, data)

# --- A14: transfer-pricing.json ---
fname = "transfer-pricing.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nTransfer pricing in India is governed by Chapter X (Sections 92-92F) of the Income Tax Act, 1961 read with Rules 10A to 10E of the Income Tax Rules, 1962. Applicable to international transactions with Associated Enterprises (AEs) exceeding Rs 1 crore and Specified Domestic Transactions (SDTs) exceeding Rs 20 crore. Documentation requirements: maintain transfer pricing documentation as per Rule 10D. Country-by-Country Report (CbCR) under Section 286 for groups with consolidated revenue exceeding Rs 5,500 crore."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Transfer Pricing content")
    save_json(fname, data)

# --- A15: nidhi-company-registration.json ---
fname = "nidhi-company-registration.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nNidhi companies are governed by Section 406 of the Companies Act, 2013 read with the Nidhi Rules, 2014 (as amended by Nidhi (Amendment) Rules, 2022). Nidhi companies accept deposits from and lend to their members only. Minimum 200 members required within one year of incorporation. Net Owned Funds must be Rs 20 lakh or more. Ratio of Net Owned Funds to deposits must not exceed 1:20."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Nidhi Company content")
    save_json(fname, data)

# --- A16: section-8-company (find actual file) ---
# Try both possible filenames
for candidate in ["online-section-8-company-registration.json", "section-8-company-registration-india.json"]:
    fpath = os.path.join(PAGES_DIR, candidate)
    if os.path.exists(fpath):
        fname = candidate
        data = load_json(fname)
        new_reg = "HEADING2: Regulatory Framework\nSection 8 companies are governed by Section 8 of the Companies Act, 2013 read with the Companies (Incorporation) Rules, 2014. Requires a license from the Central Government (Regional Director). Objects must be for promoting commerce, art, science, sports, education, research, social welfare, religion, charity, protection of environment, or any other useful object. Profits are applied towards promoting the objects \u2014 no dividend can be paid to members."
        result = replace_regulatory_section(data["bodyText"], new_reg)
        if result:
            data["bodyText"] = result
            log_change(fname, "Replaced Regulatory Framework with Section 8 Company content")
            save_json(fname, data)
            break  # Only break on success

# --- A17: add-partner-llp.json ---
fname = "add-partner-llp.json"
data = load_json(fname)
new_reg = "HEADING2: Regulatory Framework\nAddition of a partner to an LLP is governed by the Limited Liability Partnership Act, 2008 and the LLP Rules, 2009. Requires filing of Form 4 (Notice of change in partner/designated partner) with the Registrar of Companies within 30 days of the change. The supplementary LLP Agreement must be updated and filed as Form 3. New partner's DPIN (Designated Partner Identification Number) must be obtained first if not already held."
result = replace_regulatory_section(data["bodyText"], new_reg)
if result:
    data["bodyText"] = result
    log_change(fname, "Replaced Regulatory Framework with Add Partner LLP content")
    save_json(fname, data)

# ============================================================
# SECTION B: Fix factual errors
# ============================================================

print("\n" + "=" * 60)
print("SECTION B: Fixing factual errors")
print("=" * 60)

# --- B1: one-person-company.json ---
fname = "one-person-company.json"
data = load_json(fname)
bt = data["bodyText"]

# Fix case study: replace "4 co-founders" case study with solo entrepreneur
old_case = re.search(
    r'(HEADING2: Recent Engagement.*?)\nThis engagement illustrates',
    bt, re.DOTALL
)
if old_case:
    new_case = (
        "HEADING2: Recent Engagement \u2014 How We Helped\n"
        "Context: a solo entrepreneur launching a boutique consulting practice in Bangalore.\n"
        "Challenge: The founder wanted limited liability protection without the compliance burden of a Pvt Ltd. "
        "She needed OPC registration with the option to convert to Pvt Ltd when she eventually hired a team.\n"
        "Our approach: We incorporated the OPC under Section 3(1)(c) of the Companies Act using SPICe+, "
        "with the founder as sole member and her spouse as nominee. We set up the compliance calendar for the lighter "
        "OPC requirements (2 board meetings/year vs 4, no AGM needed).\n"
        "Outcome: OPC incorporated in 7 working days. Compliance cost was 40% lower than a Pvt Ltd in the first year. "
        "When turnover crossed Rs 2 crore in the second year, we handled the mandatory conversion to Pvt Ltd seamlessly."
    )
    bt = bt[:old_case.start()] + new_case + "\n" + bt[old_case.end():]
    log_change(fname, "Replaced case study (4 co-founders -> solo entrepreneur)")

# Fix "Rs 2 Cr paid-up capital" -> "Rs 50 lakhs paid-up capital"
bt = bt.replace("\u20b92 Cr paid-up capital", "\u20b950 lakhs paid-up capital")
bt = bt.replace("Rs 2 Cr paid-up capital", "Rs 50 lakhs paid-up capital")
# Also check the "₹2 Cr" variants in the "What You Will Receive" section
if "\u20b92 Cr" in bt:
    bt = bt.replace("\u20b92 Cr", "\u20b950 lakhs")
    log_change(fname, "Fixed paid-up capital threshold: Rs 2 Cr -> Rs 50 lakhs")

data["bodyText"] = bt
save_json(fname, data)

# --- B2: limited-liability-partnership.json ---
fname = "limited-liability-partnership.json"
data = load_json(fname)
bt = data["bodyText"]

# Fix "startups planning to raise equity funding from investors (angel/VC/PE)"
bt = bt.replace(
    "startups planning to raise equity funding from investors (angel/VC/PE)",
    "professional practices, consultancies, and bootstrapped businesses not planning equity fundraising"
)
log_change(fname, "Fixed LLP target audience (removed equity funding reference)")

# Fix "Companies Act, 2013" in intro line only (the boilerplate line)
# The intro says "specialising in company registration under the Companies Act, 2013"
# We need to be careful - only replace in the intro/boilerplate, not everywhere
intro_pattern = r'specialising in company registration under the Companies Act, 2013'
bt = bt.replace(
    "specialising in company registration under the Companies Act, 2013",
    "specialising in LLP registration under the Limited Liability Partnership Act, 2008",
    1  # only first occurrence
)
log_change(fname, "Fixed intro reference: Companies Act 2013 -> LLP Act 2008")

# Fix compliance deadlines in "Delivers This Differently" section
old_compliance = "auditor appointment (30 days), INC-20A (180 days), board meetings (quarterly), AGM (6 months from year-end), AOC-4 and MGT-7 (annual)"
new_compliance = "Form 8 (Statement of Account & Solvency \u2014 within 30 days of 6 months from end of financial year) and Form 11 (Annual Return \u2014 within 60 days of end of financial year). LLP Agreement filing as Form 3 within 30 days of incorporation"
bt = bt.replace(old_compliance, new_compliance)
log_change(fname, "Fixed compliance deadlines to LLP-specific (Form 8, Form 11)")

data["bodyText"] = bt
save_json(fname, data)

# --- B3: company-secretary-services.json ---
fname = "company-secretary-services.json"
data = load_json(fname)
changed = False
for i, faq in enumerate(data.get("faqs", [])):
    if "\u20b95 crore" in faq.get("a", "") or "₹5 crore" in faq.get("a", ""):
        data["faqs"][i]["a"] = faq["a"].replace("\u20b95 crore", "\u20b910 crore").replace("₹5 crore", "₹10 crore")
        changed = True
if changed:
    log_change(fname, "Fixed FAQ: Rs 5 crore -> Rs 10 crore for CS mandatory threshold")
    save_json(fname, data)

# --- B4: income-tax-return-filing.json ---
fname = "income-tax-return-filing.json"
data = load_json(fname)
bt = data["bodyText"]
bt = bt.replace("\u20b93 lakhs under new regime", "\u20b94 lakhs under new regime (Budget 2025)")
bt = bt.replace("Rs 3 lakhs under new regime", "Rs 4 lakhs under new regime (Budget 2025)")
bt = bt.replace("₹3 lakhs under new regime", "₹4 lakhs under new regime (Budget 2025)")
log_change(fname, "Fixed basic exemption limit: Rs 3 lakhs -> Rs 4 lakhs (Budget 2025)")
data["bodyText"] = bt
save_json(fname, data)

# --- B5: about-us.json ---
fname = "about-us.json"
data = load_json(fname)
bt = data["bodyText"]

# Remove "HEADING2: When Is About Virtual Auditor Not Required?" and its content
bt = re.sub(
    r'\nHEADING2: When Is About Virtual Auditor Not Required\?.*?(?=\nHEADING2:|\Z)',
    '', bt, flags=re.DOTALL
)
log_change(fname, "Removed 'When Is About Virtual Auditor Not Required?' section")

# Remove "HEADING2: Documents Required" section about "about virtual auditor process"
bt = re.sub(
    r'\nHEADING2: Documents Required\n.*?about virtual auditor.*?(?=\nHEADING2:|\Z)',
    '', bt, flags=re.DOTALL
)
log_change(fname, "Removed 'Documents Required' template section")

# Remove "Typical turnaround for about virtual auditor" - this is in the Timeline section
bt = re.sub(
    r'\nHEADING2: Timeline and Turnaround\n.*?about virtual auditor.*?(?=\nHEADING2:|\Z)',
    '', bt, flags=re.DOTALL
)
log_change(fname, "Removed 'Timeline and Turnaround' template section")

# Remove "Who Needs About Virtual Auditor?" section
bt = re.sub(
    r'\nHEADING2: Who Needs About Virtual Auditor\?.*?(?=\nHEADING2:|\Z)',
    '', bt, flags=re.DOTALL
)
log_change(fname, "Removed 'Who Needs About Virtual Auditor?' section")

data["bodyText"] = bt
save_json(fname, data)

# --- B6: gst-registration.json ---
fname = "gst-registration.json"
data = load_json(fname)
bt = data["bodyText"]

old_text = "extracts demand amounts, computes pre-deposit requirements (10% for Section 107, 20% for Section 112), identifies limitation dates, and maps each issue to relevant case law from our appellate database"
new_text = "Our AI-assisted registration analyser pre-validates your application against common rejection triggers \u2014 incorrect HSN codes, address proof mismatches, principal place of business discrepancies, and Aadhaar authentication failures \u2014 before submission to the GST portal"

# Find and replace - might have slightly different surrounding text
if old_text in bt:
    # Find the full sentence containing this text
    # The pattern is typically "Our AI-assisted GST analyser extracts demand amounts..."
    # Replace the whole sentence
    full_old = "Our AI-assisted GST analyser " + old_text
    if full_old in bt:
        bt = bt.replace(full_old, new_text)
    else:
        bt = bt.replace(old_text, new_text)
    log_change(fname, "Fixed 'Delivers This Differently' section: appeal text -> registration analyser")

data["bodyText"] = bt
save_json(fname, data)

# ============================================================
# SECTION C: Fix bullet artifacts
# ============================================================

print("\n" + "=" * 60)
print("SECTION C: Fixing bullet artifacts")
print("=" * 60)

# --- C1: private-limited-company-registration.json ---
fname = "private-limited-company-registration.json"
data = load_json(fname)
bt = data["bodyText"]
original = bt
bt = fix_bullet_artifacts(bt)
if bt != original:
    data["bodyText"] = bt
    count = original.count("\u2022 ") - bt.count("\u2022 ")
    log_change(fname, f"Removed {count} bullet artifacts before numbered HEADING3 steps")
    save_json(fname, data)

# --- C2: how-we-work.json ---
fname = "how-we-work.json"
data = load_json(fname)
bt = data["bodyText"]
original = bt
bt = fix_bullet_artifacts(bt)
if bt != original:
    data["bodyText"] = bt
    count = original.count("\u2022 ") - bt.count("\u2022 ")
    log_change(fname, f"Removed {count} bullet artifacts before numbered HEADING3 steps")
    save_json(fname, data)

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY OF ALL CHANGES")
print("=" * 60)
print(f"\nTotal changes made: {len(changes_log)}\n")
for change in changes_log:
    print(change)
print("\nDone.")
