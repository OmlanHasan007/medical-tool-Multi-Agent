"""
PDF Report Generator for the Medical Agent.
Exports the current chat session into a clean, formatted PDF report.

Requires:  pip install reportlab
"""

from __future__ import annotations
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

# ── Colour palette ──────────────────────────────────────────────────────────
PRIMARY   = colors.HexColor("#1a6b9a")
SECONDARY = colors.HexColor("#2ecc71")
LIGHT_BG  = colors.HexColor("#f0f4f8")
TEXT      = colors.HexColor("#2d3748")
MUTED     = colors.HexColor("#718096")


def _styles():
    base = getSampleStyleSheet()

    title = ParagraphStyle(
        "ReportTitle",
        parent=base["Title"],
        textColor=PRIMARY,
        fontSize=22,
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=base["Normal"],
        textColor=MUTED,
        fontSize=10,
        spaceAfter=16,
        alignment=TA_CENTER,
    )
    section = ParagraphStyle(
        "Section",
        parent=base["Heading2"],
        textColor=PRIMARY,
        fontSize=13,
        spaceBefore=14,
        spaceAfter=4,
    )
    user_label = ParagraphStyle(
        "UserLabel",
        parent=base["Normal"],
        textColor=SECONDARY,
        fontSize=9,
        fontName="Helvetica-Bold",
        spaceAfter=2,
    )
    agent_label = ParagraphStyle(
        "AgentLabel",
        parent=base["Normal"],
        textColor=PRIMARY,
        fontSize=9,
        fontName="Helvetica-Bold",
        spaceAfter=2,
    )
    body = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        textColor=TEXT,
        fontSize=10,
        leading=15,
        spaceAfter=10,
    )
    footer = ParagraphStyle(
        "Footer",
        parent=base["Normal"],
        textColor=MUTED,
        fontSize=8,
        alignment=TA_CENTER,
    )
    return title, subtitle, section, user_label, agent_label, body, footer


def generate_report(
    chat_history: List[Dict[str, str]],
    session_summary: str = "",
    filename: str = "",
) -> str:
    """
    Build a PDF from the agent chat history.

    Parameters
    ----------
    chat_history : list of {"role": "user"|"assistant", "content": str}
    session_summary : optional one-paragraph AI-generated summary
    filename : output filename (auto-generated if empty)

    Returns
    -------
    str  – absolute path to the created PDF
    """
    if not filename:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"medical_report_{ts}.pdf"

    output_path = EXPORT_DIR / filename
    title_s, subtitle_s, section_s, user_s, agent_s, body_s, footer_s = _styles()

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    story = []

    # ── Header ───────────────────────────────────────────────────────────────
    story.append(Paragraph("🧠 Multi-Tool Medical Agent", title_s))
    story.append(Paragraph(
        f"Session Report &nbsp;·&nbsp; {datetime.now().strftime('%B %d, %Y  %H:%M')}",
        subtitle_s,
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=14))

    # ── Summary (if provided) ─────────────────────────────────────────────────
    if session_summary:
        story.append(Paragraph("Session Summary", section_s))
        story.append(Paragraph(session_summary, body_s))
        story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_BG, spaceAfter=10))

    # ── Conversation ─────────────────────────────────────────────────────────
    story.append(Paragraph("Conversation Log", section_s))
    story.append(Spacer(1, 6))

    for i, msg in enumerate(chat_history, 1):
        role    = msg.get("role", "unknown")
        content = msg.get("content", "").strip()
        if not content:
            continue

        if role == "user":
            story.append(Paragraph(f"👤  You  (turn {i})", user_s))
        else:
            story.append(Paragraph(f"🤖  Medical Agent  (turn {i})", agent_s))

        # Wrap in a light-background table for visual separation
        cell = Paragraph(content.replace("\n", "<br/>"), body_s)
        bg   = LIGHT_BG if role == "user" else colors.white
        tbl  = Table([[cell]], colWidths=[14.5 * cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("BOX",        (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
            ("ROUNDEDCORNERS", [4]),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 6))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED, spaceBefore=16))
    story.append(Paragraph(
        "⚠️  This report is generated by an AI agent for informational purposes only. "
        "It is NOT a substitute for professional medical advice, diagnosis, or treatment.",
        footer_s,
    ))

    doc.build(story)
    return str(output_path.resolve())
