#!/usr/bin/env python3
"""
Virtual Auditor — Location Page Generator
Generates state-wise and city-wise pages for all 11 services.
Output: HTML files, content/pages/*.json, content/schemas/*.json
"""

import json, os, re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.now().strftime("%Y-%m-%d")
DOMAIN = "https://virtualauditor.in"

# ═══════════════════════════════════════════════════════════════
# DATA: SERVICES
# ═══════════════════════════════════════════════════════════════

SERVICES = [
    {
        "slug": "private-limited-company-registration",
        "name": "Private Limited Company Registration",
        "short": "Pvt Ltd Registration",
        "parent": "private-limited-company-registration",
        "desc": "Private limited company registration under Companies Act 2013. SPICe+ filing, DSC, DIN, MOA/AOA, PAN/TAN.",
        "price": "From ₹8,999",
        "keywords": ["company registration", "pvt ltd registration", "SPICe+", "MCA filing", "incorporate company"],
        "scope": ["SPICe+ Form Filing (INC-32)", "DSC & DIN for Directors", "Name Reservation (RUN/SPICe+ Part A)", "MOA & AOA Drafting", "PAN/TAN Allotment", "Post-Incorporation Compliance Setup"],
        "steps": [("Obtain DSC", "Digital Signature Certificate for all directors"), ("Reserve Company Name", "Via SPICe+ Part A or RUN form"), ("File SPICe+ Part B", "Integrated incorporation form INC-32"), ("Receive Certificate", "Certificate of Incorporation from ROC"), ("Post-Registration", "Auditor appointment, INC-20A, bank account")],
        "faqs_generic": [
            ("How much does Pvt Ltd registration cost?", "All-inclusive from ₹8,999 covering government fees, DSC, DIN, SPICe+ filing, MOA/AOA, PAN/TAN. No hidden charges. 5-15 working days."),
            ("What documents are needed for company registration?", "PAN & Aadhaar of directors, address proof, passport-size photos, registered office address proof (utility bill + NOC/rent agreement), and proposed company name."),
            ("How long does company registration take?", "5-15 working days from document submission. Same-day DSC issuance, 2-3 days for name approval, 3-7 days for incorporation certificate."),
        ],
    },
    {
        "slug": "gst-services",
        "name": "GST Registration, Filing & Appeal Services",
        "short": "GST Services",
        "parent": "gst-registration",
        "desc": "GST registration, monthly/quarterly return filing, GST audit, show cause notice reply, and GST appeal representation.",
        "price": "From ₹2,999",
        "keywords": ["GST registration", "GST filing", "GST return", "GST appeal", "GST notice reply"],
        "scope": ["GST Registration (New/Amendment)", "Monthly GSTR-1 & GSTR-3B Filing", "Quarterly GSTR-4 (Composition)", "Annual GSTR-9/9C", "GST Audit", "Show Cause Notice Reply (DRC-01)", "GST Appeal (Section 107)"],
        "steps": [("GST Registration", "Apply via GST portal with PAN, Aadhaar, address proof"), ("Return Filing Setup", "Configure filing frequency and HSN/SAC codes"), ("Monthly Compliance", "GSTR-1 by 11th, GSTR-3B by 20th of following month"), ("Annual Return", "GSTR-9/9C by 31st December"), ("Appeal/Notice", "Reply to SCN or file appeal within statutory deadlines")],
        "faqs_generic": [
            ("When is GST registration mandatory?", "When turnover exceeds ₹40 lakhs (goods) or ₹20 lakhs (services). Also mandatory for e-commerce sellers, inter-state suppliers, and casual taxable persons."),
            ("What is the penalty for late GST filing?", "₹50/day (₹25 CGST + ₹25 SGST) for nil returns, ₹100/day for regular returns, subject to maximum of ₹5,000 per return."),
            ("Can you help with GST show cause notices?", "Yes. We handle DRC-01 replies, Section 73/74 proceedings, and Section 107 appeals. AI-assisted order analysis within 24 hours."),
        ],
    },
    {
        "slug": "income-tax-filing-services",
        "name": "Income Tax Filing & Appeal Services",
        "short": "Income Tax Services",
        "parent": "income-tax-appeal",
        "desc": "Income tax return filing (ITR-1 to ITR-7), tax planning, notice replies, CIT(A) and ITAT appeal representation.",
        "price": "From ₹1,999",
        "keywords": ["income tax filing", "ITR filing", "tax appeal", "income tax notice", "CIT(A) appeal"],
        "scope": ["ITR Filing (ITR-1 to ITR-7)", "Tax Planning & Advisory", "Advance Tax Computation", "Section 142(1)/143(2) Notice Reply", "Section 148 Reassessment Defence", "CIT(A) Appeal Filing", "ITAT Appeal Representation"],
        "steps": [("Document Collection", "Form 16, bank statements, investment proofs, capital gains"), ("Tax Computation", "Calculate total income, deductions, and tax liability"), ("ITR Preparation", "Select correct ITR form and prepare return"), ("E-Filing", "File on income tax portal with digital signature"), ("Verification", "E-verify via Aadhaar OTP, net banking, or physical ITR-V")],
        "faqs_generic": [
            ("Which ITR form should I file?", "ITR-1 for salaried (up to ₹50L), ITR-2 for capital gains/multiple properties, ITR-3 for business income, ITR-4 for presumptive taxation."),
            ("What is the due date for ITR filing?", "31st July for individuals (non-audit), 31st October for audit cases, 30th November for transfer pricing."),
            ("Can you represent me in income tax appeals?", "Yes. We handle CIT(A) appeals, ITAT appeals, Section 264 revisions, and settlement commission applications."),
        ],
    },
    {
        "slug": "auditors-audit-services",
        "name": "Statutory Audit & Assurance Services",
        "short": "Audit Services",
        "parent": "statutory-audit-services-india",
        "desc": "Statutory audit, tax audit (44AB), internal audit, GST audit, concurrent audit, and stock audit by FCA-led practice.",
        "price": "From ₹25,000",
        "keywords": ["statutory audit", "tax audit", "internal audit", "44AB audit", "company audit"],
        "scope": ["Statutory Audit (Companies Act)", "Tax Audit (Section 44AB)", "Internal Audit", "GST Audit", "Concurrent Audit", "Stock Audit", "Revenue Audit", "Forensic Audit Support"],
        "steps": [("Engagement Letter", "Define audit scope, timeline, and fees"), ("Planning", "Understand business, assess risks, design audit procedures"), ("Fieldwork", "Test controls, verify transactions, examine records"), ("Reporting", "Draft audit report with observations and qualifications"), ("Follow-up", "Management letter with improvement recommendations")],
        "faqs_generic": [
            ("When is statutory audit required?", "All companies registered under Companies Act must get audited annually. LLPs with turnover >₹40L or capital >₹25L also require audit."),
            ("What is Section 44AB tax audit?", "Tax audit is required when business turnover exceeds ₹1 crore (₹10 crore if cash transactions <5%) or professional receipts exceed ₹50 lakhs."),
            ("How long does an audit take?", "Typically 2-4 weeks depending on company size. We provide a detailed timeline at engagement stage."),
        ],
    },
    {
        "slug": "business-valuation-services",
        "name": "Business Valuation Services",
        "short": "Business Valuation",
        "parent": "business-valuation",
        "desc": "IBBI-compliant business valuation using DCF, market approach, NAV. For M&A, fundraising, tax compliance, FEMA, IBC.",
        "price": "From ₹50,000",
        "keywords": ["business valuation", "company valuation", "IBBI valuation", "DCF valuation", "share valuation"],
        "scope": ["DCF Valuation (Discounted Cash Flow)", "Comparable Company Analysis", "NAV (Net Asset Value) Method", "FEMA/FDI Valuation (Rule 11UA)", "ESOP Valuation (Ind AS 102)", "409A Valuation", "IBC Valuation (Reg. 35)", "Fairness Opinion"],
        "steps": [("Scope Definition", "Identify valuation purpose, standard of value, premise"), ("Data Collection", "Financial statements, projections, market data"), ("Analysis", "Apply 3-5 valuation methods with Monte Carlo simulation"), ("Draft Report", "Prepare IBBI-compliant valuation report"), ("Final Report", "Incorporate feedback and issue signed report")],
        "faqs_generic": [
            ("What is an IBBI Registered Valuer?", "A professional registered with IBBI under the Registered Valuers Regulations, 2017. Required for valuations under Companies Act and IBC."),
            ("How many valuation methods do you use?", "We use up to 18 methods with 10,000 Monte Carlo simulations per engagement for statistically defensible results."),
            ("How long does a valuation report take?", "Standard reports in 7-10 working days. Complex multi-framework valuations may take 15-20 days."),
        ],
    },
    {
        "slug": "fema-compliance-fdi-advisory",
        "name": "FEMA Compliance & FDI Advisory",
        "short": "FEMA/FDI Advisory",
        "parent": "fema-valuation",
        "desc": "FEMA compliance, FDI reporting (FC-GPR/FC-TRS), ECB compliance, ODI advisory, FEMA compounding, 15CA/15CB certification.",
        "price": "From ₹15,000",
        "keywords": ["FEMA compliance", "FDI advisory", "FC-GPR", "FC-TRS", "foreign investment India"],
        "scope": ["FDI Reporting (FC-GPR, FC-TRS, LLP-I/II)", "FEMA Valuation (Rule 11UA Floor Price)", "ECB Compliance & Reporting", "ODI Advisory", "FEMA Compounding Applications", "15CA/15CB Certification", "Cross-Regulatory Conflict Detection"],
        "steps": [("Regulatory Assessment", "Identify applicable FEMA provisions and sector caps"), ("Valuation", "Determine fair value per Rule 11UA / DCF"), ("Documentation", "Prepare compliance documents and filings"), ("RBI Reporting", "File FC-GPR/FC-TRS within statutory timelines"), ("Ongoing Compliance", "Annual compliance and APR/FLA return filing")],
        "faqs_generic": [
            ("What is FC-GPR filing?", "FC-GPR (Foreign Currency - Gross Provisional Return) is filed within 30 days of share allotment to a foreign investor under FDI."),
            ("When is FEMA compounding needed?", "When there's been a contravention of FEMA provisions — late filings, incorrect pricing, or procedural non-compliance."),
            ("Do you handle cross-border transactions?", "Yes. We manage the intersection of FEMA, Income Tax, and Companies Act for cross-border investments and remittances."),
        ],
    },
    {
        "slug": "company-secretary-services",
        "name": "Company Secretary Services",
        "short": "CS Services",
        "parent": "company-secretary-services",
        "desc": "Company secretarial services — annual ROC filings, board resolutions, share transfers, director appointments, compliance calendar.",
        "price": "From ₹5,000",
        "keywords": ["company secretary", "ROC filing", "annual compliance", "board resolution", "corporate governance"],
        "scope": ["Annual ROC Filing (AOC-4, MGT-7)", "Board Resolution Drafting", "Director Appointment/Resignation (DIR-12)", "Share Transfer & Transmission", "Increase in Authorised Capital", "Registered Office Change", "Name Change (INC-24)", "Winding Up & Strike-Off"],
        "steps": [("Compliance Calendar", "Set up annual compliance calendar with all due dates"), ("Board Meetings", "Draft notices, agendas, minutes, and resolutions"), ("ROC Filings", "Prepare and file AOC-4, MGT-7, and event-based forms"), ("Statutory Registers", "Maintain all statutory registers as per Companies Act"), ("Annual Return", "Prepare and file annual return with ROC")],
        "faqs_generic": [
            ("What is included in annual ROC filing?", "AOC-4 (financial statements), MGT-7 (annual return), ADT-1 (auditor appointment). Due within 30-60 days of AGM."),
            ("Do you handle director changes?", "Yes. DIR-12 for appointment/resignation, DIR-3 KYC annual update, DIN deactivation if needed."),
            ("What happens if ROC filings are delayed?", "Additional fees of ₹100/day per form. Prolonged default can lead to company strike-off and director disqualification."),
        ],
    },
    {
        "slug": "transfer-pricing-services",
        "name": "Transfer Pricing Services",
        "short": "Transfer Pricing",
        "parent": "transfer-pricing",
        "desc": "Transfer pricing study, documentation, benchmarking, TP audit defence, APA advisory, and ITAT appeal representation.",
        "price": "From ₹75,000",
        "keywords": ["transfer pricing", "TP study", "TP documentation", "arm's length price", "APA"],
        "scope": ["TP Study & Documentation (Form 3CEB)", "Benchmarking Analysis", "TP Audit Defence", "APA (Advance Pricing Agreement) Advisory", "Secondary Adjustment Compliance", "Safe Harbour Rules Advisory", "ITAT Appeal Representation"],
        "steps": [("FAR Analysis", "Functions, Assets, and Risks analysis of related party transactions"), ("Benchmarking", "Identify comparable companies and compute arm's length range"), ("Documentation", "Prepare TP study report and Form 3CEB"), ("Filing", "File Form 3CEB with income tax return"), ("Audit Defence", "Represent before TPO/DRP if adjustment proposed")],
        "faqs_generic": [
            ("When is transfer pricing documentation required?", "When aggregate value of international transactions exceeds ₹1 crore, or specified domestic transactions exceed ₹20 crore."),
            ("What is Form 3CEB?", "Chartered accountant's report certifying arm's length nature of international and domestic related party transactions. Due by 31st October."),
            ("Can you defend TP adjustments?", "Yes. We handle TPO proceedings, DRP references, and ITAT appeals for transfer pricing disputes."),
        ],
    },
    {
        "slug": "forensic-accounting-fraud-investigation",
        "name": "Forensic Accounting & Fraud Investigation",
        "short": "Forensic Accounting",
        "parent": "forensic-accounting",
        "desc": "CFE-led forensic accounting, fraud investigation, due diligence, whistleblower investigation, and expert witness testimony.",
        "price": "From ₹1,00,000",
        "keywords": ["forensic accounting", "fraud investigation", "CFE", "due diligence", "financial fraud"],
        "scope": ["Financial Fraud Investigation", "Forensic Due Diligence (M&A)", "Whistleblower Complaint Investigation", "Employee Embezzlement Investigation", "Vendor Fraud Investigation", "Expert Witness Testimony", "Digital Forensic Accounting", "Fraud Risk Assessment"],
        "steps": [("Engagement", "Define scope, timeline, and reporting requirements"), ("Preservation", "Secure and preserve financial records and digital evidence"), ("Investigation", "Apply CFE techniques — data analytics, interviews, document examination"), ("Reporting", "Prepare forensic report with findings and evidence chain"), ("Testimony", "Expert witness support if matter goes to litigation")],
        "faqs_generic": [
            ("What is forensic accounting?", "Application of CFE investigation techniques to detect financial fraud, embezzlement, and misrepresentation. Combines accounting, auditing, and investigative skills."),
            ("Who needs forensic accounting?", "PE/VC investors for due diligence, companies investigating employee fraud, boards handling whistleblower complaints, and litigants requiring expert witness."),
            ("What credentials does your forensic team have?", "Led by CA V. Viswanathan who holds CFE (Certified Fraud Examiner) from ACFE USA, in addition to FCA and ACS."),
        ],
    },
    {
        "slug": "startup-due-diligence",
        "name": "Startup Due Diligence Services",
        "short": "Startup Due Diligence",
        "parent": "startup-due-diligence-chartered-accountant",
        "desc": "Pre-investment due diligence for startups — financial, tax, legal, FEMA compliance, cap table analysis, and valuation.",
        "price": "From ₹50,000",
        "keywords": ["startup due diligence", "investor due diligence", "pre-funding audit", "cap table", "financial due diligence"],
        "scope": ["Financial Due Diligence", "Tax Due Diligence", "FEMA/FDI Compliance Check", "Cap Table Analysis", "Related Party Transaction Review", "Contingent Liability Assessment", "Working Capital Analysis", "Valuation Cross-Check"],
        "steps": [("Scope Agreement", "Define due diligence scope with investor/startup"), ("Data Room Setup", "Collect financials, contracts, compliance records"), ("Analysis", "Review financials, tax compliance, FEMA status, cap table"), ("Red Flag Report", "Identify deal-breakers and risk factors"), ("Final Report", "Comprehensive due diligence report with recommendations")],
        "faqs_generic": [
            ("What does startup due diligence cover?", "Financial statements review, tax compliance check, FEMA/FDI status, cap table accuracy, related party transactions, and contingent liabilities."),
            ("How long does due diligence take?", "Standard due diligence: 2-3 weeks. Expedited: 7-10 days. Complex multi-entity: 4-6 weeks."),
            ("Do you work with both investors and startups?", "Yes. We represent both sides — investors seeking independent assessment, and startups preparing for fundraise."),
        ],
    },
    {
        "slug": "company-registration-consultant",
        "name": "Company Registration Consultant",
        "short": "Company Registration",
        "parent": "private-limited-company-registration",
        "desc": "Expert company registration consultant — Pvt Ltd, LLP, OPC, Section 8, Nidhi Company. End-to-end MCA filing support.",
        "price": "From ₹5,999",
        "keywords": ["company registration consultant", "business registration", "LLP registration", "OPC registration", "startup registration"],
        "scope": ["Private Limited Company Registration", "LLP Registration", "One Person Company (OPC)", "Section 8 Company", "Partnership Firm Registration", "Sole Proprietorship", "Nidhi Company Registration", "Indian Subsidiary Registration"],
        "steps": [("Consultation", "Understand business plan and recommend entity structure"), ("Documentation", "Collect KYC documents and draft incorporation papers"), ("Filing", "File SPICe+/FiLLiP with MCA"), ("Incorporation", "Receive Certificate of Incorporation"), ("Post-Registration", "PAN, TAN, bank account, GST registration setup")],
        "faqs_generic": [
            ("Which entity type is best for my business?", "Pvt Ltd for funding, LLP for professionals, OPC for solo entrepreneurs, Section 8 for non-profit. We advise based on your specific goals."),
            ("What is the cheapest company to register?", "Sole proprietorship (₹0 registration fee) or LLP (from ₹5,999). Pvt Ltd from ₹8,999 all-inclusive."),
            ("Can NRIs register a company in India?", "Yes. NRIs can be directors and shareholders. At least one director must be an Indian resident (182+ days in India)."),
        ],
    },
]

