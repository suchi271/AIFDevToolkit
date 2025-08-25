# Azure Migration Assessment Tool

A comprehensive tool for generating Azure migration assessment reports using multiple data sources including interview transcripts, Azure Migrate reports, and network dependency analysis.

## Features

- **Multi-Source Assessment**: Combines interview transcripts, Azure Migrate data, and dependency analysis
- **Network Traffic Analysis**: Analyzes 200+ network connections to recommend Azure architecture
- **Target Architecture Generation**: Creates subnet, NSG, and load balancer recommendations based on actual traffic patterns
- **Comprehensive Reports**: Generates detailed Word documents and Excel files
- **AI-Powered Analysis**: Uses OpenAI/Azure OpenAI for intelligent content generation

## Quick Start

### 1. Initial Setup

Run the setup script to install dependencies and configure the environment:

```batch
setup.bat
```

This will:
- Create a Python virtual environment
- Install all required packages
- Create a `.env` file template
- Set up input/output directories

### 2. Configure API Keys

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Prepare Input Files

Place the following files in the `input/` directory:

- **sample_transcript.txt**: Interview transcript with application details
- **Azure-Migrate-Report.xlsx**: Azure Migrate assessment report
- **questions_new.xlsx**: Questions template for assessment
- **dependency_analysis.xlsx** (optional): Network dependency analysis

### 4. Run the Assessment

```batch
python main.py
```

## Input File Formats

### Transcript File (sample_transcript.txt)
Plain text file containing interview conversation about the application to be migrated.

### Azure Migrate Report (Azure-Migrate-Report.xlsx)
Excel file exported from Azure Migrate with server assessment data. Should include:
- Server names and specifications
- Operating systems
- Applications and dependencies
- Performance metrics

### Questions File (questions_new.xlsx)
Excel file with assessment questions. Format:
- Column A: Questions
- Column B: Categories
- Additional columns for answers and notes

### Dependency Analysis (dependency_analysis.xlsx)
Network traffic analysis with columns:
- Source IP
- Destination IP  
- Destination port
- Applications
- Connection details

## Output Files

The tool generates:

### Word Document (`output/azure_migration_plan.docx`)
Comprehensive assessment report including:
- Executive Summary
- Application Portfolio Analysis
- Network Traffic Analysis and Architecture Recommendations
- Environment-specific Azure Architecture proposals
- Migration recommendations
- Risk assessment

### Excel File (`output/filled_aif.xlsx`)
Assessment framework with:
- Detailed server inventory
- Application mappings
- Dependencies analysis
- Migration readiness scores

## Network Traffic Analysis

The tool analyzes network connections to provide:

- **Subnet Recommendations**: Based on IP address patterns
- **NSG Rules**: Security rules derived from actual traffic patterns  
- **Load Balancer Configuration**: For discovered multi-server applications
- **Service Endpoint Recommendations**: For Azure service connectivity

Example output includes analysis of 200+ connections with specific port and application mappings.

## Architecture Recommendations

For each environment (Production, Development, Pre-Production), the tool generates:

- **Compute Resources**: Azure App Service, Container Apps, VMs based on discovered applications
- **Database Services**: Azure SQL, CosmosDB, MySQL based on database technologies found
- **Networking**: VNet design, subnet allocation, NSG rules based on traffic analysis
- **Security**: Key Vault, managed identities, encryption recommendations
- **Monitoring**: Application Insights, Log Analytics based on operational needs

## Configuration

### Environment Variables (.env)

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Azure OpenAI Configuration  
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Assessment Configuration
AI_MODEL=gpt-4
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.3
DETAIL_LEVEL=comprehensive
```

### Supported AI Models

- **OpenAI**: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- **Azure OpenAI**: gpt-4, gpt-35-turbo

## Troubleshooting

### Common Issues

1. **"Python not found"**
   - Install Python 3.8+ from https://python.org
   - Ensure "Add Python to PATH" is checked during installation

2. **"Package installation failed"**
   - Check internet connection
   - Try running: `pip install --upgrade pip`
   - Manually install packages: `pip install python-docx openpyxl pandas openai`

3. **"API key error"**
   - Verify API key in `.env` file
   - Check API key permissions and billing on OpenAI platform

4. **"No network connections found"**
   - Verify dependency analysis Excel format
   - Check column names match expected format (Source IP, Destination IP, etc.)

### File Permissions

Ensure the application has write permissions to the `output/` directory.

### Large Files

For large dependency analysis files (>1000 connections), processing may take several minutes.

## Technical Details

### Dependencies

- **python-docx**: Word document generation
- **openpyxl**: Excel file processing  
- **pandas**: Data analysis and manipulation
- **openai**: AI content generation
- **langchain-openai**: Advanced AI integration

### Architecture

- **Input.py**: Multi-source data parsing and integration
- **StateBase.py**: Data models and structures
- **ExcelUtils.py**: Excel processing and dependency analysis
- **AssessmentReportGenerator.py**: Report generation and AI analysis
- **MigrationPlanGenerator.py**: Word document creation

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Verify all input files are in the correct format
3. Check the console output for specific error messages
4. Ensure API keys are correctly configured

## License

Internal Microsoft Research Tool
