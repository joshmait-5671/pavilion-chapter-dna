#!/usr/bin/env python3
"""Generate AI Buddy Program overview PDF for internal sharing."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)

# Colors
DARK = HexColor("#0a0a0a")
PINK = HexColor("#E8006F")
GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#F5F5F5")
WHITE = HexColor("#FFFFFF")

def build_pdf():
    doc = SimpleDocTemplate(
        "/Users/joshmait/Desktop/Claude/AI Buddy Program/AI-Buddy-Program-Overview.pdf",
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=28,
        textColor=DARK,
        spaceAfter=4,
        fontName="Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=12,
        textColor=GRAY,
        spaceAfter=20,
        fontName="Helvetica",
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=DARK,
        spaceBefore=24,
        spaceAfter=8,
        fontName="Helvetica-Bold",
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        textColor=DARK,
        spaceAfter=6,
        fontName="Helvetica",
        leading=16,
    )
    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=body_style,
        leftIndent=20,
        bulletIndent=8,
        spaceAfter=4,
    )
    bold_body = ParagraphStyle(
        "BoldBody",
        parent=body_style,
        fontName="Helvetica-Bold",
    )
    small_gray = ParagraphStyle(
        "SmallGray",
        parent=body_style,
        fontSize=9,
        textColor=GRAY,
    )
    tier_label = ParagraphStyle(
        "TierLabel",
        parent=body_style,
        fontSize=10,
        textColor=GRAY,
        leftIndent=20,
        spaceAfter=3,
    )

    story = []

    # Title
    story.append(Paragraph("AI Buddy Program", title_style))
    story.append(Paragraph("Pavilion  |  Internal Overview  |  March 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#E0E0E0")))
    story.append(Spacer(1, 12))

    # What It Is
    story.append(Paragraph("What It Is", heading_style))
    story.append(Paragraph(
        "A peer-to-peer matching program that pairs go-to-market professionals with an AI buddy "
        "at a similar company stage and function. The goal: learn from someone facing the same "
        "challenges you are, with no hierarchy and no pressure.",
        body_style
    ))

    # Who It's For
    story.append(Paragraph("Who It's For", heading_style))
    story.append(Paragraph(
        "\xe2\x80\xa2  <b>Primary:</b> Pavilion members who don't know this exists yet",
        bullet_style
    ))
    story.append(Paragraph(
        "\xe2\x80\xa2  <b>Secondary:</b> Non-members as a prospect engagement tool (path to membership built in)",
        bullet_style
    ))

    # Matching Criteria
    story.append(Paragraph("Matching Criteria", heading_style))
    story.append(Paragraph("Every match requires the first two. The rest improve match quality.", body_style))
    story.append(Spacer(1, 6))

    match_data = [
        ["Criteria", "Required?", "Details"],
        ["Function", "Yes", "Same function always (Sales, Marketing, CS, etc.)"],
        ["Company Revenue", "Yes", "<$10M  |  $10-25M  |  $25-50M  |  $50M+"],
        ["Location", "No", "Same city ideal, same timezone as fallback"],
        ["Engagement Style", "No", "Async Slack, weekly calls, share resources, accountability"],
        ["AI Experience", "No", "Matched as peers at the same level"],
    ]
    match_table = Table(match_data, colWidths=[1.5 * inch, 1 * inch, 3.5 * inch])
    match_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#F0F0F0")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#E0E0E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(match_table)

    # Tiered Fallback
    story.append(Paragraph("Tiered Fallback (5 Business Days)", heading_style))
    story.append(Paragraph(
        "When someone signs up, we scan for the best match immediately and progressively "
        "relax criteria over 5 days to ensure everyone gets matched within a business week.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Day 1:</b>  Perfect match (all criteria hit)", tier_label))
    story.append(Paragraph("<b>Day 2:</b>  Relax location to timezone instead of city", tier_label))
    story.append(Paragraph("<b>Day 3:</b>  Allow adjacent AI experience level", tier_label))
    story.append(Paragraph("<b>Day 5:</b>  Function + revenue stage only", tier_label))
    story.append(Paragraph("<b>No match:</b>  \"We're finding the right person\" email goes out, re-scans on each new signup", tier_label))

    # Lifecycle
    story.append(Paragraph("Lifecycle", heading_style))
    story.append(Paragraph(
        "The 8-week cycle is a checkpoint, not a breakup. Buddies can stay together indefinitely.",
        body_style
    ))
    story.append(Spacer(1, 6))

    life_data = [
        ["When", "What Happens", "Action"],
        ["Match Made", "Personalized intro email connects both people", "Send a Slack message to your buddy"],
        ["Week 1", "\"Did you connect?\"", "Reply yes / not yet / need help"],
        ["Week 4", "\"How's it going? Rate 1-5\"", "Quick pulse check"],
        ["Week 8", "\"Keep, switch, or add?\"", "Keep buddy / get new / add a second"],
        ["Quarterly", "Pulse check for long-term pairs", "Same options as Week 8"],
    ]
    life_table = Table(life_data, colWidths=[1.2 * inch, 2.5 * inch, 2.3 * inch])
    life_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#F0F0F0")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#E0E0E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(life_table)

    # Key Decisions
    story.append(Paragraph("Key Decisions", heading_style))
    story.append(Paragraph("\xe2\x80\xa2  Buddies can have <b>multiple buddies</b> (2nd, 3rd) simultaneously", bullet_style))
    story.append(Paragraph("\xe2\x80\xa2  Non-members get a <b>tasteful membership nudge</b> at Week 8", bullet_style))
    story.append(Paragraph("\xe2\x80\xa2  <b>Unresponsive matches</b> flagged for human review after 14 days", bullet_style))
    story.append(Paragraph("\xe2\x80\xa2  Human reviews matches for <b>first 2-3 months</b>, then fully automated", bullet_style))
    story.append(Paragraph("\xe2\x80\xa2  <b>Launch trigger:</b> 100 waitlist signups", bullet_style))

    # Automation
    story.append(Paragraph("Automation", heading_style))
    story.append(Paragraph(
        "Once launched, the program runs with ~30 minutes/week of human oversight. "
        "Matching, intro emails, check-ins, feedback collection, and rematching are all automated. "
        "The only human touchpoints are reviewing match quality (early on) and handling edge cases.",
        body_style
    ))

    # Links
    story.append(Paragraph("Links", heading_style))
    story.append(Paragraph("\xe2\x80\xa2  <b>Waitlist page:</b> https://shimmering-mousse-a683b3.netlify.app", bullet_style))
    story.append(Paragraph("\xe2\x80\xa2  <b>Dashboard:</b> https://shimmering-mousse-a683b3.netlify.app/dashboard.html", bullet_style))
    story.append(Paragraph("\xe2\x80\xa2  <b>Google Sheet:</b> https://docs.google.com/spreadsheets/d/1nXqkzcW2HMA04jS4zjfB2Y7DT0RTjUdtVZY4XM1WFoY", bullet_style))

    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#E0E0E0")))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Prepared by Josh Mait  |  Head of Marketing, Pavilion", small_gray))

    doc.build(story)
    print("PDF generated: AI-Buddy-Program-Overview.pdf")


if __name__ == "__main__":
    build_pdf()
