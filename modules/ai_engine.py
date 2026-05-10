import google.generativeai as genai
import json

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
           - Biometric authentication support
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

        7. INTEGRATIONS
           - ITSM integration (ServiceNow, Jira) for access request tickets
           - SIEM integration for log forwarding
           - Directory services (AD, LDAP, Azure AD)
           - Cloud platforms (AWS, Azure, GCP) privileged access
           - DevOps tools (Jenkins, Ansible, Terraform) secrets management
           - API access for automation

        === KEY TEST SCENARIOS ===
        AUTHENTICATION: MFA bypass, brute force lockout, expired session reuse,
        token hijacking, SSO misconfiguration, certificate validation failure

        AUTHORIZATION: Privilege escalation, horizontal access (user A accessing user B's vault),
        RBAC bypass, JIT access after expiry, break-glass misuse

        SESSION: Recording gaps, session hijacking mid-stream, clipboard exfiltration,
        concurrent session limit bypass, admin termination latency

        VAULT: Password visible in logs, rotation failure, dual control bypass,
        checkout without approval, credential leak via API

        AUDIT: Log tampering, missing audit entries, alert not triggered on violation,
        SIEM log delay, compliance report inaccuracy

        === COMMON EDGE CASES ===
        - Network disconnect during active privileged session
        - Password rotation fails due to target system being offline
        - Admin approves access for already-compromised account
        - User checks out password and system goes into maintenance
        - Concurrent checkout by two users of same account
        - Audit log storage full — what happens to new entries
        - MFA device lost during active session
        - Discovery scan finds 10,000+ accounts — performance test
        - Break-glass used without actual emergency — detection
        - Session recording playback of deleted session
    """,

    "EPM": """
        PRODUCT: EPM (Endpoint Privilege Management)
        VENDOR CONTEXT: Removes local administrator rights from end-user workstations
        and servers, controls application privilege elevation without giving full admin.

        === CORE MODULES ===

        1. PRIVILEGE REMOVAL & LEAST PRIVILEGE
           - Remove local admin rights from all standard users
           - Enforce least privilege principle across endpoints
           - Detect and alert on re-added local admin accounts
           - Prevent users from adding themselves to admin groups
           - Admin rights audit across all managed endpoints
           - Baseline privilege policy enforcement

        2. APPLICATION CONTROL
           - Whitelist: only approved applications can run
           - Blacklist: explicitly blocked applications always denied
           - Greylist: unknown apps require approval before running
           - Publisher-based rules (trust apps from specific vendors)
           - Hash-based rules (trust specific file versions)
           - Path-based rules (trust apps from specific locations)
           - Network zone-based application rules
           - Script control (PowerShell, VBScript, batch files)
           - Browser extension control
           - DLL injection prevention

        3. ELEVATION MANAGEMENT
           - On-demand elevation: user requests to run specific app as admin
           - Self-service elevation with business justification
           - Approval workflow: request goes to manager/IT for approval
           - Time-limited elevation (e.g., 30 minutes only)
           - Automatic elevation for pre-approved applications
           - Elevation without exposing admin credentials to user
           - Elevation audit trail (who elevated what, when, why)
           - Remote elevation approval via mobile app
           - Emergency elevation with post-approval

        4. POLICY MANAGEMENT
           - Centralized policy creation and deployment
           - Policy targeting by user, group, OU, machine
           - Policy precedence and conflict resolution
           - Policy versioning and rollback
           - Real-time policy push vs scheduled sync
           - Policy testing in audit mode before enforcement
           - Group Policy integration

        5. AGENT MANAGEMENT
           - Lightweight agent installed on endpoints
           - Agent tamper protection (cannot be stopped/uninstalled by standard user)
           - Agent health monitoring and heartbeat
           - Agent self-healing if killed
           - Agent communication with server (online/offline mode)
           - Offline policy caching (works without network)
           - Agent upgrade and rollback
           - Agent log collection

        6. REPORTING & ANALYTICS
           - Application usage reports
           - Elevation request reports (approved, denied, pending)
           - Policy violation reports
           - Endpoint compliance score
           - Risk-based endpoint ranking
           - User behavior analytics
           - Threat detection from elevation patterns

        === KEY TEST SCENARIOS ===
        APPLICATION CONTROL: Blocked app execution, whitelisted app runs correctly,
        unknown app handling, script execution blocking, publisher trust validation,
        hash mismatch detection, path rule bypass attempt

        ELEVATION: Elevation without approval (should fail), elevation after approval,
        elevation time expiry enforcement, credential exposure during elevation,
        concurrent elevation requests, elevation on offline machine

        AGENT: Agent killed by user (should restart), agent uninstall by standard user (blocked),
        policy sync when network restored, offline elevation enforcement,
        agent on new machine auto-enrollment

        POLICY: Conflicting policy resolution, policy not applied to specific OU,
        audit mode vs enforcement mode, policy rollback after bad deployment

        === COMMON EDGE CASES ===
        - User installs portable app (no installer) — hash rule bypass attempt
        - Admin accidentally removes themselves from admin group
        - Elevation approved but target app crashes immediately
        - Policy deployed to wrong OU — mass impact
        - Agent update breaks application control rules
        - User renames blocked executable to bypass path rules
        - Elevation request floods approval queue (100+ simultaneous)
        - Offline laptop reconnects with 30-day-old policy
        - Dual-boot machine — EPM only on one OS
        - Virtual machine with snapshots — policy state after rollback
    """,

    "CI": """
        PRODUCT: CI (Compliance Intelligence / Continuous Intelligence)
        VENDOR CONTEXT: Continuous monitoring platform that assesses infrastructure
        against security policies, benchmarks, and compliance frameworks in real time.

        === CORE MODULES ===

        1. POLICY & BENCHMARK MANAGEMENT
           - Built-in frameworks: CIS Benchmarks, NIST, PCI-DSS, HIPAA, SOX, ISO 27001
           - Custom policy creation with custom rules
           - Policy versioning and change tracking
           - Policy assignment to specific asset groups
           - Policy exception management with approval workflow
           - Policy conflict detection
           - Benchmark scoring (pass/fail/warning per control)

        2. ASSET DISCOVERY & INVENTORY
           - Network scan-based asset discovery
           - Agent-based discovery for managed endpoints
           - Cloud asset discovery (AWS, Azure, GCP)
           - Asset classification (server, workstation, network device, cloud)
           - Asset grouping and tagging
           - Asset owner assignment
           - Rogue/unmanaged asset detection
           - Asset risk scoring

        3. COMPLIANCE SCANNING
           - Scheduled scans (daily, weekly, monthly)
           - On-demand scans triggered manually or via API
           - Agentless scanning via WMI, SSH, SNMP
           - Agent-based scanning for real-time data
           - Incremental scanning (only changed configurations)
           - Scan scope targeting (specific IPs, subnets, OUs)
           - Parallel scanning for large environments
           - Scan performance impact control (throttling)

        4. RISK SCORING & DASHBOARD
           - Per-asset compliance score (0-100)
           - Per-policy control pass/fail/exception status
           - Environment-wide risk score
           - Risk trend over time (improving/degrading)
           - Executive dashboard with high-level metrics
           - Drilldown from score to specific failed controls
           - Heatmap of riskiest assets
           - Comparison across asset groups

        5. ALERTING & NOTIFICATIONS
           - Real-time alerts on new policy violations
           - Alert severity classification (critical, high, medium, low)
           - Alert routing to specific teams/owners
           - Email, SMS, webhook notification channels
           - Alert suppression for known exceptions
           - Alert escalation if unresolved after N days
           - SIEM integration for alert forwarding
           - Alert deduplication

        6. REMEDIATION MANAGEMENT
           - Remediation guidance per failed control
           - Automated remediation scripts (optional)
           - Remediation ticket creation in ITSM (ServiceNow)
           - Remediation tracking and SLA monitoring
           - Verification scan after remediation
           - Remediation history audit trail

        7. REPORTING
           - Scheduled compliance reports
           - On-demand report generation
           - Report formats: PDF, Excel, CSV
           - Executive summary vs technical detail reports
           - Trend reports over time periods
           - Evidence collection for auditors
           - Custom report builder

        === KEY TEST SCENARIOS ===
        SCANNING: Scan detects real misconfiguration, scan misses known violation (false negative),
        scan flags compliant config as violation (false positive), scan performance on 10,000 assets,
        agentless scan on locked-down firewall, scan of cloud assets

        ALERTING: Alert fires on new violation, no alert on exception, alert routing to correct owner,
        duplicate alert suppression, SIEM receives alert within SLA, escalation after timeout

        DASHBOARD: Score reflects real-time scan, drilldown shows correct assets,
        trend graph accurate, executive vs technical view, multi-tenant data isolation

        REMEDIATION: Ticket created on violation, score improves after fix, verification scan runs,
        SLA breach escalation, false remediation marked complete

        === COMMON EDGE CASES ===
        - Scan runs during system maintenance window — impact
        - Asset decommissioned but still appears in dashboard
        - Policy exception expires — violation should reappear
        - 10,000 simultaneous scan targets — performance
        - Cloud asset spun up mid-scan — included or missed
        - Custom policy with conflicting rules — which wins
        - Remediation script causes system instability
        - Score changes without any actual configuration change
        - Audit report generated during active scan — data consistency
        - Network partition during scan — partial results handling
    """,

    "MyVault": """
        PRODUCT: MyVault (Personal Password Vault / Enterprise Password Manager)
        VENDOR CONTEXT: Secure personal credential management for end users within
        an organization. Allows employees to store, manage, and share credentials securely.

        === CORE MODULES ===

        1. VAULT & CREDENTIAL STORAGE
           - Encrypted credential storage (AES-256 at rest)
           - Store types: username/password, credit card, secure notes, SSH keys, API keys
           - Folder/category organization
           - Tagging and search
           - Favorite/pin credentials
           - Custom fields per credential
           - Credential history (last N versions)
           - Import credentials from CSV, browser export, other managers
           - Export credentials (encrypted backup)
           - Bulk operations (move, delete, tag)

        2. MASTER PASSWORD & AUTHENTICATION
           - Master password known only to user (zero-knowledge architecture)
           - Master password never stored or transmitted in plain text
           - PBKDF2 / bcrypt key derivation for master password
           - Master password strength enforcement
           - Master password hint (no actual password stored)
           - Emergency access request (trusted contact can request access)
           - Master password reset via identity verification
           - MFA on vault login (TOTP, hardware key, push notification)
           - Biometric unlock (fingerprint, face ID on mobile)
           - PIN unlock for quick access

        3. AUTO-FILL & BROWSER INTEGRATION
           - Browser extension for Chrome, Firefox, Edge
           - Auto-detect login forms and suggest credentials
           - Auto-fill username and password
           - Auto-submit option
           - Multiple accounts per website handling
           - Phishing protection (only fills on correct domain)
           - Never auto-fill on HTTP sites (HTTPS only)
           - Custom auto-fill rules per site
           - Mobile app auto-fill integration (iOS, Android)

        4. PASSWORD GENERATOR
           - Configurable length (8-128 characters)
           - Character set options (uppercase, lowercase, numbers, symbols)
           - Exclude ambiguous characters option
           - Pronounceable password option
           - Passphrase generator (word-based)
           - Password strength meter
           - Generated password history
           - One-click copy without displaying

        5. SECURE SHARING
           - Share individual credentials with specific users
           - Share folder/collection with team
           - Read-only vs edit sharing permissions
           - Time-limited sharing (auto-expires)
           - Recipient gets notification
           - Shared credential — owner can revoke anytime
           - Shared credential — recipient cannot re-share
           - Share via secure link (one-time access)
           - Organization-wide shared vault (admin managed)

        6. SECURITY FEATURES
           - Vault lock on inactivity timeout (configurable)
           - Auto-lock when browser/app closes
           - Clipboard auto-clear after N seconds
           - Password health check (weak, reused, old, breached)
           - Have I Been Pwned integration (breach detection)
           - Security score dashboard
           - Two-factor authentication enforcement by admin
           - Screen capture protection on mobile
           - Jailbreak/root detection on mobile

        7. ADMIN & ENTERPRISE FEATURES
           - Centralized admin console
           - Force MFA policy across all users
           - Inactivity timeout policy enforcement
           - Restrict sharing outside organization
           - Monitor vault health scores across users
           - Offboarding: transfer credentials on user departure
           - SSO integration for vault login
           - Directory sync (AD/LDAP) for user provisioning
           - Audit logs for admin actions
           - Data residency and sovereignty controls

        === KEY TEST SCENARIOS ===
        AUTHENTICATION: Master password wrong N times lockout, MFA device lost recovery,
        biometric spoofing attempt, session token reuse after logout, SSO bypass to vault

        STORAGE: Credential save with special characters, import 10,000 credentials performance,
        export encrypted backup and restore, custom field with max characters, duplicate URL handling

        AUTO-FILL: Fill on correct domain, no fill on lookalike phishing domain,
        HTTP site fill blocked, multiple accounts same domain, auto-fill in iframe

        SHARING: Share then revoke — recipient access immediately denied,
        read-only share — edit blocked, time-expired share no longer accessible,
        re-share attempt by recipient blocked, shared credential password changed by owner

        SECURITY: Vault lock after inactivity, clipboard cleared after timeout,
        breach alert for compromised password, weak password flagged, screen recording blocked

        === COMMON EDGE CASES ===
        - Master password forgotten with no recovery method set up
        - User account deactivated while vault has shared credentials
        - Import CSV with malformed data (XSS in credential name)
        - Auto-fill triggered on custom enterprise app (not a browser)
        - Two users share same credential — owner changes password — recipient sees new?
        - Vault accessed from new country — suspicious login alert
        - Credential shared via link — link forwarded to unauthorized person
        - MFA app uninstalled — cannot login — recovery flow
        - Admin forces password reset — does vault master password reset too?
        - Offline access to vault — cached credentials security
        - Device stolen — remote vault wipe capability
        - Browser extension update breaks auto-fill — rollback
    """
}

def generate_test_cases(product, feature, test_type, count, doc_text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    product_context = PRODUCT_KNOWLEDGE.get(product, "")

    type_instruction = (
        "Mix of Functional, Security, Negative, Boundary, Regression."
        if test_type == "all"
        else f"Focus only on {test_type} test cases."
    )

    from datetime import datetime
    today = datetime.now().strftime('%d/%m/%Y')

    prompt = f"""You are a Senior QA Engineer and Security Tester with expertise in cybersecurity products.

=== PRODUCT KNOWLEDGE ===
{product_context}

=== FEATURE TO TEST ===
{feature}

=== DOCUMENT CONTENT ===
{doc_text if doc_text else "No document uploaded. Use product knowledge above."}

=== INSTRUCTIONS ===
- Think like both an attacker and a tester
- Generate exactly {count} test cases
- Test type: {type_instruction}
- Cover: authentication, authorization, session management, audit logging, encryption, privilege escalation
- Make steps specific enough for a junior tester to execute
- Include both positive AND negative scenarios
- Make test data realistic

=== OUTPUT FORMAT ===
Return ONLY a valid JSON array. No explanation. No markdown. No backticks.
Each object must have exactly these keys:
- "serial": number starting from 1
- "date": "{today}"
- "suite_id": like "TS-{product.upper()}-001"
- "tc_id": like "TC-{product.upper()}-001" increment for each
- "objective": one sentence what this test proves
- "preconditions": what must be set up before running
- "steps": numbered steps as a single string
- "test_data": actual input values to use
- "expected_result": exact expected outcome
- "actual_result": ""
- "status": ""
- "remarks": ""

Start response with [ and end with ]"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Clean if AI adds markdown
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    test_cases = json.loads(raw)
    return test_cases