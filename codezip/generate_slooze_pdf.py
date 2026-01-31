#!/usr/bin/env python3
"""
SLOOZE DATA SCIENCE CHALLENGE - PDF DOCUMENTATION GENERATOR
===========================================================

This script generates a comprehensive PDF documentation for the Slooze 
Inventory Optimization & Supply Chain Analysis project.

Run this in Google Colab or any Python environment with the required dependencies.

Author: Data Science Team
Date: February 2026
"""

# =============================================================================
# STEP 1: INSTALL REQUIRED LIBRARIES
# =============================================================================
# Run this first if you haven't installed the dependencies:
# !pip install fpdf2 pandas numpy matplotlib seaborn plotly prophet scikit-learn kagglehub -q

from fpdf import FPDF
from datetime import datetime
import os

# =============================================================================
# STEP 2: DEFINE THE PDF CLASS WITH CUSTOM HEADER/FOOTER
# =============================================================================

class SloozePDF(FPDF):
    """
    Custom PDF class with professional header and footer styling
    for Slooze Data Science Challenge documentation.
    """
    
    def header(self):
        """Add header with document title on each page (except cover)"""
        # Skip header on first page (cover)
        if self.page_no() == 1:
            return
        
        # Set font for header
        self.set_font('Arial', 'B', 9)
        self.set_text_color(102, 102, 102)  # Gray color
        
        # Add header text
        self.cell(0, 8, 'Slooze Data Science Challenge - Technical Documentation', 
                  0, 0, 'C')
        
        # Add line below header
        self.set_draw_color(200, 200, 200)
        self.line(15, self.get_y() + 5, 195, self.get_y() + 5)
        
        # Line break
        self.ln(8)
    
    def footer(self):
        """Add footer with page number on each page (except cover)"""
        # Skip footer on first page (cover)
        if self.page_no() == 1:
            return
        
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        
        # Set font for footer
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        
        # Add page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title, level=1):
        """Add a chapter/section title with appropriate styling"""
        if level == 1:
            # Main chapter title (H1)
            self.set_font('Arial', 'B', 16)
            self.set_text_color(26, 26, 46)  # Dark blue
            self.cell(0, 12, title, 0, 1, 'L')
            
            # Add underline
            self.set_draw_color(233, 69, 96)  # Accent color
            self.set_line_width(0.5)
            self.line(15, self.get_y(), 195, self.get_y())
            
            self.ln(5)
            
        elif level == 2:
            # Section title (H2)
            self.set_font('Arial', 'B', 13)
            self.set_text_color(22, 33, 62)  # Slightly lighter
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(2)
            
        else:
            # Subsection title (H3)
            self.set_font('Arial', 'B', 11)
            self.set_text_color(51, 51, 51)
            self.cell(0, 8, title, 0, 1, 'L')
            self.ln(1)
    
    def chapter_body(self, body):
        """Add body text with proper formatting"""
        self.set_font('Arial', '', 10)
        self.set_text_color(51, 51, 51)
        self.multi_cell(0, 6, body)
        self.ln()
    
    def bullet_list(self, items, bold_prefix=True):
        """Add a bullet point list"""
        self.set_font('Arial', '', 10)
        self.set_text_color(51, 51, 51)
        
        for item in items:
            # Check if item has a prefix to bold
            if bold_prefix and ':' in item:
                parts = item.split(':', 1)
                self.cell(5)  # Indent
                self.cell(5, 6, chr(149), 0, 0, 'L')  # Bullet
                self.set_font('Arial', 'B', 10)
                self.cell(self.get_string_width(parts[0] + ': '), 6, parts[0] + ':', 0, 0)
                self.set_font('Arial', '', 10)
                self.multi_cell(0, 6, parts[1])
            else:
                self.cell(5)  # Indent
                self.cell(5, 6, chr(149), 0, 0, 'L')  # Bullet
                self.multi_cell(0, 6, item)
        
        self.ln(2)
    
    def numbered_list(self, items):
        """Add a numbered list"""
        self.set_font('Arial', '', 10)
        self.set_text_color(51, 51, 51)
        
        for i, item in enumerate(items, 1):
            self.cell(5)  # Indent
            self.cell(10, 6, f'{i}.', 0, 0, 'L')
            self.multi_cell(0, 6, item)
        
        self.ln(2)
    
    def key_finding_box(self, title, content):
        """Add a highlighted key finding box"""
        # Save current position
        start_y = self.get_y()
        
        # Draw left border
        self.set_draw_color(233, 69, 96)  # Accent color
        self.set_line_width(1)
        self.line(15, start_y, 15, start_y + 25)
        
        # Add background (light gray)
        self.set_fill_color(250, 250, 250)
        self.rect(17, start_y, 178, 25, 'F')
        
        # Add title
        self.set_xy(20, start_y + 3)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(233, 69, 96)
        self.cell(0, 6, title, 0, 1)
        
        # Add content
        self.set_xy(20, start_y + 10)
        self.set_font('Arial', '', 10)
        self.set_text_color(51, 51, 51)
        self.multi_cell(170, 5, content)
        
        # Move to next position
        self.set_y(start_y + 28)
    
    def info_box(self, title, items):
        """Add an info box with bullet points"""
        # Add title
        self.set_font('Arial', 'B', 11)
        self.set_text_color(22, 33, 62)
        self.cell(0, 8, title, 0, 1)
        
        # Add items
        self.bullet_list(items, bold_prefix=True)
    
    def create_table(self, headers, data, col_widths=None):
        """Create a professional table"""
        # Default column widths if not provided
        if col_widths is None:
            col_widths = [40] * len(headers)
        
        # Header styling
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(248, 249, 250)
        self.set_text_color(51, 51, 51)
        
        # Draw header
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'L', True)
        self.ln()
        
        # Data styling
        self.set_font('Arial', '', 9)
        self.set_fill_color(255, 255, 255)
        
        # Draw data rows
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), 1, 0, 'L')
            self.ln()
        
        self.ln(3)


