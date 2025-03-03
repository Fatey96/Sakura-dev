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
  useToast,
  Badge,
  IconButton,
  Flex,
  Code,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  FormControl,
  FormLabel,
  FormHelperText,
  Switch,
  Textarea,
  Collapse,
  Tooltip
} from '@chakra-ui/react';
import { FiBarChart2, FiCopy, FiEye, FiSun, FiMoon, FiDownload, FiEdit, FiChevronDown, FiChevronUp } from 'react-icons/fi';
import { useStix } from './StixContext';
import { MouseTrail } from '../MouseTrail/MouseTrail';
import { useMetrics } from '../../contexts/MetricsContext';
import Metrics from '../Metrics/Metrics';

const entities = [
  { category: 'Profile & Persona', items: ['Threat Actor', 'Identity'] },
  { category: 'Artifacts', items: ['Malware', 'Tool'] },
  { category: 'Tactics & Operations', items: ['Attack Pattern', 'Campaign', 'Course of Action'] },
  { category: 'Possible Intels', items: ['Indicator', 'Report'] },
  { category: 'Forensics & Countermeasures', items: ['Intrusion Set', 'Observed Data', 'Vulnerability'] },
];

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
  const [specialInstructions, setSpecialInstructions] = useState({});
  const [showInstructionsFor, setShowInstructionsFor] = useState({});
  const { stixBundle, setStixBundle } = useStix();
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [displayMode, setDisplayMode] = useState('stixBundle');
  const [totalStixCount, setTotalStixCount] = useState(0);
  const [useCache, setUseCache] = useState(true);
  const { colorMode } = useColorMode();
  const navigate = useNavigate();
  const toast = useToast();
  const { metrics, setMetrics } = useMetrics();

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

  const toggleInstructions = (entity) => {
    setShowInstructionsFor(prev => ({
      ...prev,
      [entity]: !prev[entity]
    }));
  };

  const updateSpecialInstructions = (entity, value) => {
    setSpecialInstructions(prev => ({
      ...prev,
      [entity]: value
    }));
  };

  const generateGraph = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Filter out empty special instructions and convert display names to STIX type names
      const filteredInstructions = {};
      Object.entries(specialInstructions).forEach(([entity, instructions]) => {
        if (instructions && instructions.trim() !== '') {
          // Convert display name to STIX type name (e.g., "Threat Actor" -> "threat-actor")
          const stixType = entity.toLowerCase().replace(/ /g, '-');
          filteredInstructions[stixType] = instructions.trim();
        }
      });

      const response = await fetch('http://localhost:5000/api/generate-graph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          method: 'manual',
          counts: counts,
          use_cache: useCache,
          special_instructions: filteredInstructions
        })
      });

      const data = await response.json();
      if (data.status === 'success') {
        setStixBundle(JSON.parse(data.stix_bundle));
        setStory(data.scenario);
        setMetrics(data.metrics);
      } else {
        setError(data.error || 'Failed to generate graph');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateGraphWithTotal = async () => {
    setLoading(true);
    setError(null);

    try {
      // Filter out empty special instructions and convert display names to STIX type names
      const filteredInstructions = {};
      Object.entries(specialInstructions).forEach(([entity, instructions]) => {
        if (instructions && instructions.trim() !== '') {
          // Convert display name to STIX type name (e.g., "Threat Actor" -> "threat-actor")
          const stixType = entity.toLowerCase().replace(/ /g, '-');
          filteredInstructions[stixType] = instructions.trim();
        }
      });

      const response = await fetch('http://localhost:5000/api/generate-graph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          method: 'total',
          totalCount: totalStixCount,
          use_cache: useCache,
          special_instructions: filteredInstructions
        })
      });

      const data = await response.json();
      if (data.status === 'success') {
        setStixBundle(JSON.parse(data.stix_bundle));
        setStory(data.story);
        setMetrics(data.metrics);
        
        toast({
          title: 'STIX bundle generated successfully',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      } else {
        setError(data.error || 'Failed to generate graph');
        toast({
          title: 'Error generating STIX bundle',
          description: data.error || 'Failed to generate graph',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (err) {
      setError(err.message);
      toast({
        title: 'Error',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
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

  const downloadJson = () => {
    const dataStr = JSON.stringify(stixBundle, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.download = 'stix-bundle.json';
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
  };

  const openStixVisualizer = () => {
    if (stixBundle) {
      navigate('/stix-visualizer');
    } else {
      console.error('No STIX bundle available to visualize');
      // Optionally, show an error message to the user
    }
  };

  const clearCache = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/cache/clear', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        toast({
          title: 'Cache cleared',
          description: data.message,
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      } else {
        toast({
          title: 'Error clearing cache',
          description: data.error || 'Failed to clear cache',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (err) {
      toast({
        title: 'Error',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box
      minH="100vh"
      bg="gray.900"
      position="relative"
      overflow="hidden"
    >
      <ColorModeToggle />
      <MouseTrail />
      
      <Container maxW="container.xl" py={8} position="relative" zIndex={2}>
        <VStack spacing={6}>
          <Heading
            size="2xl"
            bgGradient="linear(to-r, purple.400, sakura.400)"
            bgClip="text"
            textAlign="center"
            fontWeight="bold"
            letterSpacing="tight"
          >
            STIX Object Generator
          </Heading>

          <HStack spacing={4} justifyContent="center">
            <FormControl display="flex" alignItems="center" justifyContent="center">
              <FormLabel htmlFor="cache-toggle" mb="0" color="white">
                Use Cached Objects
              </FormLabel>
              <Switch 
                id="cache-toggle" 
                colorScheme="sakura" 
                isChecked={useCache} 
                onChange={() => setUseCache(!useCache)}
              />
            </FormControl>
            
            <Button
              size="sm"
              variant="outline"
              borderColor="sakura.400"
              color="white"
              _hover={{
                bgGradient: "linear(to-r, purple.500, sakura.500)",
                borderColor: "transparent"
              }}
              onClick={clearCache}
            >
              Clear Cache
            </Button>
          </HStack>

          <Tabs isFitted variant="unstyled" width="100%">
            <TabList 
              mb="2em"
              bg="rgba(23, 25, 35, 0.4)"
              p={1}
              borderRadius="full"
              width="fit-content"
              mx="auto"
              borderWidth="2px"
              borderColor="sakura.400"
            >
              <Tab
                _selected={{
                  bgGradient: "linear(to-r, purple.500, sakura.500)",
                  color: "white",
                  borderRadius: "full",
                }}
                _notSelected={{
                  color: "sakura.200",
                  bg: "transparent",
                }}
                px={8}
                py={3}
                fontWeight="500"
                transition="all 0.2s"
              >
                Manual Selection
              </Tab>
              <Tab
                _selected={{
                  bgGradient: "linear(to-r, purple.500, sakura.500)",
                  color: "white",
                  borderRadius: "full",
                }}
                _notSelected={{
                  color: "sakura.200",
                  bg: "transparent",
                }}
                px={8}
                py={3}
                fontWeight="500"
                transition="all 0.2s"
              >
                Total Count
              </Tab>
            </TabList>

            <TabPanels>
              <TabPanel>
                <Grid 
                  templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }} 
                  gap={6} 
                  w="full"
                >
                  {entities.map(group => (
                    <Box
                      key={group.category}
                      p={6}
                      borderRadius="xl"
                      bg="rgba(23, 25, 35, 0.4)"
                      backdropFilter="blur(5px)"
                      borderWidth="1px"
                      borderColor="whiteAlpha.200"
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
                              color="white"
                              cursor="pointer"
                              onClick={() => toggleEntity(entity)}
                              _hover={{
                                bgGradient: "linear(to-r, purple.500, sakura.500)",
                                borderColor: "transparent"
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
                    bg="rgba(23, 25, 35, 0.4)"
                    backdropFilter="blur(5px)"
                    borderWidth="1px"
                    borderColor="whiteAlpha.200"
                    mt={8}
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
                            <Box key={entity} p={3} borderWidth="1px" borderColor="whiteAlpha.200" borderRadius="md">
                              <VStack align="stretch" spacing={2}>
                                <HStack justify="space-between">
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
                                
                                <HStack justify="space-between">
                                  <Tooltip label="Add special requirements for this entity">
                                    <Button
                                      size="xs"
                                      leftIcon={showInstructionsFor[entity] ? <FiChevronUp /> : <FiChevronDown />}
                                      variant="outline"
                                      colorScheme="sakura"
                                      onClick={() => toggleInstructions(entity)}
                                    >
                                      Special Instructions
                                    </Button>
                                  </Tooltip>
                                </HStack>
                                
                                <Collapse in={showInstructionsFor[entity]} animateOpacity>
                                  <VStack align="stretch" spacing={2}>
                                    <Text fontSize="xs" color="whiteAlpha.700">
                                      Specify special requirements for {entity.toLowerCase()} objects. The system will try to incorporate these into the generated objects.
                                    </Text>
                                    <Textarea
                                      placeholder={
                                        entity === "Tool" 
                                          ? `E.g., "Include nmap as one of the tools" or "One tool should be a custom malware dropper"`
                                          : entity === "Threat Actor"
                                            ? `E.g., "One threat actor should be named Kobra Kai from Japan" or "Include a state-sponsored group"`
                                            : entity === "Malware"
                                              ? `E.g., "One malware should target banking applications" or "Include ransomware"`
                                              : entity === "Attack Pattern"
                                                ? `E.g., "Include phishing attacks" or "One attack pattern should involve supply chain compromise"`
                                                : entity === "Indicator"
                                                  ? `E.g., "Include indicators for Emotet malware" or "Add network traffic indicators for C2 communication"`
                                                  : `E.g., "One ${entity.toLowerCase()} should have specific characteristics"`
                                      }
                                      size="sm"
                                      value={specialInstructions[entity] || ''}
                                      onChange={(e) => updateSpecialInstructions(entity, e.target.value)}
                                      mt={2}
                                      bg="rgba(0, 0, 0, 0.2)"
                                      borderColor="whiteAlpha.300"
                                      _hover={{ borderColor: "sakura.300" }}
                                      _focus={{ borderColor: "sakura.500" }}
                                    />
                                    <Text fontSize="xs" color="sakura.200">
                                      Examples:
                                      {entity === "Threat Actor" && 
                                        '"Create a threat actor named Kobra Kai based in Japan" or "Include a state-sponsored threat actor from North Korea"'}
                                      {entity === "Tool" && 
                                        '"Include nmap as one of the tools" or "One tool should be a custom malware dropper"'}
                                      {entity === "Malware" && 
                                        '"One malware should target banking applications" or "Include ransomware that targets healthcare systems"'}
                                      {entity === "Attack Pattern" && 
                                        '"Include phishing attacks" or "One attack pattern should involve supply chain compromise"'}
                                      {entity === "Indicator" && 
                                        '"Include indicators for Emotet malware" or "Add network traffic indicators for C2 communication"'}
                                      {!["Threat Actor", "Tool", "Malware", "Attack Pattern", "Indicator"].includes(entity) && 
                                        `"Customize one or more ${entity.toLowerCase()} objects with specific details"`}
                                    </Text>
                                  </VStack>
                                </Collapse>
                              </VStack>
                            </Box>
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
                  mt={6}
                  mx="auto"
                  display="block"
                  minW="200px"
                >
                  Generate Graph
                </Button>
              </TabPanel>

              <TabPanel>
                <Box
                  p={6}
                  borderRadius="xl"
                  bg="rgba(23, 25, 35, 0.4)"
                  backdropFilter="blur(5px)"
                  borderWidth="1px"
                  borderColor="whiteAlpha.200"
                  maxW="600px"
                  mx="auto"
                >
                  <VStack spacing={6} align="center">
                    <FormControl>
                      <FormLabel
                        bgGradient="linear(to-r, purple.400, sakura.400)"
                        bgClip="text"
                        fontWeight="bold"
                      >
                        Total STIX Objects
                      </FormLabel>
                      <NumberInput
                        min={1}
                        value={totalStixCount}
                        onChange={(value) => setTotalStixCount(parseInt(value) || 0)}
                      >
                        <NumberInputField />
                      </NumberInput>
                      <FormHelperText color="whiteAlpha.700">
                        Enter the total number of STIX objects you want to generate
                      </FormHelperText>
                    </FormControl>

                    <Button
                      size="lg"
                      bgGradient="linear(to-r, purple.500, sakura.500)"
                      color="white"
                      _hover={{
                        bgGradient: "linear(to-r, purple.600, sakura.600)",
                        transform: "translateY(-2px)",
                        boxShadow: "xl"
                      }}
                      onClick={generateGraphWithTotal}
                      isLoading={loading}
                      loadingText="Generating..."
                      isDisabled={totalStixCount < 1}
                      minW="200px"
                    >
                      Generate Graph
                    </Button>
                  </VStack>
                </Box>
              </TabPanel>
            </TabPanels>
          </Tabs>

          {error && (
            <Text color="red.500" fontWeight="medium">{error}</Text>
          )}

          {(stixBundle || story) && (
            <Box w="full">
              <VStack spacing={8}>
                <Box w="full" px={4}>
                  <Metrics metrics={metrics} />
                </Box>

                <HStack justify="center" mb={4}>
                  <Button
                    variant="outline"
                    borderColor="brand.primary"
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
                  w="full"
                >
                  {displayMode === 'stixBundle' ? (
                    <VStack spacing={4} w="full">
                      <Heading size="md">Generated STIX Bundle</Heading>
                      <Box
                        p={4}
                        borderRadius="md"
                        w="full"
                        maxH="400px"
                        maxW="1200px"
                        overflowY="auto"
                        overflowX="auto"
                        bg={colorMode === 'dark' ? 'gray.800' : 'gray.50'}
                      >
                        <Code
                          display="block"
                          whiteSpace="pre"
                          children={JSON.stringify(stixBundle, null, 2)}
                          w="max-content"
                          minW="100%"
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
                          leftIcon={<FiDownload />}
                          onClick={downloadJson}
                          colorScheme="purple"
                          variant="outline"
                        >
                          Download JSON
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
              </VStack>
            </Box>
          )}
        </VStack>
      </Container>
    </Box>
  );
};

export default EntitySelector;