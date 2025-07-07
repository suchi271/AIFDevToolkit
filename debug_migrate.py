"""
Debug Azure Migrate Report Structure
====================================
This script analyzes the Azure Migrate report to understand its structure
and debug why no servers were found during parsing.
"""

import pandas as pd
import os
import sys

def debug_azure_migrate_report():
    file_path = r'input\Azure-Migrate-Report.xlsx'
    
    print("🔍 Debugging Azure Migrate Report Structure")
    print("=" * 60)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        excel_file = pd.ExcelFile(file_path)
        print(f"📁 File: {file_path}")
        print(f"📋 Total sheets: {len(excel_file.sheet_names)}")
        print()
        
        for i, sheet_name in enumerate(excel_file.sheet_names, 1):
            print(f"📄 Sheet {i}: '{sheet_name}'")
            print("-" * 40)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"   📊 Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
                
                if df.empty:
                    print("   ⚠️  Sheet is empty")
                    continue
                
                print("   📝 Column names:")
                for j, col in enumerate(df.columns):
                    print(f"      {j+1:2d}. {col}")
                
                # Check if this looks like server data
                columns_str = ' '.join(df.columns.astype(str)).lower()
                server_indicators = [
                    'server name', 'machine name', 'computer name', 'hostname',
                    'operating system', 'cpu', 'memory', 'disk', 'recommendation',
                    'azure vm size', 'azure readiness', 'monthly cost'
                ]
                
                found_indicators = [ind for ind in server_indicators if ind in columns_str]
                if found_indicators:
                    print(f"   ✅ Server data indicators found: {found_indicators}")
                    
                    # Show sample data
                    print("   📋 Sample data (first 3 rows):")
                    for idx, row in df.head(3).iterrows():
                        print(f"      Row {idx + 1}:")
                        for col in df.columns[:5]:  # Show first 5 columns
                            value = str(row[col])[:50]  # Truncate long values
                            print(f"         {col}: {value}")
                        print()
                else:
                    print("   ❌ No server data indicators found")
                    
                    # Check if it's a summary sheet
                    summary_indicators = ['total', 'cost', 'summary', 'assessment']
                    found_summary = [ind for ind in summary_indicators if ind in columns_str]
                    if found_summary:
                        print(f"   📊 Summary indicators found: {found_summary}")
                
            except Exception as e:
                print(f"   ❌ Error reading sheet: {e}")
            
            print()
    
    except Exception as e:
        print(f"❌ Error opening file: {e}")

if __name__ == "__main__":
    debug_azure_migrate_report()
