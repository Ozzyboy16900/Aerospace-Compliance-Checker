"""
PDF Extractor Module
YOUR TASK: Add extraction logic for technical drawing elements
"""

import PyPDF2
import re
from typing import Dict, List, Any

class PDFExtractor:
    """Extract relevant data from technical drawing PDFs"""
    
    def __init__(self):
        # Common patterns in aerospace technical drawings
        self.part_number_patterns = [
            r'P/N[\s:]*([A-Z0-9\-]+)',           # P/N: XXXX-XXXX
            r'Part Number[\s:]*([A-Z0-9\-]+)',   # Part Number: XXXX
            r'PN[\s:]*([A-Z0-9\-]+)',            # PN: XXXX
            # TODO: Add your Greenpoint-specific patterns here
        ]
        
        self.material_patterns = [
            r'Material[\s:]*([A-Za-z0-9\s\-]+)',
            r'MATL[\s:]*([A-Za-z0-9\s\-]+)',
            # TODO: Add more material identifiers you see in drawings
        ]
        
    def extract(self, filepath: str) -> Dict[str, Any]:
        """
        Extract compliance-relevant data from PDF
        
        YOUR TASK: 
        1. Add extraction for CAGE codes
        2. Add extraction for revision blocks
        3. Add extraction for notes/warnings
        4. Add extraction for export control markings
        """
        extracted_data = {
            'part_numbers': [],
            'materials': [],
            'specifications': [],
            'notes': [],
            'export_markings': [],
            'cage_code': None,
            'revision': None,
            'title_block': {},
            'raw_text': ''
        }
        
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                full_text = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    full_text += text + '\n'
                
                extracted_data['raw_text'] = full_text
                
                # Extract part numbers
                for pattern in self.part_number_patterns:
                    matches = re.findall(pattern, full_text, re.IGNORECASE)
                    extracted_data['part_numbers'].extend(matches)
                
                # Extract materials
                for pattern in self.material_patterns:
                    matches = re.findall(pattern, full_text, re.IGNORECASE)
                    extracted_data['materials'].extend(matches)
                
                # TODO: YOUR CODE HERE
                # Extract CAGE code (usually 5 characters)
                # cage_pattern = r'CAGE[\s:]*([A-Z0-9]{5})'
                # cage_match = re.search(cage_pattern, full_text)
                # if cage_match:
                #     extracted_data['cage_code'] = cage_match.group(1)
                
                # TODO: YOUR CODE HERE
                # Extract export control markings (ITAR, EAR, etc.)
                # Look for phrases like:
                # - "Export controlled"
                # - "ITAR restricted"
                # - "Subject to EAR"
                
                # TODO: YOUR CODE HERE  
                # Extract specifications (MIL-STD, AMS, etc.)
                # spec_pattern = r'(MIL-STD-\d+|AMS\d+|AS\d+)'
                
                # Clean up duplicates
                extracted_data['part_numbers'] = list(set(extracted_data['part_numbers']))
                extracted_data['materials'] = list(set(extracted_data['materials']))
                
        except Exception as e:
            extracted_data['error'] = str(e)
            
        return extracted_data
    
    def extract_title_block(self, text: str) -> Dict[str, str]:
        """
        Extract information from title block
        
        YOUR TASK: Add extraction for your company's title block format
        """
        title_block = {}
        
        # TODO: Add patterns for your title block fields
        # Examples:
        # - Drawing number
        # - Scale
        # - Sheet number
        # - Drawn by
        # - Checked by
        # - Approved by
        # - Date
        
        return title_block
    
    def check_for_restricted_materials(self, materials: List[str]) -> List[str]:
        """
        Check if any materials are restricted
        
        YOUR TASK: Add materials that are restricted in aerospace
        """
        restricted = [
            'beryllium copper',  # Restricted in crew areas
            'cadmium',          # Environmental concerns
            'lead',             # REACH compliance
            # TODO: Add more restricted materials
        ]
        
        found_restricted = []
        for material in materials:
            for restricted_mat in restricted:
                if restricted_mat.lower() in material.lower():
                    found_restricted.append(material)
                    
        return found_restricted
