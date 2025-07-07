"""
Architecture Diagram Generator for Azure Migration
==================================================

This module generates Visio-compatible architecture diagrams based on Azure Migrate reports
and transcript analysis. The diagrams are created in formats that can be opened and edited in Visio.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple
import json
import os
from datetime import datetime
import math
from .StateBase import (
    AzureMigrateReport, AzureMigrateServer, ArchitectureDiagram, 
    ArchitectureComponent, QuestionAnswer, ExcelOutputType
)
from .VisioExporter import VisioExporter


class ArchitectureDiagramGenerator:
    """Generator for Azure architecture diagrams compatible with Visio."""
    
    def __init__(self):
        self.component_types = {
            # Compute Components
            'vm': {'shape': 'Virtual Machine', 'color': '#4472C4', 'tier': 'compute'},
            'vmss': {'shape': 'VM Scale Set', 'color': '#4472C4', 'tier': 'compute'},
            'aks': {'shape': 'Kubernetes Service', 'color': '#4472C4', 'tier': 'compute'},
            'container': {'shape': 'Container Instances', 'color': '#4472C4', 'tier': 'compute'},
            'appservice': {'shape': 'App Service', 'color': '#E07C24', 'tier': 'application'},
            'function': {'shape': 'Azure Functions', 'color': '#E07C24', 'tier': 'application'},
            
            # Database Components
            'sql': {'shape': 'Azure SQL', 'color': '#70AD47', 'tier': 'data'},
            'mysql': {'shape': 'MySQL Database', 'color': '#70AD47', 'tier': 'data'},
            'postgresql': {'shape': 'PostgreSQL Database', 'color': '#70AD47', 'tier': 'data'},
            'cosmosdb': {'shape': 'Cosmos DB', 'color': '#70AD47', 'tier': 'data'},
            'redis': {'shape': 'Redis Cache', 'color': '#70AD47', 'tier': 'data'},
            
            # Storage Components
            'storage': {'shape': 'Storage Account', 'color': '#FFC000', 'tier': 'data'},
            'backup': {'shape': 'Backup Vault', 'color': '#FFC000', 'tier': 'data'},
            'fileshare': {'shape': 'File Share', 'color': '#FFC000', 'tier': 'data'},
            
            # Network Components
            'vnet': {'shape': 'Virtual Network', 'color': '#00B0F0', 'tier': 'network'},
            'subnet': {'shape': 'Subnet', 'color': '#00B0F0', 'tier': 'network'},
            'nsg': {'shape': 'Network Security Group', 'color': '#B91C1C', 'tier': 'security'},
            'loadbalancer': {'shape': 'Load Balancer', 'color': '#7030A0', 'tier': 'network'},
            'appgateway': {'shape': 'Application Gateway', 'color': '#7030A0', 'tier': 'network'},
            'frontdoor': {'shape': 'Front Door', 'color': '#7030A0', 'tier': 'network'},
            'cdn': {'shape': 'CDN', 'color': '#7030A0', 'tier': 'network'},
            'vpngateway': {'shape': 'VPN Gateway', 'color': '#7030A0', 'tier': 'network'},
            'expressroute': {'shape': 'ExpressRoute', 'color': '#7030A0', 'tier': 'network'},
            'firewall': {'shape': 'Azure Firewall', 'color': '#B91C1C', 'tier': 'security'},
            'ddos': {'shape': 'DDoS Protection', 'color': '#B91C1C', 'tier': 'security'},
            
            # Security & Identity
            'keyvault': {'shape': 'Key Vault', 'color': '#B91C1C', 'tier': 'security'},
            'aad': {'shape': 'Azure AD', 'color': '#B91C1C', 'tier': 'security'},
            'sentinel': {'shape': 'Azure Sentinel', 'color': '#B91C1C', 'tier': 'security'},
            
            # Monitoring & Management
            'monitor': {'shape': 'Azure Monitor', 'color': '#6B7280', 'tier': 'management'},
            'loganalytics': {'shape': 'Log Analytics', 'color': '#6B7280', 'tier': 'management'},
            'appinsights': {'shape': 'Application Insights', 'color': '#6B7280', 'tier': 'management'},
            
            # Integration Services
            'servicebus': {'shape': 'Service Bus', 'color': '#10B981', 'tier': 'integration'},
            'eventgrid': {'shape': 'Event Grid', 'color': '#10B981', 'tier': 'integration'},
            'apimanagement': {'shape': 'API Management', 'color': '#10B981', 'tier': 'integration'}
        }
        
        self.azure_service_mapping = {
            'windows server': 'vm',
            'linux server': 'vm',
            'ubuntu': 'vm',
            'centos': 'vm',
            'rhel': 'vm',
            'sql server': 'sql',
            'mysql': 'mysql',
            'postgresql': 'postgresql',
            'oracle': 'vm',  # Oracle on VM
            'web server': 'appservice',
            'iis': 'appservice',
            'apache': 'vm',
            'nginx': 'vm',
            'application server': 'appservice',
            'file server': 'storage',
            'domain controller': 'vm',
            'active directory': 'aad',
            'dns server': 'vm',
            'exchange server': 'vm',
            'sharepoint': 'vm'
        }
    
    def generate_architecture_from_migrate_and_transcript(
        self, 
        migrate_report: AzureMigrateReport, 
        excel_output: ExcelOutputType
    ) -> ArchitectureDiagram:
        """
        Generate architecture diagram from Azure Migrate report and transcript analysis.
        
        Args:
            migrate_report: Parsed Azure Migrate report
            excel_output: Processed Q&A from transcript
            
        Returns:
            ArchitectureDiagram object
        """
        
        # Step 1: Analyze transcript for architecture insights
        architecture_insights = self._extract_architecture_insights(excel_output)
        
        # Step 2: Map Azure Migrate servers to Azure services
        components = self._map_servers_to_azure_components(migrate_report.servers, architecture_insights)
        
        # Step 3: Add network and supporting components
        components.extend(self._add_network_components(components, architecture_insights))
        
        # Step 4: Calculate positions for components
        positioned_components = self._calculate_component_positions(components)
        
        # Step 5: Establish connections between components
        connected_components = self._establish_connections(positioned_components, architecture_insights)
        
        # Create the architecture diagram
        diagram = ArchitectureDiagram(
            title=f"Azure Target Architecture - {datetime.now().strftime('%Y-%m-%d')}",
            components=connected_components,
            metadata={
                "source_servers": len(migrate_report.servers),
                "azure_components": len(connected_components),
                "generation_method": "azure_migrate_and_transcript",
                "insights_used": len(architecture_insights),
                "migrate_summary": migrate_report.summary
            }
        )
        
        return diagram
    
    def _extract_architecture_insights(self, excel_output: ExcelOutputType) -> Dict[str, Any]:
        """Extract architecture-relevant insights from transcript Q&A."""
        insights = {
            'technologies': [],
            'requirements': [],
            'constraints': [],
            'preferences': {},
            'performance_needs': {},
            'security_requirements': [],
            'compliance_needs': []
        }
        
        # Keywords to look for in Q&A
        tech_keywords = {
            'database': ['sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'cosmos'],
            'web': ['web server', 'iis', 'apache', 'nginx', 'tomcat'],
            'application': ['app server', 'application', 'middleware', 'api'],
            'container': ['docker', 'kubernetes', 'container', 'k8s'],
            'storage': ['file server', 'storage', 'nas', 'san', 'backup'],
            'security': ['firewall', 'vpn', 'security', 'authentication', 'ssl', 'tls']
        }
        
        # Analyze Q&A for insights
        for qa in excel_output.questions_answers:
            if qa.is_answered:
                answer_lower = qa.answer.lower()
                question_lower = qa.question.lower()
                
                # Extract technologies mentioned
                for category, keywords in tech_keywords.items():
                    for keyword in keywords:
                        if keyword in answer_lower or keyword in question_lower:
                            if category not in [tech['category'] for tech in insights['technologies']]:
                                insights['technologies'].append({
                                    'category': category,
                                    'keyword': keyword,
                                    'confidence': qa.confidence
                                })
                
                # Extract requirements
                if any(req_word in question_lower for req_word in ['requirement', 'need', 'must', 'should']):
                    insights['requirements'].append({
                        'requirement': qa.question,
                        'answer': qa.answer,
                        'confidence': qa.confidence
                    })
                
                # Extract performance needs
                if any(perf_word in answer_lower for perf_word in ['performance', 'load', 'users', 'concurrent']):
                    insights['performance_needs'][qa.question] = qa.answer
                
                # Extract security requirements
                if any(sec_word in answer_lower for sec_word in ['security', 'compliance', 'encrypt', 'audit']):
                    insights['security_requirements'].append({
                        'question': qa.question,
                        'answer': qa.answer
                    })
        
        return insights
    
    def _map_servers_to_azure_components(
        self, 
        servers: List[AzureMigrateServer], 
        insights: Dict[str, Any]
    ) -> List[ArchitectureComponent]:
        """Map Azure Migrate servers to Azure components."""
        components = []
        
        for i, server in enumerate(servers):
            # Determine Azure service based on server characteristics and insights
            azure_service = self._determine_azure_service(server, insights)
            component_type = self._get_component_type(azure_service)
            
            component = ArchitectureComponent(
                component_id=f"comp_{i+1}",
                component_type=component_type,
                name=server.server_name or f"Server_{i+1}",
                azure_service=azure_service,
                tier=self.component_types.get(component_type, {}).get('tier', 'compute'),
                properties={
                    'cpu_cores': server.cpu_cores,
                    'memory_gb': server.memory_gb,
                    'disk_size_gb': server.disk_size_gb,
                    'operating_system': server.operating_system,
                    'original_server': server.server_name,
                    'estimated_cost': server.estimated_cost,
                    'readiness': server.readiness,
                    'recommendation': server.recommendation
                },
                source_server=server.server_name,
                migration_type=self._determine_migration_type(server, insights)
            )
            
            components.append(component)
        
        return components
    
    def _determine_azure_service(self, server: AzureMigrateServer, insights: Dict[str, Any]) -> str:
        """Determine the appropriate Azure service for a server."""
        
        # Check explicit recommendations first
        if server.recommendation:
            rec_lower = server.recommendation.lower()
            if 'app service' in rec_lower:
                return 'Azure App Service'
            elif 'sql' in rec_lower:
                return 'Azure SQL Database'
            elif 'vm' in rec_lower or 'virtual machine' in rec_lower:
                return 'Azure Virtual Machine'
            elif 'function' in rec_lower:
                return 'Azure Functions'
            elif 'container' in rec_lower:
                return 'Azure Container Instances'
        
        # Check server type and OS
        server_info = f"{server.server_type} {server.operating_system}".lower()
        
        # Database servers
        if any(db in server_info for db in ['sql', 'database', 'mysql', 'postgresql', 'oracle']):
            if 'sql server' in server_info:
                return 'Azure SQL Database'
            else:
                return 'Azure Database for MySQL'  # Default for other databases
        
        # Web servers
        if any(web in server_info for web in ['web', 'iis', 'apache', 'nginx']):
            return 'Azure App Service'
        
        # File servers
        if 'file' in server_info or 'storage' in server_info:
            return 'Azure Storage Account'
        
        # Domain controllers and specialized servers
        if any(dc in server_info for dc in ['domain controller', 'active directory', 'ldap']):
            return 'Azure Virtual Machine'  # These typically need VMs
        
        # Check insights for additional context
        tech_categories = [tech['category'] for tech in insights.get('technologies', [])]
        if 'container' in tech_categories:
            return 'Azure Container Instances'
        elif 'web' in tech_categories and server.memory_gb <= 4:
            return 'Azure App Service'
        
        # Default to VM for unknown or complex applications
        return 'Azure Virtual Machine'
    
    def _get_component_type(self, azure_service: str) -> str:
        """Get component type from Azure service name."""
        service_lower = azure_service.lower()
        
        if 'virtual machine' in service_lower or 'vm' in service_lower:
            return 'vm'
        elif 'sql' in service_lower or 'database' in service_lower:
            return 'database'
        elif 'app service' in service_lower:
            return 'appservice'
        elif 'storage' in service_lower:
            return 'storage'
        elif 'function' in service_lower:
            return 'function'
        elif 'container' in service_lower:
            return 'container'
        elif 'kubernetes' in service_lower:
            return 'aks'
        else:
            return 'vm'  # Default
    
    def _determine_migration_type(self, server: AzureMigrateServer, insights: Dict[str, Any]) -> str:
        """Determine migration strategy based on server and insights."""
        
        # Check for modernization indicators in insights
        tech_categories = [tech['category'] for tech in insights.get('technologies', [])]
        
        if 'container' in tech_categories:
            return 'containerize'
        
        # Check server characteristics for modernization opportunities
        if server.operating_system and 'windows' in server.operating_system.lower():
            if server.memory_gb <= 8 and any(web in (server.server_type or "").lower() for web in ['web', 'iis']):
                return 'modernize'
        
        # Default to lift-and-shift
        return 'lift-and-shift'
    
    def _add_network_components(
        self, 
        components: List[ArchitectureComponent], 
        insights: Dict[str, Any]
    ) -> List[ArchitectureComponent]:
        """Add comprehensive Azure network and security components."""
        additional_components = []
        
        # Determine if this is a multi-tier application
        has_web_tier = any(c.tier in ['application'] for c in components)
        has_data_tier = any(c.tier == 'data' for c in components)
        has_compute_tier = any(c.tier == 'compute' for c in components)
        
        # Add Virtual Network with subnets
        vnet = ArchitectureComponent(
            component_id="vnet_main",
            component_type="vnet",
            name="Production VNet",
            azure_service="Azure Virtual Network",
            tier="network",
            properties={
                'address_space': '10.0.0.0/16',
                'location': 'East US 2',
                'dns_servers': ['168.63.129.16']  # Azure DNS
            }
        )
        additional_components.append(vnet)
        
        # Add subnets based on tiers
        subnet_configs = []
        if has_web_tier or has_compute_tier:
            web_subnet = ArchitectureComponent(
                component_id="subnet_web",
                component_type="subnet",
                name="Web Subnet",
                azure_service="Azure Subnet",
                tier="network",
                properties={
                    'address_prefix': '10.0.1.0/24',
                    'parent_vnet': 'vnet_main'
                }
            )
            additional_components.append(web_subnet)
            subnet_configs.append('web')
        
        if has_compute_tier or len([c for c in components if c.tier == 'application']) > 0:
            app_subnet = ArchitectureComponent(
                component_id="subnet_app",
                component_type="subnet",
                name="Application Subnet",
                azure_service="Azure Subnet",
                tier="network",
                properties={
                    'address_prefix': '10.0.2.0/24',
                    'parent_vnet': 'vnet_main'
                }
            )
            additional_components.append(app_subnet)
            subnet_configs.append('app')
        
        if has_data_tier:
            data_subnet = ArchitectureComponent(
                component_id="subnet_data",
                component_type="subnet",
                name="Data Subnet",
                azure_service="Azure Subnet",
                tier="network",
                properties={
                    'address_prefix': '10.0.3.0/24',
                    'parent_vnet': 'vnet_main'
                }
            )
            additional_components.append(data_subnet)
            subnet_configs.append('data')
        
        # Add Network Security Groups for each subnet
        for subnet_type in subnet_configs:
            nsg = ArchitectureComponent(
                component_id=f"nsg_{subnet_type}",
                component_type="nsg",
                name=f"{subnet_type.title()} NSG",
                azure_service="Network Security Group",
                tier="security",
                properties={
                    'associated_subnet': f"subnet_{subnet_type}",
                    'rules': self._get_nsg_rules(subnet_type, insights)
                }
            )
            additional_components.append(nsg)
        
        # Add Application Gateway for web applications
        if has_web_tier or any('web' in c.azure_service.lower() or 'app service' in c.azure_service.lower() 
                              for c in components):
            app_gateway = ArchitectureComponent(
                component_id="appgw_main",
                component_type="appgateway",
                name="Application Gateway",
                azure_service="Azure Application Gateway",
                tier="network",
                properties={
                    'sku': 'Standard_v2',
                    'tier': 'Standard_v2',
                    'subnet': 'subnet_web',
                    'features': ['WAF', 'SSL Termination', 'URL Routing']
                }
            )
            additional_components.append(app_gateway)
        
        # Add Load Balancer for multiple VMs
        vm_components = [c for c in components if c.component_type == 'vm']
        if len(vm_components) > 1:
            lb = ArchitectureComponent(
                component_id="lb_internal",
                component_type="loadbalancer",
                name="Internal Load Balancer",
                azure_service="Azure Load Balancer",
                tier="network",
                properties={
                    'type': 'Internal',
                    'sku': 'Standard',
                    'backend_pools': [c.component_id for c in vm_components]
                }
            )
            additional_components.append(lb)
        
        # Add Azure Firewall for centralized security
        firewall = ArchitectureComponent(
            component_id="fw_main",
            component_type="firewall",
            name="Azure Firewall",
            azure_service="Azure Firewall",
            tier="security",
            properties={
                'sku': 'Standard',
                'threat_intel_mode': 'Alert',
                'dns_proxy': True
            }
        )
        additional_components.append(firewall)
        
        # Add Key Vault for secrets management
        keyvault = ArchitectureComponent(
            component_id="kv_main",
            component_type="keyvault",
            name="Key Vault",
            azure_service="Azure Key Vault",
            tier="security",
            properties={
                'access_policies': 'Managed Identity',
                'soft_delete': True,
                'purge_protection': True
            }
        )
        additional_components.append(keyvault)
        
        # Add Storage Account for general storage needs
        if not any(c.component_type == 'storage' for c in components):
            storage = ArchitectureComponent(
                component_id="storage_main",
                component_type="storage",
                name="General Storage",
                azure_service="Azure Storage Account",
                tier="data",
                properties={
                    'type': 'Standard_LRS',
                    'tier': 'Hot',
                    'encryption': 'Microsoft Managed',
                    'secure_transfer': True
                }
            )
            additional_components.append(storage)
        
        # Add Azure Backup for backup services
        backup = ArchitectureComponent(
            component_id="backup_main",
            component_type="backup",
            name="Backup Vault",
            azure_service="Azure Backup",
            tier="data",
            properties={
                'vault_type': 'Recovery Services',
                'backup_policy': 'Daily',
                'retention': '30 days'
            }
        )
        additional_components.append(backup)
        
        # Add monitoring components
        monitor = ArchitectureComponent(
            component_id="monitor_main",
            component_type="monitor",
            name="Azure Monitor",
            azure_service="Azure Monitor",
            tier="management",
            properties={
                'metrics_retention': '93 days',
                'log_retention': '30 days'
            }
        )
        additional_components.append(monitor)
        
        log_analytics = ArchitectureComponent(
            component_id="la_main",
            component_type="loganalytics",
            name="Log Analytics Workspace",
            azure_service="Log Analytics",
            tier="management",
            properties={
                'retention': '30 days',
                'sku': 'PerGB2018'
            }
        )
        additional_components.append(log_analytics)
        
        # Add connectivity to on-premises (VPN Gateway or ExpressRoute)
        # Check insights for hybrid connectivity requirements
        needs_hybrid = any(
            'on-premise' in str(insight).lower() or 'on-prem' in str(insight).lower() or
            'hybrid' in str(insight).lower() or 'vpn' in str(insight).lower()
            for insight in insights.get('requirements', [])
        )
        
        if needs_hybrid:
            vpn_gateway = ArchitectureComponent(
                component_id="vpngw_main",
                component_type="vpngateway",
                name="VPN Gateway",
                azure_service="Azure VPN Gateway",
                tier="network",
                properties={
                    'sku': 'VpnGw1',
                    'vpn_type': 'RouteBased',
                    'active_active': False
                }
            )
            additional_components.append(vpn_gateway)
        
        return additional_components
    
    def _get_nsg_rules(self, subnet_type: str, insights: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate NSG rules based on subnet type and insights."""
        base_rules = [
            {
                'name': 'DenyAllInbound',
                'priority': '4000',
                'direction': 'Inbound',
                'access': 'Deny',
                'protocol': '*',
                'source': '*',
                'destination': '*'
            }
        ]
        
        if subnet_type == 'web':
            base_rules.extend([
                {
                    'name': 'AllowHTTP',
                    'priority': '1000',
                    'direction': 'Inbound',
                    'access': 'Allow',
                    'protocol': 'TCP',
                    'source': '*',
                    'destination': '*',
                    'port': '80'
                },
                {
                    'name': 'AllowHTTPS',
                    'priority': '1010',
                    'direction': 'Inbound',
                    'access': 'Allow',
                    'protocol': 'TCP',
                    'source': '*',
                    'destination': '*',
                    'port': '443'
                }
            ])
        elif subnet_type == 'app':
            base_rules.extend([
                {
                    'name': 'AllowWebToApp',
                    'priority': '1000',
                    'direction': 'Inbound',
                    'access': 'Allow',
                    'protocol': 'TCP',
                    'source': '10.0.1.0/24',
                    'destination': '*',
                    'port': '8080'
                }
            ])
        elif subnet_type == 'data':
            base_rules.extend([
                {
                    'name': 'AllowAppToData',
                    'priority': '1000',
                    'direction': 'Inbound',
                    'access': 'Allow',
                    'protocol': 'TCP',
                    'source': '10.0.2.0/24',
                    'destination': '*',
                    'port': '1433'
                }
            ])
        
        return base_rules
    
    def _calculate_component_positions(
        self, 
        components: List[ArchitectureComponent]
    ) -> List[ArchitectureComponent]:
        """Calculate positions for components in a comprehensive Azure architecture layout."""
        
        # Group components by tier with Azure-specific grouping
        tiers = {
            'security': [],      # Top tier - Security & Identity
            'network': [],       # Network components
            'application': [],   # Application tier
            'compute': [],       # Compute tier
            'data': [],         # Data tier
            'management': [],   # Management & Monitoring
            'integration': []   # Integration services
        }
        
        for component in components:
            tier = component.tier
            if tier not in tiers:
                tiers[tier] = []
            tiers[tier].append(component)
        
        # Define tier positions with more space for complex architectures
        tier_y_positions = {
            'security': 50,      # Security at top
            'network': 200,      # Network layer
            'application': 350,  # Application layer
            'compute': 350,      # Compute on same level as application
            'data': 500,        # Data layer
            'management': 650,   # Management at bottom
            'integration': 650   # Integration on same level as management
        }
        
        # Position components within each tier
        positioned_components = []
        canvas_width = 1200  # Wider canvas for complex architectures
        
        for tier, tier_components in tiers.items():
            if not tier_components:
                continue
                
            y_pos = tier_y_positions.get(tier, 400)
            
            # Special handling for different tiers
            if tier == 'network':
                # Network components in a grid pattern
                positioned_components.extend(
                    self._position_network_components(tier_components, y_pos)
                )
            elif tier == 'security':
                # Security components spread across top
                positioned_components.extend(
                    self._position_security_components(tier_components, y_pos, canvas_width)
                )
            else:
                # Standard horizontal layout for other tiers
                x_spacing = canvas_width / max(len(tier_components), 1)
                x_start = 100
                
                for i, component in enumerate(tier_components):
                    component.position = {
                        'x': x_start + (i * x_spacing),
                        'y': y_pos,
                        'width': 140,
                        'height': 90
                    }
                    positioned_components.append(component)
        
        return positioned_components
    
    def _position_network_components(
        self, 
        components: List[ArchitectureComponent], 
        y_base: int
    ) -> List[ArchitectureComponent]:
        """Position network components in a logical layout."""
        positioned = []
        
        # Categorize network components
        vnets = [c for c in components if c.component_type == 'vnet']
        subnets = [c for c in components if c.component_type == 'subnet']
        gateways = [c for c in components if c.component_type in ['appgateway', 'vpngateway']]
        load_balancers = [c for c in components if c.component_type == 'loadbalancer']
        other_network = [c for c in components if c not in vnets + subnets + gateways + load_balancers]
        
        x_pos = 100
        
        # Position VNets first (largest network container)
        for vnet in vnets:
            vnet.position = {
                'x': x_pos,
                'y': y_base,
                'width': 300,  # Larger for VNet
                'height': 120
            }
            positioned.append(vnet)
            x_pos += 350
        
        # Position subnets within or near VNet
        subnet_y = y_base + 40
        subnet_x = 120
        for subnet in subnets:
            subnet.position = {
                'x': subnet_x,
                'y': subnet_y,
                'width': 100,
                'height': 60
            }
            positioned.append(subnet)
            subnet_x += 120
        
        # Position gateways
        for gateway in gateways:
            gateway.position = {
                'x': x_pos,
                'y': y_base,
                'width': 120,
                'height': 80
            }
            positioned.append(gateway)
            x_pos += 140
        
        # Position load balancers
        for lb in load_balancers:
            lb.position = {
                'x': x_pos,
                'y': y_base,
                'width': 120,
                'height': 80
            }
            positioned.append(lb)
            x_pos += 140
        
        # Position other network components
        for comp in other_network:
            comp.position = {
                'x': x_pos,
                'y': y_base,
                'width': 120,
                'height': 80
            }
            positioned.append(comp)
            x_pos += 140
        
        return positioned
    
    def _position_security_components(
        self, 
        components: List[ArchitectureComponent], 
        y_pos: int,
        canvas_width: int
    ) -> List[ArchitectureComponent]:
        """Position security components across the top of the architecture."""
        positioned = []
        
        if not components:
            return positioned
        
        # Spread security components across the top
        x_spacing = (canvas_width - 200) / max(len(components), 1)
        x_start = 100
        
        for i, component in enumerate(components):
            component.position = {
                'x': x_start + (i * x_spacing),
                'y': y_pos,
                'width': 120,
                'height': 80
            }
            positioned.append(component)
        
        return positioned
    
    def export_to_visio_vsdx(self, diagram: ArchitectureDiagram, output_path: str):
        """Export diagram to VSDX format using the enhanced VisioExporter."""
        visio_exporter = VisioExporter()
        visio_exporter.export_to_vsdx(diagram, output_path)
    
    def export_to_visio_xml(self, diagram: ArchitectureDiagram, output_path: str):
        """Export diagram to enhanced Visio XML format."""
        visio_exporter = VisioExporter()
        visio_exporter.export_to_visio_xml_enhanced(diagram, output_path)
    
    def export_to_json(self, diagram: ArchitectureDiagram, output_path: str):
        """Export diagram to JSON format for further processing."""
        
        diagram_dict = {
            "diagram_id": diagram.diagram_id,
            "title": diagram.title,
            "created_date": diagram.created_date,
            "metadata": diagram.metadata,
            "components": [
                {
                    "component_id": comp.component_id,
                    "component_type": comp.component_type,
                    "name": comp.name,
                    "azure_service": comp.azure_service,
                    "tier": comp.tier,
                    "position": comp.position,
                    "properties": comp.properties,
                    "connections": comp.connections,
                    "source_server": comp.source_server,
                    "migration_type": comp.migration_type
                }
                for comp in diagram.components
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(diagram_dict, f, indent=2, ensure_ascii=False)
    
    def export_to_svg(self, diagram: ArchitectureDiagram, output_path: str):
        """Export diagram to SVG format that can be imported into Visio."""
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .component-rect {{ fill: #4472C4; stroke: #2E4A8B; stroke-width: 2; }}
      .component-text {{ fill: white; font-family: Arial; font-size: 12px; text-anchor: middle; }}
      .tier-label {{ fill: #333; font-family: Arial; font-size: 14px; font-weight: bold; }}
      .connection-line {{ stroke: #666; stroke-width: 2; marker-end: url(#arrowhead); }}
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
    </marker>
  </defs>
  
  <title>{diagram.title}</title>
'''
        
        # Add tier labels
        tier_positions = {'network': 100, 'application': 250, 'compute': 400, 'data': 550}
        for tier, y_pos in tier_positions.items():
            if any(c.tier == tier for c in diagram.components):
                svg_content += f'  <text x="20" y="{y_pos + 40}" class="tier-label">{tier.title()} Tier</text>\n'
        
        # Add components
        for component in diagram.components:
            x = component.position.get('x', 0)
            y = component.position.get('y', 0)
            width = component.position.get('width', 120)
            height = component.position.get('height', 80)
            
            # Component shape color based on type
            color = self.component_types.get(component.component_type, {}).get('color', '#4472C4')
            
            svg_content += f'''  <rect x="{x}" y="{y}" width="{width}" height="{height}" 
                              fill="{color}" stroke="#2E4A8B" stroke-width="2" rx="5"/>
  <text x="{x + width/2}" y="{y + height/2 - 10}" class="component-text">{component.name}</text>
  <text x="{x + width/2}" y="{y + height/2 + 10}" class="component-text" font-size="10">{component.azure_service}</text>
'''
        
        # Add connections
        component_lookup = {c.component_id: c for c in diagram.components}
        for component in diagram.components:
            for connection_id in component.connections:
                if connection_id in component_lookup:
                    target = component_lookup[connection_id]
                    x1 = component.position.get('x', 0) + component.position.get('width', 120) / 2
                    y1 = component.position.get('y', 0) + component.position.get('height', 80)
                    x2 = target.position.get('x', 0) + target.position.get('width', 120) / 2
                    y2 = target.position.get('y', 0)
                    
                    svg_content += f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="connection-line"/>\n'
        
        svg_content += '</svg>'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
    
    def _establish_connections(
        self, 
        components: List[ArchitectureComponent], 
        insights: Dict[str, Any]
    ) -> List[ArchitectureComponent]:
        """Establish comprehensive connections between Azure components."""
        
        # Create component lookup
        component_lookup = {c.component_id: c for c in components}
        
        # Get component categories for easier connection logic
        vnets = [c for c in components if c.component_type == 'vnet']
        subnets = [c for c in components if c.component_type == 'subnet']
        nsgs = [c for c in components if c.component_type == 'nsg']
        vms = [c for c in components if c.component_type == 'vm']
        app_services = [c for c in components if c.component_type == 'appservice']
        databases = [c for c in components if c.component_type in ['sql', 'mysql', 'postgresql', 'cosmosdb']]
        storage_accounts = [c for c in components if c.component_type == 'storage']
        app_gateways = [c for c in components if c.component_type == 'appgateway']
        load_balancers = [c for c in components if c.component_type == 'loadbalancer']
        firewalls = [c for c in components if c.component_type == 'firewall']
        key_vaults = [c for c in components if c.component_type == 'keyvault']
        monitoring = [c for c in components if c.component_type in ['monitor', 'loganalytics']]
        
        # Establish VNet to Subnet connections
        for vnet in vnets:
            vnet_subnets = [s for s in subnets if s.properties.get('parent_vnet') == vnet.component_id]
            vnet.connections.extend([s.component_id for s in vnet_subnets])
        
        # Connect NSGs to their associated subnets
        for nsg in nsgs:
            associated_subnet = nsg.properties.get('associated_subnet')
            if associated_subnet:
                # Find the actual subnet component
                subnet_component = next((s for s in subnets if s.component_id == associated_subnet), None)
                if subnet_component:
                    nsg.connections.append(subnet_component.component_id)
                    subnet_component.connections.append(nsg.component_id)
        
        # Connect Application Gateway to web-tier components
        for app_gw in app_gateways:
            # Connect to App Services and web VMs
            web_targets = app_services + [vm for vm in vms if 'web' in vm.name.lower() or 'iis' in vm.properties.get('operating_system', '').lower()]
            app_gw.connections.extend([target.component_id for target in web_targets])
        
        # Connect Load Balancers to VMs
        for lb in load_balancers:
            backend_pools = lb.properties.get('backend_pools', [])
            if backend_pools:
                lb.connections.extend(backend_pools)
            else:
                # Connect to all VMs if no specific backend pools defined
                lb.connections.extend([vm.component_id for vm in vms])
        
        # Connect application tier to data tier
        app_tier_components = app_services + [vm for vm in vms if vm.tier in ['application', 'compute']]
        for app_comp in app_tier_components:
            # Connect to databases
            app_comp.connections.extend([db.component_id for db in databases])
            # Connect to storage accounts
            app_comp.connections.extend([storage.component_id for storage in storage_accounts])
        
        # Connect VMs to storage for diagnostics and data
        for vm in vms:
            if storage_accounts:
                vm.connections.append(storage_accounts[0].component_id)  # Connect to primary storage
        
        # Connect all components to Key Vault for secrets
        secure_components = vms + app_services + databases
        for kv in key_vaults:
            kv.connections.extend([comp.component_id for comp in secure_components])
        
        # Connect all resources to monitoring
        all_azure_resources = [c for c in components if c.tier not in ['management']]
        for monitor_comp in monitoring:
            monitor_comp.connections.extend([comp.component_id for comp in all_azure_resources])
        
        # Connect Firewall to subnets for traffic inspection
        for firewall in firewalls:
            firewall.connections.extend([subnet.component_id for subnet in subnets])
        
        # Establish subnet-based connections (components in same subnet connect to each other)
        subnet_mappings = {
            'subnet_web': [c for c in components if c.tier == 'application' or 'web' in c.name.lower()],
            'subnet_app': [c for c in components if c.tier == 'compute' or c.component_type == 'vm'],
            'subnet_data': databases + storage_accounts
        }
        
        for subnet_id, subnet_components in subnet_mappings.items():
            # Components in the same subnet can communicate with each other
            for comp in subnet_components:
                other_components = [c for c in subnet_components if c.component_id != comp.component_id]
                comp.connections.extend([c.component_id for c in other_components if c.component_id not in comp.connections])
        
        # Remove duplicate connections and self-references
        for component in components:
            component.connections = list(set(component.connections))
            if component.component_id in component.connections:
                component.connections.remove(component.component_id)
        
        return components
