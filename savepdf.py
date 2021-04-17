import pdfkit
from flask import send_file
def downpdf(string):
    pdfkit.from_string(string, 'Crossword.pdf')
    