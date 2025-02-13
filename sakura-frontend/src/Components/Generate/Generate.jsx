import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { ForceGraph2D } from 'react-force-graph';
import { generateSyntheticData } from '../syntheticDataGenerator';
import { 
  Box, 
  Container, 
  VStack, 
  Heading, 
  Text,
  useColorMode,
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Icon,
  Code,
  SimpleGrid,
  IconButton,
  HStack
} from '@chakra-ui/react';
import { FiBarChart2, FiCode, FiBook, FiDownload, FiCopy, FiEye } from 'react-icons/fi';
import { MouseTrail } from '../MouseTrail/MouseTrail';

const TabButton = ({ icon, label, isSelected, onClick }) => {
  const { colorMode } = useColorMode();
  
  return (
    <Box
      as="button"
      p={6}
      w="full"
      borderRadius="xl"
      bg={isSelected 
        ? 'transparent'
        : colorMode === 'dark' 
          ? 'rgba(23, 25, 35, 0.4)' 
          : 'rgba(255, 255, 255, 0.4)'
      }
      borderWidth="1px"
      borderColor={isSelected ? 'sakura.500' : 'transparent'}
      onClick={onClick}
      position="relative"
      transition="all 0.3s"
      _hover={{
        transform: 'translateY(-2px)',
        borderColor: 'sakura.500'
      }}
    >
      {isSelected && (
        <Box
          position="absolute"
          top={0}
          left={0}
          right={0}
          bottom={0}
          borderRadius="xl"
          bgGradient="linear(to-r, purple.500, sakura.500)"
          opacity={0.1}
        />
      )}
      <VStack spacing={4}>
        <Icon 
          as={icon} 
          boxSize={6} 
          color={isSelected ? 'sakura.500' : 'gray.500'}
        />
        <Text
          fontWeight="bold"
          color={isSelected ? 'sakura.500' : 'gray.500'}
        >
          {label}
        </Text>
      </VStack>
    </Box>
  );
};

