"""
PDF Processor Module
Handles technical drawing PDFs - extracts text and identifies compliance issues
"""

import PyPDF2
import re
from typing import Dict, List

class PDFProcessor:
    def __init__(self):
        self.drawing_requirements = self.load_drawing_requirements()
    
    def load_drawing_requirements(self):
        """
        Drawing requirements per AS9100
        OTHMAN: Add requirements specific to your VIP aircraft drawings!
        """
        return {
            'title_block': [
                'part_number',
                'revision',
                'date',
                'drawn_by',
                'checked_by',
                'approved_by'
            ],
            'specifications': [
                'material_specification',
                'surface_finish',
                'tolerance_block',
                'scale'
            ],
            'notes': [
                'general_notes',
                'revision_history',
                'critical_dimensions'
            ]
        }
    
    def extract_content(self, filepath: str) -> Dict:
        """Extract text content from PDF technical drawing"""
        try:
            content = ""
            metadata = {}
            
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', '')
                    }
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            # Parse drawing information
            parsed_data = self.parse_drawing_content(content)
            parsed_data['metadata'] = metadata
            parsed_data['content'] = content
            parsed_data['file_path'] = filepath
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    def parse_drawing_content(self, content: str) -> Dict:
        """
        Parse technical drawing content
        OTHMAN: Add patterns for Greenpoint's drawing standards!
        """
        parsed = {
            'part_number': self.extract_part_number(content),
            'revision': self.extract_revision(content),
            'material': self.extract_material(content),
            'tolerances': self.extract_tolerances(content),
            'surface_finish': self.extract_surface_finish(content),
            'has_export_warning': self.check_export_warning(content),
            'critical_characteristics': self.extract_critical_chars(content)
        }
        
        return parsed
    
    def extract_part_number(self, content: str) -> str:
        """Extract part number from drawing"""
        # Common patterns - CUSTOMIZE based on your drawings
        patterns = [
            r'P/N[:\s]+([A-Z0-9\-]+)',
            r'PART NUMBER[:\s]+([A-Z0-9\-]+)',
            r'PART NO[:\s]+([A-Z0-9\-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""
    
    def extract_revision(self, content: str) -> str:
        """Extract revision from drawing"""
        patterns = [
            r'REV[:\s]+([A-Z0-9]+)',
            r'REVISION[:\s]+([A-Z0-9]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""
    
    def extract_material(self, content: str) -> str:
        """Extract material specification"""
        patterns = [
            r'MATERIAL[:\s]+([^\n]+)',
            r'MATL[:\s]+([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def extract_tolerances(self, content: str) -> List[str]:
        """Extract tolerance specifications"""
        tolerances = []
        
        # Look for tolerance callouts (±0.005, etc.)
        tolerance_pattern = r'[±+-]\d+\.?\d*'
        matches = re.findall(tolerance_pattern, content)
        tolerances.extend(matches)
        
        return list(set(tolerances))
    
    def extract_surface_finish(self, content: str) -> str:
        """Extract surface finish requirements"""
        patterns = [
            r'SURFACE FINISH[:\s]+(\d+)',
            r'(\d+)\s*Ra',
            r'(\d+)\s*RMS'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""
    
    def check_export_warning(self, content: str) -> bool:
        """Check if drawing has ITAR/export warning"""
        export_keywords = [
            'ITAR',
            'export control',
            'export restricted',
            'EAR99',
            '22 CFR',
            'arms export control act'
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in export_keywords)
    
    def extract_critical_chars(self, content: str) -> List[str]:
        """
        Extract critical characteristics
        OTHMAN: Add symbols/patterns used in your drawings!
        """
        critical = []
        
        # Look for critical characteristic symbols
        if '⚠' in content or 'CRITICAL' in content.upper():
            critical.append('Critical characteristics identified')
        
        # Add more patterns based on your experience
        
        return critical
