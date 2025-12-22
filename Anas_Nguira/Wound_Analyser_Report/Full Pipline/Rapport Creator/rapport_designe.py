# === DÉPLACÉ EN HAUT DU FICHIER (juste après tes imports) ===
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import json
import uuid
from datetime import datetime
import os

# Styles (une seule fois au démarrage)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleBlue', fontSize=26, leading=32, textColor=colors.HexColor("#1d4ed8"), alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle(name='Subtitle', fontSize=18, textColor=colors.HexColor("#1e40af"), alignment=TA_CENTER, spaceAfter=30))
styles.add(ParagraphStyle(name='Header', fontSize=14, leading=18, textColor=colors.HexColor("#1e40af"), spaceBefore=20))
styles.add(ParagraphStyle(name='Body', fontSize=11, leading=16, spaceAfter=12))


# === FONCTION DE RAPPORT BEAU (corrigée) ===
async def generate_beautiful_report(
    analysis_json: dict,
    original_filename: str,
    report_chain,
    original_image_path: str
) -> str:
    report_id = uuid.uuid4().hex[:8]
    pdf_path = f"rapport_dermatologie_{report_id}.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    story = []

    # === EN-TÊTE ===
    story.append(Paragraph("Service de Dermatologie Numérique", styles['TitleBlue']))
    story.append(Paragraph("Rapport d'analyse automatisée de plaie", styles['Subtitle']))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>Date :</b> {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}", styles['Body']))
    story.append(Paragraph(f"<b>Fichier analysé :</b> {original_filename}", styles['Body']))
    story.append(Spacer(1, 30))

    # === TABLEAU DES POURCENTAGES ===
    data = [
        ["Type de tissu", "Pourcentage", "Signification"],
        ["Fibrine (rouge)", f"{analysis_json['analysis']['fibrin_red']:.1f} %", "Tissu nécrotique"],
        ["Granulation (vert)", f"{analysis_json['analysis']['granulation_green']:.1f} %", "Tissu de réparation"],
        ["Cal (bleu)", f"{analysis_json['analysis']['callus_blue']:.1f} %", "Cicatrisation avancée"],
        ["Fond / peau saine", f"{analysis_json['analysis']['background']:.1f} %", "Zone non lésée"],
    ]

    table = Table(data, colWidths=[7*cm, 3*cm, 6*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e40af")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 13),
        ('ALIGN', (1,1), (1,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f0f9ff")),
        ('GRID', (0,0), (-1,-1), 1.5, colors.HexColor("#0ea5e9")),
        ('BOX', (0,0), (-1,-1), 2, colors.HexColor("#1e40af")),
        ('ROUNDEDCORNERS', [15, 15, 15, 15]),
    ]))
    story.append(table)
    story.append(Spacer(1, 30))

    # === ANALYSE CLINIQUE IA ===
    try:
        report_text = report_chain.invoke({
            "analysis_json": json.dumps(analysis_json, indent=2, ensure_ascii=False)
        })
    except:
        report_text = "Analyse clinique en cours de génération..."

    story.append(Paragraph("<b>Analyse clinique détaillée :</b>", styles['Header']))
    for para in report_text.split('\n\n'):
        if para.strip():
            story.append(Paragraph(para.replace('\n', '<br/>'), styles['Body']))
    story.append(Spacer(1, 30))

    # === IMAGE ORIGINALE SEULE (TRÈS PROPRE) ===
    story.append(Paragraph("<b>Image de la plaie analysée :</b>", styles['Header']))
    story.append(Spacer(1, 15))

    if os.path.exists(original_image_path):
        try:
            # Image centrée, belle taille
            img = RLImage(original_image_path, width=14*cm, height=14*cm)
            img.hAlign = 'CENTER'
            story.append(img)
        except Exception as e:
            story.append(Paragraph("Impossible d'afficher l'image.", styles['Body']))
    else:
        story.append(Paragraph("Image originale non trouvée.", styles['Body']))

    story.append(Spacer(1, 40))

    # === PIED DE PAGE ===
    story.append(Paragraph("Rapport généré automatiquement par <b>MedOrient AI</b>", styles['Body']))
    story.append(Paragraph("École Supérieure Privée d'Ingénierie et de Technologies – ESPRIT © 2025", styles['Body']))

    # Génération du PDF
    doc.build(story)
    return pdf_path