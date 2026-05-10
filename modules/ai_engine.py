import google.generativeai as genai
import json
import time
from modules.parser import split_into_chunks

PRODUCT_KNOWLEDGE = {

    "PAM": """
        PRODUCT: PAM (Privileged Access Management)
        VENDOR CONTEXT: Enterprise cybersecurity product managing privileged accounts,
        sessions, and credentials across IT infrastructure.

        === CORE MODULES ===

        1. VAULT / CREDENTIAL MANAGEMENT
           - Password vault stores privileged credentials encrypted (AES-256)
           - Checkout mechanism: user requests password, vault releases for limited time
           - Auto password rotation after checkout expires
           - Dual control: two approvers needed for critical accounts
           - Password complexity policies (length, special chars, expiry)
           - SSH key and certificate management
           - API key and service account credential storage
           - Password history enforcement (no reuse of last N passwords)

        2. SESSION MANAGEMENT
           - RDP, SSH, HTTPS session proxying through PAM gateway
           - Live session monitoring by security admin
           - Session recording (video + keystrokes + commands)
           - Session recording stored encrypted, tamper-proof
           - Session termination by admin in real time
           - Session shadowing (admin joins live session)
           - Concurrent session limits per user
           - Session timeout on inactivity
           - Clipboard restriction during privileged sessions
           - File transfer restrictions (block upload/download)

        3. ACCESS CONTROL & AUTHORIZATION
           - Role-Based Access Control (RBAC)
           - Just-In-Time (JIT) access: access granted only when needed, auto-expires
           - Just-Enough-Access (JEA): only necessary permissions granted
           - Access request and approval workflow (multi-level)
           - Time-bound access with automatic revocation
           - Emergency break-glass access with full audit
           - IP-based access restrictions
           - Device-based access policies
           - Geo-location based restrictions

        4. AUTHENTICATION
           - Multi-Factor Authentication (MFA) enforcement
           - SSO integration (SAML, OAuth, OIDC)
           - Active Directory / LDAP integration
           - RADIUS authentication support
           - Certificate-based authentication
           - Adaptive authentication based on risk score
           - Failed login lockout policies
           - Session token management and expiry

        5. DISCOVERY & ONBOARDING
           - Automatic discovery of privileged accounts across network
           - Discovery of unmanaged accounts (shadow IT)
           - Service account discovery
           - Local admin account discovery on endpoints
           - Scheduled vs on-demand discovery scans
           - Auto-onboarding of discovered accounts to vault

        6. AUDIT & COMPLIANCE
           - Full audit trail of every action (who, what, when, from where)
           - Immutable audit logs (cannot be modified or deleted)
           - Real-time alerts on suspicious activity
           - SIEM integration (Splunk, QRadar, ArcSight)
           - Compliance reports (SOX, PCI-DSS, HIPAA, ISO 27001)
           - Privileged access review and certification
           - Anomaly detection on session behavior

        === KEY TEST SCENARIOS ===
        AUTHENTICATION: MFA bypass, brute force lockout, expired session reuse,
        token hijacking, SSO misconfiguration, certificate validation failure

        AUTHORIZATION: Privilege escalation, horizontal access, RBAC bypass,
        JIT access after expiry, break-glass misuse

        SESSION: Recording gaps, session hijacking, clipboard exfiltration,
        concurrent session limit bypass, admin termination latency

        VAULT: Password visible in logs, rotation failure, dual control bypass,
        checkout without approval, credential leak via API

        AUDIT: Log tampering, missing audit entries, alert not triggered,
        SIEM log delay, compliance report inaccuracy

        === EDGE CASES ===
        - Network disconnect during active privileged session
        - Password rotation fails due to target system being offline
        - Concurrent checkout by two users of same account
        - Audit log storage full
        - MFA device lost during active session
        - Break-glass used without actual emergency
    """,

    "EPM": """
        PRODUCT: EPM (Endpoint Privilege Management)
        VENDOR CONTEXT: Removes local administrator rights from endpoints,
        controls application privilege elevation without giving full admin.

        === CORE MODULES ===

        1. PRIVILEGE REMOVAL & LEAST PRIVILEGE
           - Remove local admin rights from all standard users
           - Enforce least privilege principle across endpoints
           - Detect and alert on re-added local admin accounts
           - Prevent users from adding themselves to admin groups

        2. APPLICATION CONTROL
           - Whitelist: only approved applications can run
           - Blacklist: explicitly blocked applications always denied
           - Greylist: unknown apps require approval before running
           - Publisher-based rules
           - Hash-based rules
           - Path-based rules
           - Script control (PowerShell, VBScript, batch files)
           - DLL injection prevention

        3. ELEVATION MANAGEMENT
           - On-demand elevation with business justification
           - Approval workflow: request goes to manager/IT
           - Time-limited elevation
           - Automatic elevation for pre-approved applications
           - Elevation audit trail
           - Remote elevation approval via mobile app

        4. AGENT MANAGEMENT
           - Agent tamper protection
           - Agent self-healing if killed
           - Offline policy caching
           - Agent upgrade and rollback

        === KEY TEST SCENARIOS ===
        APPLICATION CONTROL: Blocked app execution, whitelisted app runs,
        unknown app handling, script execution blocking, hash mismatch detection

        ELEVATION: Elevation without approval fails, elevation after approval works,
        elevation time expiry enforced, concurrent elevation requests

        AGENT: Agent killed by user restarts, agent uninstall blocked,
        policy sync when network restored, offline enforcement

        === EDGE CASES ===
        - User renames blocked executable to bypass path rules
        - Elevation request floods approval queue
        - Offline laptop reconnects with 30-day-old policy
        - Agent update breaks application control rules
    """,

    "CI": """
        PRODUCT: CI (Compliance Intelligence)
        VENDOR CONTEXT: Continuous monitoring platform assessing infrastructure
        against security policies and compliance frameworks in real time.

        === CORE MODULES ===

        1. POLICY & BENCHMARK MANAGEMENT
           - CIS Benchmarks, NIST, PCI-DSS, HIPAA, SOX, ISO 27001
           - Custom policy creation
           - Policy exception management with approval workflow
           - Benchmark scoring per control

        2. ASSET DISCOVERY & INVENTORY
           - Network scan-based asset discovery
           - Cloud asset discovery (AWS, Azure, GCP)
           - Rogue/unmanaged asset detection
           - Asset risk scoring

        3. COMPLIANCE SCANNING
           - Scheduled and on-demand scans
           - Agentless scanning via WMI, SSH, SNMP
           - Incremental scanning
           - Parallel scanning for large environments

        4. RISK SCORING & DASHBOARD
           - Per-asset compliance score (0-100)
           - Environment-wide risk score and trend
           - Executive dashboard with drilldown
           - Heatmap of riskiest assets

        5. ALERTING & NOTIFICATIONS
           - Real-time alerts on policy violations
           - Alert severity classification
           - Alert routing to specific teams
           - SIEM integration

        === KEY TEST SCENARIOS ===
        SCANNING: Detects real misconfiguration, false negative check,
        false positive check, performance on large environment

        ALERTING: Alert fires on violation, no alert on approved exception,
        correct routing, SIEM receives within SLA

        === EDGE CASES ===
        - Asset decommissioned but still in dashboard
        - Policy exception expires — violation reappears
        - Score changes without configuration change
        - Audit report during active scan — data consistency
    """,

    "MyVault": """
        PRODUCT: MyVault (Personal Password Vault)
        VENDOR CONTEXT: Secure personal credential management for end users
        within an organization.

        === CORE MODULES ===

        1. VAULT & CREDENTIAL STORAGE
           - AES-256 encrypted storage
           - Credential history tracking
           - Import from CSV, browser export
           - Encrypted backup export

        2. MASTER PASSWORD & AUTHENTICATION
           - Zero-knowledge architecture
           - Master password never stored or transmitted
           - MFA on vault login (TOTP, hardware key)
           - Biometric unlock on mobile
           - Emergency access via trusted contact

        3. AUTO-FILL & BROWSER INTEGRATION
           - Phishing protection — fills only on correct domain
           - Never auto-fill on HTTP sites
           - Multiple accounts per website support

        4. SECURE SHARING
           - Read-only vs edit permissions
           - Time-limited sharing with auto-expiry
           - Owner can revoke anytime
           - Recipient cannot re-share

        5. SECURITY FEATURES
           - Vault lock on inactivity timeout
           - Clipboard auto-clear after N seconds
           - Have I Been Pwned breach detection
           - Screen capture protection on mobile

        === KEY TEST SCENARIOS ===
        AUTHENTICATION: Wrong master password lockout,
        MFA device lost recovery, token reuse after logout

        SHARING: Revoke access — recipient denied immediately,
        read-only share edit blocked, expired share inaccessible

        === EDGE CASES ===
        - Master password forgotten with no recovery set up
        - Import CSV with malformed or malicious data
        - Owner changes shared credential password
        - Vault accessed from new country — suspicious login
        - Device stolen — remote vault wipe
    """
}


