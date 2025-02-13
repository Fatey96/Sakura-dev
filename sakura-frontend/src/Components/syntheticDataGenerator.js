import { v4 as uuidv4 } from 'uuid';

const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];

const generateThreatActor = () => ({
  type: "threat-actor",
  spec_version: "2.1",
  id: `threat-actor--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Silent", "Crimson", "Phantom", "Cyber", "Shadow"])} ${getRandomElement(["Dragon", "Viper", "Ghost", "Falcon", "Wolf"])}`,
  description: `A sophisticated threat actor known for ${getRandomElement(["financial crimes", "espionage", "sabotage", "data theft"])}`,
  threat_actor_types: [getRandomElement(["nation-state", "criminal", "hacktivist"])],
  aliases: [`TA-${Math.floor(1000 + Math.random() * 9000)}`],
  first_seen: new Date().toISOString(),
  last_seen: new Date().toISOString(),
  goals: [getRandomElement(["Financial gain", "Intelligence gathering", "Disruption of services", "Geopolitical advantage"])],
  sophistication: getRandomElement(["novice", "intermediate", "expert"]),
  resource_level: getRandomElement(["individual", "club", "organization", "government"]),
  primary_motivation: getRandomElement(["ideology", "financial", "strategic-advantage"])
});

const generateMalware = () => ({
  type: "malware",
  spec_version: "2.1",
  id: `malware--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Toxic", "Shadow", "Stealth", "Chaos", "Venom"])}${getRandomElement(["Worm", "Trojan", "Ransomware", "Spyware"])}`,
  description: `A type of malware designed for ${getRandomElement(["data exfiltration", "system disruption", "financial fraud", "espionage"])}`,
  malware_types: [getRandomElement(["ransomware", "trojan", "backdoor", "spyware"])],
  is_family: false,
  first_seen: new Date().toISOString(),
  operating_system_refs: [getRandomElement(["Windows", "macOS", "Linux", "Android", "iOS"])],
  architecture_execution_envs: [getRandomElement(["x86", "x64", "ARM"])],
  implementation_languages: [getRandomElement(["C", "C++", "Python", "JavaScript"])],
  capabilities: [getRandomElement(["compromise-data", "anti-debugging", "anti-vm", "communicate-with-c2"])]
});

const generateIdentity = () => ({
  type: "identity",
  spec_version: "2.1",
  id: `identity--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["John", "Jane", "Alex", "Sam"])} ${getRandomElement(["Doe", "Smith", "Johnson", "Brown"])}`,
  description: `An identity associated with ${getRandomElement(["a threat actor", "a victim", "a security researcher", "an organization"])}`,
  identity_class: getRandomElement(["individual", "group", "organization", "class", "unknown"]),
  sectors: [getRandomElement(["technology", "finance", "healthcare", "energy", "government"])],
  contact_information: `email: ${Math.random().toString(36).substring(2, 8)}@example.com`
});

const generateIndicator = () => ({
  type: "indicator",
  spec_version: "2.1",
  id: `indicator--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Suspicious", "Malicious", "Anomalous", "Threat"])} ${getRandomElement(["Traffic", "File", "Behavior", "Pattern"])}`,
  description: `An indicator of ${getRandomElement(["potential compromise", "malware infection", "data exfiltration", "unauthorized access"])}`,
  indicator_types: [getRandomElement(["malicious-activity", "benign-activity", "anomalous-activity"])],
  pattern: `[ipv4-addr:value = '${Math.floor(1 + Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}']`,
  pattern_type: "stix",
  pattern_version: "2.1",
  valid_from: new Date().toISOString(),
  valid_until: new Date(Date.now() + 30*24*60*60*1000).toISOString()
});

const generateTool = () => ({
  type: "tool",
  spec_version: "2.1",
  id: `tool--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Cyber", "Net", "Hack", "Sec"])}${getRandomElement(["Knife", "Hammer", "Blade", "Shield"])}`,
  description: `A tool used for ${getRandomElement(["network scanning", "password cracking", "data exfiltration", "privilege escalation"])}`,
  tool_types: [getRandomElement(["remote-access", "vulnerability-scanner", "network-scanner", "credential-exploitation"])],
  aliases: [`TL-${Math.floor(1000 + Math.random() * 9000)}`],
  tool_version: `${Math.floor(1 + Math.random() * 5)}.${Math.floor(Math.random() * 10)}.${Math.floor(Math.random() * 10)}`
});

