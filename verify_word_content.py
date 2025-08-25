#!/usr/bin/env python3
"""
Verification script to confirm network analysis content is in Word documents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SorthaDevKit.ExcelUtils import ExcelProcessor
from SorthaDevKit.AssessmentReportGenerator import ApplicationAssessmentReportGenerator, AssessmentReportData
from Input import Input

def verify_word_content():
    """Verify that network analysis content is being included in Word documents"""
    
    print("🔍 VERIFYING WORD DOCUMENT CONTENT")
    print("=" * 50)
    
    try:
        # Load dependency analysis data
        excel_utils = ExcelProcessor()
        dependency_file = Input["azmigrate_dependency_analysis"].file_path
        dependency_analysis = excel_utils.read_dependency_analysis(dependency_file)
        
        # Create assessment report generator
        generator = ApplicationAssessmentReportGenerator()
        
        # Generate target architecture
        target_architecture = generator._generate_target_architecture(
            [], None, dependency_analysis
        )
        
        # Create mock assessment data
        assessment_data = AssessmentReportData()
        assessment_data.application_name = "Test Application"
        assessment_data.questions_answers = []
        assessment_data.target_architecture = target_architecture
        
        print("✓ Generated test assessment data")
        print(f"✓ Target architecture has {len(target_architecture.network_connections)} connections")
        print()
        
        # Test the proposed architecture content generation for all environments
        environments = ["Production", "Development", "Pre-Production"]
        
        for env in environments:
            print(f"📋 TESTING {env.upper()} ENVIRONMENT CONTENT:")
            print("-" * 60)
            
            content = generator._generate_proposed_architecture_content(env, assessment_data)
            
            # Check if key network analysis elements are present
            checks = {
                "Network Architecture Analysis": "🏗️ **Network Architecture Analysis:**" in content,
                "Subnet Recommendations": "• Subnet Recommendations:" in content,
                "NSG Rules Generated": "• NSG Rules Generated:" in content,
                "Load Balancer Recommendations": "• Load Balancer Recommendations:" in content,
                "Compute Recommendations": "💻 **Compute Recommendations:" in content,
                "Network Diagram Description": "📋 **Network Diagram Description:**" in content,
                "221 connections mentioned": "221 network connections" in content,
                "Oracle references": "oracle" in content.lower(),
                "Port references": "Port 1521" in content or "Port 3872" in content
            }
            
            print("Content verification checks:")
            for check_name, result in checks.items():
                status = "✅" if result else "❌"
                print(f"  {status} {check_name}: {'PASS' if result else 'FAIL'}")
            
            # Show first 500 characters of content
            print(f"\nFirst 500 characters of content:")
            print("-" * 40)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("\n" + "=" * 60 + "\n")
        
        print("💡 If all checks show ✅ PASS, then the comprehensive network analysis")
        print("   is being properly included in the Word document content!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_word_content()