def safe_parse_json(raw):
    """Safely parses JSON even if AI response is incomplete"""
    raw = raw.strip()

    # Remove markdown code blocks if present
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            stripped = part.strip()
            if stripped.startswith("json"):
                stripped = stripped[4:].strip()
            if stripped.startswith("["):
                raw = stripped
                break

    raw = raw.strip()

    # Try full parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # AI hit token limit mid-response — fix incomplete JSON
    try:
        last_complete = raw.rfind('},')
        if last_complete == -1:
            last_complete = raw.rfind('}')
        if last_complete != -1:
            fixed = raw[:last_complete + 1] + ']'
            return json.loads(fixed)
    except:
        pass

    return []


def remove_duplicates(all_cases):
    """Remove duplicate test cases based on objective similarity"""
    seen_objectives = set()
    unique_cases = []

    for tc in all_cases:
        objective = tc.get('objective', '').lower().strip()
        # Check if very similar objective already exists
        is_duplicate = False
        for seen in seen_objectives:
            # Simple duplicate check — first 60 chars match
            if objective[:60] == seen[:60]:
                is_duplicate = True
                break

        if not is_duplicate:
            seen_objectives.add(objective)
            unique_cases.append(tc)

    return unique_cases


def renumber_cases(cases, product):
    """Renumber all test cases sequentially after combining chunks"""
    from datetime import datetime
    today = datetime.now().strftime('%d/%m/%Y')

    for i, tc in enumerate(cases, 1):
        tc['serial'] = i
        tc['tc_id'] = f"TC-{product.upper()}-{str(i).zfill(3)}"
        tc['suite_id'] = f"TS-{product.upper()}-001"
        tc['date'] = today

    return cases