# =============================================================================
# STEP 3: CREATE THE PDF DOCUMENT
# =============================================================================

def create_slooze_documentation():
    """
    Generate the complete Slooze Data Science Challenge PDF documentation.
    
    Returns:
        str: Path to the generated PDF file
    """
    
    # Initialize PDF
    pdf = SloozePDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # ========================================================================
    # COVER PAGE
    # ========================================================================
    pdf.add_page()
    
    # Cover background styling
    pdf.set_fill_color(26, 26, 46)  # Dark blue background
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Accent bar at bottom
    pdf.set_fill_color(233, 69, 96)
    pdf.rect(0, 289, 210, 8, 'F')
    
    # Badge
    pdf.set_xy(65, 60)
    pdf.set_fill_color(233, 69, 96)
    pdf.rect(65, 60, 80, 10, 'F')
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(65, 63)
    pdf.cell(80, 6, 'DATA SCIENCE CHALLENGE', 0, 0, 'C')
    
    # Main title
    pdf.set_xy(15, 100)
    pdf.set_font('Arial', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(180, 15, 'Inventory Optimization &', 0, 1, 'C')
    pdf.cell(180, 15, 'Supply Chain Analysis', 0, 1, 'C')
    
    # Subtitle
    pdf.set_xy(15, 145)
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(180, 10, 'Slooze Take-Home Challenge', 0, 1, 'C')
    
    # Divider line
    pdf.set_draw_color(233, 69, 96)
    pdf.set_line_width(1)
    pdf.line(85, 175, 125, 175)
    
    # Meta information
    pdf.set_xy(15, 200)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(180, 8, 'Technical Documentation', 0, 1, 'C')
    pdf.cell(180, 8, 'Comprehensive Analysis Report', 0, 1, 'C')
    pdf.cell(180, 8, datetime.now().strftime('%B %Y'), 0, 1, 'C')
    
    # ========================================================================
    # TABLE OF CONTENTS
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('Table of Contents', level=1)
    
    toc_items = [
        ('1. Executive Summary', 3),
        ('2. Problem Statement & Objectives', 4),
        ('   2.1 Business Context', 4),
        ('   2.2 Core Objectives', 4),
        ('3. Dataset Overview', 5),
        ('4. Methodology', 6),
        ('   4.1 Phase 1: Data Exploration & Cleaning', 6),
        ('   4.2 Phase 2: ABC Analysis', 7),
        ('   4.3 Phase 2.2: Demand Forecasting', 8),
        ('   4.4 Phase 2.3: Reorder Point Analysis', 8),
        ('   4.5 Phase 2.4: Lead Time Analysis', 9),
        ('5. Key Results', 10),
        ('6. Assumptions & Limitations', 12),
        ('7. Business Recommendations', 13),
        ('8. How to Run the Code', 14),
        ('9. Conclusion', 15),
    ]
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(51, 51, 51)
    
    for item, page in toc_items:
        if item.startswith('   '):
            pdf.cell(10)  # Indent
            pdf.set_font('Arial', '', 10)
        else:
            pdf.set_font('Arial', 'B', 11)
        
        pdf.cell(150, 7, item.strip(), 0, 0)
        pdf.cell(0, 7, str(page), 0, 1, 'R')
    
    # ========================================================================
    # SECTION 1: EXECUTIVE SUMMARY
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('1. Executive Summary', level=1)
    
    pdf.chapter_body(
        "This analysis presents a comprehensive inventory optimization system for Slooze, "
        "a retail wine and spirits company operating across multiple locations. Using "
        "2.37 million purchase records, 1.05 million sales transactions, and inventory "
        "data from 2016, we implemented four core analytical frameworks to transform raw "
        "transactional data into actionable business intelligence."
    )
    
    pdf.chapter_title('Key Deliverables', level=2)
    
    deliverables = [
        "ABC Analysis: Classified 7,658 products by revenue contribution using the 80/20 rule",
        "Demand Forecasting: Built Facebook Prophet time-series models for top 5 A-Class products",
        "Reorder Point Analysis: Calculated optimal inventory triggers with 95% service level safety stock",
        "Lead Time Analysis: Evaluated 120 vendors across $321.9 million procurement spend"
    ]
    pdf.bullet_list(deliverables)
    
    pdf.key_finding_box(
        'Critical Finding',
        '80% of revenue comes from only 19.6% of products (A-Class), yet none of these '
        'critical products use Premium suppliers. This creates a significant supply chain '
        'vulnerability that requires immediate attention.'
    )
    
    # Metrics summary
    pdf.chapter_title('Summary Metrics', level=2)
    
    metrics_headers = ['Metric', 'Value']
    metrics_data = [
        ['Total Revenue Analyzed', '$33.1 Million'],
        ['Unique Products', '7,658'],
        ['Vendors Evaluated', '128'],
        ['Store Locations', '79'],
    ]
    pdf.create_table(metrics_headers, metrics_data, [80, 80])
    
    # ========================================================================
    # SECTION 2: PROBLEM STATEMENT
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('2. Problem Statement & Objectives', level=1)
    
    pdf.chapter_title('2.1 Business Context', level=2)
    
    pdf.chapter_body(
        "Slooze manages millions of transactions across sales, purchases, and inventory "
        "records spanning 79+ store locations. Traditional spreadsheet-based analysis is "
        "inadequate for this data volume, creating risks of:"
    )
    
    risks = [
        "Stockouts of high-revenue items leading to lost sales",
        "Excess inventory carrying costs tying up working capital",
        "Missed optimization opportunities from lack of data-driven insights",
        "Supplier inefficiencies going undetected"
    ]
    pdf.bullet_list(risks)
    
    pdf.chapter_title('2.2 Core Objectives', level=2)
    
    objectives_headers = ['Objective', 'Description', 'Success Metric']
    objectives_data = [
        ['Inventory Optimization', 'Determine ideal stock levels by category', 'Reduced stockouts + carrying costs'],
        ['Sales & Purchase Insights', 'Identify trends and supplier efficiency', 'Clear product/vendor segmentation'],
        ['Process Improvement', 'Optimize procurement and stock control', 'Data-driven reorder triggers'],
    ]
    pdf.create_table(objectives_headers, objectives_data, [50, 65, 55])
    
    pdf.chapter_title('Analytical Tasks Completed', level=2)
    
    tasks = [
        "ABC Analysis - Product classification by revenue contribution",
        "Demand Forecasting - Time-series prediction using Prophet",
        "Reorder Point Analysis - Inventory trigger calculations with safety stock",
        "Lead Time Analysis - Supplier performance evaluation"
    ]
    pdf.numbered_list(tasks)
    
    # ========================================================================
    # SECTION 3: DATASET OVERVIEW
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('3. Dataset Overview', level=1)
    
    pdf.chapter_title('Data Sources (6 Files)', level=2)
    
    dataset_headers = ['File Name', 'Size', 'Records', 'Purpose']
    dataset_data = [
        ['SalesFINAL12312016.csv', '127.86 MB', '1,048,575', 'Sales transactions'],
        ['PurchasesFINAL12312016.csv', '401.75 MB', '2,372,474', 'Purchase orders'],
        ['BegInvFINAL12312016.csv', '19.31 MB', '206,529', 'Beginning inventory'],
        ['EndInvFINAL12312016.csv', '21.00 MB', '224,489', 'Ending inventory'],
        ['InvoicePurchases12312016.csv', '591 KB', '5,543', 'Invoice records'],
        ['2017PurchasePricesDec.csv', '1.16 MB', '12,261', 'Price reference'],
    ]
    pdf.create_table(dataset_headers, dataset_data, [55, 30, 30, 55])
    
    pdf.chapter_title('Data Quality Summary', level=2)
    
    pdf.info_box('Dataset Characteristics', [
        'Date Range: January 1 - December 31, 2016 (with February anomaly)',
        'Geography: 79-81 store locations across multiple cities',
        'Products: ~7,658 unique SKUs',
        'Vendors: 128 significant suppliers (>10 purchase orders)',
        'Total Records: 3.87 million rows analyzed'
    ])
    
    # ========================================================================
    # SECTION 4: METHODOLOGY
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('4. Methodology', level=1)
    
    pdf.chapter_title('4.1 Phase 1: Data Exploration & Cleaning', level=2)
    
    pdf.chapter_body(
        "The dataset was automatically downloaded using KaggleHub (61.9 MB compressed). "
        "All 6 CSV files were loaded into pandas DataFrames with appropriate data type "
        "optimization for memory efficiency."
    )
    
    pdf.chapter_title('Data Cleaning Steps', level=3)
    
    cleaning_steps = [
        "Standardized date formats (PODate, ReceivingDate, SalesDate)",
        "Calculated derived metrics (LeadTime_Days, Revenue)",
        "Removed invalid lead times (negative or zero values)",
        "Converted 2,372,474 purchase records to datetime format",
        "Stripped whitespace from string columns",
        "Validated referential integrity across datasets"
    ]
    pdf.numbered_list(cleaning_steps)
    
    pdf.chapter_title('4.2 Phase 2: ABC Analysis', level=2)
    
    pdf.chapter_body(
        "Classify inventory by revenue contribution to prioritize management attention "
        "and allocate resources effectively."
    )
    
    pdf.chapter_title('Classification Criteria', level=3)
    
    abc_headers = ['Class', 'Criteria', 'Priority']
    abc_data = [
        ['A-Class', 'Top 80% cumulative revenue', 'High'],
        ['B-Class', '80-95% cumulative revenue', 'Medium'],
        ['C-Class', 'Bottom 5% cumulative revenue', 'Low'],
    ]
    pdf.create_table(abc_headers, abc_data, [30, 80, 50])
    
    pdf.chapter_title('4.3 Phase 2.2: Demand Forecasting', level=2)
    
    pdf.chapter_body(
        "Implemented Facebook Prophet models with daily and weekly seasonality, "
        "multiplicative seasonality mode, and 14-day forecast horizon. MAE and RMSE "
        "calculated for model validation."
    )
    
    pdf.chapter_title('4.4 Phase 2.3: Reorder Point Analysis', level=2)
    
    pdf.chapter_body(
        "ROP = (Average Daily Demand x Lead Time) + Safety Stock"
    )
    
    pdf.chapter_body(
        "Where Safety Stock = Z x Standard Deviation x sqrt(Lead Time)"
    )
    
    rop_headers = ['Parameter', 'Value', 'Description']
    rop_data = [
        ['Service Level', '95%', 'Z-score = 1.65 (industry standard)'],
        ['Lead Time', '7.3-7.6 days', 'Vendor-specific average'],
        ['Safety Stock', 'Variable', 'Based on demand variability'],
    ]
    pdf.create_table(rop_headers, rop_data, [40, 35, 75])
    
    pdf.chapter_title('4.5 Phase 2.4: Lead Time Analysis', level=2)
    
    vendor_headers = ['Classification', 'Lead Time', 'Std Dev', 'Risk']
    vendor_data = [
        ['Premium', '<= 7.7 days', '<= 2.2 days', 'Low'],
        ['Fast but Variable', '<= 7.7 days', '> 2.2 days', 'Medium'],
        ['Slow but Steady', '> 7.7 days', '<= 2.2 days', 'Low-Medium'],
        ['High Risk', '> 7.7 days', '> 2.2 days', 'High'],
    ]
    pdf.create_table(vendor_headers, vendor_data, [45, 35, 35, 25])
    
    # ========================================================================
    # SECTION 5: KEY RESULTS
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('5. Key Results', level=1)
    
    pdf.chapter_title('ABC Analysis Results', level=2)
    
    abc_results_headers = ['Category', 'Products', '% SKUs', 'Revenue', '% Revenue']
    abc_results_data = [
        ['A-Class', '1,502', '19.6%', '$26.51M', '80.0%'],
        ['B-Class', '1,813', '23.7%', '$4.97M', '15.0%'],
        ['C-Class', '4,343', '56.7%', '$1.66M', '5.0%'],
    ]
    pdf.create_table(abc_results_headers, abc_results_data, [25, 30, 25, 35, 30])
    
    pdf.chapter_title('Top 5 Revenue Products', level=2)
    
    top5_headers = ['Rank', 'Product', 'Revenue', '% of Total']
    top5_data = [
        ['1', 'Captain Morgan Spiced Rum', '$444,811', '1.34%'],
        ['2', 'Ketel One Vodka', '$357,759', '1.08%'],
        ['3', 'Jack Daniels No 7 Black', '$344,712', '1.04%'],
        ['4', 'Absolut 80 Proof', '$288,135', '0.87%'],
        ['5', "Tito's Handmade Vodka", '$275,163', '0.83%'],
    ]
    pdf.create_table(top5_headers, top5_data, [15, 85, 35, 25])
    
    pdf.chapter_title('Reorder Point Results', level=2)
    
    rop_headers = ['Product', 'ROP', 'Current', 'Status']
    rop_data = [
        ['Captain Morgan', '5,676', '16,769', 'Healthy'],
        ['Ketel One', '3,616', '16,770', 'Healthy'],
        ['Jack Daniels', '2,620', '15,047', 'Healthy'],
        ['Absolut', '2,978', '12,268', 'Healthy'],
        ["Tito's", '2,811', '14,018', 'Healthy'],
    ]
    pdf.create_table(rop_headers, rop_data, [45, 35, 35, 25])
    
    pdf.key_finding_box(
        'Inventory Status',
        'All products are currently healthy with current stock levels 2-4x above '
        'reorder points. No immediate stockout risk detected.'
    )
    
    pdf.chapter_title('Lead Time Analysis Results', level=2)
    
    lead_headers = ['Tier', 'Vendors', 'Spend', 'Risk']
    lead_data = [
        ['Premium', '26 (21.7%)', '$50.6M', 'Low'],
        ['Fast but Variable', '34 (28.3%)', '$165.0M', 'Medium'],
        ['Slow but Steady', '35 (29.2%)', '$82.9M', 'Low-Medium'],
        ['High Risk', '25 (20.8%)', '$23.5M', 'High'],
    ]
    pdf.create_table(lead_headers, lead_data, [40, 35, 35, 30])
    
    pdf.key_finding_box(
        'Critical Supplier Risk',
        'All top 5 revenue products use "Fast but Variable" or "Slow but Steady" '
        'vendors. None use Premium vendors. Vendor 3960 (Diageo) supplies 40% of '
        'A-Class revenue - significant concentration risk.'
    )
    
    # ========================================================================
    # SECTION 6: ASSUMPTIONS & LIMITATIONS
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('6. Assumptions & Limitations', level=1)
    
    pdf.chapter_title('Data Limitations', level=2)
    
    data_limits = [
        "Temporal Scope: Only 60 days of reliable data (January 2016). February showed 90% sales drop.",
        "Missing Costs: No carrying cost or ordering cost data prevented EOQ calculation.",
        "Vendor Names: Some vendors only had ID numbers; names extracted from InvoicePurchases."
    ]
    pdf.numbered_list(data_limits)
    
    pdf.chapter_title('Analytical Assumptions', level=2)
    
    assumptions = [
        "Service Level: 95% used for safety stock calculations (Z = 1.65, industry standard)",
        "Lead Time Distribution: Assumed normal distribution for safety stock formula",
        "Demand Stability: Used January 2016 averages (ignoring February anomaly)",
        "Product Classification: ABC based on 2-month snapshot; annual data would be more robust"
    ]
    pdf.numbered_list(assumptions)
    
    pdf.chapter_title('Technical Constraints', level=2)
    
    constraints = [
        "Prophet Forecasts: Limited by short time series (60 observations)",
        "External Regressors: No weather, holidays, or promotions included",
        "Vendor Classification: Thresholds based on median rather than business SLAs"
    ]
    pdf.numbered_list(constraints)
    
    # ========================================================================
    # SECTION 7: BUSINESS RECOMMENDATIONS
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('7. Business Recommendations', level=1)
    
    pdf.chapter_title('Immediate Actions (0-30 Days)', level=2)
    
    rec1 = [
        "Dual-Source Vendor 3960: 40% of A-Class revenue depends on single supplier (Diageo)",
        "Renegotiate SLAs: $85M spent with vendors slower than 7.7 days; implement penalties",
        "Increase Safety Stock: Apply 1.5x multiplier for 'Fast but Variable' vendors",
        "Consolidate Orders: Top 3 vendors = 618K orders; negotiate volume discounts"
    ]
    pdf.numbered_list(rec1)
    
    pdf.chapter_title('Strategic Initiatives (30-90 Days)', level=2)
    
    rec2 = [
        "Supplier Development: Move A-Class products to Premium vendors (currently 0/5)",
        "Inventory Rationalization: Review 4,343 C-Class products for discontinuation",
        "Data Infrastructure: Collect full year of data for seasonal forecasting"
    ]
    pdf.numbered_list(rec2)
    
    pdf.chapter_title('Risk Mitigation Priorities', level=2)
    
    risk_headers = ['Risk Factor', 'Exposure', 'Mitigation']
    risk_data = [
        ['Vendor Concentration', '21.7% Premium tier', 'Diversify supplier base'],
        ['Variable Suppliers', '$165M (51.2%) spend', 'Increase safety stock'],
        ['Lead Time Buffer', '7.6-day avg, 2.2-day var', 'Maintain safety coverage'],
    ]
    pdf.create_table(risk_headers, risk_data, [45, 55, 50])
    
    # ========================================================================
    # SECTION 8: HOW TO RUN
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('8. How to Run the Code', level=1)
    
    pdf.chapter_title('Prerequisites', level=2)
    
    prereqs = [
        "Python 3.8 or higher",
        "Google Colab (recommended) or Jupyter Notebook",
        "16GB RAM (for large CSV processing)"
    ]
    pdf.bullet_list(prereqs)
    
    pdf.chapter_title('Installation', level=2)
    
    pdf.set_font('Courier', '', 9)
    pdf.set_fill_color(245, 245, 245)
    pdf.multi_cell(0, 6, "pip install pandas numpy matplotlib seaborn plotly prophet scikit-learn kagglehub", fill=True)
    pdf.ln(3)
    
    pdf.chapter_title('Execution Steps', level=2)
    
    steps = [
        "Download Dataset: Automatically via KaggleHub",
        "Phase 1: Data Loading & Cleaning",
        "Phase 2: ABC Analysis",
        "Phase 2.2: Demand Forecasting",
        "Phase 2.3: Reorder Point Analysis",
        "Phase 2.4: Lead Time Analysis"
    ]
    pdf.numbered_list(steps)
    
    pdf.chapter_title('Output Files', level=2)
    
    outputs = [
        "ABC_Analysis_Results.csv",
        "Reorder_Point_Analysis.csv",
        "Vendor_Performance_Scorecard.csv",
        "AClass_Vendor_Analysis.csv",
        "Demand_Forecast_Detailed.csv"
    ]
    pdf.bullet_list(outputs)
    
    # ========================================================================
    # SECTION 9: CONCLUSION
    # ========================================================================
    pdf.add_page()
    pdf.chapter_title('9. Conclusion', level=1)
    
    pdf.chapter_body(
        "This analysis transformed Slooze's raw transactional data into actionable "
        "inventory intelligence. Through ABC classification, we identified that 20% "
        "of products drive 80% of revenue - yet these critical items rely on variable "
        "suppliers, creating significant supply chain vulnerability."
    )
    
    pdf.chapter_body(
        "The reorder point system provides data-driven triggers for procurement, while "
        "vendor analysis reveals $85 million in spend with suboptimal suppliers. By "
        "implementing the dual-sourcing and safety stock recommendations, Slooze can "
        "protect high-revenue streams while optimizing working capital across the portfolio."
    )
    
    pdf.chapter_title('Key Deliverables Provided', level=2)
    
    deliverables = [
        "Automated data pipeline with KaggleHub integration",
        "Statistical product classification (ABC Analysis)",
        "Predictive demand models with uncertainty quantification",
        "Operational reorder triggers with safety stock buffers",
        "Strategic vendor scorecards with risk classification"
    ]
    pdf.bullet_list(deliverables)
    
    pdf.key_finding_box(
        'Final Note',
        'All code is modular, documented, and ready for production deployment. The '
        'analysis framework can be extended to include additional data sources and more '
        'sophisticated forecasting models as the data infrastructure matures.'
    )
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, '--- End of Documentation ---', 0, 0, 'C')
    
    # ========================================================================
    # SAVE THE PDF
    # ========================================================================
    output_filename = 'Slooze_Analysis_Documentation_FPDF.pdf'
    pdf.output(output_filename)
    
    print(f"=" * 60)
    print(f"PDF GENERATED SUCCESSFULLY!")
    print(f"=" * 60)
    print(f"Filename: {output_filename}")
    print(f"Pages: {pdf.page_no()}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=" * 60)
    
    return output_filename


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SLOOZE DATA SCIENCE CHALLENGE - PDF DOCUMENTATION GENERATOR")
    print("=" * 60 + "\n")
    
    # Check if fpdf is installed
    try:
        from fpdf import FPDF
    except ImportError:
        print("ERROR: fpdf2 is not installed.")
        print("Please run: pip install fpdf2")
        exit(1)
    
    # Generate the PDF
    output_file = create_slooze_documentation()
    
    print(f"\nDocumentation saved to: {os.path.abspath(output_file)}")