# ═══════════════════════════════════════════════════════════════
# DATA: STATES & UTs
# ═══════════════════════════════════════════════════════════════

STATES = [
    {"name": "Andhra Pradesh", "slug": "andhra-pradesh", "capital": "Amaravati", "lat": 15.9129, "lon": 79.7400, "roc": "ROC Hyderabad", "pin": "522503", "stamp_duty": "5% on authorised capital", "prof_tax": "₹2,500/year"},
    {"name": "Arunachal Pradesh", "slug": "arunachal-pradesh", "capital": "Itanagar", "lat": 27.0844, "lon": 93.6053, "roc": "ROC Shillong", "pin": "791111", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Assam", "slug": "assam", "capital": "Dispur", "lat": 26.1445, "lon": 91.7362, "roc": "ROC Shillong", "pin": "781006", "stamp_duty": "As per state schedule", "prof_tax": "₹2,500/year"},
    {"name": "Bihar", "slug": "bihar", "capital": "Patna", "lat": 25.6093, "lon": 85.1376, "roc": "ROC Patna", "pin": "800001", "stamp_duty": "As per state schedule", "prof_tax": "₹2,500/year"},
    {"name": "Chhattisgarh", "slug": "chhattisgarh", "capital": "Raipur", "lat": 21.2514, "lon": 81.6296, "roc": "ROC Mumbai (Chhattisgarh)", "pin": "492001", "stamp_duty": "As per state schedule", "prof_tax": "₹2,500/year"},
    {"name": "Goa", "slug": "goa", "capital": "Panaji", "lat": 15.4909, "lon": 73.8278, "roc": "ROC Mumbai (Goa)", "pin": "403001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Gujarat", "slug": "gujarat", "capital": "Gandhinagar", "lat": 23.2156, "lon": 72.6369, "roc": "ROC Ahmedabad", "pin": "382010", "stamp_duty": "0.15% on authorised capital", "prof_tax": "₹2,500/year"},
    {"name": "Haryana", "slug": "haryana", "capital": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "roc": "ROC Delhi (Haryana)", "pin": "160001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Himachal Pradesh", "slug": "himachal-pradesh", "capital": "Shimla", "lat": 31.1048, "lon": 77.1734, "roc": "ROC Delhi (HP)", "pin": "171001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Jharkhand", "slug": "jharkhand", "capital": "Ranchi", "lat": 23.3441, "lon": 85.3096, "roc": "ROC Patna (Jharkhand)", "pin": "834001", "stamp_duty": "As per state schedule", "prof_tax": "₹2,500/year"},
    {"name": "Karnataka", "slug": "karnataka", "capital": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "roc": "ROC Bangalore", "pin": "560001", "stamp_duty": "0.5% on authorised capital (max ₹25L)", "prof_tax": "₹2,500/year"},
    {"name": "Kerala", "slug": "kerala", "capital": "Thiruvananthapuram", "lat": 8.5241, "lon": 76.9366, "roc": "ROC Ernakulam", "pin": "695001", "stamp_duty": "0.2% on authorised capital", "prof_tax": "₹2,500/year"},
    {"name": "Madhya Pradesh", "slug": "madhya-pradesh", "capital": "Bhopal", "lat": 23.2599, "lon": 77.4126, "roc": "ROC Gwalior", "pin": "462001", "stamp_duty": "As per state schedule", "prof_tax": "₹2,500/year"},
    {"name": "Maharashtra", "slug": "maharashtra", "capital": "Mumbai", "lat": 19.0760, "lon": 72.8777, "roc": "ROC Mumbai", "pin": "400001", "stamp_duty": "0.15-0.25% on authorised capital", "prof_tax": "₹2,500/year"},
    {"name": "Manipur", "slug": "manipur", "capital": "Imphal", "lat": 24.8170, "lon": 93.9368, "roc": "ROC Shillong", "pin": "795001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Meghalaya", "slug": "meghalaya", "capital": "Shillong", "lat": 25.5788, "lon": 91.8933, "roc": "ROC Shillong", "pin": "793001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Mizoram", "slug": "mizoram", "capital": "Aizawl", "lat": 23.7271, "lon": 92.7176, "roc": "ROC Shillong", "pin": "796001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Nagaland", "slug": "nagaland", "capital": "Kohima", "lat": 25.6751, "lon": 94.1086, "roc": "ROC Shillong", "pin": "797001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Odisha", "slug": "odisha", "capital": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245, "roc": "ROC Cuttack", "pin": "751001", "stamp_duty": "As per state schedule", "prof_tax": "₹2,500/year"},
    {"name": "Punjab", "slug": "punjab", "capital": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "roc": "ROC Chandigarh", "pin": "160001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Rajasthan", "slug": "rajasthan", "capital": "Jaipur", "lat": 26.9124, "lon": 75.7873, "roc": "ROC Jaipur", "pin": "302001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Sikkim", "slug": "sikkim", "capital": "Gangtok", "lat": 27.3389, "lon": 88.6065, "roc": "ROC Shillong", "pin": "737101", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Tamil Nadu", "slug": "tamil-nadu", "capital": "Chennai", "lat": 13.0827, "lon": 80.2707, "roc": "ROC Chennai", "pin": "600001", "stamp_duty": "0.15% on authorised capital (max ₹25L)", "prof_tax": "₹2,500/year"},
    {"name": "Telangana", "slug": "telangana", "capital": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "roc": "ROC Hyderabad", "pin": "500001", "stamp_duty": "0.15% on authorised capital", "prof_tax": "₹2,500/year"},
    {"name": "Tripura", "slug": "tripura", "capital": "Agartala", "lat": 23.8315, "lon": 91.2868, "roc": "ROC Shillong", "pin": "799001", "stamp_duty": "As per state schedule", "prof_tax": "₹2,500/year"},
    {"name": "Uttar Pradesh", "slug": "uttar-pradesh", "capital": "Lucknow", "lat": 26.8467, "lon": 80.9462, "roc": "ROC Kanpur", "pin": "226001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "Uttarakhand", "slug": "uttarakhand", "capital": "Dehradun", "lat": 30.3165, "lon": 78.0322, "roc": "ROC Delhi (Uttarakhand)", "pin": "248001", "stamp_duty": "As per state schedule", "prof_tax": "Not applicable"},
    {"name": "West Bengal", "slug": "west-bengal", "capital": "Kolkata", "lat": 22.5726, "lon": 88.3639, "roc": "ROC Kolkata", "pin": "700001", "stamp_duty": "0.15% on authorised capital", "prof_tax": "₹2,500/year"},
    # Union Territories
    {"name": "Delhi", "slug": "delhi", "capital": "New Delhi", "lat": 28.6139, "lon": 77.2090, "roc": "ROC Delhi", "pin": "110001", "stamp_duty": "As per Delhi schedule", "prof_tax": "Not applicable"},
    {"name": "Chandigarh", "slug": "chandigarh", "capital": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "roc": "ROC Chandigarh", "pin": "160001", "stamp_duty": "As per UT schedule", "prof_tax": "Not applicable"},
    {"name": "Puducherry", "slug": "puducherry", "capital": "Puducherry", "lat": 11.9416, "lon": 79.8083, "roc": "ROC Chennai", "pin": "605001", "stamp_duty": "As per UT schedule", "prof_tax": "₹2,500/year"},
    {"name": "Jammu and Kashmir", "slug": "jammu-and-kashmir", "capital": "Srinagar", "lat": 34.0837, "lon": 74.7973, "roc": "ROC Jammu", "pin": "190001", "stamp_duty": "As per UT schedule", "prof_tax": "Not applicable"},
    {"name": "Ladakh", "slug": "ladakh", "capital": "Leh", "lat": 34.1526, "lon": 77.5771, "roc": "ROC Jammu", "pin": "194101", "stamp_duty": "As per UT schedule", "prof_tax": "Not applicable"},
    {"name": "Andaman and Nicobar Islands", "slug": "andaman-and-nicobar", "capital": "Port Blair", "lat": 11.6234, "lon": 92.7265, "roc": "ROC Chennai", "pin": "744101", "stamp_duty": "As per UT schedule", "prof_tax": "Not applicable"},
    {"name": "Dadra Nagar Haveli and Daman Diu", "slug": "dadra-nagar-haveli-daman-diu", "capital": "Daman", "lat": 20.3974, "lon": 72.8328, "roc": "ROC Ahmedabad", "pin": "396210", "stamp_duty": "As per UT schedule", "prof_tax": "Not applicable"},
    {"name": "Lakshadweep", "slug": "lakshadweep", "capital": "Kavaratti", "lat": 10.5669, "lon": 72.6417, "roc": "ROC Ernakulam", "pin": "682555", "stamp_duty": "As per UT schedule", "prof_tax": "Not applicable"},
]

# ═══════════════════════════════════════════════════════════════
# DATA: CITIES (beyond existing Chennai/Bangalore/Mumbai areas)
# ═══════════════════════════════════════════════════════════════

CITIES = [
    {"name": "Hyderabad", "slug": "hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "pin": "500001", "roc": "ROC Hyderabad", "desc": "IT hub and pharmaceutical capital of India"},
    {"name": "New Delhi", "slug": "new-delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "pin": "110001", "roc": "ROC Delhi", "desc": "National capital and major business centre"},
    {"name": "Kolkata", "slug": "kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639, "pin": "700001", "roc": "ROC Kolkata", "desc": "Eastern India's commercial capital"},
    {"name": "Pune", "slug": "pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "pin": "411001", "roc": "ROC Pune", "desc": "IT and automotive hub of Maharashtra"},
    {"name": "Ahmedabad", "slug": "ahmedabad", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714, "pin": "380001", "roc": "ROC Ahmedabad", "desc": "Commercial capital of Gujarat"},
    {"name": "Jaipur", "slug": "jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "pin": "302001", "roc": "ROC Jaipur", "desc": "Capital of Rajasthan and emerging startup hub"},
    {"name": "Lucknow", "slug": "lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462, "pin": "226001", "roc": "ROC Kanpur", "desc": "Capital of India's most populous state"},
    {"name": "Chandigarh", "slug": "chandigarh-city", "state": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "pin": "160001", "roc": "ROC Chandigarh", "desc": "Planned city and joint capital of Punjab and Haryana"},
    {"name": "Kochi", "slug": "kochi", "state": "Kerala", "lat": 9.9312, "lon": 76.2673, "pin": "682001", "roc": "ROC Ernakulam", "desc": "Commercial capital of Kerala and IT corridor"},
    {"name": "Coimbatore", "slug": "coimbatore", "state": "Tamil Nadu", "lat": 11.0168, "lon": 76.9558, "pin": "641001", "roc": "ROC Coimbatore", "desc": "Manchester of South India — textile and engineering hub"},
    {"name": "Indore", "slug": "indore", "state": "Madhya Pradesh", "lat": 22.7196, "lon": 75.8577, "pin": "452001", "roc": "ROC Gwalior", "desc": "Commercial capital of Madhya Pradesh"},
    {"name": "Bhopal", "slug": "bhopal", "state": "Madhya Pradesh", "lat": 23.2599, "lon": 77.4126, "pin": "462001", "roc": "ROC Gwalior", "desc": "Capital of Madhya Pradesh"},
    {"name": "Nagpur", "slug": "nagpur", "state": "Maharashtra", "lat": 21.1458, "lon": 79.0882, "pin": "440001", "roc": "ROC Mumbai (Nagpur)", "desc": "Orange City — central India's largest business hub"},
    {"name": "Visakhapatnam", "slug": "visakhapatnam", "state": "Andhra Pradesh", "lat": 17.6868, "lon": 83.2185, "pin": "530001", "roc": "ROC Hyderabad", "desc": "Port city and IT hub of Andhra Pradesh"},
    {"name": "Patna", "slug": "patna", "state": "Bihar", "lat": 25.6093, "lon": 85.1376, "pin": "800001", "roc": "ROC Patna", "desc": "Capital of Bihar — growing business centre"},
    {"name": "Bhubaneswar", "slug": "bhubaneswar", "state": "Odisha", "lat": 20.2961, "lon": 85.8245, "pin": "751001", "roc": "ROC Cuttack", "desc": "Temple City and Odisha's IT corridor"},
    {"name": "Thiruvananthapuram", "slug": "thiruvananthapuram", "state": "Kerala", "lat": 8.5241, "lon": 76.9366, "pin": "695001", "roc": "ROC Ernakulam", "desc": "Capital of Kerala — IT and space technology hub"},
    {"name": "Guwahati", "slug": "guwahati", "state": "Assam", "lat": 26.1445, "lon": 91.7362, "pin": "781001", "roc": "ROC Shillong", "desc": "Gateway to Northeast India"},
    {"name": "Vadodara", "slug": "vadodara", "state": "Gujarat", "lat": 22.3072, "lon": 73.1812, "pin": "390001", "roc": "ROC Ahmedabad", "desc": "Cultural capital of Gujarat — chemical and petrochemical hub"},
    {"name": "Surat", "slug": "surat", "state": "Gujarat", "lat": 21.1702, "lon": 72.8311, "pin": "395001", "roc": "ROC Ahmedabad", "desc": "Diamond and textile capital of India"},
    {"name": "Noida", "slug": "noida", "state": "Uttar Pradesh", "lat": 28.5355, "lon": 77.3910, "pin": "201301", "roc": "ROC Kanpur", "desc": "NCR IT hub and startup ecosystem"},
    {"name": "Gurugram", "slug": "gurugram", "state": "Haryana", "lat": 28.4595, "lon": 77.0266, "pin": "122001", "roc": "ROC Delhi", "desc": "Millennium City — India's top corporate hub"},
    {"name": "Mysuru", "slug": "mysuru", "state": "Karnataka", "lat": 12.2958, "lon": 76.6394, "pin": "570001", "roc": "ROC Bangalore", "desc": "Heritage City and growing IT destination"},
    {"name": "Vijayawada", "slug": "vijayawada", "state": "Andhra Pradesh", "lat": 16.5062, "lon": 80.6480, "pin": "520001", "roc": "ROC Hyderabad", "desc": "Commercial hub near new capital Amaravati"},
    {"name": "Madurai", "slug": "madurai", "state": "Tamil Nadu", "lat": 9.9252, "lon": 78.1198, "pin": "625001", "roc": "ROC Chennai", "desc": "Temple City — southern Tamil Nadu's business centre"},
    {"name": "Raipur", "slug": "raipur", "state": "Chhattisgarh", "lat": 21.2514, "lon": 81.6296, "pin": "492001", "roc": "ROC Mumbai", "desc": "Capital of Chhattisgarh — steel and mining hub"},
    {"name": "Ranchi", "slug": "ranchi", "state": "Jharkhand", "lat": 23.3441, "lon": 85.3096, "pin": "834001", "roc": "ROC Patna", "desc": "Capital of Jharkhand — mining and steel belt"},
    {"name": "Dehradun", "slug": "dehradun", "state": "Uttarakhand", "lat": 30.3165, "lon": 78.0322, "pin": "248001", "roc": "ROC Delhi", "desc": "Capital of Uttarakhand — education and IT hub"},
    {"name": "Mangalore", "slug": "mangalore", "state": "Karnataka", "lat": 12.9141, "lon": 74.8560, "pin": "575001", "roc": "ROC Bangalore", "desc": "Port city and banking capital of Karnataka"},
    {"name": "Hubli-Dharwad", "slug": "hubli-dharwad", "state": "Karnataka", "lat": 15.3647, "lon": 75.1240, "pin": "580001", "roc": "ROC Bangalore", "desc": "North Karnataka's commercial twin-city"},
    {"name": "Tiruchirappalli", "slug": "tiruchirappalli", "state": "Tamil Nadu", "lat": 10.7905, "lon": 78.7047, "pin": "620001", "roc": "ROC Chennai", "desc": "Central Tamil Nadu's industrial hub"},
    {"name": "Salem", "slug": "salem", "state": "Tamil Nadu", "lat": 11.6643, "lon": 78.1460, "pin": "636001", "roc": "ROC Chennai", "desc": "Steel City of Tamil Nadu"},
    {"name": "Jodhpur", "slug": "jodhpur", "state": "Rajasthan", "lat": 26.2389, "lon": 73.0243, "pin": "342001", "roc": "ROC Jaipur", "desc": "Blue City — handicraft and tourism hub"},
    {"name": "Udaipur", "slug": "udaipur", "state": "Rajasthan", "lat": 24.5854, "lon": 73.7125, "pin": "313001", "roc": "ROC Jaipur", "desc": "City of Lakes — tourism and zinc industry"},
    {"name": "Amritsar", "slug": "amritsar", "state": "Punjab", "lat": 31.6340, "lon": 74.8723, "pin": "143001", "roc": "ROC Chandigarh", "desc": "Holy City — textile and food processing hub"},
    {"name": "Ludhiana", "slug": "ludhiana", "state": "Punjab", "lat": 30.9010, "lon": 75.8573, "pin": "141001", "roc": "ROC Chandigarh", "desc": "Manchester of India — bicycle and hosiery capital"},
    {"name": "Agra", "slug": "agra", "state": "Uttar Pradesh", "lat": 27.1767, "lon": 78.0081, "pin": "282001", "roc": "ROC Kanpur", "desc": "Tourism and leather industry hub"},
    {"name": "Varanasi", "slug": "varanasi", "state": "Uttar Pradesh", "lat": 25.3176, "lon": 83.0103, "pin": "221001", "roc": "ROC Kanpur", "desc": "Spiritual capital — textile and silk industry"},
    {"name": "Kanpur", "slug": "kanpur", "state": "Uttar Pradesh", "lat": 26.4499, "lon": 80.3319, "pin": "208001", "roc": "ROC Kanpur", "desc": "Industrial capital of UP — leather and textile hub"},
    {"name": "Nashik", "slug": "nashik", "state": "Maharashtra", "lat": 20.0063, "lon": 73.7898, "pin": "422001", "roc": "ROC Mumbai", "desc": "Wine capital and MIDC industrial corridor"},
    {"name": "Aurangabad", "slug": "aurangabad", "state": "Maharashtra", "lat": 19.8762, "lon": 75.3433, "pin": "431001", "roc": "ROC Mumbai", "desc": "Tourism and auto-component manufacturing hub"},
    {"name": "Rajkot", "slug": "rajkot", "state": "Gujarat", "lat": 22.3039, "lon": 70.8022, "pin": "360001", "roc": "ROC Ahmedabad", "desc": "Engineering and auto-parts manufacturing centre"},
    {"name": "Thane", "slug": "thane-city", "state": "Maharashtra", "lat": 19.2183, "lon": 72.9781, "pin": "400601", "roc": "ROC Mumbai", "desc": "Lake City — IT and pharmaceutical hub near Mumbai"},
    {"name": "Ghaziabad", "slug": "ghaziabad", "state": "Uttar Pradesh", "lat": 28.6692, "lon": 77.4538, "pin": "201001", "roc": "ROC Kanpur", "desc": "NCR industrial and residential hub"},
    {"name": "Faridabad", "slug": "faridabad", "state": "Haryana", "lat": 28.4089, "lon": 77.3178, "pin": "121001", "roc": "ROC Delhi", "desc": "NCR industrial town — auto and engineering"},
    {"name": "Meerut", "slug": "meerut", "state": "Uttar Pradesh", "lat": 28.9845, "lon": 77.7064, "pin": "250001", "roc": "ROC Kanpur", "desc": "Sports goods and scissors manufacturing hub"},
    {"name": "Jammu", "slug": "jammu", "state": "Jammu and Kashmir", "lat": 32.7266, "lon": 74.8570, "pin": "180001", "roc": "ROC Jammu", "desc": "Winter capital of J&K — emerging business centre"},
    {"name": "Goa", "slug": "goa-city", "state": "Goa", "lat": 15.4909, "lon": 73.8278, "pin": "403001", "roc": "ROC Mumbai", "desc": "Tourism capital — hospitality and IT startups"},
    {"name": "Shimla", "slug": "shimla", "state": "Himachal Pradesh", "lat": 31.1048, "lon": 77.1734, "pin": "171001", "roc": "ROC Delhi", "desc": "Capital of HP — tourism and education hub"},
    {"name": "Panaji", "slug": "panaji", "state": "Goa", "lat": 15.4909, "lon": 73.8278, "pin": "403001", "roc": "ROC Mumbai", "desc": "State capital — IT parks and startup ecosystem"},
]


# ═══════════════════════════════════════════════════════════════
# TEMPLATE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def make_meta_title(service, location):
    """Generate title under 70 chars"""
    t = f"{service['short']} in {location['name']} | Virtual Auditor"
    if len(t) > 70:
        t = f"{service['short']} {location['name']} | Virtual Auditor"
    return t[:70]

def make_meta_desc(service, location):
    """Generate description under 155 chars"""
    d = f"{service['short']} in {location['name']}. {service['price']}. FCA, ACS, CFE, IBBI RV. {service['desc'][:60]}. Contact +91 99622 60333."
    return d[:155]

def make_body_text(service, location, loc_type):
    """Generate bodyText for content/pages JSON"""
    name = location['name']
    state = location.get('state', location['name'])

    lines = []
    lines.append(f"What is {service['name'].lower()}? {service['desc']}")
    lines.append(f"{service['name']} is a professional service offered by Virtual Auditor, an AI-powered CA and IBBI Registered Valuer firm (IBBI/RV/03/2019/12333) led by CA V. Viswanathan (FCA, ACS, CFE, IBBI RV), serving clients in {name}, {state} since 2012.")
    lines.append(f"Quick Answer: {service['short']} in {name} — {service['desc'][:100]}. {service['price']}. Contact +91 99622 60333.")
    lines.append("")

    lines.append(f"HEADING2: {service['name']} in {name}")
    if loc_type == 'state':
        lines.append(f"Virtual Auditor provides {service['name'].lower()} across {name}. With offices in Chennai, Bangalore, and Mumbai, we serve businesses throughout {name} with the same quality of FCA + ACS + CFE + IBBI RV-led professional services.")
        lines.append(f"The {location['roc']} handles company registrations and filings for {name}. Stamp duty: {location['stamp_duty']}. Professional tax: {location['prof_tax']}.")
    else:
        lines.append(f"Virtual Auditor provides {service['name'].lower()} in {name}, {state}. {location.get('desc', '')}. Our multi-credential practice (FCA, ACS, CFE, IBBI RV) ensures comprehensive professional service delivery.")
        lines.append(f"ROC jurisdiction: {location['roc']}. Pincode: {location['pin']}.")
    lines.append("")

    lines.append("HEADING2: Our Service Scope")
    for item in service['scope']:
        lines.append(f"• {item}")
    lines.append("")

    lines.append(f"HEADING2: Step-by-Step Process")
    for i, (step_name, step_desc) in enumerate(service['steps'], 1):
        lines.append(f"• {i}")
        lines.append(f"HEADING3: Step {i}: {step_name}")
        lines.append(step_desc)
    lines.append("")

    if loc_type == 'state':
        lines.append(f"HEADING2: {name}-Specific Compliance Information")
        lines.append(f"ROC Office | {location['roc']}")
        lines.append(f"State Capital | {location['capital']}")
        lines.append(f"Stamp Duty | {location['stamp_duty']}")
        lines.append(f"Professional Tax | {location['prof_tax']}")
        lines.append(f"Pincode (Capital) | {location['pin']}")
    else:
        lines.append(f"HEADING2: {name} Compliance Information")
        lines.append(f"ROC Office | {location['roc']} |")
        lines.append(f"City | {name} |")
        lines.append(f"State | {state} |")
        lines.append(f"Pincode | {location['pin']} |")
    lines.append("")

    lines.append(f"HEADING2: Indicative Fee Structure")
    lines.append(f"Service | Fee |")
    lines.append(f"{service['short']} | {service['price']} |")
    lines.append(f"Consultation | Free (30 minutes) |")
    lines.append("")
    lines.append(f"*Prices are indicative. Actual fees depend on complexity and regulatory requirements. Contact us for a detailed quote.")
    lines.append("")

    lines.append(f"HEADING2: Why Virtual Auditor for {name}")
    lines.append(f"Our founder CA V. Viswanathan holds four credentials — FCA, ACS, CFE, IBBI RV — which means your {service['short'].lower()} is handled by the same qualified professional, not a rotating cast of junior associates.")
    lines.append("Technology that accelerates: Automated compliance calendars, AI-assisted document analysis, and 10,000 Monte Carlo simulations for valuations.")
    lines.append("")

    lines.append("HEADING2: Frequently Asked Questions")

    return "\n".join(lines)

def make_faqs(service, location, loc_type):
    """Generate FAQ list"""
    name = location['name']
    faqs = list(service['faqs_generic'])

    if loc_type == 'state':
        faqs.append((f"Do you provide {service['short'].lower()} services in {name}?", f"Yes. Virtual Auditor serves clients across {name} from our offices in Chennai, Bangalore, and Mumbai. We handle the complete process remotely with in-person meetings available at our nearest office. Contact +91 99622 60333."))
        faqs.append((f"What is the ROC jurisdiction for {name}?", f"Companies registered in {name} fall under {location['roc']}. Virtual Auditor handles all ROC filings for {name}-registered companies."))
        faqs.append((f"What is the stamp duty for company registration in {name}?", f"Stamp duty in {name}: {location['stamp_duty']}. Professional tax: {location['prof_tax']}. Contact us for exact computation based on your authorised capital."))
    else:
        state = location.get('state', name)
        faqs.append((f"Do you provide {service['short'].lower()} in {name}?", f"Yes. Virtual Auditor serves clients in {name}, {state}. {location.get('desc', '')}. Contact +91 99622 60333 for a free consultation."))
        faqs.append((f"What is the nearest Virtual Auditor office to {name}?", f"Our nearest office depends on your location. Chennai (HQ): Spencer Plaza, Anna Salai. Bangalore: MG Road. Mumbai: Goregaon West. All services available remotely for {name} clients."))
        faqs.append((f"How do I get started with {service['short'].lower()} in {name}?", f"Call +91 99622 60333 or WhatsApp us. Free 30-minute consultation. We handle the complete process for {name} businesses with no location surcharges."))

    return faqs

def make_schema(service, location, loc_type, slug, faqs):
    """Generate schema JSON"""
    name = location['name']
    state = location.get('state', location['name'])
    title = make_meta_title(service, location)
    desc = make_meta_desc(service, location)
    url = f"{DOMAIN}/{slug}"

    graph = [
        {"@type": "WebSite", "@id": f"{DOMAIN}/#website", "name": "Virtual Auditor", "url": DOMAIN, "publisher": {"@id": f"{DOMAIN}/#organization"}, "inLanguage": "en-IN"},
        {"@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": "Virtual Auditor", "legalName": "Virtual Auditor Private Limited", "url": DOMAIN, "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/images/logo2png.png"}, "founder": {"@type": "Person", "@id": f"{DOMAIN}/#founder", "name": "CA V. Viswanathan"}, "foundingDate": "2012", "contactPoint": {"@type": "ContactPoint", "telephone": "+91-9962260333", "contactType": "customer service", "areaServed": "IN", "availableLanguage": ["English", "Tamil", "Hindi"]}},
        {"@type": "WebPage", "@id": f"{url}/#webpage", "url": f"{url}/", "name": title, "description": desc, "isPartOf": {"@id": f"{DOMAIN}/#website"}, "inLanguage": "en-IN", "datePublished": TODAY, "dateModified": TODAY, "breadcrumb": {"@id": f"{url}/#breadcrumb"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@type": "Article", "@id": f"{url}/#article", "headline": f"{service['short']} in {name}", "description": desc, "author": {"@type": "Person", "@id": f"{DOMAIN}/#founder", "name": "CA V. Viswanathan", "jobTitle": "FCA, ACS, CFE, IBBI Registered Valuer", "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "FCA", "name": "Fellow Chartered Accountant — ICAI"}, {"@type": "EducationalOccupationalCredential", "credentialCategory": "IBBI RV", "name": "IBBI Registered Valuer — IBBI/RV/03/2019/12333"}]}, "publisher": {"@id": f"{DOMAIN}/#organization"}, "datePublished": TODAY, "dateModified": TODAY},
        {"@type": "BreadcrumbList", "@id": f"{url}/#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"}, {"@type": "ListItem", "position": 2, "name": service['short'], "item": f"{DOMAIN}/{service['parent']}/"}, {"@type": "ListItem", "position": 3, "name": f"{service['short']} in {name}"}]},
        {"@type": "ProfessionalService", "@id": f"{url}/#business", "name": f"Virtual Auditor — {name}", "description": f"{service['short']} in {name}. FCA + ACS + CFE + IBBI RV.", "url": url, "telephone": "+91-9962260333", "email": "support@virtualauditor.in", "address": {"@type": "PostalAddress", "addressLocality": location.get('capital', name) if loc_type == 'state' else name, "addressRegion": state if loc_type == 'city' else name, "postalCode": location['pin'], "addressCountry": "IN"}, "geo": {"@type": "GeoCoordinates", "latitude": location['lat'], "longitude": location['lon']}, "areaServed": [{"@type": "State" if loc_type == 'state' else "City", "name": name}, {"@type": "Country", "name": "India"}], "priceRange": "₹₹", "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.8, "reviewCount": 150, "bestRating": 5}, "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "18:00"}]},
    ]

    return {
        "schemas": [{"@context": "https://schema.org", "@graph": graph}],
        "faqs": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
        "howToSteps": [{"@type": "HowToStep", "position": i+1, "text": desc, "name": f"Step {i+1}: {name}"} for i, (name, desc) in enumerate(service['steps'])],
        "howToName": f"{service['short']} in {location['name']}",
        "howToDescription": make_meta_desc(service, location)
    }

def make_html(service, location, loc_type, slug, schema_json, faqs, body_text):
    """Generate complete HTML file"""
    title = make_meta_title(service, location)
    desc = make_meta_desc(service, location)
    url = f"{DOMAIN}/{slug}"
    name = location['name']
    state = location.get('state', location['name'])
    schema_str = json.dumps(schema_json['schemas'][0], ensure_ascii=False)

    faq_html = ""
    for q, a in faqs:
        faq_html += f'<details><summary>{q}</summary><p>{a}</p></details>\n'

    scope_html = ""
    for item in service['scope']:
        scope_html += f"<li>{item}</li>\n"

    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{url}" />
    <meta name="robots" content="index, follow" />
    <meta property="og:site_name" content="Virtual Auditor" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{DOMAIN}/opengraph.jpg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="en_IN" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{DOMAIN}/opengraph.jpg" />
    <link rel="alternate" hreflang="en-in" href="{url}" />
    <link rel="alternate" hreflang="en" href="{url}" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="icon" type="image/png" href="/favicon.png" />
    <link rel="apple-touch-icon" href="/favicon.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" crossorigin href="/assets/index-C4HJVHqv.css">
    <link rel="modulepreload" crossorigin href="/assets/react-vendor-BBuEwoGx.js">
    <link rel="modulepreload" crossorigin href="/assets/ui-vendor-hG3chjpU.js">
    <script type="application/ld+json">{schema_str}</script>
    <link rel="stylesheet" href="/css/override.css">
  </head>
  <body>
    <div id="root"><article>
<h1>{service['name']} in {name}</h1>
<p>{service['desc']} Virtual Auditor provides expert {service['short'].lower()} in {name}{', ' + state if loc_type == 'city' else ''}. FCA, ACS, CFE, IBBI Registered Valuer (IBBI/RV/03/2019/12333). Since 2012. Contact +91 99622 60333.</p>
<h2>Our Service Scope in {name}</h2>
<ul>
{scope_html}</ul>
<h2>Compliance Information</h2>
<p>ROC: {location['roc']}. Pincode: {location['pin']}.</p>
<h2>Indicative Fee Structure</h2>
<table><thead><tr><th>Service</th><th>Fee</th></tr></thead>
<tbody><tr><td>{service['short']}</td><td>{service['price']}</td></tr>
<tr><td>Free Consultation</td><td>30 minutes, no obligation</td></tr></tbody></table>
<section>
<h2>Frequently Asked Questions</h2>
{faq_html}</section>
<nav aria-label="Related Services"><h2>Other Services in {name}</h2><ul>
{"".join(f'<li><a href="/{s["slug"]}-in-{location["slug"]}">{s["short"]} in {name}</a></li>' for s in SERVICES if s['slug'] != service['slug'])}
</ul></nav>
</article></div>
    <script type="module" crossorigin src="/assets/index-BKPeGC_C.js"></script>
  </body>
</html>'''


# ═══════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════

def generate():
    pages_dir = os.path.join(BASE_DIR, "content", "pages")
    schemas_dir = os.path.join(BASE_DIR, "content", "schemas")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(schemas_dir, exist_ok=True)

    new_slugs = []
    total = 0
    skipped = 0

    # Generate STATE pages
    for state in STATES:
        for service in SERVICES:
            slug = f"{service['slug']}-in-{state['slug']}"
            html_path = os.path.join(BASE_DIR, f"{slug}.html")

            if os.path.exists(html_path):
                skipped += 1
                continue

            faqs = make_faqs(service, state, 'state')
            body_text = make_body_text(service, state, 'state')
            schema = make_schema(service, state, 'state', slug, faqs)
            html = make_html(service, state, 'state', slug, schema, faqs, body_text)

            # Write HTML
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)

            # Write content JSON
            content_json = {
                "title": make_meta_title(service, state),
                "description": make_meta_desc(service, state),
                "bodyText": body_text,
                "faqs": [{"q": q, "a": a} for q, a in faqs]
            }
            with open(os.path.join(pages_dir, f"{slug}.json"), 'w', encoding='utf-8') as f:
                json.dump(content_json, f, ensure_ascii=False)

            # Write schema JSON
            with open(os.path.join(schemas_dir, f"{slug}.json"), 'w', encoding='utf-8') as f:
                json.dump(schema, f, ensure_ascii=False)

            new_slugs.append(slug)
            total += 1

    # Generate CITY pages
    for city in CITIES:
        for service in SERVICES:
            slug = f"{service['slug']}-in-{city['slug']}"
            html_path = os.path.join(BASE_DIR, f"{slug}.html")

            if os.path.exists(html_path):
                skipped += 1
                continue

            faqs = make_faqs(service, city, 'city')
            body_text = make_body_text(service, city, 'city')
            schema = make_schema(service, city, 'city', slug, faqs)
            html = make_html(service, city, 'city', slug, schema, faqs, body_text)

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)

            content_json = {
                "title": make_meta_title(service, city),
                "description": make_meta_desc(service, city),
                "bodyText": body_text,
                "faqs": [{"q": q, "a": a} for q, a in faqs]
            }
            with open(os.path.join(pages_dir, f"{slug}.json"), 'w', encoding='utf-8') as f:
                json.dump(content_json, f, ensure_ascii=False)

            with open(os.path.join(schemas_dir, f"{slug}.json"), 'w', encoding='utf-8') as f:
                json.dump(schema, f, ensure_ascii=False)

            new_slugs.append(slug)
            total += 1

    # Update page-index.json
    page_index_path = os.path.join(BASE_DIR, "content", "page-index.json")
    if os.path.exists(page_index_path):
        existing = json.loads(open(page_index_path).read())
    else:
        existing = []

    existing.extend(new_slugs)
    existing = sorted(set(existing))
    with open(page_index_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    # Update sitemap.xml
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    if os.path.exists(sitemap_path):
        sitemap = open(sitemap_path).read()
        insert_point = sitemap.rfind('</urlset>')
        if insert_point > 0:
            new_entries = ""
            for slug in new_slugs:
                new_entries += f"  <url><loc>{DOMAIN}/{slug}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n"
            sitemap = sitemap[:insert_point] + new_entries + sitemap[insert_point:]
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(sitemap)

    print(f"Generated: {total} new pages ({total * 3} files)")
    print(f"Skipped (already exist): {skipped}")
    print(f"Total slugs in page-index: {len(existing)}")
    return new_slugs

if __name__ == "__main__":
    slugs = generate()
    print(f"\nDone. {len(slugs)} new location pages created.")
