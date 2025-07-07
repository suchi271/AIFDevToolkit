# SorthaDevKit - Enhanced Developer Toolkit

## Overview

The SorthaDevKit is an AI-powered toolkit for processing transcripts, filling AIF (Architecture Investigation Framework) questionnaires, and generating Azure target architecture diagrams based on Azure Migrate reports.

## Features

### Core Functionality
- **Transcript Analysis**: Process conversation transcripts using Azure OpenAI
- **AIF Completion**: Automatically fill AIF questionnaires based on transcript insights
- **Excel Processing**: Read questions from Excel files and generate comprehensive reports

### Enhanced Functionality (New)
- **Azure Migrate Integration**: Process Azure Migrate discovery reports
- **Architecture Diagram Generation**: Create target architecture diagrams combining Azure Migrate data and transcript insights
- **Visio Compatibility**: Export diagrams in formats compatible with Microsoft Visio

## Enhanced Azure Migrate Integration

### Supported Azure Migrate Sheet Types
- **Assessment Summary**: Overview and migration readiness statistics
- **All Assessed Machines**: Complete server inventory with specifications
- **Assessment Properties**: Configuration and assessment parameters  
- **All Assessed Disks**: Storage configuration and recommendations

### Comprehensive Architecture Components
- **Compute**: VMs, VM Scale Sets, App Services, Functions, AKS, Container Instances
- **Database**: Azure SQL, MySQL, PostgreSQL, Cosmos DB, Redis Cache
- **Storage**: Storage Accounts, File Shares, Backup Vaults
- **Network**: VNets, Subnets, Load Balancers, Application Gateway, VPN Gateway
- **Security**: Network Security Groups, Azure Firewall, Key Vault, Azure AD
- **Management**: Azure Monitor, Log Analytics, Application Insights

### Advanced Networking Features
- **Multi-tier Architecture**: Automatic subnet creation for web, app, and data tiers
- **Network Security Groups**: Tier-appropriate security rules
- **Load Balancing**: Application Gateway for web tier, Internal LB for VMs
- **Security**: Centralized firewall, Key Vault integration
- **Monitoring**: Comprehensive logging and monitoring setup
- **Hybrid Connectivity**: VPN Gateway for on-premises integration

## Output Formats

### AIF Reports
- **Excel Report**: Comprehensive Q&A report with confidence scores and analysis
- **Summary Sheet**: Statistics and confidence distribution
- **Unanswered Questions**: List of questions that couldn't be answered

### Architecture Diagrams
- **VSDX Format**: Native Microsoft Visio format for direct editing
- **JSON Format**: Structured data for programmatic access
- **SVG Format**: Vector graphics for web viewing and import
- **Enhanced XML**: Visio-compatible XML with Azure properties

## Workflow Options

### 1. Standard AIF Completion (Original)
```
python main.py 1
```
- Processes transcript and questions only
- Generates filled AIF Excel report
- Uses existing workflow

### 2. Enhanced AIF Completion with Architecture Diagram (New)
```
python main.py 2
```
- Processes transcript, questions, AND Azure Migrate report
- Generates filled AIF Excel report
- Creates target architecture diagrams in multiple formats
- Provides comprehensive migration insights

## File Structure

```
DeveloperToolkit/
├── main.py                     # Entry point with workflow selection
├── Config.py                   # Configuration settings
├── Input.py                    # Input file paths and settings
├── State.py                    # State management
├── Workflow.py                 # Core workflow logic
├── requirements.txt            # Python dependencies
├── input/                      # Input files directory
│   ├── input2.txt             # Transcript file
│   ├── questions.xlsx         # AIF questions
│   └── Azure-Migrate-Report.xlsx  # Azure Migrate discovery report
├── output/                     # Output files directory
│   ├── filled_aif.xlsx        # Generated AIF report
│   ├── architecture_diagram.vsdx  # Native Visio format
│   ├── architecture_diagram.json  # Architecture in JSON format
│   ├── architecture_diagram.svg   # Architecture in SVG format
│   └── architecture_diagram.xml   # Architecture in enhanced XML format
├── SorthaDevKit/              # Core utilities
│   ├── StateBase.py           # Data models and state definitions
│   ├── ExcelUtils.py          # Excel processing utilities
│   ├── ArchitectureDiagram.py # Architecture diagram generation
│   ├── VisioExporter.py       # Enhanced Visio export capabilities
│   └── WorkFlowBase.py        # Base workflow classes
└── Workflows/                 # Workflow implementations
    ├── FilledAIF.py           # Original AIF completion workflow
    └── EnhancedFilledAIF.py   # Enhanced workflow with architecture
```