def call_gemini(client, prompt):
    """Single API call to Gemini with retry on rate limit"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg or 'quota' in error_msg.lower():
                wait_time = 30 * (attempt + 1)
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Gemini API rate limit exceeded after retries.")


def generate_for_chunk(client, product, feature, test_type,
                       chunk_text, chunk_num, total_chunks, product_context):
    """Generate test cases for a single document chunk"""

    from datetime import datetime
    today = datetime.now().strftime('%d/%m/%Y')

    type_instruction = (
        "Mix of Functional, Security, Negative, Boundary, Regression."
        if test_type == "all"
        else f"Focus only on {test_type} test cases."
    )

    chunk_info = (
        f"This is chunk {chunk_num} of {total_chunks} of the full document."
        if total_chunks > 1
        else "This is the complete document."
    )

    prompt = f"""You are a Senior QA Engineer and Security Tester with deep expertise in cybersecurity products.

=== PRODUCT KNOWLEDGE ===
{product_context}

=== FEATURE / SCENARIO TO TEST ===
{feature}

=== DOCUMENT SECTION ===
{chunk_info}
{chunk_text}

=== INSTRUCTIONS ===
- Read the document section above carefully
- Generate test cases ONLY for what is described in this document section
- DO NOT invent scenarios not mentioned in the document
- If document section mentions a feature — generate ALL possible test cases for it
- Test type: {type_instruction}
- Think like both an attacker and a tester
- Cover for each feature:
    * Happy path (positive)
    * Wrong/invalid input (negative)
    * Empty/null/boundary values (boundary)
    * Unauthorized access attempt (security)
    * Session timeout / expiry scenarios (edge case)
    * Concurrent usage (edge case)
