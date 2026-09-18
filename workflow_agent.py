import uuid


# =========================================================
# Workflow Agent
# =========================================================

def process_business_request(question: str) -> str:
    """
    Process common employee business requests.

    This is a simulated workflow engine.
    No real company system is modified.
    """

    question_lower = question.lower().strip()


    # =====================================================
    # 1. Travel reimbursement issue
    # =====================================================

    travel_keywords = [
        "travel reimbursement",
        "travel expense",
        "reimbursement rejected",
        "reimbursement was rejected",
        "hotel receipt",
        "travel claim"
    ]

    if any(
        keyword in question_lower
        for keyword in travel_keywords
    ):

        ticket_id = (
            "EXP-"
            + str(uuid.uuid4())[:8].upper()
        )

        # -----------------------------------------------
        # Missing receipt
        # -----------------------------------------------

        if (
            "missing receipt" in question_lower
            or "forgot the hotel receipt" in question_lower
            or "forgot hotel receipt" in question_lower
            or "without receipt" in question_lower
        ):

            return f"""
Process: Travel Reimbursement

Issue:
Required hotel receipt is missing.

Required Action:
Upload the valid hotel receipt and resubmit the
expense claim through the company expense management system.

Status:
Pending employee action

Simulated Ticket:
{ticket_id}
""".strip()


        # -----------------------------------------------
        # Reimbursement rejected
        # -----------------------------------------------

        if (
            "rejected" in question_lower
            or "declined" in question_lower
        ):

            return f"""
Process: Travel Reimbursement

Issue:
The reimbursement request has been rejected.

Required Action:
Review the expense claim, verify that all required
supporting documents are attached, and contact the
Finance team if clarification is required.

Status:
Pending review

Simulated Ticket:
{ticket_id}
""".strip()


        # -----------------------------------------------
        # General travel claim
        # -----------------------------------------------

        return f"""
Process: Travel Reimbursement

Action:
Review the travel expense claim and ensure that all
required receipts and supporting documents are attached.

Status:
Pending employee review

Simulated Ticket:
{ticket_id}
""".strip()


    # =====================================================
    # 2. Password reset request
    # =====================================================

    if (
        "password" in question_lower
        and (
            "forgot" in question_lower
            or "reset" in question_lower
            or "locked" in question_lower
        )
    ):

        ticket_id = (
            "IT-"
            + str(uuid.uuid4())[:8].upper()
        )

        return f"""
Process: IT Password Assistance

Issue:
Employee requires password assistance.

Required Action:
Contact the IT Support team and follow the company's
approved password recovery procedure.

Status:
Pending IT Support

Simulated Ticket:
{ticket_id}
""".strip()


    # =====================================================
    # 3. Lost company equipment
    # =====================================================

    if (
    "lost laptop" in question_lower
    or "laptop was lost" in question_lower
    or "company laptop was lost" in question_lower
    or "lost company laptop" in question_lower
    or "lost device" in question_lower
    or "device was lost" in question_lower
    or "company device was lost" in question_lower
    or "stolen laptop" in question_lower
    or "laptop was stolen" in question_lower
    or "company laptop was stolen" in question_lower
    or "stolen device" in question_lower
    or "device was stolen" in question_lower
):
        ticket_id = (
            "IT-"
            + str(uuid.uuid4())[:8].upper()
        )

        return f"""
Process: Lost Company Equipment

Issue:
A company-owned device has been reported as lost or stolen.

Required Action:
Report the incident to the IT Support team as soon as possible.

Status:
High-priority IT action

Simulated Ticket:
{ticket_id}
""".strip()


    # =====================================================
    # 4. Generic workflow request
    # =====================================================

    if (
        "request" in question_lower
        or "issue" in question_lower
        or "problem" in question_lower
        or "rejected" in question_lower
    ):

        ticket_id = (
            "REQ-"
            + str(uuid.uuid4())[:8].upper()
        )

        return f"""
Process: General Employee Request

Issue:
The request requires further review.

Required Action:
Provide the relevant supporting information and
contact the appropriate company team.

Status:
Pending review

Simulated Ticket:
{ticket_id}
""".strip()


    # =====================================================
    # 5. Unsupported workflow
    # =====================================================

    return (
        "The workflow agent could not identify a supported "
        "business process for this request."
    )