const generateIntrusionSet = () => ({
  type: "intrusion-set",
  spec_version: "2.1",
  id: `intrusion-set--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `Operation ${getRandomElement(["Silent", "Dark", "Cyber", "Shadow"])} ${getRandomElement(["Storm", "Eagle", "Viper", "Wolf"])}`,
  description: `A set of malicious activities carried out by ${getRandomElement(["a nation-state", "a criminal organization", "a hacktivist group", "an unknown entity"])}`,
  aliases: [`IS-${Math.floor(1000 + Math.random() * 9000)}`],
  first_seen: new Date(Date.now() - 365*24*60*60*1000).toISOString(),
  last_seen: new Date().toISOString(),
  goals: [getRandomElement(["Espionage", "Financial gain", "Sabotage", "Data theft"])],
  resource_level: getRandomElement(["individual", "club", "organization", "government"]),
  primary_motivation: getRandomElement(["ideology", "financial", "dominance", "destruction"])
});

const generateCourseOfAction = () => ({
  type: "course-of-action",
  spec_version: "2.1",
  id: `course-of-action--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Patch", "Update", "Configure", "Disable"])} ${getRandomElement(["System", "Network", "Application", "Protocol"])}`,
  description: `A course of action to ${getRandomElement(["mitigate a vulnerability", "prevent an attack", "respond to an incident", "improve security posture"])}`,
  action_type: getRandomElement(["preventative", "detective", "reactive"]),
  action_reference: {
    source_name: "Security Best Practices Guide",
    url: `https://example.com/security-guide-${Math.floor(100 + Math.random() * 900)}`
  }
});

const generateAttackPattern = () => ({
  type: "attack-pattern",
  spec_version: "2.1",
  id: `attack-pattern--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Phishing", "DDoS", "SQL Injection", "Man-in-the-Middle"])} Attack`,
  description: `A technique used by threat actors to ${getRandomElement(["gain unauthorized access", "disrupt services", "exfiltrate data", "escalate privileges"])}`,
  kill_chain_phases: [
    {
      kill_chain_name: "lockheed-martin-cyber-kill-chain",
      phase_name: getRandomElement(["reconnaissance", "weaponization", "delivery", "exploitation", "installation", "command-and-control", "actions-on-objectives"])
    }
  ]
});

const generateInfrastructure = () => ({
  type: "infrastructure",
  spec_version: "2.1",
  id: `infrastructure--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Botnet", "C2 Server", "Proxy Network", "Bulletproof Hosting"])} Infrastructure`,
  description: `An infrastructure used for ${getRandomElement(["command and control", "data exfiltration", "anonymization", "malware distribution"])}`,
  infrastructure_types: [getRandomElement(["botnet", "command-and-control", "anonymization", "hosting-malware"])],
  first_seen: new Date(Date.now() - 180*24*60*60*1000).toISOString(),
  last_seen: new Date().toISOString()
});

const generateCampaign = () => ({
  type: "campaign",
  spec_version: "2.1",
  id: `campaign--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `Operation ${getRandomElement(["Silent", "Dark", "Cyber", "Shadow"])} ${getRandomElement(["Thunder", "Viper", "Eagle", "Storm"])}`,
  description: `A campaign targeting ${getRandomElement(["financial institutions", "government agencies", "critical infrastructure", "tech companies"])}`,
  aliases: [`CP-${Math.floor(1000 + Math.random() * 9000)}`],
  first_seen: new Date(Date.now() - 90*24*60*60*1000).toISOString(),
  last_seen: new Date().toISOString(),
  objective: `${getRandomElement(["Data theft", "Financial fraud", "Service disruption", "Espionage"])}`
});

const generateOpinion = () => ({
  type: "opinion",
  spec_version: "2.1",
  id: `opinion--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  explanation: `Based on the observed behavior and indicators, it is ${getRandomElement(["highly likely", "possible", "unlikely", "certain"])} that this activity is associated with ${getRandomElement(["a known threat group", "a new threat actor", "a false flag operation", "a cyber espionage campaign"])}`,
  authors: [`analyst-${Math.floor(100 + Math.random() * 900)}@example.com`],
  opinion: getRandomElement(["strongly-agree", "agree", "neutral", "disagree", "strongly-disagree"])
});

const generateReport = () => ({
  type: "report",
  spec_version: "2.1",
  id: `report--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `Threat Intelligence Report: ${getRandomElement(["APT Group Activities", "Malware Analysis", "Cybercrime Trends", "Vulnerability Assessment"])}`,
  description: `A comprehensive report on ${getRandomElement(["recent cyber attacks", "emerging threats", "vulnerability exploits", "threat actor tactics"])}`,
  report_types: [getRandomElement(["threat-report", "attack-pattern", "malware", "threat-actor"])],
  published: new Date().toISOString()
});

const generateLocation = () => ({
  type: "location",
  spec_version: "2.1",
  id: `location--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  name: `${getRandomElement(["Shadowy", "Cyber", "Digital", "Ghost", "Phantom"])} ${getRandomElement(["Hub", "Nexus", "Center", "Base", "Outpost"])}`,
  description: `A location known for ${getRandomElement(["cyber operations", "data storage", "command and control activities", "hacker meetups"])}`,
  latitude: (Math.random() * 180 - 90).toFixed(6),
  longitude: (Math.random() * 360 - 180).toFixed(6),
  region: getRandomElement(["North America", "South America", "Europe", "Asia", "Africa", "Australia"]),
  country: getRandomElement(["USA", "China", "Russia", "UK", "Germany", "Brazil", "India", "Japan"]),
  city: getRandomElement(["Megacity", "Cybertown", "Hackerville", "Datapolis", "Securicity"])
});

