import React, { useRef, useEffect, useState, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { FaSearch, FaCompressArrowsAlt, FaInfoCircle } from 'react-icons/fa';
import { useStix } from '../EntitySelector/StixContext';
import './STIXVisualizer.css';

// STIX 2 Icon paths
const iconPaths = {
'attack-pattern': '/icons/attack_pattern.png',
'campaign': '/icons/campaign.png',
'course-of-action': '/icons/course_of_action.png',
'identity': '/icons/identity.png',
'indicator': '/icons/indicator.png',
'intrusion-set': '/icons/intrusion_set.png',
'malware': '/icons/malware.png',
'observed-data': '/icons/observed_data.png',
'report': '/icons/report.png',
'threat-actor': '/icons/threat_actor.png',
'tool': '/icons/tool.png',
'vulnerability': '/icons/vulnerability.png',
// Add more mappings as needed
};

const entityTypes = Object.keys(iconPaths);

const relationshipColors = {
'uses': '#4a90e2',
'mitigates': '#27ae60',
'indicates': '#e74c3c',
'attributed-to': '#f39c12',
// Add more relationship types and colors as needed
};

const EntityDetails = ({ entity, stixBundle, onClose }) => {
const [relatedEntities, setRelatedEntities] = useState([]);

useEffect(() => {
const related = stixBundle.objects.filter(obj =>
obj.type === 'relationship' && (obj.source_ref === entity.id || obj.target_ref === entity.id)
).map(rel => {
const relatedObj = stixBundle.objects.find(obj => obj.id === (rel.source_ref === entity.id ? rel.target_ref : rel.source_ref));
return { ...relatedObj, relationship: rel.relationship_type, direction: rel.source_ref === entity.id ? 'outgoing' : 'incoming' };
});
setRelatedEntities(related);
}, [entity, stixBundle]);

return (
<div className="entity-details panel">
<button className="close-btn" onClick={onClose}>×</button>
<h3>{entity.type.replace('-', ' ').toUpperCase()}</h3>
<div className="entity-content">
<p><strong>Name:</strong> {entity.name}</p>
<p><strong>ID:</strong> {entity.id}</p>
<p><strong>Created:</strong> {entity.created}</p>
<p><strong>Modified:</strong> {entity.modified}</p>
<p><strong>Description:</strong> {entity.description || 'N/A'}</p>
{entity.aliases && (
<>
<h4>Aliases</h4>
<ul>
{entity.aliases.map((alias, index) => <li key={index}>{alias}</li>)}
</ul>
</>
)}

<h4>Related Entities</h4>
<ul>
{relatedEntities.map((related, index) => (
<li key={index}>
{related.name} ({related.type}) - {related.relationship} ({related.direction})
</li>
))}
</ul>

{entity.kill_chain_phases && (
<>
<h4>Kill Chain Phases</h4>
<ul>
{entity.kill_chain_phases.map((phase, index) => (
<li key={index}>{phase.kill_chain_name}: {phase.phase_name}</li>
))}
</ul>
</>
)}
</div>
</div>
);
};

const STIXVisualizer = () => {
const { stixBundle } = useStix();
const [graphData, setGraphData] = useState({ nodes: [], links: [] });
const [selectedEntity, setSelectedEntity] = useState(null);
const [searchTerm, setSearchTerm] = useState('');
const [filters, setFilters] = useState(entityTypes.reduce((acc, type) => ({ ...acc, [type]: true }), {}));
const [showLegend, setShowLegend] = useState(false);
const graphRef = useRef();

useEffect(() => {
if (!stixBundle) return;

const nodes = stixBundle.objects
.filter(obj => obj.type !== 'relationship')
.map(obj => ({
id: obj.id,
name: obj.name || obj.type,
type: obj.type,
}));

const links = stixBundle.objects
.filter(obj => obj.type === 'relationship')
.map(obj => ({
source: obj.source_ref,
target: obj.target_ref,
type: obj.relationship_type,
}));

setGraphData({ nodes, links });
}, [stixBundle]);

const handleNodeClick = useCallback(node => {
const fullEntity = stixBundle.objects.find(obj => obj.id === node.id);
setSelectedEntity(fullEntity);
}, [stixBundle]);

const handleCloseEntityDetails = useCallback(() => {
setSelectedEntity(null);
}, []);

const handleSearch = useCallback((event) => {
setSearchTerm(event.target.value);
}, []);

const handleFilterChange = useCallback((type) => {
setFilters(prev => ({ ...prev, [type]: !prev[type] }));
}, []);

const handleZoomToFit = useCallback(() => {
graphRef.current.zoomToFit(400);
}, []);

const toggleLegend = useCallback(() => {
setShowLegend(prev => !prev);
}, []);

if (!stixBundle) {
return <div className="loading-message">Loading STIX data...</div>;
}

const filteredNodes = graphData.nodes.filter(node =>
filters[node.type] && node.name.toLowerCase().includes(searchTerm.toLowerCase())
);

return (
<div className="stix-visualizer">
<header className="header">
<h1>SAKURA Intelligence Data Visualizer</h1>
<div className="search-bar">
<FaSearch />
<input
type="text"
placeholder="Search entities..."
value={searchTerm}
onChange={handleSearch}
/>
</div>
<div className="filters">
{entityTypes.map((type) => (
<label key={type} className="filter-toggle">
<input
type="checkbox"
checked={filters[type]}
onChange={() => handleFilterChange(type)}
/>
<img src={iconPaths[type]} alt={type} className="filter-icon" />
<span>{type.replace('-', ' ')}</span>
</label>
))}
</div>
<button className="control-btn" onClick={handleZoomToFit}>
<FaCompressArrowsAlt /> Fit View
</button>
<button className="control-btn" onClick={toggleLegend}>
<FaInfoCircle /> {showLegend ? 'Hide' : 'Show'} Legend
</button>
</header>
<main className="main-content">
<div className="graph-container">
<ForceGraph2D
ref={graphRef}
graphData={{ nodes: filteredNodes, links: graphData.links }}
nodeLabel="name"
nodeCanvasObject={(node, ctx, globalScale) => {
const image = new Image();
const size = 24 / globalScale;
image.src = iconPaths[node.type];
ctx.drawImage(image, node.x - size / 2, node.y - size / 2, size, size);
}}
nodeCanvasObjectMode={() => 'replace'}
linkColor={link => relationshipColors[link.type] || '#999999'}
linkDirectionalArrowLength={3}
linkDirectionalArrowRelPos={1}
linkCurvature={0.25}
linkLabel="type"
onNodeClick={handleNodeClick}
backgroundColor="#ffffff"
/>
</div>
{selectedEntity && (
<EntityDetails
entity={selectedEntity}
stixBundle={stixBundle}
onClose={handleCloseEntityDetails}
/>
)}
</main>
{showLegend && (
<div className="legend panel">
<h3>Legend</h3>
<div className="legend-content">
<h4>Entity Types</h4>
{entityTypes.map(type => (
<div key={type} className="legend-item">
<img src={iconPaths[type]} alt={type} className="legend-icon" />
<span>{type.replace('-', ' ')}</span>
</div>
))}
<h4>Relationship Types</h4>
{Object.entries(relationshipColors).map(([type, color]) => (
<div key={type} className="legend-item">
<span className="legend-color" style={{backgroundColor: color}}></span>
<span>{type}</span>
</div>
))}
</div>
</div>
)}
</div>
);
};

export default STIXVisualizer;