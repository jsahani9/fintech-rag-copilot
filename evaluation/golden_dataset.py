"""
Golden evaluation dataset for the FinTech RAG Copilot.

15 realistic compliance questions drawn from the OSFI and international
regulatory documents in data/pdfs/. Ground-truth answers represent the
ideal response a senior compliance analyst would give — used by RAGAS
context_precision and context_recall as the reference signal.

Coverage:
  Q01-03  OSFI Corporate Governance Guideline 2018
  Q04-05  OSFI Technology and Cyber Risk Management
  Q06-07  OSFI Technology and Cyber Incident Reporting
  Q08-09  OSFI Third-Party Risk Management Guideline
  Q10-11  OSFI Operational Risk Management and Resilience
  Q12     Foreign Entities Operating in Canada on a Branch Basis
  Q13     NIST Cybersecurity Framework 2.0
  Q14     BIS d431 — Fintech Implications for Banks and Supervisors
  Q15     BIS d516 — Principles for Operational Resilience
"""

GOLDEN_DATASET = [
    # ── Corporate Governance ──────────────────────────────────────────────────
    {
        "question": (
            "What are the primary responsibilities of the board of directors "
            "under OSFI's Corporate Governance Guideline?"
        ),
        "ground_truth": (
            "Under OSFI's Corporate Governance Guideline, the board of directors "
            "is responsible for the overall stewardship of the institution. This "
            "includes approving and overseeing strategic objectives, the risk "
            "appetite framework, and significant policies. The board must ensure "
            "senior management implements systems to identify, assess, and control "
            "material risks, promote a culture of ethical conduct and compliance, "
            "oversee succession planning for key executive roles, and satisfy itself "
            "that the institution operates in a safe, sound, and prudent manner."
        ),
    },
    {
        "question": (
            "How does OSFI expect the Chief Risk Officer to function within a "
            "federally regulated financial institution?"
        ),
        "ground_truth": (
            "OSFI expects the Chief Risk Officer (CRO) to serve as an independent "
            "executive who leads the enterprise risk management function. The CRO "
            "must have unfettered access to the board and its risk committee, be "
            "free from conflicts of interest with revenue-generating business lines, "
            "and be responsible for overseeing the identification, measurement, "
            "monitoring, and control of all material risks. The CRO should be "
            "consulted on significant business decisions that affect the institution's "
            "risk profile and must report independently to the board on risk matters."
        ),
    },
    {
        "question": (
            "What is the three lines of defence model as described in OSFI's "
            "corporate governance expectations?"
        ),
        "ground_truth": (
            "The three lines of defence model is a governance structure with clear "
            "accountability at each layer. The first line consists of business units "
            "and front-line managers who own and manage risks as part of their daily "
            "operations. The second line comprises risk management and compliance "
            "functions that develop frameworks, set policies, and provide oversight "
            "and challenge of the first line. The third line is internal audit, which "
            "provides independent, objective assurance over the adequacy and "
            "effectiveness of both the first and second lines. Together they ensure "
            "risk-taking, risk oversight, and assurance remain clearly separated."
        ),
    },
    # ── Technology and Cyber Risk Management ──────────────────────────────────
    {
        "question": (
            "What does OSFI's Technology and Cyber Risk Management guideline "
            "require federally regulated financial institutions to establish?"
        ),
        "ground_truth": (
            "OSFI requires FRFIs to establish a comprehensive technology and cyber "
            "risk management framework encompassing clear governance and accountability "
            "structures, a board-approved technology risk appetite, processes for "
            "identifying and assessing technology risks across the full asset lifecycle, "
            "layered controls protecting systems and data, active cyber threat monitoring "
            "and detection capabilities, and regularly tested incident response and "
            "recovery plans. Institutions must maintain accurate technology asset "
            "inventories and actively manage cyber risks introduced by vendors and "
            "third-party providers."
        ),
    },
    {
        "question": (
            "What cyber resilience expectations does OSFI hold for financial "
            "institutions under its technology risk guidelines?"
        ),
        "ground_truth": (
            "OSFI expects financial institutions to be cyber resilient — able to "
            "prevent, withstand, and recover from cyber attacks with minimal "
            "disruption to critical services. Requirements include implementing "
            "defence-in-depth security controls, conducting regular vulnerability "
            "assessments and penetration testing, maintaining a cyber threat "
            "intelligence program, testing incident response plans under realistic "
            "scenarios, and ensuring critical systems can be recovered within "
            "pre-defined recovery time objectives. Institutions must also embed "
            "cybersecurity culture through mandatory employee training and awareness."
        ),
    },
    # ── Technology and Cyber Incident Reporting ───────────────────────────────
    {
        "question": (
            "What is the mandatory reporting timeline for technology and cyber "
            "security incidents under OSFI guidelines?"
        ),
        "ground_truth": (
            "Under OSFI's Technology and Cyber Incident Reporting requirements, "
            "federally regulated financial institutions must notify OSFI as soon as "
            "possible and no later than 72 hours after becoming aware of a technology "
            "or cyber security incident that meets the reporting threshold. The initial "
            "notification must contain preliminary details. Institutions must then "
            "provide ongoing status updates as new information becomes available and "
            "submit a formal post-incident review report once the incident is resolved."
        ),
    },
    {
        "question": (
            "What information must be included in an initial technology or cyber "
            "incident report submitted to OSFI?"
        ),
        "ground_truth": (
            "An initial OSFI technology or cyber incident report must include: the "
            "date and time the incident was detected, a description of the nature and "
            "type of incident (e.g., ransomware, data breach, system outage), the "
            "systems, services, and data affected, an estimate of operational and "
            "customer impact, initial containment and mitigation steps already taken, "
            "a preliminary assessment of whether personal or sensitive customer data "
            "has been compromised, and the name and contact details of the institution's "
            "primary incident management contact for OSFI communications."
        ),
    },
    # ── Third-Party Risk Management ───────────────────────────────────────────
    {
        "question": (
            "How does OSFI define a material third-party arrangement in its "
            "Third-Party Risk Management Guideline?"
        ),
        "ground_truth": (
            "Under OSFI's Third-Party Risk Management Guideline, a material arrangement "
            "is one where disruption or failure of the third party could significantly "
            "impair the FRFI's operations, ability to meet regulatory obligations, "
            "financial condition, or reputation. Key factors that make an arrangement "
            "material include: criticality of the service to core or regulated business "
            "functions, sensitivity of data the third party can access, difficulty of "
            "transitioning to an alternative provider, and potential impact on customers "
            "and counterparties. Material arrangements require heightened due diligence, "
            "robust contracts, and continuous oversight."
        ),
    },
    {
        "question": (
            "What due diligence must a federally regulated financial institution "
            "perform before entering a material third-party arrangement under OSFI guidelines?"
        ),
        "ground_truth": (
            "Before entering a material third-party arrangement, OSFI requires FRFIs "
            "to conduct comprehensive pre-arrangement due diligence covering: the third "
            "party's financial stability and viability, operational capabilities and "
            "performance track record, information security and data protection "
            "practices, business continuity and disaster recovery plans, sub-contracting "
            "or fourth-party arrangements, regulatory compliance history, and "
            "concentration risk implications. Findings must be documented. Contracts "
            "must include audit rights, data ownership clauses, regulatory access "
            "provisions, performance standards, and clearly defined exit and transition "
            "arrangements."
        ),
    },
    # ── Operational Risk Management and Resilience ────────────────────────────
    {
        "question": (
            "What does OSFI mean by operational resilience and how should federally "
            "regulated financial institutions achieve it?"
        ),
        "ground_truth": (
            "OSFI defines operational resilience as the ability of an FRFI to prevent, "
            "adapt to, respond to, recover from, and learn from operational disruptions "
            "of any kind. Institutions achieve operational resilience by: identifying "
            "their critical operations and the internal and external dependencies "
            "supporting those operations, setting impact tolerances that define the "
            "maximum acceptable level and duration of disruption, stress-testing their "
            "ability to remain within those tolerances under severe but plausible "
            "scenarios, and maintaining tested response, recovery, and communications "
            "plans to restore critical services promptly. Lessons from incidents and "
            "exercises must feed back into continuous improvement."
        ),
    },
    {
        "question": (
            "What are the key business continuity planning requirements under OSFI's "
            "Operational Risk Management and Resilience Guideline?"
        ),
        "ground_truth": (
            "OSFI requires business continuity planning to be grounded in a thorough "
            "business impact analysis that identifies critical processes and their "
            "recovery time and recovery point objectives. Plans must address a range "
            "of severe but plausible disruption scenarios including natural disasters, "
            "technology failures, pandemic events, and supply chain disruptions. "
            "Institutions must maintain alternate processing capabilities and documented "
            "communication strategies for staff, regulators, and customers. Plans must "
            "be tested regularly through realistic exercises and drills, and updated "
            "to reflect organisational changes. Crisis management and regulatory "
            "notification protocols must be integrated into the plans."
        ),
    },
    # ── Foreign Entities Operating in Canada ──────────────────────────────────
    {
        "question": (
            "What are the key regulatory requirements for foreign banks operating "
            "in Canada on a branch basis under OSFI guidelines?"
        ),
        "ground_truth": (
            "Under OSFI's guideline for foreign entities operating on a branch basis, "
            "foreign banks must: maintain adequate capital allocated to Canadian "
            "operations and hold sufficient liquidity in Canada to meet local "
            "obligations, appoint a Principal Officer in Canada who is directly "
            "accountable to OSFI, maintain books and records in Canada sufficient "
            "for supervisory review, submit required regulatory reports and filings "
            "to OSFI, obtain prior OSFI approval for significant operational or "
            "structural changes, and demonstrate that the home-country regulatory "
            "regime meets OSFI's standards. The branch must comply with all applicable "
            "Canadian legislation and OSFI guidelines."
        ),
    },
    # ── NIST Cybersecurity Framework 2.0 ──────────────────────────────────────
    {
        "question": "What are the six core functions of the NIST Cybersecurity Framework 2.0?",
        "ground_truth": (
            "NIST Cybersecurity Framework 2.0 organises cybersecurity activities into "
            "six core functions: (1) Govern — establishes cybersecurity risk governance, "
            "strategy, roles, responsibilities, and policy (new in version 2.0); "
            "(2) Identify — develops understanding of cybersecurity risks to systems, "
            "assets, data, and capabilities; (3) Protect — implements safeguards to "
            "limit the impact of cyber events; (4) Detect — enables timely discovery "
            "of cybersecurity events and anomalies; (5) Respond — defines actions taken "
            "after a detected cybersecurity incident; (6) Recover — supports restoration "
            "of capabilities or services impaired by an incident. The framework is "
            "voluntary and designed to be applicable across sectors and organisation sizes."
        ),
    },
    # ── FinTech Implications for Banks (BIS d431) ─────────────────────────────
    {
        "question": (
            "What key supervisory challenges does the Basel Committee identify "
            "for banks and bank supervisors arising from fintech developments?"
        ),
        "ground_truth": (
            "The Basel Committee identifies several supervisory challenges from fintech "
            "developments. First, maintaining the regulatory perimeter is difficult "
            "because fintech firms often offer banking-like services outside traditional "
            "prudential oversight, and authorities may lack a remit over non-bank firms. "
            "Second, the cross-border nature of technologies such as DLT and smart "
            "contracts requires increased international cooperation and legal certainty "
            "across jurisdictions. Third, supervisors must develop new internal skills "
            "and capabilities — including revised hiring profiles and direct "
            "experimentation with AI/ML and DLT — to supervise technology-driven "
            "business models effectively. Fourth, banks face operational, reputational, "
            "and strategic risks when partnering with or competing against fintech firms. "
            "Supervisors are responding through innovation offices, regulatory sandboxes, "
            "and suptech tools that apply AI to supervisory data."
        ),
    },
    # ── Basel Committee Operational Resilience (BIS d516) ─────────────────────
    {
        "question": (
            "What are the Basel Committee's Principles for Operational Resilience "
            "and what do they require banks to maintain?"
        ),
        "ground_truth": (
            "The Basel Committee's 2021 Principles for Operational Resilience establish "
            "that banks must be able to withstand, adapt to, and recover from potential "
            "hazards with minimal disruption to critical operations. The principles "
            "require banks to: develop board-approved governance frameworks and "
            "operational resilience strategies; identify and map critical operations "
            "and their internal and external interconnections; set impact tolerances "
            "that define the maximum level and duration of disruption tolerable for "
            "each critical operation; conduct business continuity planning and testing "
            "under severe but plausible scenarios; manage third-party dependencies "
            "rigorously; maintain effective incident management capabilities; and ensure "
            "resilient ICT infrastructure and cybersecurity controls. The principles "
            "apply on a consolidated basis consistent with the scope of the Basel "
            "Framework and are intended to be proportionate to each bank's size, "
            "complexity, and risk profile."
        ),
    },
]
