"""In-memory support-policy chunks for the RAG pattern. Not a vector store."""

from pydantic import BaseModel


class RagChunk(BaseModel):
    id: str
    title: str
    text: str


RAG_CHUNKS: list[RagChunk] = [
    RagChunk(
        id="refund-limit",
        title="Refund amount limit",
        text=(
            "Agents may issue refunds of $50 or less. Refunds over $50 need a human manager. "
            "Never promise a larger refund in the customer email."
        ),
    ),
    RagChunk(
        id="duplicate-charge",
        title="Duplicate charges",
        text=(
            "If a customer reports a duplicate pending charge, do not confirm a second capture. "
            "Say we will check the payment record. Do not invent amounts."
        ),
    ),
    RagChunk(
        id="shipping-processing",
        title="Processing orders have no tracking",
        text=(
            "Orders still in processing have no tracking number yet. Do not invent tracking. "
            "Ask for the order id if it is missing."
        ),
    ),
    RagChunk(
        id="shipping-shipped",
        title="Shipped orders include tracking",
        text=(
            "Once an order is shipped, the site shows a tracking number. "
            "Only quote tracking that a lookup returned; never guess."
        ),
    ),
    RagChunk(
        id="cancel-processing",
        title="Cancel before ship",
        text=(
            "Processing orders can be cancelled. Shipped orders cannot be cancelled; "
            "offer a return instead."
        ),
    ),
    RagChunk(
        id="tone",
        title="Tone and blame",
        text=(
            "Be concise and professional. Do not blame the customer. "
            "Do not invent order status."
        ),
    ),
    RagChunk(
        id="chargeback",
        title="Chargeback threats",
        text=(
            "If a customer mentions a chargeback, stay calm, do not argue, and do not "
            "accelerate a refund past policy. Offer the next in-policy step."
        ),
    ),
]
