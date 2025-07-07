"""
Enhanced Visio Export for Azure Architecture Diagrams
=====================================================

This module provides enhanced Visio export capabilities, generating files that can be
directly opened and edited in Microsoft Visio.
"""

import xml.etree.ElementTree as ET
import zipfile
import json
import os
from typing import List, Dict, Any
from .StateBase import ArchitectureDiagram, ArchitectureComponent


class VisioExporter:
    """Enhanced Visio exporter for Azure architecture diagrams."""
    
    def __init__(self):
        # Visio stencil mappings for Azure components
        self.visio_stencils = {
            # Compute
            'vm': {'stencil': 'Azure', 'master': 'Virtual Machine', 'icon': 'VM'},
            'vmss': {'stencil': 'Azure', 'master': 'Virtual Machine Scale Set', 'icon': 'VMSS'},
            'aks': {'stencil': 'Azure', 'master': 'Kubernetes Service', 'icon': 'AKS'},
            'container': {'stencil': 'Azure', 'master': 'Container Instances', 'icon': 'ACI'},
            'appservice': {'stencil': 'Azure', 'master': 'App Services', 'icon': 'AppService'},
            'function': {'stencil': 'Azure', 'master': 'Function App', 'icon': 'Functions'},
            
            # Database
            'sql': {'stencil': 'Azure', 'master': 'SQL Database', 'icon': 'SQLDatabase'},
            'mysql': {'stencil': 'Azure', 'master': 'Database for MySQL', 'icon': 'MySQL'},
            'postgresql': {'stencil': 'Azure', 'master': 'Database for PostgreSQL', 'icon': 'PostgreSQL'},
            'cosmosdb': {'stencil': 'Azure', 'master': 'Cosmos DB', 'icon': 'CosmosDB'},
            'redis': {'stencil': 'Azure', 'master': 'Cache for Redis', 'icon': 'Redis'},
            
            # Storage
            'storage': {'stencil': 'Azure', 'master': 'Storage Account', 'icon': 'Storage'},
            'backup': {'stencil': 'Azure', 'master': 'Backup', 'icon': 'Backup'},
            'fileshare': {'stencil': 'Azure', 'master': 'Files', 'icon': 'Files'},
            
            # Network
            'vnet': {'stencil': 'Azure', 'master': 'Virtual Network', 'icon': 'VNet'},
            'subnet': {'stencil': 'Azure', 'master': 'Subnet', 'icon': 'Subnet'},
            'nsg': {'stencil': 'Azure', 'master': 'Network Security Group', 'icon': 'NSG'},
            'loadbalancer': {'stencil': 'Azure', 'master': 'Load Balancer', 'icon': 'LoadBalancer'},
            'appgateway': {'stencil': 'Azure', 'master': 'Application Gateway', 'icon': 'AppGateway'},
            'vpngateway': {'stencil': 'Azure', 'master': 'VPN Gateway', 'icon': 'VPNGateway'},
            'firewall': {'stencil': 'Azure', 'master': 'Firewall', 'icon': 'Firewall'},
            
            # Security
            'keyvault': {'stencil': 'Azure', 'master': 'Key Vault', 'icon': 'KeyVault'},
            'aad': {'stencil': 'Azure', 'master': 'Active Directory', 'icon': 'AAD'},
            
            # Management
            'monitor': {'stencil': 'Azure', 'master': 'Monitor', 'icon': 'Monitor'},
            'loganalytics': {'stencil': 'Azure', 'master': 'Log Analytics', 'icon': 'LogAnalytics'},
        }
        
        # Color scheme for different tiers
        self.tier_colors = {
            'security': '#B91C1C',      # Red
            'network': '#00B0F0',       # Blue
            'application': '#E07C24',   # Orange
            'compute': '#4472C4',       # Dark Blue
            'data': '#70AD47',          # Green
            'management': '#6B7280',    # Gray
            'integration': '#10B981'    # Teal
        }
    
    def export_to_vsdx(self, diagram: ArchitectureDiagram, output_path: str):
        """
        Export diagram to VSDX format (Visio 2013+ format).
        This creates a simplified VSDX that Visio can open and edit.
        """
        try:
            # Create the VSDX package structure
            self._create_vsdx_package(diagram, output_path)
            print(f"✅ VSDX file created: {output_path}")
            
        except Exception as e:
            print(f"❌ Error creating VSDX file: {e}")
            # Fallback to enhanced XML
            xml_path = output_path.replace('.vsdx', '_visio.xml')
            self.export_to_visio_xml_enhanced(diagram, xml_path)
            print(f"📄 Created enhanced XML instead: {xml_path}")
    
    def _create_vsdx_package(self, diagram: ArchitectureDiagram, output_path: str):
        """Create a simplified VSDX package structure."""
        
        # Create a temporary directory structure
        package_files = {}
        
        # 1. Create [Content_Types].xml
        package_files['[Content_Types].xml'] = self._create_content_types()
        
        # 2. Create _rels/.rels
        package_files['_rels/.rels'] = self._create_main_rels()
        
        # 3. Create visio/document.xml
        package_files['visio/document.xml'] = self._create_document_xml(diagram)
        
        # 4. Create visio/pages/page1.xml
        package_files['visio/pages/page1.xml'] = self._create_page_xml(diagram)
        
        # 5. Create visio/pages/_rels/page1.xml.rels
        package_files['visio/pages/_rels/page1.xml.rels'] = self._create_page_rels()
        
        # 6. Create docProps/app.xml
        package_files['docProps/app.xml'] = self._create_app_properties(diagram)
        
        # 7. Create docProps/core.xml
        package_files['docProps/core.xml'] = self._create_core_properties(diagram)
        
        # Create the VSDX file (which is a ZIP archive)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as vsdx_zip:
            for file_path, content in package_files.items():
                vsdx_zip.writestr(file_path, content)
    
    def _create_content_types(self) -> str:
        """Create the Content_Types.xml file."""
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="xml" ContentType="application/xml"/>
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>
    <Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>
    <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
    <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''
    
    def _create_main_rels(self) -> str:
        """Create the main relationships file."""
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/document" Target="visio/document.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''
    
    def _create_document_xml(self, diagram: ArchitectureDiagram) -> str:
        """Create the main document.xml file."""
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VisioDocument xmlns="http://schemas.microsoft.com/office/visio/2012/main">
    <DocumentSettings>
        <DefaultTabStyle>0</DefaultTabStyle>
        <DefaultTextStyle>0</DefaultTextStyle>
        <DefaultGuideStyle>0</DefaultGuideStyle>
    </DocumentSettings>
    <Colors>
        <ColorEntry IX="0" RGB="#000000"/>
        <ColorEntry IX="1" RGB="#FFFFFF"/>
        <ColorEntry IX="2" RGB="#4472C4"/>
        <ColorEntry IX="3" RGB="#70AD47"/>
        <ColorEntry IX="4" RGB="#E07C24"/>
        <ColorEntry IX="5" RGB="#B91C1C"/>
    </Colors>
    <Pages>
        <Page ID="1" Name="{diagram.title}" NameU="page-1">
            <PageSheet>
                <PageProps>
                    <PageWidth Unit="IN">11</PageWidth>
                    <PageHeight Unit="IN">8.5</PageHeight>
                </PageProps>
            </PageSheet>
        </Page>
    </Pages>
