import jinja2
import pdfkit
from datetime import datetime

# date_completed = datetime.now().strftime("%Y-%m-%d")

# name = "Frank Ocean"
# general = "General blah blah blah"
# symptoms = "Symptoms blah blah blah"
# exposure = "Exposure blah blah blah"
# ai_comments = "AI Comments blah blah blah"
# risk_level_summary = "Risk Level Summary blah blah blah"

# context = {'name': name, 'date_completed': date_completed, 'general': general, 'symptoms': symptoms, 'exposure': exposure, 'ai_comments': ai_comments, 'risk_level_summary': risk_level_summary}

# template_loader = jinja2.FileSystemLoader('./')
# template_env = jinja2.Environment(loader=template_loader)

# html_template = 'doctor_report.html'
# template = template_env.get_template(html_template)
# output_text = template.render(context)

# config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
# output_pdf = 'doctor_report.pdf'
# pdfkit.from_string(output_text, output_pdf, configuration=config, options={"enable-local-file-access": ""})

def generate_report(name, general, symptoms, exposure, ai_comments, risk_level_summary):
    date_completed = datetime.now().strftime("%Y-%m-%d")
    context = {'name': name, 'date_completed': date_completed, 'general': general, 'symptoms': symptoms, 'exposure': exposure, 'ai_comments': ai_comments, 'risk_level_summary': risk_level_summary}

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'doctor_report_template.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    output_pdf = 'doctor_report_2.pdf'
    pdfkit.from_string(output_text, output_pdf, configuration=config, options={"enable-local-file-access": ""})

    return output_pdf

generate_report("Frank Ocean 2", "General blah blah blah blah", "Symptoms blah blah blah", "Exposure blah blah blah", "AI Comments blah blah blah", "Risk Level Summary blah blah blah")