- Make steps specific and executable for a junior tester
- Make test data realistic with actual values
- Do NOT add a fixed count — generate as many as the content requires

=== OUTPUT FORMAT ===
Return ONLY a valid JSON array. No explanation. No markdown. No backticks.
Start with [ and end with ]
Each object must have exactly these keys:
{{
  "serial": 1,
  "date": "{today}",
  "suite_id": "TS-{product.upper()}-001",
  "tc_id": "TC-{product.upper()}-001",
  "objective": "one sentence what this test proves",
  "preconditions": "what must be set up before running",
  "steps": "1. Step one 2. Step two 3. Step three",
  "test_data": "actual input values to use",
  "expected_result": "exact expected outcome",
  "actual_result": "",
  "status": "",
  "remarks": ""
}}"""

    raw = call_gemini(client, prompt)
    cases = safe_parse_json(raw)
    return cases


def generate_test_cases(product, feature, test_type, doc_text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    product_context = PRODUCT_KNOWLEDGE.get(product, "")
    all_test_cases = []

    if doc_text:
        # Split full document into chunks
        chunks = split_into_chunks(doc_text, chunk_size=8000, overlap=500)
        total_chunks = len(chunks)

        print(f"Document split into {total_chunks} chunk(s). Processing...")

        for i, chunk in enumerate(chunks, 1):
            print(f"Processing chunk {i} of {total_chunks}...")

            cases = generate_for_chunk(
                model, product, feature, test_type,
                chunk, i, total_chunks, product_context
            )

            all_test_cases.extend(cases)
            print(f"Chunk {i} generated {len(cases)} test cases.")

            # Delay between chunks to avoid rate limiting
            if i < total_chunks:
                print("Waiting 10 seconds before next chunk...")
                time.sleep(10)

    else:
        # No document — generate from feature description + product knowledge
        print("No document uploaded. Generating from feature description...")

        from datetime import datetime
        today = datetime.now().strftime('%d/%m/%Y')

        type_instruction = (
            "Mix of Functional, Security, Negative, Boundary, Regression."
            if test_type == "all"
            else f"Focus only on {test_type} test cases."
        )

        prompt = f"""You are a Senior QA Engineer and Security Tester with deep expertise in cybersecurity products.

=== PRODUCT KNOWLEDGE ===
{product_context}

=== FEATURE / SCENARIO TO TEST ===
{feature}

=== INSTRUCTIONS ===
- Analyze the feature/scenario deeply
- Generate ALL possible test cases this scenario requires
- Test type: {type_instruction}
- Think like both an attacker and a tester
- Cover: happy path, negative, boundary, security, edge cases
- Make steps executable for a junior tester
- Make test data realistic

=== OUTPUT FORMAT ===
Return ONLY a valid JSON array. No explanation. No markdown. No backticks.
Start with [ and end with ]
Each object must have exactly these keys:
{{
  "serial": 1,
  "date": "{today}",
  "suite_id": "TS-{product.upper()}-001",
  "tc_id": "TC-{product.upper()}-001",
  "objective": "one sentence what this test proves",
  "preconditions": "what must be set up before running",
  "steps": "1. Step one 2. Step two 3. Step three",
  "test_data": "actual input values to use",
  "expected_result": "exact expected outcome",
  "actual_result": "",
  "status": "",
  "remarks": ""
}}"""

        raw = call_gemini(model, prompt)
        all_test_cases = safe_parse_json(raw)

    # Remove duplicates across chunks
    all_test_cases = remove_duplicates(all_test_cases)

    # Renumber everything cleanly 001, 002, 003...
    all_test_cases = renumber_cases(all_test_cases, product)

    print(f"Total unique test cases generated: {len(all_test_cases)}")
    return all_test_cases