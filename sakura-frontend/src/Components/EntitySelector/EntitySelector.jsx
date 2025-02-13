import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { 
  Box, 
  Container, 
  Heading, 
  VStack, 
  HStack, 
  Button, 
  Text, 
  useColorMode,
  Grid,
  NumberInput,
  NumberInputField,
  Tag,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  Code,
  List,
  ListItem,
  Stat,
  StatLabel,
  StatNumber,
  Divider,
  IconButton,
  Flex,
  useToast,
  Badge
} from '@chakra-ui/react';
import { FiBarChart2, FiCopy, FiEye, FiSun, FiMoon } from 'react-icons/fi';
import { useStix } from './StixContext';
import { MouseTrail } from '../MouseTrail/MouseTrail';

const entities = [
  { category: 'Profile & Persona', items: ['Threat Actor', 'Identity'] },
  { category: 'Artifacts', items: ['Malware', 'Tool'] },
  { category: 'Tactics & Operations', items: ['Attack Pattern', 'Campaign', 'Course of Action'] },
  { category: 'Possible Intels', items: ['Indicator', 'Report'] },
  { category: 'Frameworks & Geolocation Data', items: ['Infrastructure', 'Location'] },
  { category: 'Forensics & Countermeasures', items: ['Intrusion Set', 'Malware Analysis', 'Opinion', 'Vulnerability'] },
];

