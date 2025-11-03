"""
Report Generator Module
Creates professional compliance reports in multiple formats
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class ReportGenerator:
    def __init__(self):
        self.report_dir = 'reports'
        os.makedirs(self.report_dir, exist_ok=True)
    
    def create_report(self, filename: str, document_type: str, 
                     violations: List[Dict], risk_score: int, 
                     extracted_data: Dict) -> str:
        """Generate comprehensive compliance report"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_name = f"compliance_report_{timestamp}.json"
        report_path = os.path.join(self.report_dir, report_name)
        
        # Create report structure
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'original_file': filename,
                'document_type': document_type,
                'analyzer_version': '1.0.0'
            },
            'summary': {
                'risk_score': risk_score,
                'total_violations': len(violations),
                'critical_violations': len([v for v in violations if v.get('severity') == 'Critical']),
                'high_violations': len([v for v in violations if v.get('severity') == 'High']),
                'medium_violations': len([v for v in violations if v.get('severity') == 'Medium']),
                'low_violations': len([v for v in violations if v.get('severity') == 'Low'])
            },
            'violations': violations,
            'recommendations': self.generate_recommendations(violations),
            'cost_analysis': self.calculate_cost_impact(violations),
            'extracted_data': extracted_data
        }
        
        # Save report
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_path
    
    def generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on violations"""
        recommendations = []
        
        if any(v.get('type') == 'Non-Certified Supplier' for v in violations):
            recommendations.append("Implement supplier certification tracking system")
            recommendations.append("Require AS9100 certification for all aerospace suppliers")
        
        if any(v.get('type') == 'Missing Export Control Statement' for v in violations):
            recommendations.append("Add ITAR/export control review to document release process")
            recommendations.append("Train staff on export control requirements")
        
        if any(v.get('type') == 'Restricted Material' for v in violations):
            recommendations.append("Update approved materials list")
            recommendations.append("Implement material review board process")
        
        if not violations:
            recommendations.append("Document is compliant - maintain current processes")
        
        return recommendations
    
    def calculate_cost_impact(self, violations: List[Dict]) -> Dict:
        """Calculate potential cost of violations"""
        
        # Cost estimates based on industry data
        # OTHMAN: Update these with real costs from your experience!
        cost_map = {
            'Critical': 50000,  # Major compliance failure
            'High': 15000,      # Significant issue
            'Medium': 5000,     # Moderate issue
            'Low': 1000         # Minor issue
        }
        
        total_risk = 0
        breakdown = {}
        
        for violation in violations:
            severity = violation.get('severity', 'Medium')
            cost = cost_map.get(severity, 5000)
            total_risk += cost
            
            vtype = violation.get('type', 'Other')
            if vtype not in breakdown:
                breakdown[vtype] = 0
            breakdown[vtype] += cost
        
        return {
            'total_potential_cost': total_risk,
            'cost_by_violation_type': breakdown,
            'cost_avoidance': total_risk,
            'roi_message': f'This check prevented potential losses of ${total_risk:,}'
        }
