import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import asdict
import math
import statistics
from .StateBase import (
    AzureMigrationPlan, AzureMigrateReport, ArchitectureDiagram, 
    MigrationWave, MigrationRisk, CostEstimate, MigrationTimeline,
    AzureMigrateServer, QuestionAnswer
)

class AzureMigrationPlanGenerator:
    """Generator for comprehensive Azure Migration Plan documents."""
    
    def __init__(self):
        self.migration_strategies = {
            "lift-and-shift": "Rehost applications in Azure with minimal changes",
            "modernize": "Refactor applications to leverage Azure PaaS services",
            "rearchitect": "Rebuild applications with cloud-native architecture",
            "replace": "Replace with Azure SaaS solutions",
            "retire": "Decommission applications no longer needed"
        }
        
        self.risk_categories = {
            "technical": "Technical risks related to compatibility and performance",
            "business": "Business risks related to operations and continuity",
            "security": "Security and compliance related risks",
            "operational": "Operational risks related to deployment and management"
        }
    
    def generate_migration_plan(
        self, 
        azure_migrate_data: AzureMigrateReport,
        architecture_diagram: ArchitectureDiagram,
        transcript_insights: List[QuestionAnswer],
        project_name: str = "Azure Migration Project"
    ) -> AzureMigrationPlan:
        """
        Generate a comprehensive Azure Migration Plan document.
        
        Args:
            azure_migrate_data: Parsed Azure Migrate report data
            architecture_diagram: Generated target architecture
            transcript_insights: Q&A insights from transcript analysis
            project_name: Name of the migration project
            
        Returns:
            Complete Azure Migration Plan document
        """
        
        # Generate executive summary and business case
        executive_summary = self._generate_executive_summary(azure_migrate_data, project_name)
        business_case = self._generate_business_case(azure_migrate_data, transcript_insights)
        
        # Analyze current infrastructure
        current_infrastructure = self._analyze_current_infrastructure(azure_migrate_data)
        
        # Generate target services analysis
        target_services = self._analyze_target_services(architecture_diagram, azure_migrate_data)
        
        # Create migration waves
        migration_waves = self._create_migration_waves(azure_migrate_data.servers, transcript_insights)
        
        # Generate timeline
        migration_timeline = self._generate_migration_timeline(migration_waves)
        
        # Assess risks
        risks = self._assess_migration_risks(azure_migrate_data, migration_waves, transcript_insights)
        
        # Calculate cost estimates
        cost_estimates = self._calculate_cost_estimates(azure_migrate_data, migration_waves)
        
        # Generate implementation plans
        resource_plan = self._generate_resource_plan(migration_waves, azure_migrate_data)
        training_plan = self._generate_training_plan(target_services, transcript_insights)
        communication_plan = self._generate_communication_plan(migration_timeline)
        
        # Define governance and compliance
        security_requirements = self._define_security_requirements(transcript_insights)
        compliance_requirements = self._define_compliance_requirements(transcript_insights)
        governance_model = self._define_governance_model(transcript_insights)
        
        # Generate success metrics
        kpis = self._generate_kpis(azure_migrate_data, cost_estimates)
        success_criteria = self._generate_success_criteria(migration_waves, transcript_insights)
        
        # Create technical specifications
        technical_specifications = self._generate_technical_specifications(
            azure_migrate_data, architecture_diagram
        )
        
        # Identify vendor requirements
        vendor_requirements = self._identify_vendor_requirements(target_services, transcript_insights)
        
        # Calculate totals
        total_investment = sum(ce.one_time_migration_cost + ce.azure_monthly_cost * 12 for ce in cost_estimates)
        expected_savings = sum(ce.annual_savings for ce in cost_estimates)
        
        return AzureMigrationPlan(
            project_name=project_name,
            executive_summary=executive_summary,
            business_case=business_case,
            current_infrastructure=current_infrastructure,
            azure_migrate_data=azure_migrate_data,
            architecture_diagram=architecture_diagram,
            target_services=target_services,
            migration_approach=self._determine_migration_approach(azure_migrate_data, transcript_insights),
            migration_timeline=migration_timeline,
            migration_waves=migration_waves,
            risks=risks,
            assumptions=self._generate_assumptions(transcript_insights),
            constraints=self._generate_constraints(transcript_insights),
            cost_estimates=cost_estimates,
            total_investment=total_investment,
            expected_savings=expected_savings,
            resource_plan=resource_plan,
            training_plan=training_plan,
            communication_plan=communication_plan,
            security_requirements=security_requirements,
            compliance_requirements=compliance_requirements,
            governance_model=governance_model,
            kpis=kpis,
            success_criteria=success_criteria,
            technical_specifications=technical_specifications,
            vendor_requirements=vendor_requirements
        )
    
    def _generate_executive_summary(self, azure_migrate_data: AzureMigrateReport, project_name: str) -> str:
        """Generate executive summary section."""
        total_servers = len(azure_migrate_data.servers)
        ready_servers = len([s for s in azure_migrate_data.servers if 'ready' in s.readiness.lower()])
        
        return f"""
{project_name} Executive Summary

This document outlines the comprehensive migration plan for transitioning {total_servers} on-premises servers to Microsoft Azure. The migration assessment indicates {ready_servers} servers ({ready_servers/total_servers*100:.1f}%) are ready for Azure migration.

Key Highlights:
• Infrastructure Scale: {total_servers} servers assessed for migration
• Migration Readiness: {ready_servers} servers ready, {total_servers - ready_servers} require remediation
• Target Architecture: Modern, scalable, and secure Azure infrastructure
• Expected Benefits: Improved scalability, enhanced security, reduced operational overhead

Strategic Objectives:
1. Minimize business disruption during migration
2. Optimize cost and performance in Azure
3. Enhance security and compliance posture
4. Enable future digital transformation initiatives

This migration represents a strategic investment in the organization's digital future, positioning it for enhanced agility, innovation, and competitive advantage in the cloud-first era.
        """.strip()
    
    def _generate_business_case(self, azure_migrate_data: AzureMigrateReport, transcript_insights: List[QuestionAnswer]) -> str:
        """Generate business case section."""
        total_monthly_cost = sum(server.estimated_cost for server in azure_migrate_data.servers)
        
        # Extract business drivers from transcript
        business_drivers = []
        for qa in transcript_insights:
            if any(keyword in qa.question.lower() for keyword in ['business', 'benefit', 'driver', 'reason', 'why']):
                if qa.answer:
                    business_drivers.append(qa.answer)
        
        business_case = f"""
Business Case for Azure Migration

Financial Benefits:
• Estimated Azure monthly cost: ${total_monthly_cost:,.2f}
• Potential operational savings: 20-30% through automation
• Capital expenditure reduction: Eliminate hardware refresh cycles
• Improved resource utilization and rightsizing opportunities

Strategic Benefits:
• Enhanced business agility and scalability
• Improved disaster recovery and business continuity
• Access to advanced Azure services and AI capabilities
• Enhanced security and compliance capabilities
• Reduced IT operational overhead

Business Drivers Identified:
"""
        
        for i, driver in enumerate(business_drivers[:5], 1):  # Top 5 drivers
            business_case += f"• {driver}\n"
        
        business_case += """
Risk Mitigation:
• Reduced dependency on aging on-premises infrastructure
• Enhanced data protection and backup capabilities
• Improved regulatory compliance posture
• Better disaster recovery options

Return on Investment:
• Expected ROI within 18-24 months
• Ongoing operational savings of 20-30%
• Improved staff productivity and focus on strategic initiatives
• Enhanced innovation capabilities through cloud services
        """
        
        return business_case.strip()
    
    def _analyze_current_infrastructure(self, azure_migrate_data: AzureMigrateReport) -> Dict[str, Any]:
        """Analyze current infrastructure state."""
        servers = azure_migrate_data.servers
        
        os_distribution = {}
        cpu_distribution = {}
        memory_distribution = {}
        
        for server in servers:
            # OS distribution
            os_key = server.operating_system if server.operating_system else "Unknown"
            os_distribution[os_key] = os_distribution.get(os_key, 0) + 1
            
            # CPU distribution
            cpu_range = self._get_cpu_range(server.cpu_cores)
            cpu_distribution[cpu_range] = cpu_distribution.get(cpu_range, 0) + 1
            
            # Memory distribution
            memory_range = self._get_memory_range(server.memory_gb)
            memory_distribution[memory_range] = memory_distribution.get(memory_range, 0) + 1
        
        total_cpu_cores = sum(server.cpu_cores for server in servers)
        total_memory_gb = sum(server.memory_gb for server in servers)
        total_storage_gb = sum(server.disk_size_gb for server in servers)
        
        return {
            "total_servers": len(servers),
            "total_cpu_cores": total_cpu_cores,
            "total_memory_gb": total_memory_gb,
            "total_storage_gb": total_storage_gb,
            "os_distribution": os_distribution,
            "cpu_distribution": cpu_distribution,
            "memory_distribution": memory_distribution,
            "average_cpu_per_server": total_cpu_cores / len(servers) if servers else 0,
            "average_memory_per_server": total_memory_gb / len(servers) if servers else 0,
            "average_storage_per_server": total_storage_gb / len(servers) if servers else 0
        }
    
    def _analyze_target_services(self, architecture_diagram: ArchitectureDiagram, azure_migrate_data: AzureMigrateReport) -> List[Dict[str, Any]]:
        """Analyze target Azure services."""
        service_analysis = []
        
        # Group components by Azure service type
        service_groups = {}
        for component in architecture_diagram.components:
            service_type = component.azure_service
            if service_type not in service_groups:
                service_groups[service_type] = []
            service_groups[service_type].append(component)
        
        for service_type, components in service_groups.items():
            analysis = {
                "service_name": service_type,
                "component_count": len(components),
                "migration_strategy": self._determine_service_migration_strategy(service_type),
                "benefits": self._get_service_benefits(service_type),
                "considerations": self._get_service_considerations(service_type),
                "estimated_effort": self._estimate_service_effort(service_type, len(components)),
                "components": [comp.name for comp in components]
            }
            service_analysis.append(analysis)
        
        return service_analysis
    
    def _create_migration_waves(self, servers: List[AzureMigrateServer], transcript_insights: List[QuestionAnswer]) -> List[MigrationWave]:
        """Create migration waves based on complexity and dependencies."""
        waves = []
        
        # Categorize servers by complexity and readiness
        wave_1_servers = []  # Ready servers, low complexity
        wave_2_servers = []  # Ready servers, medium complexity
        wave_3_servers = []  # Servers requiring remediation
        
        for server in servers:
            complexity_score = self._calculate_server_complexity(server)
            
            if 'ready' in server.readiness.lower():
                if complexity_score <= 3:
                    wave_1_servers.append(server)
                else:
                    wave_2_servers.append(server)
            else:
                wave_3_servers.append(server)
        
        # Create waves
        if wave_1_servers:
            waves.append(MigrationWave(
                wave_number=1,
                name="Pilot Migration - Low Complexity Systems",
                description="Migration of ready servers with low complexity to validate processes and tools",
                servers=wave_1_servers,
                duration_weeks=4,
                dependencies=["Azure environment setup", "Network connectivity", "Migration tools"],
                risk_level="Low",
                estimated_cost=sum(s.estimated_cost * 0.5 for s in wave_1_servers),  # Setup costs
                prerequisites=[
                    "Azure subscription and governance setup",
                    "Network connectivity established",
                    "Migration tooling configured",
                    "Backup and recovery procedures validated"
                ],
                success_criteria=[
                    "All pilot servers migrated successfully",
                    "Performance baselines met or exceeded",
                    "No data loss during migration",
                    "Rollback procedures validated"
                ]
            ))
        
        if wave_2_servers:
            waves.append(MigrationWave(
                wave_number=2,
                name="Production Migration - Medium Complexity Systems",
                description="Migration of production servers with moderate complexity",
                servers=wave_2_servers,
                duration_weeks=8,
                dependencies=["Wave 1 completion", "Lessons learned integration"],
                risk_level="Medium",
                estimated_cost=sum(s.estimated_cost * 0.7 for s in wave_2_servers),
                prerequisites=[
                    "Wave 1 successfully completed",
                    "Migration procedures refined",
                    "Extended maintenance windows approved",
                    "Additional monitoring tools deployed"
                ],
                success_criteria=[
                    "All production servers migrated with <2hr downtime each",
                    "No business service interruptions",
                    "Performance optimization completed",
                    "Security configurations validated"
                ]
            ))
        
        if wave_3_servers:
            waves.append(MigrationWave(
                wave_number=3,
                name="Complex Systems Migration",
                description="Migration of servers requiring remediation and complex applications",
                servers=wave_3_servers,
                duration_weeks=12,
                dependencies=["Wave 2 completion", "Remediation activities", "Application modernization"],
                risk_level="High",
                estimated_cost=sum(s.estimated_cost * 1.2 for s in wave_3_servers),  # Higher costs for complexity
                prerequisites=[
                    "Application compatibility issues resolved",
                    "Legacy system dependencies addressed",
                    "Extended testing completed",
                    "Specialized migration tools configured"
                ],
                success_criteria=[
                    "All complex systems successfully migrated",
                    "Application performance optimized",
                    "Legacy integrations maintained",
                    "Technical debt reduction achieved"
                ]
            ))
        
        return waves
    
    def _calculate_server_complexity(self, server: AzureMigrateServer) -> int:
        """Calculate complexity score for a server (1-10 scale)."""
        complexity = 1
        
        # OS complexity
        if 'windows' in server.operating_system.lower():
            if '2008' in server.operating_system or '2012' in server.operating_system:
                complexity += 2  # Older OS requires more work
            else:
                complexity += 1
        else:
            complexity += 1  # Linux systems
        
        # Resource complexity
        if server.cpu_cores > 8:
            complexity += 1
        if server.memory_gb > 32:
            complexity += 1
        if server.disk_size_gb > 500:
            complexity += 1
        
        # Application complexity
        if server.applications:
            complexity += len(server.applications) // 2
        
        # Readiness issues
        if 'not ready' in server.readiness.lower() or 'conditionally ready' in server.readiness.lower():
            complexity += 3
        
        return min(complexity, 10)
    
    def _generate_migration_timeline(self, migration_waves: List[MigrationWave]) -> MigrationTimeline:
        """Generate overall migration timeline."""
        total_weeks = sum(wave.duration_weeks for wave in migration_waves) + 4  # Add buffer
        total_months = math.ceil(total_weeks / 4)
        
        # Generate key milestones
        milestones = [
            {"milestone": "Project Initiation", "date": "Week 0", "description": "Project kickoff and team mobilization"},
            {"milestone": "Azure Environment Setup", "date": "Week 2", "description": "Azure subscription and base infrastructure setup"},
            {"milestone": "Migration Tools Setup", "date": "Week 3", "description": "Migration tooling configuration and testing"},
        ]
        
        current_week = 4
        for wave in migration_waves:
            milestones.append({
                "milestone": f"{wave.name} Start",
                "date": f"Week {current_week}",
                "description": f"Begin {wave.name}"
            })
            current_week += wave.duration_weeks
            milestones.append({
                "milestone": f"{wave.name} Complete",
                "date": f"Week {current_week}",
                "description": f"Complete {wave.name}"
            })
        
        milestones.append({
            "milestone": "Project Closure",
            "date": f"Week {current_week + 2}",
            "description": "Project closure and knowledge transfer"
        })
        
        critical_path = [
            "Azure environment setup",
            "Network connectivity establishment",
            "Migration tool configuration",
            "Pilot migration execution",
            "Production migration execution",
            "Complex systems migration"
        ]
        
        resource_requirements = {
            "project_manager": "1 FTE for entire duration",
            "azure_architect": "1 FTE for setup phase, 0.5 FTE ongoing",
            "migration_engineer": "2-3 FTE during active migration phases",
            "application_owner": "0.5 FTE per application during migration",
            "security_specialist": "0.5 FTE for setup and validation",
            "network_engineer": "1 FTE for setup phase, on-call during migration"
        }
        
        return MigrationTimeline(
            total_duration_months=total_months,
            waves=migration_waves,
            key_milestones=milestones,
            critical_path=critical_path,
            resource_requirements=resource_requirements
        )
    
    def _assess_migration_risks(self, azure_migrate_data: AzureMigrateReport, migration_waves: List[MigrationWave], transcript_insights: List[QuestionAnswer]) -> List[MigrationRisk]:
        """Assess migration risks."""
        risks = []
        
        # Technical risks
        not_ready_servers = [s for s in azure_migrate_data.servers if 'not ready' in s.readiness.lower()]
        if not_ready_servers:
            risks.append(MigrationRisk(
                risk_id="TECH-001",
                description=f"{len(not_ready_servers)} servers are not ready for migration due to compatibility issues",
                impact="High",
                probability="High",
                mitigation="Conduct detailed compatibility assessment and remediation plan",
                owner="Technical Team",
                category="Technical"
            ))
        
        # Business continuity risks
        high_risk_waves = [w for w in migration_waves if w.risk_level in ["High", "Critical"]]
        if high_risk_waves:
            risks.append(MigrationRisk(
                risk_id="BUS-001",
                description="Business disruption during complex system migration",
                impact="High",
                probability="Medium",
                mitigation="Implement comprehensive rollback procedures and extended maintenance windows",
                owner="Business Owner",
                category="Business"
            ))
        
        # Security risks
        risks.append(MigrationRisk(
            risk_id="SEC-001",
            description="Data exposure during migration process",
            impact="Critical",
            probability="Low",
            mitigation="Implement encryption in transit and at rest, conduct security assessments",
            owner="Security Team",
            category="Security"
        ))
        
        # Operational risks
        risks.append(MigrationRisk(
            risk_id="OPS-001",
            description="Skills gap in Azure technologies",
            impact="Medium",
            probability="Medium",
            mitigation="Conduct comprehensive training program and engage Azure consulting partners",
            owner="Operations Manager",
            category="Operational"
        ))
        
        return risks
    
    def _calculate_cost_estimates(self, azure_migrate_data: AzureMigrateReport, migration_waves: List[MigrationWave]) -> List[CostEstimate]:
        """Calculate comprehensive cost estimates."""
        cost_estimates = []
        
        # Compute costs
        total_azure_compute = sum(server.estimated_cost for server in azure_migrate_data.servers)
        compute_estimate = CostEstimate(
            category="Compute",
            current_monthly_cost=total_azure_compute * 1.3,  # Assume current is 30% higher
            azure_monthly_cost=total_azure_compute,
            one_time_migration_cost=len(azure_migrate_data.servers) * 500,  # $500 per server migration
            annual_savings=(total_azure_compute * 1.3 - total_azure_compute) * 12,
            roi_months=18,
            details={
                "total_servers": len(azure_migrate_data.servers),
                "average_monthly_cost_per_server": total_azure_compute / len(azure_migrate_data.servers) if azure_migrate_data.servers else 0
            }
        )
        cost_estimates.append(compute_estimate)
        
        # Storage costs
        total_storage_gb = sum(server.disk_size_gb for server in azure_migrate_data.servers)
        storage_monthly_cost = total_storage_gb * 0.05  # $0.05 per GB estimate
        storage_estimate = CostEstimate(
            category="Storage",
            current_monthly_cost=storage_monthly_cost * 1.2,
            azure_monthly_cost=storage_monthly_cost,
            one_time_migration_cost=total_storage_gb * 0.01,  # Data transfer costs
            annual_savings=(storage_monthly_cost * 1.2 - storage_monthly_cost) * 12,
            roi_months=24,
            details={
                "total_storage_gb": total_storage_gb,
                "cost_per_gb": 0.05
            }
        )
        cost_estimates.append(storage_estimate)
        
        # Network costs
        network_estimate = CostEstimate(
            category="Network",
            current_monthly_cost=2000,  # Estimate current network costs
            azure_monthly_cost=1500,   # Azure network costs
            one_time_migration_cost=10000,  # Network setup costs
            annual_savings=(2000 - 1500) * 12,
            roi_months=20,
            details={
                "vpn_gateway": 150,
                "load_balancer": 25,
                "data_transfer": 500
            }
        )
        cost_estimates.append(network_estimate)
        
        # Management and monitoring
        management_estimate = CostEstimate(
            category="Management",
            current_monthly_cost=1000,
            azure_monthly_cost=800,
            one_time_migration_cost=5000,
            annual_savings=(1000 - 800) * 12,
            roi_months=25,
            details={
                "azure_monitor": 300,
                "log_analytics": 200,
                "backup": 300
            }
        )
        cost_estimates.append(management_estimate)
        
        return cost_estimates
    
    def _get_cpu_range(self, cpu_cores: int) -> str:
        """Get CPU range category."""
        if cpu_cores <= 2:
            return "1-2 cores"
        elif cpu_cores <= 4:
            return "3-4 cores"
        elif cpu_cores <= 8:
            return "5-8 cores"
        else:
            return "8+ cores"
    
    def _get_memory_range(self, memory_gb: float) -> str:
        """Get memory range category."""
        if memory_gb <= 4:
            return "1-4 GB"
        elif memory_gb <= 8:
            return "5-8 GB"
        elif memory_gb <= 16:
            return "9-16 GB"
        elif memory_gb <= 32:
            return "17-32 GB"
        else:
            return "32+ GB"
    
    def _determine_migration_approach(self, azure_migrate_data: AzureMigrateReport, transcript_insights: List[QuestionAnswer]) -> str:
        """Determine overall migration approach."""
        # Analyze transcript for migration preferences
        approach_keywords = {
            "lift-and-shift": ["rehost", "lift", "shift", "minimal changes"],
            "modernize": ["modernize", "refactor", "paas", "platform"],
            "rearchitect": ["rearchitect", "rebuild", "cloud-native", "containerize"]
        }
        
        approach_scores = {"lift-and-shift": 0, "modernize": 0, "rearchitect": 0}
        
        for qa in transcript_insights:
            content = (qa.question + " " + qa.answer).lower()
            for approach, keywords in approach_keywords.items():
                for keyword in keywords:
                    if keyword in content:
                        approach_scores[approach] += 1
        
        # Default to balanced approach if no clear preference
        primary_approach = max(approach_scores, key=approach_scores.get)
        
        return f"Hybrid approach with primary focus on {primary_approach}"
    
    def _generate_assumptions(self, transcript_insights: List[QuestionAnswer]) -> List[str]:
        """Generate project assumptions."""
        return [
            "Azure subscription and necessary permissions will be available",
            "Network connectivity between on-premises and Azure will be established",
            "Business stakeholders will provide necessary approvals for maintenance windows",
            "Sufficient budget allocation for migration tools and Azure resources",
            "Technical team will receive appropriate Azure training",
            "Current server performance baselines are representative of production load",
            "No major application changes will be required during migration timeframe"
        ]
    
    def _generate_constraints(self, transcript_insights: List[QuestionAnswer]) -> List[str]:
        """Generate project constraints."""
        constraints = [
            "Limited maintenance windows for production systems",
            "Compliance requirements must be maintained throughout migration",
            "No data loss tolerance for critical business applications"
        ]
        
        # Extract specific constraints from transcript
        for qa in transcript_insights:
            if any(keyword in qa.question.lower() for keyword in ['constraint', 'limitation', 'requirement', 'compliance']):
                if qa.answer and len(qa.answer) > 10:
                    constraints.append(qa.answer)
        
        return constraints[:10]  # Limit to top 10
    
    def _generate_resource_plan(self, migration_waves: List[MigrationWave], azure_migrate_data: AzureMigrateReport) -> Dict[str, Any]:
        """Generate resource allocation plan."""
        return {
            "project_team": {
                "project_manager": {
                    "role": "Project Manager",
                    "duration": "Full project duration",
                    "responsibilities": ["Overall project coordination", "Stakeholder management", "Risk management"]
                },
                "azure_architect": {
                    "role": "Azure Solution Architect",
                    "duration": "Full project duration",
                    "responsibilities": ["Architecture design", "Azure best practices", "Technical governance"]
                },
                "migration_engineers": {
                    "role": "Migration Engineers",
                    "count": len(migration_waves),
                    "duration": "Active migration phases",
                    "responsibilities": ["Server migration execution", "Testing and validation", "Issue resolution"]
                }
            },
            "training_requirements": {
                "azure_fundamentals": "All technical team members",
                "azure_administration": "Operations team",
                "azure_security": "Security team",
                "migration_tools": "Migration engineers"
            },
            "external_resources": {
                "azure_consulting": "Architecture review and best practices",
                "migration_tools": "Azure Migrate, third-party tools as needed",
                "training_provider": "Microsoft or certified Azure training partner"
            }
        }
    
    def _generate_training_plan(self, target_services: List[Dict[str, Any]], transcript_insights: List[QuestionAnswer]) -> Dict[str, Any]:
        """Generate comprehensive training plan."""
        return {
            "azure_fundamentals": {
                "target_audience": "All project team members",
                "duration": "2 days",
                "delivery": "Instructor-led or online",
                "content": ["Azure basics", "Core services", "Pricing and support"]
            },
            "azure_administration": {
                "target_audience": "IT Operations team",
                "duration": "5 days",
                "delivery": "Hands-on workshop",
                "content": ["Resource management", "Monitoring and alerts", "Security configuration"]
            },
            "migration_specific": {
                "target_audience": "Migration team",
                "duration": "3 days",
                "delivery": "Hands-on workshop",
                "content": ["Azure Migrate tools", "Migration best practices", "Troubleshooting"]
            },
            "ongoing_enablement": {
                "description": "Monthly knowledge sharing sessions",
                "duration": "2 hours per month",
                "content": "New Azure features, lessons learned, best practices"
            }
        }
    
    def _generate_communication_plan(self, migration_timeline: MigrationTimeline) -> Dict[str, Any]:
        """Generate communication plan."""
        return {
            "stakeholder_meetings": {
                "executive_updates": {
                    "frequency": "Monthly",
                    "audience": "Executive sponsors",
                    "content": "High-level progress, risks, budget status"
                },
                "project_team_meetings": {
                    "frequency": "Weekly",
                    "audience": "Core project team",
                    "content": "Detailed progress, technical issues, next steps"
                },
                "business_updates": {
                    "frequency": "Bi-weekly",
                    "audience": "Business stakeholders",
                    "content": "Impact on business operations, upcoming changes"
                }
            },
            "communication_channels": {
                "project_portal": "Centralized project documentation and status",
                "email_updates": "Weekly progress emails to all stakeholders",
                "teams_channel": "Real-time communication for project team"
            },
            "change_management": {
                "user_communications": "Regular updates on system changes",
                "training_announcements": "Schedule and requirements for user training",
                "go_live_notifications": "Detailed communications for each migration wave"
            }
        }
    
    def _define_security_requirements(self, transcript_insights: List[QuestionAnswer]) -> List[str]:
        """Define security requirements."""
        requirements = [
            "Implement Azure Security Center for continuous security monitoring",
            "Enable Azure AD for identity and access management",
            "Configure Network Security Groups for network segmentation",
            "Implement Azure Key Vault for secrets management",
            "Enable encryption at rest and in transit for all data",
            "Configure Azure Backup for data protection",
            "Implement Azure Monitor for security event logging",
            "Conduct security assessment post-migration"
        ]
        
        # Extract specific security requirements from transcript
        for qa in transcript_insights:
            if any(keyword in qa.question.lower() for keyword in ['security', 'compliance', 'encryption', 'access']):
                if qa.answer and len(qa.answer) > 10:
                    requirements.append(qa.answer)
        
        return requirements[:15]  # Limit to top 15
    
    def _define_compliance_requirements(self, transcript_insights: List[QuestionAnswer]) -> List[str]:
        """Define compliance requirements."""
        requirements = [
            "Maintain data residency requirements",
            "Implement audit logging for compliance reporting",
            "Configure data retention policies",
            "Ensure GDPR compliance for EU data",
            "Implement proper access controls and segregation of duties"
        ]
        
        # Extract specific compliance requirements from transcript
        for qa in transcript_insights:
            if any(keyword in qa.question.lower() for keyword in ['compliance', 'regulation', 'audit', 'gdpr', 'hipaa']):
                if qa.answer and len(qa.answer) > 10:
                    requirements.append(qa.answer)
        
        return requirements
    
    def _define_governance_model(self, transcript_insights: List[QuestionAnswer]) -> Dict[str, Any]:
        """Define governance model."""
        return {
            "governance_structure": {
                "steering_committee": "Executive oversight and decision making",
                "project_management_office": "Project coordination and reporting",
                "technical_working_group": "Technical decisions and standards",
                "business_working_group": "Business requirements and validation"
            },
            "decision_authority": {
                "architectural_decisions": "Azure Architect with steering committee approval",
                "migration_schedule": "Project Manager with business approval",
                "scope_changes": "Steering committee",
                "technical_issues": "Technical working group"
            },
            "standards_and_policies": {
                "naming_conventions": "Azure resource naming standards",
                "security_policies": "Enterprise security requirements in Azure",
                "cost_management": "Budget controls and resource optimization",
                "change_management": "Formal change control process"
            }
        }
    
    def _generate_kpis(self, azure_migrate_data: AzureMigrateReport, cost_estimates: List[CostEstimate]) -> List[Dict[str, Any]]:
        """Generate key performance indicators."""
        return [
            {
                "kpi": "Migration Success Rate",
                "target": "99%",
                "measurement": "Percentage of servers successfully migrated",
                "frequency": "Per migration wave"
            },
            {
                "kpi": "Downtime per Server",
                "target": "<4 hours",
                "measurement": "Average downtime during migration",
                "frequency": "Per server migration"
            },
            {
                "kpi": "Cost Optimization",
                "target": "20% reduction",
                "measurement": "Monthly infrastructure cost reduction",
                "frequency": "Monthly post-migration"
            },
            {
                "kpi": "Performance Baseline",
                "target": "Meet or exceed",
                "measurement": "Application performance vs. baseline",
                "frequency": "Post-migration validation"
            },
            {
                "kpi": "Security Posture",
                "target": "Zero critical findings",
                "measurement": "Security assessment results",
                "frequency": "Post-migration security scan"
            }
        ]
    
    def _generate_success_criteria(self, migration_waves: List[MigrationWave], transcript_insights: List[QuestionAnswer]) -> List[str]:
        """Generate overall success criteria."""
        criteria = [
            "All in-scope servers successfully migrated to Azure",
            "No data loss during migration process",
            "Application performance meets or exceeds baseline",
            "Security and compliance requirements fully implemented",
            "Total project delivered within approved budget and timeline",
            "Team successfully trained on Azure operations",
            "Business operations continue without significant disruption"
        ]
        
        # Add wave-specific criteria
        for wave in migration_waves:
            criteria.extend([f"{wave.name}: " + criterion for criterion in wave.success_criteria])
        
        return criteria
    
    def _generate_technical_specifications(self, azure_migrate_data: AzureMigrateReport, architecture_diagram: ArchitectureDiagram) -> Dict[str, Any]:
        """Generate technical specifications."""
        return {
            "azure_services": {
                service.azure_service: {
                    "component_count": len([c for c in architecture_diagram.components if c.azure_service == service.azure_service]),
                    "configuration": service.properties
                }
                for service in architecture_diagram.components
            },
            "network_architecture": {
                "virtual_networks": len([c for c in architecture_diagram.components if "Virtual Network" in c.azure_service]),
                "subnets": len([c for c in architecture_diagram.components if "Subnet" in c.azure_service]),
                "security_groups": len([c for c in architecture_diagram.components if "NSG" in c.azure_service or "Security Group" in c.azure_service])
            },
            "compute_specifications": {
                "total_servers": len(azure_migrate_data.servers),
                "total_cpu_cores": sum(s.cpu_cores for s in azure_migrate_data.servers),
                "total_memory_gb": sum(s.memory_gb for s in azure_migrate_data.servers),
                "total_storage_gb": sum(s.disk_size_gb for s in azure_migrate_data.servers)
            },
            "migration_tools": {
                "azure_migrate": "Primary assessment and migration tool",
                "azure_site_recovery": "Replication and failover",
                "azure_database_migration_service": "Database migrations",
                "azure_data_box": "Large data transfers if needed"
            }
        }
    
    def _identify_vendor_requirements(self, target_services: List[Dict[str, Any]], transcript_insights: List[QuestionAnswer]) -> List[str]:
        """Identify vendor and partner requirements."""
        requirements = [
            "Microsoft Azure subscription with appropriate service limits",
            "Azure support plan (Professional Direct or Premier recommended)",
            "Network service provider for ExpressRoute or VPN connectivity",
            "Azure Migrate licensing for assessment tools"
        ]
        
        # Add service-specific vendor requirements
        service_vendors = {
            "Azure SQL": "Microsoft SQL Server licensing considerations",
            "Azure AD": "Active Directory domain services integration",
            "Azure Backup": "Third-party backup tool migration planning"
        }
        
        for service in target_services:
            service_name = service.get("service_name", "")
            if service_name in service_vendors:
                requirements.append(service_vendors[service_name])
        
        return list(set(requirements))  # Remove duplicates
    
    def _determine_service_migration_strategy(self, service_type: str) -> str:
        """Determine migration strategy for Azure service."""
        strategies = {
            "Azure Virtual Machine": "Lift-and-shift",
            "Azure App Service": "Modernize",
            "Azure SQL Database": "Modernize",
            "Azure Container Instances": "Containerize",
            "Azure Kubernetes Service": "Rearchitect",
            "Azure Functions": "Rearchitect"
        }
        return strategies.get(service_type, "Lift-and-shift")
    
    def _get_service_benefits(self, service_type: str) -> List[str]:
        """Get benefits for Azure service."""
        benefits = {
            "Azure Virtual Machine": ["Familiar environment", "Minimal application changes", "Quick migration"],
            "Azure App Service": ["Managed platform", "Auto-scaling", "Built-in monitoring"],
            "Azure SQL Database": ["Managed service", "Built-in high availability", "Automatic backups"],
            "Azure Container Instances": ["Resource efficiency", "Fast startup", "Pay-per-second billing"],
            "Azure Kubernetes Service": ["Container orchestration", "Auto-scaling", "DevOps integration"]
        }
        return benefits.get(service_type, ["Cloud benefits", "Scalability", "Managed service"])
    
    def _get_service_considerations(self, service_type: str) -> List[str]:
        """Get considerations for Azure service."""
        considerations = {
            "Azure Virtual Machine": ["OS licensing costs", "Patching responsibility", "Limited auto-scaling"],
            "Azure App Service": ["Application compatibility", "Framework limitations", "Code changes may be required"],
            "Azure SQL Database": ["Feature compatibility", "Connection string changes", "Potential performance tuning"],
            "Azure Container Instances": ["Application containerization", "State management", "Networking complexity"],
            "Azure Kubernetes Service": ["Container expertise required", "Complex networking", "Operational overhead"]
        }
        return considerations.get(service_type, ["Cost optimization", "Security configuration", "Operational procedures"])
    
    def _estimate_service_effort(self, service_type: str, component_count: int) -> str:
        """Estimate effort for service migration."""
        base_efforts = {
            "Azure Virtual Machine": 2,  # days per VM
            "Azure App Service": 5,      # days per app
            "Azure SQL Database": 3,     # days per database
            "Azure Container Instances": 4,  # days per container group
            "Azure Kubernetes Service": 10   # days per cluster
        }
        
        base_effort = base_efforts.get(service_type, 3)
        total_days = base_effort * component_count
        
        if total_days <= 5:
            return "Low (< 1 week)"
        elif total_days <= 20:
            return "Medium (1-4 weeks)"
        elif total_days <= 60:
            return "High (1-3 months)"
        else:
            return "Very High (3+ months)"