const MetricsSidebar = ({ metrics, isOpen, onClose }) => {
  return (
    <Drawer isOpen={isOpen} placement="right" onClose={onClose} size="md">
      <DrawerOverlay backdropFilter="blur(10px)" />
      <DrawerContent
        bg="rgba(23, 25, 35, 0.95)"
        borderLeft="1px solid"
        borderColor="whiteAlpha.200"
      >
        <DrawerCloseButton color="white" />
        <DrawerHeader
          bgGradient="linear(to-r, purple.400, sakura.400)"
          bgClip="text"
        >
          Metrics
        </DrawerHeader>
        <DrawerBody>
          {metrics && (
            <VStack spacing={6} align="stretch">
              <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                <Stat>
                  <StatLabel color="gray.300">Total Objects</StatLabel>
                  <StatNumber color="white">{metrics.total_objects}</StatNumber>
                </Stat>
                <Stat>
                  <StatLabel>Completeness</StatLabel>
                  <StatNumber>{metrics.completeness_score.toFixed(2)}%</StatNumber>
                </Stat>
                <Stat>
                  <StatLabel>Consistency</StatLabel>
                  <StatNumber>{metrics.consistency_score.toFixed(2)}%</StatNumber>
                </Stat>
                <Stat>
                  <StatLabel>Timeliness</StatLabel>
                  <StatNumber>{metrics.timeliness_score.toFixed(2)}%</StatNumber>
                </Stat>
              </Grid>
              
              <Divider borderColor="whiteAlpha.300" />
              
              <Box>
                <Text fontWeight="bold" color="white" mb={2}>
                  Object Type Distribution:
                </Text>
                <List spacing={2}>
                  {Object.entries(metrics.object_type_distribution).map(([type, count]) => (
                    <ListItem key={type}>
                      <HStack justify="space-between">
                        <Text color="gray.300">{type}</Text>
                        <Badge
                          bgGradient="linear(to-r, purple.500, sakura.500)"
                          color="white"
                        >
                          {count}
                        </Badge>
                      </HStack>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </VStack>
          )}
        </DrawerBody>
      </DrawerContent>
    </Drawer>
  );
};

const ColorModeToggle = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <IconButton
      position="fixed"
      top={4}
      right={4}
      icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
      onClick={toggleColorMode}
      variant="ghost"
      color="current"
      aria-label="Toggle color mode"
      zIndex={2}
    />
  );
};

const EntitySelector = () => {
  const [selectedEntities, setSelectedEntities] = useState({});
  const [counts, setCounts] = useState({});
  const { stixBundle, setStixBundle } = useStix();
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [displayMode, setDisplayMode] = useState('stixBundle');
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { colorMode } = useColorMode();
  const navigate = useNavigate();
  const toast = useToast();

  const toggleEntity = (entity) => {
    setSelectedEntities(prev => ({
      ...prev,
      [entity]: !prev[entity]
    }));
  };

  const updateCount = (entity, value) => {
    setCounts(prev => ({
      ...prev,
      [entity]: Math.max(0, parseInt(value) || 0)
    }));
  };

  const generateGraph = async () => {
    setLoading(true);
    setError(null);
    setStixBundle(null);
    setStory(null);
    setMetrics(null);

    const selectedCounts = Object.entries(selectedEntities)
      .filter(([, selected]) => selected)
      .reduce((acc, [entity]) => {
        acc[entity.toLowerCase().replace(' ', '-')] = counts[entity] || 0;
        return acc;
      }, {});

    const formData = new FormData();
    Object.entries(selectedCounts).forEach(([key, value]) => {
      formData.append(key + '-count', value);
    });

    try {
      const response = await axios.post('http://127.0.0.1:5000/generate-graph', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStixBundle(JSON.parse(response.data.stix_bundle));
      setStory(response.data.story);
      setMetrics(response.data.metrics);
    } catch (err) {
      setError('An error occurred while generating the graph. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleDisplayMode = () => {
    setDisplayMode(prev => prev === 'stixBundle' ? 'story' : 'stixBundle');
  };

  const copyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(stixBundle, null, 2));
    toast({
      title: 'JSON copied to clipboard!',
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  const openStixVisualizer = () => {
    if (stixBundle) {
      navigate('/stix-visualizer');
    } else {
      console.error('No STIX bundle available to visualize');
      // Optionally, show an error message to the user
    }
  };

  return (
    <Box
      minH="100vh"
      bg={colorMode === 'dark' ? 'gray.900' : 'gray.50'}
      position="relative"
      overflow="hidden"
    >
      <ColorModeToggle />
      <MouseTrail />
      
      <Container maxW="container.xl" py={10} position="relative" zIndex={2}>
        <VStack spacing={8}>
          <Heading
            size="2xl"
            bgGradient="linear(to-r, purple.400, sakura.400)"
            bgClip="text"
            textAlign="center"
          >
            Select STIX Entities
          </Heading>

          <IconButton
            position="fixed"
            right={4}
            top="50%"
            transform="translateY(-50%)"
            icon={<FiBarChart2 />}
            onClick={onOpen}
            bgGradient="linear(to-r, purple.500, sakura.500)"
            color="white"
            _hover={{
              bgGradient: "linear(to-r, purple.600, sakura.600)",
            }}
            zIndex={3}
          />

          <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }} gap={6} w="full">
            {entities.map(group => (
              <Box
                key={group.category}
                p={6}
                borderRadius="xl"
                bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.7)' : 'rgba(255, 255, 255, 0.7)'}
                backdropFilter="blur(10px)"
                borderWidth="1px"
                borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
              >
                <VStack align="stretch" spacing={4}>
                  <Heading
                    size="md"
                    bgGradient="linear(to-r, purple.400, sakura.400)"
                    bgClip="text"
                  >
                    {group.category}
                  </Heading>
                  <Flex wrap="wrap" gap={2}>
                    {group.items.map(entity => (
                      <Tag
                        key={entity}
                        size="lg"
                        borderWidth="1px"
                        borderColor={selectedEntities[entity] ? "transparent" : "sakura.500"}
                        bgGradient={selectedEntities[entity] 
                          ? "linear(to-r, purple.500, sakura.500)"
                          : "none"}
                        color={colorMode === 'dark' ? 'white' : 'gray.800'}
                        cursor="pointer"
                        onClick={() => toggleEntity(entity)}
                        _hover={{
                          bgGradient: "linear(to-r, purple.500, sakura.500)",
                          borderColor: "transparent",
                          color: "white"
                        }}
                      >
                        {entity}
                      </Tag>
                    ))}
                  </Flex>
                </VStack>
              </Box>
            ))}
          </Grid>

          {Object.keys(selectedEntities).some(key => selectedEntities[key]) && (
            <Box
              w="full"
              p={6}
              borderRadius="xl"
              bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.7)' : 'rgba(255, 255, 255, 0.7)'}
              backdropFilter="blur(10px)"
              borderWidth="1px"
              borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
            >
              <VStack spacing={4}>
                <Heading
                  size="md"
                  bgGradient="linear(to-r, purple.400, sakura.400)"
                  bgClip="text"
                >
                  Selected Entities
                </Heading>
                <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }} gap={4} w="full">
                  {Object.entries(selectedEntities)
                    .filter(([, selected]) => selected)
                    .map(([entity]) => (
                      <HStack key={entity} justify="space-between" p={2}>
                        <Text color={colorMode === 'dark' ? 'white' : 'gray.800'}>{entity}</Text>
                        <NumberInput
                          min={0}
                          value={counts[entity] || ''}
                          onChange={(value) => updateCount(entity, value)}
                          w="100px"
                          size="sm"
                        >
                          <NumberInputField />
                        </NumberInput>
                      </HStack>
                    ))}
                </Grid>
              </VStack>
            </Box>
          )}

          <Button
            size="lg"
            bgGradient="linear(to-r, purple.500, sakura.500)"
            color="white"
            _hover={{
              bgGradient: "linear(to-r, purple.600, sakura.600)",
              transform: "translateY(-2px)",
              boxShadow: "xl"
            }}
            onClick={generateGraph}
            isLoading={loading}
            loadingText="Generating..."
            w={{ base: 'full', md: 'auto' }}
          >
            Generate Graph
          </Button>

          {error && (
            <Text color="red.500" fontWeight="medium">{error}</Text>
          )}

          {(stixBundle || story) && (
            <Box w="full">
              <HStack justify="center" mb={4}>
                <Button
                  variant="outline"
                  borderColor="sakura.500"
                  color="white"
                  _hover={{
                    bgGradient: "linear(to-r, purple.500, sakura.500)",
                    borderColor: "transparent"
                  }}
                  onClick={toggleDisplayMode}
                >
                  {displayMode === 'stixBundle' ? 'Show Story' : 'Show STIX Bundle'}
                </Button>
              </HStack>

              <Box
                p={6}
                borderRadius="xl"
                borderWidth="1px"
                borderColor={colorMode === 'dark' ? 'whiteAlpha.200' : 'gray.200'}
                bg={colorMode === 'dark' ? 'rgba(23, 25, 35, 0.7)' : 'rgba(255, 255, 255, 0.7)'}
                backdropFilter="blur(10px)"
              >
                {displayMode === 'stixBundle' ? (
                  <VStack spacing={4}>
                    <Heading size="md">Generated STIX Bundle</Heading>
                    <Box
                      p={4}
                      borderRadius="md"
                      w="full"
                      maxH="400px"
                      overflowY="auto"
                      bg={colorMode === 'dark' ? 'gray.800' : 'gray.50'}
                    >
                      <Code
                        display="block"
                        whiteSpace="pre"
                        children={JSON.stringify(stixBundle, null, 2)}
                        overflowX="auto"
                        w="full"
                      />
                    </Box>
                    <HStack>
                      <Button
                        leftIcon={<FiCopy />}
                        onClick={copyJson}
                        colorScheme="purple"
                        variant="outline"
                      >
                        Copy JSON
                      </Button>
                      <Button
                        leftIcon={<FiEye />}
                        onClick={openStixVisualizer}
                        colorScheme="purple"
                      >
                        Visualize
                      </Button>
                    </HStack>
                  </VStack>
                ) : (
                  <VStack spacing={4}>
                    <Heading size="md">Generated Story</Heading>
                    <Text>{story}</Text>
                  </VStack>
                )}
              </Box>
            </Box>
          )}
        </VStack>
      </Container>
      
      <MetricsSidebar
        metrics={metrics}
        isOpen={isOpen}
        onClose={onClose}
      />
    </Box>
  );
};

export default EntitySelector;