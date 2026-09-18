import html
import io
import textwrap

from telegram import InputFile, Update
from telegram.ext import ContextTypes

from gemini import generate_diagram_spec


def render_svg(spec):
    title = html.escape(str(spec.get("title", "NEET Biology Diagram")))
    nodes = spec.get("nodes", [])[:9]
    edges = spec.get("edges", [])
    width = 760
    node_width = 520
    node_height = 78
    left = (width - node_width) // 2
    top = 105
    gap = 58
    positions = {}
    for index, node in enumerate(nodes):
        positions[str(node.get("id", f"n{index + 1}"))] = (left, top + index * (node_height + gap))
    height = top + max(1, len(nodes)) * (node_height + gap) + 70

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#4778d0"/></marker></defs>',
        '<rect width="100%" height="100%" rx="22" fill="#f8fbff"/>',
        f'<text x="{width / 2}" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="25" font-weight="700" fill="#172b4d">{title}</text>',
    ]

    for edge in edges:
        source = positions.get(str(edge.get("from")))
        target = positions.get(str(edge.get("to")))
        if not source or not target:
            continue
        x = source[0] + node_width / 2
        y1 = source[1] + node_height
        y2 = target[1]
        parts.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#4778d0" stroke-width="3" marker-end="url(#arrow)"/>')
        label = html.escape(str(edge.get("label", "")))
        if label:
            parts.append(f'<text x="{x + 10}" y="{(y1 + y2) / 2}" font-family="Arial, sans-serif" font-size="13" fill="#5b6b84">{label}</text>')

    for index, node in enumerate(nodes):
        node_id = str(node.get("id", f"n{index + 1}"))
        x, y = positions[node_id]
        fill = "#eaf2ff" if index % 2 == 0 else "#fff0e9"
        stroke = "#4778d0" if index % 2 == 0 else "#e07b54"
        parts.append(f'<rect x="{x}" y="{y}" width="{node_width}" height="{node_height}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        label_lines = textwrap.wrap(str(node.get("label", "")), width=47)[:2]
        for line_index, line in enumerate(label_lines):
            safe_line = html.escape(line)
            parts.append(f'<text x="{x + node_width / 2}" y="{y + 33 + line_index * 20}" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="600" fill="#20334f">{safe_line}</text>')

    parts.append('</svg>')
    return "".join(parts).encode("utf-8")


async def diagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args).strip()
    if not topic:
        await update.message.reply_text("उदाहरण: /diagramaar परागण और निषेचन")
        return
    await update.message.reply_text("Educational diagram तैयार हो रहा है...")
    try:
        spec = generate_diagram_spec(topic)
        svg = render_svg(spec)
        await update.message.reply_document(
            document=InputFile(io.BytesIO(svg), filename="neet-diagram.svg"),
            caption="यह आपके topic का generated educational diagram है।",
        )
    except Exception as error:
        await update.message.reply_text(f"Diagram generate नहीं हो पाया: {error}")
