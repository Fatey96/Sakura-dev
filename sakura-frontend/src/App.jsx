import React, { useRef } from 'react';
import { 
  ChakraProvider, 
  Box, 
  VStack, 
  Heading, 
  Text, 
  Button, 
  Container, 
  Icon, 
  SimpleGrid,
  useColorMode,
  IconButton,
  HStack
} from '@chakra-ui/react';
import { FiDatabase, FiShare2, FiShield, FiSun, FiMoon } from 'react-icons/fi';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import theme from './theme';
import Home from './Components/Home/Home';
import EntitySelector from './Components/EntitySelector/EntitySelector';
import Generate from './Components/Generate/Generate';
import STIXVisualizer from './Components/STIXVisualizer/STIXVisualizer';
import { StixProvider } from './Components/EntitySelector/StixContext';
import { MouseTrail } from './Components/MouseTrail/MouseTrail';
import { Canvas, useFrame } from '@react-three/fiber';
import { Icosahedron } from '@react-three/drei';

const Feature = ({ icon, title, description }) => {
  return (
    <VStack
      bg="transparent"
      p={8}
      borderRadius="xl"
      borderWidth="1px"
      borderColor="whiteAlpha.200"
      backdropFilter="blur(5px)"
      spacing={4}
      align="start"
      transition="all 0.3s"
      _hover={{ 
        transform: 'translateY(-5px)',
        borderColor: 'sakura.500',
        boxShadow: '0 0 20px rgba(233, 57, 175, 0.2)'
      }}
    >
      <Icon as={icon} boxSize={8} color="sakura.500" />
      <Heading size="md">{title}</Heading>
      <Text opacity={0.9}>{description}</Text>
    </VStack>
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

const Earth = () => {
  const meshRef = useRef();

  useFrame(({ clock }) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = -clock.getElapsedTime() * 0.1;
      meshRef.current.position.y = Math.sin(clock.getElapsedTime() * 0.5) * 0.1;
    }
  });

  return (
    <group ref={meshRef} position={[0, 0, 0]} scale={[2, 2, 2]}>
      <Icosahedron args={[1, 2]}>
        <meshPhongMaterial
          color="#000000"
          emissive="#e939af"
          emissiveIntensity={0.6}
          wireframe={true}
          wireframeLinewidth={2}
          transparent
          opacity={1}
        />
      </Icosahedron>
    </group>
  );
};

const LandingPage = () => {
  const navigate = useNavigate();
  const { colorMode } = useColorMode();

  return (
    <Box minH="100vh" position="relative" bg="gray.900">
      <ColorModeToggle />
      
      {/* Globe Background */}
      <Box
        position="fixed"
        top={0}
        left={0}
        right={0}
        bottom={0}
        zIndex={0}
      >
        <Canvas
          camera={{ position: [0, 0, 8], fov: 50 }}
          style={{ background: 'transparent' }}
        >
          <ambientLight intensity={1} />
          <pointLight position={[10, 10, 10]} intensity={2} />
          <Earth />
        </Canvas>
      </Box>

      <MouseTrail />

      {/* Content */}
      <Box
        position="relative"
        zIndex={1}
        bg="rgba(23, 25, 35, 0.4)"
        backdropFilter="blur(5px)"
      >
        {/* Hero Section */}
        <Container maxW="container.xl" pt={32} pb={20}>
          <VStack spacing={8} align="center" textAlign="center">
            <Heading 
              size="2xl" 
              fontWeight="bold"
              bgGradient="linear(to-r, purple.400, sakura.400)"
              bgClip="text"
            >
              Welcome to Sakura STIX
            </Heading>
            <Text 
              fontSize="xl" 
              maxW="2xl" 
              opacity={0.9}
              color={colorMode === 'dark' ? 'whiteAlpha.900' : 'gray.700'}
            >
              An advanced AI-powered platform for generating synthetic STIX cyber threat intelligence data. 
              Create realistic threat scenarios and relationships using state-of-the-art language models.
            </Text>
            <HStack spacing={4}>
              <Button
                size="lg"
                bgGradient="linear(to-r, purple.500, sakura.500)"
                color="white"
                _hover={{
                  bgGradient: "linear(to-r, purple.600, sakura.600)",
                  transform: "translateY(-2px)",
                  boxShadow: "xl"
                }}
                onClick={() => navigate('/entitySelector')}
              >
                Get Started
              </Button>
              <Button
                size="lg"
                variant="outline"
                borderColor="sakura.500"
                _hover={{
                  bg: "whiteAlpha.200",
                  transform: "translateY(-2px)",
                  boxShadow: "xl"
                }}
                onClick={() => navigate('/stix-visualizer')}
              >
                View Demo
              </Button>
            </HStack>
          </VStack>
        </Container>

        {/* Features Section */}
        <Box py={20}>
          <Container maxW="container.xl">
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
              <Feature
                icon={FiDatabase}
                title="STIX Data Generation"
                description="Leverage advanced LLMs and LangChain to generate synthetic STIX data with context-aware relationships and realistic scenarios."
              />
              <Feature
                icon={FiShare2}
                title="Graph Visualization"
                description="Visualize complex relationships between threat actors, indicators, and other STIX objects in interactive graphs."
              />
              <Feature
                icon={FiShield}
                title="Seamless Data Sharing"
                description="Coming Soon... Share and collaborate on threat intelligence data securely across your organization."
              />
            </SimpleGrid>
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

function App() {
  return (
    <ChakraProvider theme={theme}>
      <StixProvider>
        <Router>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/home" element={<Home />} />
            <Route path="/entitySelector" element={<EntitySelector />} />
            <Route path="/generate" element={<Generate />} />
            <Route path="/stix-visualizer" element={<STIXVisualizer />} />
          </Routes>
        </Router>
      </StixProvider>
    </ChakraProvider>
  );
}

export default App;