</VisioDocument>'''
    
    def _create_page_xml(self, diagram: ArchitectureDiagram) -> str:
        """Create the page XML with shapes representing Azure components."""
        
        # Start the page XML
        page_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PageContents xmlns="http://schemas.microsoft.com/office/visio/2012/main">
    <Shapes>'''
        
        # Add shapes for each component
        for i, component in enumerate(diagram.components, 1):
            shape_xml = self._create_shape_xml(component, i)
            page_xml += shape_xml
        
        # Add connections
        connection_xml = self._create_connections_xml(diagram.components)
        page_xml += connection_xml
        
        # Close the page XML
        page_xml += '''
    </Shapes>
</PageContents>'''
        
        return page_xml
    
    def _create_shape_xml(self, component: ArchitectureComponent, shape_id: int) -> str:
        """Create XML for a single shape representing an Azure component."""
        
        # Get position and size
        x = component.position.get('x', 100) / 72  # Convert pixels to inches
        y = component.position.get('y', 100) / 72
        width = component.position.get('width', 120) / 72
        height = component.position.get('height', 80) / 72
        
        # Get color based on tier
        fill_color = self.tier_colors.get(component.tier, '#4472C4')
        
        # Get Visio stencil info
        stencil_info = self.visio_stencils.get(component.component_type, {
            'stencil': 'Basic',
            'master': 'Rectangle',
            'icon': 'Rect'
        })
        
        return f'''
        <Shape ID="{shape_id}" Type="Shape" Master="{stencil_info['master']}">
            <XForm>
                <PinX Unit="IN">{x + width/2}</PinX>
                <PinY Unit="IN">{8.5 - (y + height/2)}</PinY>
                <Width Unit="IN">{width}</Width>
                <Height Unit="IN">{height}</Height>
            </XForm>
            <Text>{component.name}&#10;{component.azure_service}</Text>
            <Fill>
                <FillColor>{fill_color}</FillColor>
            </Fill>
            <Line>
                <LineColor>#000000</LineColor>
                <LineWeight Unit="PT">1</LineWeight>
            </Line>
            <Data>
                <ComponentType>{component.component_type}</ComponentType>
                <AzureService>{component.azure_service}</AzureService>
                <Tier>{component.tier}</Tier>
                <SourceServer>{component.source_server or ''}</SourceServer>
                <MigrationType>{component.migration_type}</MigrationType>
            </Data>
        </Shape>'''
    
    def _create_connections_xml(self, components: List[ArchitectureComponent]) -> str:
        """Create XML for connections between shapes."""
        connections_xml = ""
        connection_id = len(components) + 1
        
        # Create component lookup
        component_lookup = {c.component_id: i+1 for i, c in enumerate(components)}
        
        for i, component in enumerate(components):
            shape_id = i + 1
            for connection_target_id in component.connections:
                if connection_target_id in component_lookup:
                    target_shape_id = component_lookup[connection_target_id]
                    connections_xml += f'''
        <Shape ID="{connection_id}" Type="Shape" Master="Dynamic Connector">
            <XForm>
                <PinX Unit="IN">4</PinX>
                <PinY Unit="IN">4</PinY>
            </XForm>
            <Connects>
                <Connect FromSheet="{connection_id}" FromCell="BeginX" ToSheet="{shape_id}" ToCell="Connections.X1"/>
                <Connect FromSheet="{connection_id}" FromCell="EndX" ToSheet="{target_shape_id}" ToCell="Connections.X1"/>
            </Connects>
            <Line>
                <LineColor>#666666</LineColor>
                <LineWeight Unit="PT">1</LineWeight>
            </Line>
        </Shape>'''
                    connection_id += 1
        
        return connections_xml
    
    def _create_page_rels(self) -> str:
        """Create page relationships file."""
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
    
    def _create_app_properties(self, diagram: ArchitectureDiagram) -> str:
        """Create application properties."""
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
    <Application>SorthaDevKit Architecture Generator</Application>
    <AppVersion>1.0</AppVersion>
    <Company>Microsoft</Company>
    <Manager>Azure Migration</Manager>
