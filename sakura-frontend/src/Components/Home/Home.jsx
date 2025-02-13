import React from 'react';
import { Box, Container, VStack, Heading, Text, Button, SimpleGrid, Icon, useColorMode } from '@chakra-ui/react';
import { FiDatabase, FiShare2, FiShield } from 'react-icons/fi';
import { MouseTrail } from '../MouseTrail/MouseTrail';
import { Link } from 'react-router-dom';

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
        >
            <Icon as={icon} boxSize={8} color="sakura.500" />
            <Heading size="md">{title}</Heading>
            <Text opacity={0.9}>{description}</Text>
        </VStack>
    );
};

const Home = () => {
    const { colorMode } = useColorMode();

    return (
        <Box 
            minH="100vh" 
            bg={colorMode === 'dark' ? 'gray.900' : 'gray.50'} 
            position="relative"
            overflow="hidden"
        >
            <MouseTrail />
            
            {/* Content */}
            <Container maxW="container.xl" position="relative" zIndex={2}>
                <VStack spacing={20} py={20}>
                    {/* Hero Section */}
                    <VStack spacing={8} textAlign="center">
                        <Heading
                            size="2xl"
                            bgGradient="linear(to-r, purple.400, sakura.400)"
                            bgClip="text"
                        >
                            WELCOME TO SAKURA STIX
                        </Heading>
                        <Text 
                            fontSize="xl" 
                            maxW="2xl" 
                            color={colorMode === 'dark' ? 'gray.300' : 'gray.600'}
                        >
                            A modern platform for managing and visualizing STIX cyber threat
                            intelligence data with powerful graph visualization capabilities.
                        </Text>
                        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                            <Link to="/entitySelector">
                                <Button
                                    size="lg"
                                    w="full"
                                    bgGradient="linear(to-r, purple.500, sakura.500)"
                                    color="white"
                                    _hover={{
                                        bgGradient: "linear(to-r, purple.600, sakura.600)",
                                    }}
                                >
                                    Get Started
                                </Button>
                            </Link>
                            <Link to="/stix-visualizer">
                                <Button
                                    size="lg"
                                    w="full"
                                    variant="outline"
                                    borderColor="sakura.500"
                                    _hover={{
                                        bgGradient: "linear(to-r, purple.500, sakura.500)",
                                        color: "white"
                                    }}
                                >
                                    View Demo
                                </Button>
                            </Link>
                        </SimpleGrid>
                    </VStack>

                    {/* Features Section */}
                    <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} w="full">
                        <Feature
                            icon={FiDatabase}
                            title="STIX Data Management"
                            description="Efficiently manage and organize your STIX cyber threat intelligence data with our intuitive interface."
                        />
                        <Feature
                            icon={FiShare2}
                            title="Graph Visualization"
                            description="Visualize complex relationships between threat actors, indicators, and other STIX objects in interactive graphs."
                        />
                        <Feature
                            icon={FiShield}
                            title="Security Analysis"
                            description="Analyze and understand cyber threats with powerful visualization and analysis tools."
                        />
                    </SimpleGrid>
                </VStack>
            </Container>
        </Box>
    );
};

export default Home;