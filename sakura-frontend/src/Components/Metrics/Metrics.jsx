import React from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  Grid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Progress,
  Button,
  Collapse,
  HStack,
  Icon,
  SimpleGrid,
  CircularProgress,
  CircularProgressLabel,
} from '@chakra-ui/react';
import { FiBarChart2, FiChevronDown, FiChevronUp } from 'react-icons/fi';

const MetricCard = ({ label, value, helpText, progress }) => (
  <Stat
    px={4}
    py={3}
    bg="rgba(23, 25, 35, 0.4)"
    backdropFilter="blur(5px)"
    borderRadius="xl"
    borderWidth="1px"
    borderColor="whiteAlpha.200"
    _hover={{
      borderColor: 'sakura.400',
      transform: 'translateY(-2px)',
      transition: 'all 0.2s',
    }}
  >
    <StatLabel 
      bgGradient="linear(to-r, purple.400, sakura.400)"
      bgClip="text"
      fontWeight="bold"
    >
      {label}
    </StatLabel>
    <StatNumber color="white" fontSize="2xl">
      {typeof value === 'number' ? value.toFixed(1) : value}
    </StatNumber>
    {helpText && (
      <StatHelpText color="whiteAlpha.700">
        {helpText}
      </StatHelpText>
    )}
    {progress && (
      <Progress
        value={value}
        colorScheme="pink"
        size="sm"
        borderRadius="full"
        mt={2}
      />
    )}
  </Stat>
);

const DEFAULT_METRICS = {
  basic_metrics: {
    summary: {
      total_objects: 0,
      relationship_count: 0,
      quality_score: 0,
      completeness_score: 0,
      consistency_score: 0,
      relationship_score: 0,
      relationship_density: 0
    }
  }
};

const Metrics = ({ metrics }) => {
  const [isOpen, setIsOpen] = React.useState(true);

  // Add defensive check - if metrics is missing or malformed, use defaults
  const safeMetrics = metrics && metrics.basic_metrics && metrics.basic_metrics.summary 
    ? metrics 
    : DEFAULT_METRICS;
  
  const summary = safeMetrics.basic_metrics.summary;

  if (!metrics) return null;

  return (
    <Box 
      w="full" 
      position="relative"
      bg="rgba(23, 25, 35, 0.2)"
      borderRadius="xl"
      p={4}
    >
      <Button
        onClick={() => setIsOpen(!isOpen)}
        variant="ghost"
        w="full"
        mb={isOpen ? 4 : 0}
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        _hover={{
          bg: "rgba(236, 72, 153, 0.1)",
        }}
      >
        <HStack>
          <Icon as={FiBarChart2} color="sakura.400" />
          <Heading
            size="md"
            bgGradient="linear(to-r, purple.400, sakura.400)"
            bgClip="text"
          >
            STIX Bundle Metrics
          </Heading>
        </HStack>
        <Icon 
          as={isOpen ? FiChevronUp : FiChevronDown}
          color="sakura.400"
          transition="transform 0.3s ease"
        />
      </Button>

      <Collapse in={isOpen} animateOpacity>
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={5}>
          <MetricCard
            label="Total Objects"
            value={summary.total_objects}
            helpText="Total number of STIX objects generated"
          />
          <MetricCard
            label="Quality Score"
            value={summary.quality_score}
            helpText="Overall quality score"
          />
          <MetricCard
            label="Completeness"
            value={summary.completeness_score}
            helpText="Data completeness score"
          />
          <MetricCard
            label="Consistency"
            value={summary.consistency_score}
            helpText="Data consistency score"
          />
          <MetricCard
            label="Relationship Score"
            value={summary.relationship_score}
            helpText="Quality of relationships"
          />
          <MetricCard
            label="Relationship Density"
            value={summary.relationship_density}
            helpText="Density of object relationships"
          />
        </SimpleGrid>
      </Collapse>
    </Box>
  );
};

export default Metrics; 