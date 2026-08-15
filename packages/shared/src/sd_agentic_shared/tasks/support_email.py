from pydantic import BaseModel, Field


class TicketDraft(BaseModel):
    summary: str
    reply: str
    policy_ok: str = Field(description="PASS or FAIL plus a short reason from the checker")


SUPPORT_EMAIL = """
hi so i ordered wireless headphones last tuesday, i think the order was
#A-18422 or maybe A-18423, anyway they still havent shown up and the tracking
on the site just says "processing" which is useless. i already paid $89 and
i want a full refund today or im going to chargeback. also you guys charged
me twice?? my wife said she saw another $89 pending. fix this now.
""".strip()

SHIPPING_EMAIL = """
hey my package of the blue water bottle (order A-18423) still isnt here.
site said shipped yesterday. can you tell me where it is? i do NOT want a
refund i just want the bottle.
""".strip()

CANCEL_EMAIL = """
please cancel order A-18422. i ordered the headphones by accident and they
have not shipped yet according to the site. thanks.
""".strip()

BILLING_EMAIL = """
you billed me $12.99 for a warranty I never bought on order A-18422.
remove that charge. i already paid for the headphones.
""".strip()

SAMPLE_EMAILS: dict[str, str] = {
    "mixed": SUPPORT_EMAIL,
    "shipping": SHIPPING_EMAIL,
    "cancel": CANCEL_EMAIL,
    "billing": BILLING_EMAIL,
}

MEMORY_FOLLOWUP_1 = """
its me again about the headphones. you should already have my order numbers.
still no tracking. i told you i paid 89. what is the status??
""".strip()

MEMORY_FOLLOWUP_2 = """
ok forget the refund. just tell me if A-18422 shipped. you already know this
order from earlier.
""".strip()

MEMORY_THREAD: list[str] = [SUPPORT_EMAIL, MEMORY_FOLLOWUP_1, MEMORY_FOLLOWUP_2]