## Architecture Diagram Features

### Component Types Supported
- **Virtual Machines**: Azure VMs for lift-and-shift scenarios
- **App Services**: For modernized web applications
- **Databases**: Azure SQL, MySQL, PostgreSQL
- **Storage**: Azure Storage Accounts
- **Networking**: Virtual Networks, Load Balancers
- **Containers**: Azure Container Instances, AKS
- **Functions**: Azure Functions for serverless

### Migration Strategies
- **Lift-and-Shift**: Direct VM migration
- **Modernize**: Platform-as-a-Service adoption
- **Containerize**: Container-based deployment
- **Rearchitect**: Cloud-native redesign

### Diagram Layouts
- **Tiered Architecture**: Network, Application, Compute, Data layers
- **Automatic Positioning**: Components positioned by tier
- **Connection Mapping**: Logical connections between components
- **Visual Indicators**: Color coding by component type

## Configuration

### Input Configuration (Input.py)
```python
Input = {
    "transcript": FileInputType(file_path="input/input2.txt"),
    "questions_excel": FileInputType(file_path="input/questions.xlsx"),
    "azure_migrate_report": FileInputType(file_path="input/Azure-Migrate-Report.xlsx")
}
```

### Output Configuration
```python
OUTPUT_CONFIG = {
    "output_file_path": "output/filled_aif.xlsx",
    "architecture_diagram_json": "output/architecture_diagram.json",
    "architecture_diagram_svg": "output/architecture_diagram.svg",
    "architecture_diagram_xml": "output/architecture_diagram.xml"
}
```

## Azure Migrate Report Support

### Supported Sheet Types
- **Server Assessment Sheets**: Machine inventory and recommendations
- **Application Discovery**: Installed applications and dependencies
- **Summary Reports**: Cost estimates and readiness assessments

### Extracted Information
- Server specifications (CPU, memory, disk)
- Operating systems and applications
- Azure service recommendations
- Cost estimates and readiness status
- Dependencies and relationships

## Usage Examples

### Basic Usage
```bash
# Run enhanced workflow (default)
python main.py

# Run standard workflow
python main.py 1

# Run enhanced workflow explicitly
python main.py 2
```

### Expected Output
```
Enhanced SorthaDevKit AIF Completion with Architecture Diagram
======================================================================
Started: 2025-07-07 10:30:00

✓ Modules loaded
✓ Input files validated
✓ Connected to gpt-4
✓ Processed 15 servers from Azure Migrate report
✓ Processing complete!
✓ Generated architecture with 18 components
✓ JSON diagram saved: output/architecture_diagram.json
✓ SVG diagram saved: output/architecture_diagram.svg
✓ Visio XML diagram saved: output/architecture_diagram.xml

🎉 Processing complete!
📋 Q&A Processing:
   Questions processed: 45
   Questions answered: 38
   Answer rate: 84.4%

🏗️  Architecture Diagram:
   Source servers: 15
   Azure components: 18
   Diagram formats: VSDX, JSON, SVG, XML
```

## Working with Generated Diagrams

### Opening in Visio
1. **VSDX Method**: Double-click the .vsdx file to open directly in Visio
2. **SVG Import**: Import the SVG file into Visio for basic editing
3. **XML Import**: Import the enhanced XML file (may require Visio developer mode)
4. **Manual Recreation**: Use the JSON data to manually recreate in Visio

### Customization Options
- Open VSDX file directly in Visio for full editing capabilities
- Modify component properties and positioning
- Add custom Azure services and connections
- Update styling, colors, and layout
- Export to other formats from Visio

## Dependencies

- Python 3.8+
- pandas (Excel processing)
- openpyxl (Excel file handling)
- pydantic (Data modeling)
- langchain-openai (Azure OpenAI integration)

## Future Enhancements

- Direct Visio file (.vsdx) generation
- Interactive web-based diagram editor
- Cost estimation integration
- Network security group recommendations
- Automated deployment script generation
- Integration with Azure Resource Manager templates

## Troubleshooting

### Common Issues

1. **Azure Migrate File Not Found**
   - Ensure the Excel file is in the correct input directory
   - Check file permissions and naming

2. **No Servers Detected**
   - Verify the Azure Migrate report format
   - Check sheet names and column headers

3. **Diagram Generation Fails**
   - Ensure output directory exists and is writable
   - Check for sufficient disk space

4. **Missing Dependencies**
   - Run: `pip install -r requirements.txt`
   - Verify all required packages are installed

### Support
For issues and feature requests, please check the existing codebase and configuration files.
