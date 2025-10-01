# AIFDevToolkit Runbook

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage Instructions](#usage-instructions)
- [Input Files](#input-files)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)
- [Workflows](#workflows)
- [Azure Migration Integration](#azure-migration-integration)

## Overview
Migration projects often face significant delays due to manual, time-consuming, and error-prone processes such as application intake, assessment, and documentation. These tasks can take hours to complete, slowing cloud adoption and driving up project costs.

The AIFDevToolkit addresses this challenge with an Agentic AI-powered application assessment and migration planning toolkit. Designed for multi-cloud environments—including AWS, GCP, and Azure—it leverages advanced AI models to automate discovery, analysis, and reporting. The solution streamlines the extraction and organization of application details from calls and documents, generating accurate migration plans, assessment reports, and supporting documentation in minutes.

By reducing manual effort, improving accuracy, and accelerating decision-making, the AIFDevToolkit helps organizations adopt cloud platforms faster, at lower cost, and with greater scalability.

### Key Features
- **AI-Driven Assessment**: Automated application analysis using OpenAI models
- **Migration Planning**: Generates detailed Azure migration strategies
- **Document Generation**: Creates professional Word and Excel reports
- **Azure Integration**: Works with Azure Migrate assessment data
- **Workflow Automation**: Uses LangGraph for orchestrated processing

## Prerequisites

- **Python**: 3.8 or higher
- **Azure Account**: For migration services and OpenAI integration
- **OpenAI API Key**: Required for AI-powered analysis
- **Microsoft Office**: For viewing generated Word/Excel documents (optional)

## Setup and Installation

### 1. Initial Setup
```bash
# Navigate to the project directory
cd "c:\AIFDevToolkit"

# Run the setup script to install dependencies
.\setup.bat
```

### 2. Manual Installation (if setup.bat fails)
```bash
pip install python-dotenv
pip install python-docx
pip install langgraph
pip install openai
pip install openpyxl
pip install pandas
pip install langchain
pip install langchain_openai
```

### 3. Environment Configuration
Create a `.env` file in the root directory with your configuration:
```env
OPENAI_API_KEY=your_openai_api_key_here
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id
AZURE_TENANT_ID=your_azure_tenant_id
```

## Project Structure

```
AIFDevToolkit/
├── Config.py                 # Configuration settings
├── Input.py                  # Input data processing
├── main.py                   # Main execution entry point
├── setup.bat                 # Dependency installation script
├── input/                    # Input files directory
│   ├── aif_unfilled.xlsx            # Application Information Form template
│   ├── app_interview_transcript.txt  # Application interview data
│   ├── azmigrate_dependency_analysis.xlsx # Dependency analysis
│   └── azure_migrate_assessment.xlsx # Azure Migrate assessment data
├── output/                   # Generated output files
│   ├── application_assessment_report.docx # Assessment report
│   ├── azure_migration_plan.docx         # Migration plan document
│   └── filled_aif.xlsx                   # Completed AIF with Q&A
├── SorthaDevKit/            # Core processing modules
│   ├── AssessmentReportGenerator.py # Assessment report generation
│   ├── ExcelUtils.py               # Excel processing utilities
│   ├── MigrationPlanExporter.py    # Migration plan export
│   ├── MigrationPlanGenerator.py   # Migration plan generation
│   ├── StateBase.py               # Base state management
│   └── WorkFlowBase.py            # Base workflow classes
└── Workflows/               # Processing workflows
    ├── __init__.py
    └── LangGraphMigrationPlan.py  # Main migration workflow
```

## Configuration

### Config.py Settings
The `Config.py` file contains all necessary configuration parameters:
- API endpoints and keys
- File paths and directories
- Processing parameters
- Output formatting settings

### Environment Variables
Ensure the following environment variables are set:
- `OPENAI_API_KEY`: Your OpenAI API key for AI processing
- Additional Azure credentials as needed

## Usage Instructions

### Basic Usage
1. **Prepare Input Files**: Place your input files in the `input/` directory
2. **Configure Settings**: Update `Config.py` with your specific parameters
3. **Run the Toolkit**:
   ```bash
   python main.py
   ```
4. **Review Output**: Check the `output/` directory for generated documents

### Advanced Usage
For custom workflows or specific processing requirements, you can:
- Modify workflow parameters in `LangGraphMigrationPlan.py`
- Customize document templates in the respective generator files
- Add custom processing steps to the workflow

## Input Files

### Required Files
1. **aif_unfilled.xlsx**: Application Information Form template
   - Contains questionnaire structure for application assessment
   - Used as base template for AI-driven completion

2. **app_interview_transcript.txt**: Application interview data
   - Contains detailed application information from stakeholder interviews
   - Used by AI to understand application context and requirements

3. **azure_migrate_assessment.xlsx** (optional): Azure Migrate assessment data
   - Contains technical assessment results from Azure Migrate
   - Provides infrastructure and dependency information

4. **azmigrate_dependency_analysis.xlsx** (optional): Dependency analysis data
   - Contains application dependency mapping
   - Used for migration strategy planning

### File Format Requirements
- Excel files must be in `.xlsx` format
- Text files should be in UTF-8 encoding
- Ensure all required sheets/columns are present in Excel files

## Output Files

### Generated Documents

1. **filled_aif.xlsx**: Completed Application Information Form
   - AI-generated responses to assessment questions
   - Analysis summary and categorization
   - Question-answer mapping and statistics

2. **application_assessment_report.docx**: Comprehensive Assessment Report
   - Executive summary and business drivers
   - Current architecture analysis
   - Azure target architecture recommendations
   - Risk assessment and mitigation strategies

3. **azure_migration_plan.docx**: Detailed Migration Plan
   - Migration strategy and approach
   - Timeline and phases
   - Resource requirements and costs
   - Implementation roadmap

## Troubleshooting

### Common Issues

#### Setup.bat Fails (Exit Code 1)
**Symptoms**: Installation script fails with error code 1
**Solutions**:
1. Run PowerShell/Command Prompt as Administrator
2. Check Python installation: `python --version`
3. Verify pip is working: `pip --version`
4. Install dependencies manually using the commands in setup.bat

#### Missing OpenAI API Key
**Symptoms**: API authentication errors
**Solutions**:
1. Verify `.env` file exists and contains valid `OPENAI_API_KEY`
2. Check API key permissions and quota
3. Ensure network connectivity to OpenAI services

#### Input File Format Issues
**Symptoms**: Processing errors or unexpected results
**Solutions**:
1. Verify input files are in correct format (.xlsx for Excel, .txt for text)
2. Check that all required sheets/columns exist in Excel files
3. Ensure text files are UTF-8 encoded

#### Memory Issues with Large Files
**Symptoms**: Out of memory errors during processing
**Solutions**:
1. Process smaller batches of data
2. Increase system memory allocation
3. Optimize input file sizes

### Error Codes and Messages
- **Import Error**: Missing dependencies - run setup.bat or install packages manually
- **File Not Found**: Check input file paths and ensure files exist
- **API Error**: Verify OpenAI API key and network connectivity
- **Processing Error**: Check input file formats and content structure

## Workflows

### LangGraph Migration Workflow
The main workflow (`LangGraphMigrationPlan.py`) orchestrates the entire process:

1. **Input Processing**: Loads and validates input files
2. **AI Analysis**: Uses OpenAI to analyze application data
3. **Q&A Generation**: Creates comprehensive question-answer pairs
4. **Assessment Generation**: Produces detailed assessment reports
5. **Migration Planning**: Develops migration strategies and timelines
6. **Document Export**: Generates final Word and Excel documents

### Workflow States
- **Input State**: Initial data loading and validation
- **Processing State**: AI analysis and content generation
- **Export State**: Document generation and output creation
- **Completion State**: Final validation and cleanup

### Customizing Workflows
To modify the workflow:
1. Edit `LangGraphMigrationPlan.py` for process changes
2. Update state definitions in `StateBase.py`
3. Modify generator classes for output customization

## Azure Migration Integration

### Azure Migrate Integration
The toolkit integrates with Azure Migrate assessments:
- Processes Azure Migrate assessment data
- Incorporates dependency analysis results
- Aligns recommendations with Azure best practices

### Future Azure Integration
The `YetToBeIntegrated` directory contains modules for:
- Direct Azure API integration
- Real-time assessment data retrieval
- Automated report synchronization

### Azure Authentication
For Azure integration features:
1. Configure Azure service principal
2. Set up appropriate RBAC permissions
3. Update authentication settings in configuration files

## Best Practices

### Data Preparation
- Ensure input data is clean and complete
- Validate Excel file structures before processing
- Keep backup copies of original input files

### Performance Optimization
- Process during off-peak hours for large datasets
- Monitor API usage and rate limits
- Use batch processing for multiple applications

### Security Considerations
- Protect API keys and credentials
- Ensure input data doesn't contain sensitive information
- Follow organizational data handling policies

### Output Management
- Review generated documents before sharing
- Customize templates for organizational branding
- Maintain version control of output documents

## Support and Maintenance

### Regular Updates
- Keep dependencies updated using pip
- Monitor for new versions of AI models
- Update Azure integration components as needed

### Monitoring
- Track API usage and costs
- Monitor processing performance
- Log errors and processing statistics

### Backup and Recovery
- Regular backup of configuration files
- Version control for custom modifications
- Document any customizations made

## Getting Help

For issues or questions:
1. Check this runbook for common solutions
2. Review error logs in the console output
3. Verify all prerequisites are met
4. Contact the development team with specific error details

---

*Last Updated: October 2025*
*Version: 1.0*