</Properties>'''
    
    def _create_core_properties(self, diagram: ArchitectureDiagram) -> str:
        """Create core properties."""
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" 
                   xmlns:dc="http://purl.org/dc/elements/1.1/" 
                   xmlns:dcterms="http://purl.org/dc/terms/" 
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/" 
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <dc:title>{diagram.title}</dc:title>
    <dc:creator>SorthaDevKit</dc:creator>
    <dcterms:created xsi:type="dcterms:W3CDTF">{diagram.created_date}</dcterms:created>
    <dcterms:modified xsi:type="dcterms:W3CDTF">{diagram.created_date}</dcterms:modified>
    <dc:description>Azure target architecture generated from Azure Migrate report and transcript analysis</dc:description>
    <cp:keywords>Azure, Migration, Architecture, Cloud</cp:keywords>
</cp:coreProperties>'''
    
    def export_to_visio_xml_enhanced(self, diagram: ArchitectureDiagram, output_path: str):
        """Export to enhanced XML format with proper Visio elements."""
        
        # Create comprehensive XML structure
        root = ET.Element("VisioDocument")
        root.set("xmlns", "http://schemas.microsoft.com/office/visio/2003/core")
        root.set("xmlns:vx", "http://schemas.microsoft.com/office/visio/2006/extension")
        
        # Document properties
        doc_props = ET.SubElement(root, "DocumentProperties")
        title_elem = ET.SubElement(doc_props, "Title")
        title_elem.text = diagram.title
        
        creator_elem = ET.SubElement(doc_props, "Creator")
        creator_elem.text = "SorthaDevKit Azure Migration"
        
        description_elem = ET.SubElement(doc_props, "Description")
        description_elem.text = f"Azure target architecture with {len(diagram.components)} components"
        
        # Document settings
        doc_settings = ET.SubElement(root, "DocumentSettings")
        default_units = ET.SubElement(doc_settings, "DefaultUnits")
        default_units.text = "inches"
        
        # Pages
        pages = ET.SubElement(root, "Pages")
        page = ET.SubElement(pages, "Page")
        page.set("ID", "1")
        page.set("Name", "Architecture")
        
        # Page properties
        page_props = ET.SubElement(page, "PageProps")
        page_width = ET.SubElement(page_props, "PageWidth")
        page_width.text = "11"
        page_height = ET.SubElement(page_props, "PageHeight")
        page_height.text = "8.5"
        
        # Shapes
        shapes = ET.SubElement(page, "Shapes")
        
        # Add each component as a shape
        for i, component in enumerate(diagram.components, 1):
            shape = self._create_enhanced_shape_element(shapes, component, i)
        
        # Add connections
        connections = ET.SubElement(page, "Connections")
        self._add_enhanced_connections(connections, diagram.components)
        
        # Format and write XML
        self._format_xml(root)
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
    
    def _create_enhanced_shape_element(self, parent, component: ArchitectureComponent, shape_id: int):
        """Create an enhanced shape element with Azure-specific properties."""
        
        shape = ET.SubElement(parent, "Shape")
        shape.set("ID", str(shape_id))
        shape.set("Name", component.name)
        shape.set("Type", "Shape")
        
        # Get Visio stencil information
        stencil_info = self.visio_stencils.get(component.component_type, {
            'master': 'Rectangle',
            'icon': 'Rect'
        })
        shape.set("Master", stencil_info['master'])
        
        # XForm (position and size)
        xform = ET.SubElement(shape, "XForm")
        pin_x = ET.SubElement(xform, "PinX")
        pin_x.text = str(component.position.get('x', 100) / 72)  # Convert to inches
        pin_y = ET.SubElement(xform, "PinY")
        pin_y.text = str((600 - component.position.get('y', 100)) / 72)  # Flip Y and convert
        width = ET.SubElement(xform, "Width")
        width.text = str(component.position.get('width', 120) / 72)
        height = ET.SubElement(xform, "Height")
        height.text = str(component.position.get('height', 80) / 72)
        
        # Text
        text = ET.SubElement(shape, "Text")
        text.text = f"{component.name}\\n{component.azure_service}"
        
        # Fill color based on tier
        fill = ET.SubElement(shape, "Fill")
        fill_color = ET.SubElement(fill, "FillColor")
        fill_color.text = self.tier_colors.get(component.tier, '#4472C4')
        
        # Custom properties
        custom_props = ET.SubElement(shape, "CustomProperties")
        
        # Add Azure-specific properties
        azure_props = {
            'ComponentType': component.component_type,
            'AzureService': component.azure_service,
            'Tier': component.tier,
            'SourceServer': component.source_server or '',
            'MigrationType': component.migration_type
        }
        
        for key, value in azure_props.items():
            prop = ET.SubElement(custom_props, "CustomProperty")
            prop.set("Name", key)
            prop.set("Value", str(value))
        
        # Add component properties
        for key, value in component.properties.items():
            prop = ET.SubElement(custom_props, "CustomProperty")
            prop.set("Name", f"Prop_{key}")
            prop.set("Value", str(value))
        
        return shape
    
    def _add_enhanced_connections(self, connections_elem, components: List[ArchitectureComponent]):
        """Add enhanced connection elements."""
        
        component_lookup = {c.component_id: i+1 for i, c in enumerate(components)}
        connection_id = len(components) + 1
        
        for i, component in enumerate(components):
            shape_id = i + 1
            for target_id in component.connections:
                if target_id in component_lookup:
                    target_shape_id = component_lookup[target_id]
                    
                    conn = ET.SubElement(connections_elem, "Connection")
                    conn.set("ID", str(connection_id))
                    conn.set("FromSheet", str(shape_id))
                    conn.set("ToSheet", str(target_shape_id))
                    conn.set("FromCell", "Connections.X1")
                    conn.set("ToCell", "Connections.X1")
                    
                    connection_id += 1
    
    def _format_xml(self, element, level=0):
        """Format XML with proper indentation."""
        indent = "\\n" + level * "  "
        if len(element):
            if not element.text or not element.text.strip():
                element.text = indent + "  "
            if not element.tail or not element.tail.strip():
                element.tail = indent
            for child in element:
                self._format_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not element.tail or not element.tail.strip()):
                element.tail = indent