const Generate = () => {
  const location = useLocation();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const [story, setStory] = useState('');
  const [metrics, setMetrics] = useState(null);
  const { colorMode } = useColorMode();
  const [activeTab, setActiveTab] = useState('bundle');

  // Link color mapping for different relationship types
  const getLinkColor = (relationship) => {
    const relationshipColors = {
      'uses': '#e939af',            // Sakura pink for 'uses' relationships
      'targets': '#9c2db3',         // Purple for 'targets'
      'attributed-to': '#b83280',   // Another shade of pink
      'indicates': '#805ad5',       // Another shade of purple
      'mitigates': '#d53f8c',       // Another pink variant
      'located-at': '#b794f4',      // Light purple
      'related-to': '#fbb6ce',      // Light pink
    };
    return relationshipColors[relationship] || '#718096'; // Default gray color
  };

  useEffect(() => {
    const selectedEntities = location.state?.selectedEntities || {};
    const counts = location.state?.counts || {};
    
    if (Object.keys(selectedEntities).length > 0) {
      generateSyntheticData(selectedEntities, counts)
        .then(data => {
          setGraphData(data);
          setStory(data.story || '');
          setMetrics(data.metrics || null);
          setLoading(false);
        })
        .catch(error => {
          console.error('Error generating data:', error);
          setLoading(false);
        });
    }
  }, [location]);

  const handleDownload = () => {
    const jsonString = JSON.stringify(graphData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'stix-bundle.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(graphData, null, 2));
  };

  const handleVisualize = () => {
    // Your existing visualization logic
  };

  if (loading) {
    return (
      <Box 
        minH="100vh" 
        bg={colorMode === 'dark' ? 'gray.900' : 'gray.50'} 
        position="relative"
      >
        <MouseTrail />
        <Container maxW="container.xl" centerContent py={20}>
          <VStack spacing={8}>
            <Spinner 
              size="xl" 
              color="sakura.500" 
              thickness="4px"
              speed="0.65s"
            />
            <Text 
              fontSize="xl"
              bgGradient="linear(to-r, purple.400, sakura.400)"
              bgClip="text"
            >
              Generating STIX Data...
            </Text>
          </VStack>
        </Container>
      </Box>
    );
  }

  if (graphData.nodes.length === 0) {
    return (
      <Box 
        minH="100vh" 
        bg={colorMode === 'dark' ? 'gray.900' : 'gray.50'} 
        position="relative"
      >
        <MouseTrail />
        <Container maxW="container.xl" centerContent py={20}>
          <Alert
            status="warning"
            variant="subtle"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            textAlign="center"
            bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.7)' : 'rgba(255, 255, 255, 0.7)'}
            backdropFilter="blur(10px)"
            borderRadius="xl"
            borderWidth="1px"
            borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
            p={8}
          >
            <AlertIcon boxSize="40px" mr={0} />
            <AlertTitle 
              mt={4} 
              mb={1} 
              fontSize="lg"
              bgGradient="linear(to-r, purple.400, sakura.400)"
              bgClip="text"
            >
              No Data Available
            </AlertTitle>
            <AlertDescription maxWidth="sm">
              Please select entities and their counts to generate STIX data.
            </AlertDescription>
          </Alert>
        </Container>
      </Box>
    );
  }

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
            Generated STIX Graph
          </Heading>

          {graphData.nodes.length > 0 && (
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} w="full">
              <TabButton
                icon={FiCode}
                label="STIX Bundle"
                isSelected={activeTab === 'bundle'}
                onClick={() => setActiveTab('bundle')}
              />
              <TabButton
                icon={FiBook}
                label="Generated Story"
                isSelected={activeTab === 'story'}
                onClick={() => setActiveTab('story')}
              />
              <TabButton
                icon={FiBarChart2}
                label="Metrics"
                isSelected={activeTab === 'metrics'}
                onClick={() => setActiveTab('metrics')}
              />
            </SimpleGrid>
          )}

          <Box
            w="full"
            bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.7)' : 'rgba(255, 255, 255, 0.7)'}
            backdropFilter="blur(10px)"
            borderRadius="xl"
            borderWidth="1px"
            borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
            overflow="hidden"
          >
            {activeTab === 'bundle' && (
              <Box h="70vh" position="relative">
                <HStack 
                  position="absolute" 
                  top={4} 
                  right={4} 
                  zIndex={2} 
                  spacing={2}
                >
                  <IconButton
                    icon={<FiDownload />}
                    onClick={handleDownload}
                    aria-label="Download JSON"
                    bgGradient="linear(to-r, purple.500, sakura.500)"
                    color="white"
                    _hover={{
                      bgGradient: "linear(to-r, purple.600, sakura.600)",
                    }}
                    size="sm"
                  />
                  <IconButton
                    icon={<FiCopy />}
                    onClick={handleCopy}
                    aria-label="Copy JSON"
                    variant="outline"
                    borderColor="sakura.500"
                    _hover={{
                      bgGradient: "linear(to-r, purple.500, sakura.500)",
                      color: "white"
                    }}
                    size="sm"
                  />
                  <IconButton
                    icon={<FiEye />}
                    onClick={handleVisualize}
                    aria-label="Visualize"
                    variant="outline"
                    borderColor="sakura.500"
                    _hover={{
                      bgGradient: "linear(to-r, purple.500, sakura.500)",
                      color: "white"
                    }}
                    size="sm"
                  />
                </HStack>
                <ForceGraph2D
                  graphData={graphData}
                  nodeLabel="name"
                  nodeColor={() => colorMode === 'dark' ? '#e939af' : '#d53f8c'}
                  nodeRelSize={6}
                  linkColor={link => getLinkColor(link.relationship)}
                  linkWidth={2}
                  linkDirectionalParticles={2}
                  linkDirectionalParticleSpeed={0.005}
                  backgroundColor="transparent"
                  onNodeDragEnd={node => {
                    node.fx = null;
                    node.fy = null;
                  }}
                />
              </Box>
            )}

            {activeTab === 'story' && (
              <Box 
                p={6} 
                maxH="70vh" 
                overflowY="auto"
                whiteSpace="pre-wrap"
              >
                <Text>{story}</Text>
              </Box>
            )}

            {activeTab === 'metrics' && (
              <Box p={6} maxH="70vh" overflowY="auto">
                {metrics && (
                  <VStack align="stretch" spacing={6}>
                    {Object.entries(metrics).map(([key, value]) => (
                      <Box key={key}>
                        <Text 
                          fontWeight="bold" 
                          mb={2}
                          bgGradient="linear(to-r, purple.400, sakura.400)"
                          bgClip="text"
                        >
                          {key.replace(/_/g, ' ').toUpperCase()}
                        </Text>
                        <Code p={4} borderRadius="md" w="full">
                          {JSON.stringify(value, null, 2)}
                        </Code>
                      </Box>
                    ))}
                  </VStack>
                )}
              </Box>
            )}
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};

export default Generate;