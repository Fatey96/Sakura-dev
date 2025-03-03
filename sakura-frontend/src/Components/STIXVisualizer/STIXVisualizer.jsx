import React, { useRef, useEffect, useState, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { FaSearch, FaCompressArrowsAlt, FaInfoCircle } from 'react-icons/fa';
import { useStix } from '../EntitySelector/StixContext';
import { 
  Box, 
  Container, 
  VStack, 
  Heading, 
  Input,
  InputGroup,
  InputLeftElement,
  Button,
  SimpleGrid,
  Text,
  useColorMode,
  Checkbox,
  HStack,
  IconButton,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
} from '@chakra-ui/react';
import { MouseTrail } from '../MouseTrail/MouseTrail';
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
  const { colorMode } = useColorMode();

  useEffect(() => {
    const related = stixBundle.objects.filter(obj => 
      obj.type === 'relationship' && (obj.source_ref === entity.id || obj.target_ref === entity.id)
    ).map(rel => {
      const relatedObj = stixBundle.objects.find(obj => obj.id === (rel.source_ref === entity.id ? rel.target_ref : rel.source_ref));
      return { ...relatedObj, relationship: rel.relationship_type, direction: rel.source_ref === entity.id ? 'outgoing' : 'incoming' };
    });
    setRelatedEntities(related);
  }, [entity, stixBundle]);

  // Helper function to format field values
  const formatValue = (value) => {
    if (Array.isArray(value)) {
      return value.join(', ');
    } else if (typeof value === 'object' && value !== null) {
      return JSON.stringify(value, null, 2);
    }
    return value;
  };

  // Get all fields except those we handle specially
  const specialFields = ['type', 'id', 'created', 'modified', 'name', 'description', 'aliases', 'kill_chain_phases'];
  const additionalFields = Object.entries(entity).filter(([key]) => !specialFields.includes(key));

  return (
    <Box
      p={6}
      bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.7)' : 'rgba(255, 255, 255, 0.7)'}
      backdropFilter="blur(10px)"
      borderRadius="xl"
      borderWidth="1px"
      borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
    >
      <VStack align="stretch" spacing={4}>
        <HStack justify="space-between">
          <Heading 
            size="md"
            bgGradient="linear(to-r, purple.400, sakura.400)"
            bgClip="text"
          >
            {entity.type.replace('-', ' ').toUpperCase()}
          </Heading>
          <IconButton
            icon={<FaInfoCircle />}
            onClick={onClose}
            variant="ghost"
            size="sm"
          />
        </HStack>
        
        <VStack align="stretch" spacing={2}>
          {/* Basic Information */}
          <Box borderWidth="1px" borderRadius="md" p={3}>
            <Text fontWeight="bold" mb={2}>Basic Information</Text>
            <Text><strong>Name:</strong> {entity.name || 'N/A'}</Text>
            <Text><strong>ID:</strong> {entity.id}</Text>
            <Text><strong>Created:</strong> {new Date(entity.created).toLocaleString()}</Text>
            <Text><strong>Modified:</strong> {new Date(entity.modified).toLocaleString()}</Text>
            <Text><strong>Description:</strong> {entity.description || 'N/A'}</Text>
          </Box>

          {/* Aliases */}
          {entity.aliases && entity.aliases.length > 0 && (
            <Box borderWidth="1px" borderRadius="md" p={3}>
              <Text fontWeight="bold" mb={2}>Aliases</Text>
              {entity.aliases.map((alias, idx) => (
                <Text key={idx}>• {alias}</Text>
              ))}
            </Box>
          )}

          {/* Kill Chain Phases */}
          {entity.kill_chain_phases && entity.kill_chain_phases.length > 0 && (
            <Box borderWidth="1px" borderRadius="md" p={3}>
              <Text fontWeight="bold" mb={2}>Kill Chain Phases</Text>
              {entity.kill_chain_phases.map((phase, idx) => (
                <Text key={idx}>
                  • {phase.kill_chain_name}: {phase.phase_name}
                </Text>
              ))}
            </Box>
          )}

          {/* Related Entities */}
          {relatedEntities.length > 0 && (
            <Box borderWidth="1px" borderRadius="md" p={3}>
              <Text fontWeight="bold" mb={2}>Related Entities</Text>
              {relatedEntities.map((related, idx) => (
                <Text key={idx}>
                  • {related.name} ({related.type}) - {related.relationship} ({related.direction})
                </Text>
              ))}
            </Box>
          )}

          {/* Additional Fields */}
          {additionalFields.length > 0 && (
            <Box borderWidth="1px" borderRadius="md" p={3}>
              <Text fontWeight="bold" mb={2}>Additional Properties</Text>
              {additionalFields.map(([key, value]) => (
                <Text key={key}>
                  <strong>{key.replace(/_/g, ' ')}:</strong> {formatValue(value)}
                </Text>
              ))}
            </Box>
          )}
        </VStack>
      </VStack>
    </Box>
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
  const { colorMode } = useColorMode();

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
    <Box 
      minH="100vh" 
      bg={colorMode === 'dark' ? 'gray.900' : 'gray.50'} 
      position="relative"
      overflow="hidden"
    >
      <MouseTrail />
      
      <Container maxW="container.xl" py={8} position="relative" zIndex={2}>
        <VStack spacing={8}>
          <Heading
            size="2xl"
            bgGradient="linear(to-r, purple.400, sakura.400)"
            bgClip="text"
            textAlign="center"
          >
            STIX Data Visualizer
          </Heading>

          <HStack w="full" spacing={4}>
            <InputGroup>
              <InputLeftElement pointerEvents="none">
                <FaSearch color="gray.300" />
              </InputLeftElement>
              <Input
                placeholder="Search entities..."
                value={searchTerm}
                onChange={handleSearch}
                borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
                _hover={{ borderColor: 'sakura.500' }}
              />
            </InputGroup>
            
            <Button
              leftIcon={<FaCompressArrowsAlt />}
              onClick={handleZoomToFit}
              bgGradient="linear(to-r, purple.500, sakura.500)"
              color="white"
              _hover={{
                bgGradient: "linear(to-r, purple.600, sakura.600)",
              }}
            >
              Fit View
            </Button>
            
            <Button
              leftIcon={<FaInfoCircle />}
              onClick={toggleLegend}
              variant="outline"
              borderColor="sakura.500"
              _hover={{
                bgGradient: "linear(to-r, purple.500, sakura.500)",
                color: "white"
              }}
            >
              {showLegend ? 'Hide' : 'Show'} Legend
            </Button>
          </HStack>

          <SimpleGrid columns={{ base: 2, md: 4, lg: 6 }} spacing={4} w="full">
            {entityTypes.map((type) => (
              <Checkbox
                key={type}
                isChecked={filters[type]}
                onChange={() => handleFilterChange(type)}
                colorScheme="purple"
              >
                <HStack>
                  <img src={iconPaths[type]} alt={type} width="20" height="20" />
                  <Text>{type.replace('-', ' ')}</Text>
                </HStack>
              </Checkbox>
            ))}
          </SimpleGrid>

          <Box
            w="full"
            h="600px"
            bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.7)' : 'rgba(255, 255, 255, 0.7)'}
            backdropFilter="blur(10px)"
            borderRadius="xl"
            borderWidth="1px"
            borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
            overflow="hidden"
          >
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
              backgroundColor={colorMode === 'dark' ? '#171923' : '#F7FAFC'}
            />
          </Box>
        </VStack>
      </Container>

      {selectedEntity && (
        <Drawer
          isOpen={!!selectedEntity}
          placement="right"
          onClose={handleCloseEntityDetails}
          size="md"
        >
          <DrawerOverlay backdropFilter="blur(10px)" />
          <DrawerContent
            bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.95)' : 'rgba(255, 255, 255, 0.95)'}
          >
            <DrawerCloseButton />
            <DrawerHeader
              bgGradient="linear(to-r, purple.400, sakura.400)"
              bgClip="text"
            >
              Entity Details
            </DrawerHeader>
            <DrawerBody>
              <EntityDetails
                entity={selectedEntity}
                stixBundle={stixBundle}
                onClose={handleCloseEntityDetails}
              />
            </DrawerBody>
          </DrawerContent>
        </Drawer>
      )}

      {showLegend && (
        <Box
          position="fixed"
          top={4}
          right={4}
          p={6}
          bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.9)' : 'rgba(255, 255, 255, 0.9)'}
          backdropFilter="blur(10px)"
          borderRadius="xl"
          borderWidth="1px"
          borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
          maxW="300px"
          zIndex={1000}
        >
          <VStack align="stretch" spacing={4}>
            <Heading
              size="md"
              bgGradient="linear(to-r, purple.400, sakura.400)"
              bgClip="text"
            >
              Legend
            </Heading>
            <Text><strong>Entity Types:</strong></Text>
            {entityTypes.map(type => (
              <Text key={type}>{type.replace('-', ' ')}</Text>
            ))}
            <Text><strong>Relationship Types:</strong></Text>
            {Object.entries(relationshipColors).map(([type, color]) => (
              <Text key={type}>
                <span style={{ backgroundColor: color, width: '10px', height: '10px', display: 'inline-block', marginRight: '5px' }}></span>
                {type}
              </Text>
            ))}
          </VStack>
        </Box>
      )}
    </Box>
  );
};

export default STIXVisualizer;