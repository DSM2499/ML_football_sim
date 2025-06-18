from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "EPL Simulation Report", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        self.ln(10)
    
    def add_image_with_title(self, title, image_path, w = 180, h = 0):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.image(image_path, w=w, h=h)
        self.ln(10)
    
    def add_paragraph(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, text)
        self.ln(5)

pdf = PDFReport()
pdf.add_page()

# Title summary
pdf.add_paragraph("This report summarizes the results of 10,000 EPL season simulations using a Poisson-based goal model. Each simulation predicts final league standings by sampling scorelines based on predicted expected goals.")

# Add Title Odds Chart
pdf.add_image_with_title("Top 10 Teams by Title Probability", "data/visuals/title_odds.png")

# Add Volatility Chart
pdf.add_image_with_title("Top 10 Most Volatile Teams (Finish Position Std Dev)", "data/visuals/volatility_chart.png")

# Save the report
report_path = "data/epl_simulation_report.pdf"
pdf.output(report_path)