const generateMalwareAnalysis = () => ({
  type: "malware-analysis",
  spec_version: "2.1",
  id: `malware-analysis--${uuidv4()}`,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  product: `${getRandomElement(["CyberAnalyzer", "MalwareHunter", "ThreatScanner", "CodeInspector"])} v${Math.floor(1 + Math.random() * 5)}.${Math.floor(Math.random() * 10)}`,
  version: `${Math.floor(1 + Math.random() * 5)}.${Math.floor(Math.random() * 10)}.${Math.floor(Math.random() * 10)}`,
  host_vm: getRandomElement(["Windows 10", "Ubuntu 20.04", "macOS Big Sur", "Kali Linux"]),
  operating_system: getRandomElement(["Windows", "Linux", "macOS"]),
  installed_software: `${getRandomElement(["Python", "Java", "C++", "Ruby"])} ${Math.floor(2 + Math.random() * 3)}.${Math.floor(Math.random() * 10)}`,
  analysis_started: new Date(Date.now() - 7*24*60*60*1000).toISOString(),
  analysis_ended: new Date().toISOString(),
  result: getRandomElement(["malicious", "suspicious", "benign", "unknown"])
});

const generateObservedData = () => ({
    type: "observed-data",
    spec_version: "2.1",
    id: `observed-data--${uuidv4()}`,
    created: new Date().toISOString(),
    modified: new Date().toISOString(),
    first_observed: new Date(Date.now() - 30*24*60*60*1000).toISOString(),
    last_observed: new Date().toISOString(),
    number_observed: Math.floor(1 + Math.random() * 100),
    objects: {
      "0": {
        type: "ipv4-addr",
        value: `${Math.floor(1 + Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`
      },
      "1": {
        type: "network-traffic",
        src_ref: "0",
        dst_port: Math.floor(1 + Math.random() * 65535),
        protocols: [
          getRandomElement(["tcp", "udp", "http", "https", "ftp"])
        ]
      }
    }
  });
  
  const generateRelationship = (source, target) => ({
    type: "relationship",
    spec_version: "2.1",
    id: `relationship--${uuidv4()}`,
    created: new Date().toISOString(),
    modified: new Date().toISOString(),
    relationship_type: getRandomElement(["uses", "targets", "located-at", "indicates", "mitigates", "originates-from", "investigates", "attributed-to"]),
    source_ref: source.id,
    target_ref: target.id
  });
  
  export const generateSyntheticData = (counts) => {
    const objects = [];
    
    // Generate STIX objects based on counts
    for (const [type, count] of Object.entries(counts)) {
      for (let i = 0; i < count; i++) {
        switch (type) {
          case "Threat Actor":
            objects.push(generateThreatActor());
            break;
          case "Malware":
            objects.push(generateMalware());
            break;
          case "Identity":
            objects.push(generateIdentity());
            break;
          case "Indicator":
            objects.push(generateIndicator());
            break;
          case "Tool":
            objects.push(generateTool());
            break;
          case "Intrusion Set":
            objects.push(generateIntrusionSet());
            break;
          case "Course of Action":
            objects.push(generateCourseOfAction());
            break;
          case "Attack Pattern":
            objects.push(generateAttackPattern());
            break;
          case "Infrastructure":
            objects.push(generateInfrastructure());
            break;
          case "Campaign":
            objects.push(generateCampaign());
            break;
          case "Opinion":
            objects.push(generateOpinion());
            break;
          case "Report":
            objects.push(generateReport());
            break;
          case "Location":
            objects.push(generateLocation());
            break;
          case "Malware Analysis":
            objects.push(generateMalwareAnalysis());
            break;
          case "Observed Data":
            objects.push(generateObservedData());
            break;
        }
      }
    }
    
    // Generate some relationships
    objects.forEach(source => {
      if (Math.random() < 0.7) {  // 70% chance to create a relationship
        const potentialTargets = objects.filter(obj => obj.id !== source.id);
        if (potentialTargets.length > 0) {
          const target = getRandomElement(potentialTargets);
          objects.push(generateRelationship(source, target));
        }
      }
    });
    
    return {
      type: "bundle",
      id: `bundle--${uuidv4()}`,
      objects: objects
    };
  };