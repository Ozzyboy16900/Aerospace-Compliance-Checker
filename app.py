"""
Aerospace Compliance Checker
Author: Othman Abunamous
Description: Automated validation of technical drawings and BOMs against AS9100, ITAR, and FAR standards
Purpose: Save 10-20 hours per project, prevent $100K+ compliance violations
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import PyPDF2
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('reports', exist_ok=True)

class ComplianceChecker:
    """Main compliance validation engine"""
    
    def __init__(self):
        self.violations = []
        self.warnings = []
        self.risk_score = 0
        self.checked_items = 0
        
    def validate_document(self, file_path: str, doc_type: str) -> Dict:
        """
        Main validation method - delegates to specific validators
        
        Args:
            file_path: Path to uploaded file
            doc_type: Type of document (drawing, bom, etc.)
        
        Returns:
            Compliance report dictionary
        """
        self.violations = []
        self.warnings = []
        self.risk_score = 0
        
        if doc_type == 'drawing':
            self._validate_technical_drawing(file_path)
        elif doc_type == 'bom':
            self._validate_bom(file_path)
        
        # Calculate risk score (0-100)
        self.risk_score = min(100, len(self.violations) * 15 + len(self.warnings) * 5)
        
        return self._generate_report()
    
    def _validate_technical_drawing(self, file_path: str):
        """Validate PDF technical drawings"""
        try:
            # Extract text from PDF
            text = self._extract_pdf_text(file_path)
            
            # Check for ITAR markings
            if not self._check_itar_marking(text):
                self.violations.append({
                    'rule': 'ITAR-001',
                    'description': 'Missing ITAR export control statement',
                    'severity': 'HIGH',
                    'fix': 'Add standard ITAR warning to title block',
                    'cost_impact': '$10,000-$100,000 potential fine'
                })
            
            # Check for material compliance
            restricted_materials = self._check_restricted_materials(text)
            for material in restricted_materials:
                self.violations.append({
                    'rule': 'AS9100-MAT-001',
                    'description': f'Restricted material detected: {material}',
                    'severity': 'HIGH',
                    'fix': f'Replace {material} with approved alternative',
                    'cost_impact': 'Potential rejection of entire batch'
                })
            
            # Check for proper revision control
            if not self._check_revision_marking(text):
                self.warnings.append({
                    'rule': 'AS9100-DOC-002',
                    'description': 'No revision number detected',
                    'severity': 'MEDIUM',
                    'fix': 'Add revision letter/number to title block'
                })
            
            # Check for traceability requirements
            if not self._check_traceability(text):
                self.violations.append({
                    'rule': 'AS9100-TRACE-001',
                    'description': 'Missing traceability requirements',
                    'severity': 'HIGH',
                    'fix': 'Add serial number or lot traceability note'
                })
                
        except Exception as e:
            self.warnings.append({
                'rule': 'SYSTEM',
                'description': f'Could not fully parse drawing: {str(e)}',
                'severity': 'LOW',
                'fix': 'Manual review recommended'
            })
    
    def _validate_bom(self, file_path: str):
        """Validate Bill of Materials (Excel/CSV)"""
        try:
            # Read BOM file
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            
            self.checked_items = len(df)
            
            # Standard column names (adjust based on actual BOMs)
            part_col = self._find_column(df, ['Part Number', 'P/N', 'Part'])
            material_col = self._find_column(df, ['Material', 'Mat', 'Composition'])
            supplier_col = self._find_column(df, ['Supplier', 'Vendor', 'Manufacturer'])
            
            # Check each part
            for idx, row in df.iterrows():
                # Check for ITAR controlled items
                if part_col and self._is_itar_controlled(str(row.get(part_col, ''))):
                    self.warnings.append({
                        'rule': 'ITAR-BOM-001',
                        'description': f'ITAR controlled part: {row.get(part_col, "Unknown")}',
                        'severity': 'HIGH',
                        'fix': 'Ensure proper export licensing',
                        'location': f'Row {idx + 2}'  # +2 for header and 0-index
                    })
                
                # Check material compliance
                if material_col and pd.notna(row.get(material_col)):
                    material = str(row.get(material_col, '')).upper()
                    if self._is_restricted_material(material):
                        self.violations.append({
                            'rule': 'AS9100-MAT-002',
                            'description': f'Restricted material in BOM: {material}',
                            'severity': 'HIGH',
                            'fix': 'Replace with approved material',
                            'location': f'Row {idx + 2}, Part: {row.get(part_col, "Unknown")}'
                        })
                
                # Check supplier certification
                if supplier_col and pd.notna(row.get(supplier_col)):
                    supplier = str(row.get(supplier_col, ''))
                    if not self._is_certified_supplier(supplier):
                        self.warnings.append({
                            'rule': 'AS9100-SUP-001',
                            'description': f'Non-certified supplier: {supplier}',
                            'severity': 'MEDIUM',
                            'fix': 'Verify AS9100 certification status',
                            'location': f'Row {idx + 2}'
                        })
                
                # Check for missing critical data
                if part_col and pd.isna(row.get(part_col)):
                    self.violations.append({
                        'rule': 'AS9100-DATA-001',
                        'description': 'Missing part number',
                        'severity': 'HIGH',
                        'fix': 'All items must have part numbers',
                        'location': f'Row {idx + 2}'
                    })
                    
        except Exception as e:
            self.warnings.append({
                'rule': 'SYSTEM',
                'description': f'Error processing BOM: {str(e)}',
                'severity': 'MEDIUM',
                'fix': 'Check file format and structure'
            })
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
        return text
    
    def _check_itar_marking(self, text: str) -> bool:
        """Check for required ITAR export control markings"""
        itar_keywords = [
            'ITAR', 'export control', 'EAR99', '22 CFR',
            'International Traffic in Arms', 'export license'
        ]
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in itar_keywords)
    
    def _check_restricted_materials(self, text: str) -> List[str]:
        """Check for restricted/controlled materials"""
        restricted = [
            'beryllium copper',  # Restricted in crew areas
            'cadmium',          # Carcinogenic
            'mercury',          # Toxic
            'lead',             # Restricted in many applications
            'hexavalent chromium',  # Carcinogenic
            'asbestos'          # Banned in most applications
        ]
        
        found_materials = []
        text_lower = text.lower()
        for material in restricted:
            if material.lower() in text_lower:
                found_materials.append(material)
        
        return found_materials
    
    def _check_revision_marking(self, text: str) -> bool:
        """Check for revision/version control markings"""
        revision_patterns = [
            r'[Rr]ev[ision]?\s*[A-Z0-9]+',
            r'[Vv]ersion\s*[0-9.]+',
            r'[Dd]ate:\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        ]
        
        for pattern in revision_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _check_traceability(self, text: str) -> bool:
        """Check for traceability requirements"""
        traceability_keywords = [
            'serial number', 'lot number', 'batch',
            'traceability', 'track', 'S/N', 'L/N'
        ]
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in traceability_keywords)
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """Find column by possible names"""
        for col in df.columns:
            for name in possible_names:
                if name.lower() in str(col).lower():
                    return col
        return None
    
    def _is_itar_controlled(self, part_number: str) -> bool:
        """Check if part number indicates ITAR controlled item"""
        # Common ITAR indicators in part numbers
        itar_indicators = ['MIL-', 'MS', 'NAS', 'AN', 'CAGE']
        part_upper = part_number.upper()
        return any(indicator in part_upper for indicator in itar_indicators)
    
    def _is_restricted_material(self, material: str) -> bool:
        """Check if material is restricted"""
        restricted = [
            'BERYLLIUM', 'CADMIUM', 'MERCURY', 
            'LEAD', 'CHROMIUM VI', 'ASBESTOS'
        ]
        material_upper = material.upper()
        return any(rest in material_upper for rest in restricted)
    
    def _is_certified_supplier(self, supplier: str) -> bool:
        """Check if supplier is AS9100 certified (simplified for demo)"""
        # In production, this would check against a database
        certified_suppliers = [
            'BOEING', 'LOCKHEED', 'RAYTHEON', 'NORTHROP',
            'HONEYWELL', 'COLLINS', 'PARKER', 'EATON'
        ]
        supplier_upper = supplier.upper()
        return any(cert in supplier_upper for cert in certified_suppliers)
    
    def _generate_report(self) -> Dict:
        """Generate compliance report"""
        status = 'PASS' if len(self.violations) == 0 else 'FAIL'
        
        return {
            'status': status,
            'risk_score': self.risk_score,
            'violations': self.violations,
            'warnings': self.warnings,
            'checked_items': self.checked_items,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_violations': len(self.violations),
                'total_warnings': len(self.warnings),
                'estimated_risk': self._calculate_risk_cost()
            }
        }
    
    def _calculate_risk_cost(self) -> str:
        """Calculate potential cost of non-compliance"""
        base_cost = len(self.violations) * 50000  # $50K per major violation
        warning_cost = len(self.warnings) * 5000   # $5K per warning
        total = base_cost + warning_cost
        
        if total > 1000000:
            return f"${total/1000000:.1f}M potential exposure"
        elif total > 0:
            return f"${total:,} potential exposure"
        else:
            return "Minimal risk"

# Initialize checker
checker = ComplianceChecker()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/validate', methods=['POST'])
def validate():
    """API endpoint for document validation"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    doc_type = request.form.get('doc_type', 'drawing')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Validate document
    try:
        report = checker.validate_document(filepath, doc_type)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-data')
def sample_data():
    """Generate sample compliance report for demo"""
    sample_report = {
        'status': 'FAIL',
        'risk_score': 75,
        'violations': [
            {
                'rule': 'ITAR-001',
                'description': 'Missing ITAR export control statement',
                'severity': 'HIGH',
                'fix': 'Add ITAR warning to title block',
                'cost_impact': '$10,000-$100,000 fine'
            },
            {
                'rule': 'AS9100-MAT-001',
                'description': 'Restricted material: Beryllium Copper in crew area',
                'severity': 'HIGH',
                'fix': 'Replace with phosphor bronze',
                'cost_impact': 'Batch rejection risk'
            }
        ],
        'warnings': [
            {
                'rule': 'AS9100-SUP-001',
                'description': 'Supplier not AS9100 certified',
                'severity': 'MEDIUM',
                'fix': 'Verify certification status'
            }
        ],
        'summary': {
            'total_violations': 2,
            'total_warnings': 1,
            'estimated_risk': '$250,000 potential exposure'
        },
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(sample_report)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Port 5001 to not conflict with PLM dashboard
