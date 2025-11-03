"""
Compliance Engine Module
THIS IS WHERE YOUR EXPERTISE MATTERS MOST!
Add real compliance rules from your experience at Greenpoint
"""

import json
import re
from typing import Dict, List, Any

class ComplianceEngine:
    """
    Core engine that checks documents against compliance standards
    """
    
    def __init__(self):
        self.load_rules()
        
    def load_rules(self):
        """Load compliance rules from JSON files"""
        self.rules = {
            'as9100': self.load_as9100_rules(),
            'itar': self.load_itar_rules(),
            'far': self.load_far_rules()
        }
    
    def load_as9100_rules(self) -> Dict:
        """
        AS9100 Quality Management System Requirements
        
        YOUR TASK: Add specific AS9100 rules you know
        """
        return {
            'material_requirements': {
                'restricted_materials': [
                    {
                        'material': 'beryllium copper',
                        'restriction': 'Prohibited in crew compartments',
                        'severity': 'violation',
                        'reference': 'AS9100D Section 8.5.1'
                    },
                    {
                        'material': 'cadmium',
                        'restriction': 'Requires special handling and disposal',
                        'severity': 'warning',
                        'reference': 'Environmental compliance'
                    },
                    # TODO: Add more restricted materials
                ],
                'material_traceability': {
                    'required': True,
                    'message': 'All materials must have full traceability to mill source',
                    'severity': 'violation'
                }
            },
            'documentation_requirements': {
                'first_article_inspection': {
                    'required': True,
                    'message': 'FAI required for all flight-critical parts',
                    'severity': 'violation'
                },
                # TODO: Add more documentation requirements
            },
            'supplier_requirements': {
                'certification_required': 'AS9100',
                'approved_supplier_list': True,
                # TODO: Add supplier audit requirements
            }
        }
    
    def load_itar_rules(self) -> Dict:
        """
        ITAR (International Traffic in Arms Regulations) Rules
        
        YOUR TASK: Add ITAR compliance checks you've encountered
        """
        return {
            'export_control': {
                'marking_required': True,
                'required_statement': 'This document contains technical data subject to ITAR',
                'keywords_to_check': [
                    'military',
                    'defense',
                    'weapon',
                    'missile',
                    'satellite',
                    # TODO: Add more ITAR trigger words
                ],
                'restricted_countries': [
                    'China', 'Russia', 'Iran', 'North Korea',
                    # TODO: Add complete list
                ]
            },
            'access_control': {
                'us_person_only': True,
                'message': 'Access restricted to US persons only',
                'severity': 'violation'
            }
        }
    
    def load_far_rules(self) -> Dict:
        """
        FAR (Federal Acquisition Regulation) Rules
        
        YOUR TASK: Add FAR compliance requirements
        """
        return {
            'buy_american': {
                'domestic_content_requirement': 0.75,  # 75% domestic content
                'message': 'Must meet Buy American Act requirements',
                'severity': 'warning'
            },
            'small_business': {
                'set_aside_threshold': 250000,  # Contracts over $250k
                'message': 'Consider small business set-aside requirements'
            }
            # TODO: Add more FAR requirements
        }
    
    def check(self, data: Dict[str, Any], standard: str) -> Dict[str, List]:
        """
        Main checking function
        
        YOUR TASK: Implement the actual checking logic
        """
        result = {
            'violations': [],
            'warnings': [],
            'recommendations': []
        }
        
        if standard == 'as9100':
            result = self.check_as9100(data)
        elif standard == 'itar':
            result = self.check_itar(data)
        elif standard == 'far':
            result = self.check_far(data)
            
        return result
    
    def check_as9100(self, data: Dict[str, Any]) -> Dict[str, List]:
        """
        Check against AS9100 requirements
        
        YOUR TASK: Implement specific AS9100 checks based on your experience
        """
        violations = []
        warnings = []
        recommendations = []
        
        rules = self.rules['as9100']
        
        # Check materials
        if 'materials' in data:
            for material in data['materials']:
                # Check against restricted materials
                for restricted in rules['material_requirements']['restricted_materials']:
                    if restricted['material'].lower() in material.lower():
                        if restricted['severity'] == 'violation':
                            violations.append({
                                'type': 'Restricted Material',
                                'description': f"Found {restricted['material']}: {restricted['restriction']}",
                                'reference': restricted['reference'],
                                'location': material
                            })
                        else:
                            warnings.append({
                                'type': 'Material Warning',
                                'description': f"Found {restricted['material']}: {restricted['restriction']}",
                                'reference': restricted['reference']
                            })
        
        # TODO: YOUR CODE HERE
        # Check for supplier certification
        # if 'suppliers' in data:
        #     for supplier in data['suppliers']:
        #         # Check if supplier is AS9100 certified
        #         pass
        
        # TODO: YOUR CODE HERE
        # Check for required documentation
        # - First Article Inspection (FAI)
        # - Certificate of Conformance (CoC)
        # - Material certifications
        
        # TODO: YOUR CODE HERE
        # Check part traceability
        # All parts should have:
        # - Lot/batch numbers
        # - Serial numbers (for critical parts)
        # - Revision control
        
        # Add recommendations based on findings
        if len(violations) > 3:
            recommendations.append({
                'priority': 'high',
                'message': 'Multiple AS9100 violations found. Recommend full compliance review.',
                'action': 'Schedule compliance audit with quality team'
            })
            
        return {
            'violations': violations,
            'warnings': warnings,
            'recommendations': recommendations
        }
    
    def check_itar(self, data: Dict[str, Any]) -> Dict[str, List]:
        """
        Check against ITAR requirements
        
        YOUR TASK: Add your ITAR compliance knowledge
        """
        violations = []
        warnings = []
        recommendations = []
        
        rules = self.rules['itar']
        
        # Check for export control markings
        if 'raw_text' in data:
            text = data['raw_text'].lower()
            
            # Check if document has required ITAR marking
            has_itar_marking = any(marker in text for marker in [
                'itar', 'export controlled', 'technical data'
            ])
            
            if not has_itar_marking:
                # Check if document contains ITAR keywords
                contains_itar_content = any(
                    keyword.lower() in text 
                    for keyword in rules['export_control']['keywords_to_check']
                )
                
                if contains_itar_content:
                    violations.append({
                        'type': 'Missing Export Control Marking',
                        'description': 'Document contains ITAR-controlled content but lacks proper marking',
                        'reference': '22 CFR 120-130',
                        'action': 'Add ITAR warning statement to document'
                    })
        
        # TODO: YOUR CODE HERE
        # Check for unauthorized foreign suppliers
        # if 'suppliers' in data:
        #     for supplier in data['suppliers']:
        #         # Check if supplier is from restricted country
        #         pass
        
        # TODO: YOUR CODE HERE
        # Check for technical data that shouldn't be shared
        # - Performance specifications
        # - Design methodologies
        # - Manufacturing processes
        
        return {
            'violations': violations,
            'warnings': warnings,
            'recommendations': recommendations
        }
    
    def check_far(self, data: Dict[str, Any]) -> Dict[str, List]:
        """
        Check against FAR requirements
        
        YOUR TASK: Implement FAR compliance checks
        """
        violations = []
        warnings = []
        recommendations = []
        
        # TODO: YOUR CODE HERE
        # Implement FAR checks:
        # - Buy American Act compliance
        # - Small business requirements
        # - Cost accounting standards
        # - Conflict minerals reporting
        
        return {
            'violations': violations,
            'warnings': warnings,
            'recommendations': recommendations
        }
    
    def calculate_risk_score(self, violations: List, warnings: List) -> int:
        """
        Calculate overall compliance risk score
        
        YOUR TASK: Adjust scoring based on your experience with violation severity
        """
        base_score = 100
        
        # Deduct points for violations and warnings
        for violation in violations:
            base_score -= 15  # Major deduction for violations
            
        for warning in warnings:
            base_score -= 5   # Minor deduction for warnings
            
        return max(0, base_score)
