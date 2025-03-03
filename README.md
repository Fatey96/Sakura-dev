# 🌸 Sakura STIX Generator

![Sakura STIX Generator](https://img.shields.io/badge/Sakura-STIX%20Generator-e939af?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=flat-square&logo=react)
![Flask](https://img.shields.io/badge/Flask-2.0.0-000000?style=flat-square&logo=flask)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat-square&logo=openai)

Sakura is an advanced AI-powered platform for generating synthetic STIX (Structured Threat Information Expression) cyber threat intelligence data. Create realistic threat scenarios and relationships using state-of-the-art language models.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [Command Line Interface](#command-line-interface)
- [STIX Generation Process](#stix-generation-process)
- [API Endpoints](#api-endpoints)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🔍 Overview

Sakura STIX Generator is a comprehensive tool designed to create synthetic cyber threat intelligence data in STIX 2.1 format. It leverages advanced language models to generate realistic threat scenarios, indicators, and relationships between various STIX objects. The platform consists of a Python Flask backend for data generation and a React frontend for intuitive visualization and interaction.

## ✨ Features

- **AI-Powered STIX Generation**: Leverage OpenAI's GPT models to create contextually rich and realistic threat intelligence data
- **Interactive Object Selection**: Choose specific STIX object types and quantities through an intuitive UI
- **Relationship Generation**: Automatically create meaningful relationships between STIX objects
- **Graph Visualization**: View and explore generated STIX data through interactive force-directed graphs
- **Metrics Dashboard**: Analyze the quality and characteristics of generated data
- **Export Capabilities**: Download generated STIX bundles in JSON format
- **Command Line Interface**: Generate STIX data directly from the command line for automation
- **Caching System**: Improve performance with intelligent caching of generated content

## 🏗️ Architecture

Sakura consists of two main components:

### Backend (Python Flask)

The backend is built with Flask and provides:
- RESTful API endpoints for STIX generation
- Integration with OpenAI's GPT models
- STIX object and relationship generation logic
- Bundle creation and serialization
- Metrics calculation and analysis

### Frontend (React)

The frontend is built with React and Chakra UI and provides:
- Modern, responsive user interface
- Interactive object selection
- Force-directed graph visualization
- Metrics display
- File management

## 📋 Prerequisites

- Python 3.8+ 
- Node.js 16+
- npm or yarn
- OpenAI API key

## 🚀 Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sakura-stix-generator.git
   cd sakura-stix-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   cd stix_generator
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the `stix_generator` directory with the following content:
   ```
   OPENAI_API_KEY="your-openai-api-key"
   FLASK_SECRET_KEY="your-secret-key"
   FLASK_DEBUG=True
   FLASK_HOST="0.0.0.0"
   FLASK_PORT=5000
   ```

5. Start the Flask server:
   ```bash
   python -m stix_generator.app
   ```
   The backend will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd sakura-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Configure the API endpoint:
   Create a `.env` file in the `sakura-frontend` directory:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```

4. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```
   The frontend will be available at http://localhost:3000

## 🖥️ Usage

### Web Interface

1. **Home Page**: Visit http://localhost:3000 to access the landing page
2. **Entity Selection**: Click "Get Started" to navigate to the entity selector page
3. **Configure Objects**: Select the types and quantities of STIX objects you want to generate
4. **Generate Data**: Click "Generate" to create your STIX bundle
5. **Visualize Results**: Explore the generated data through the interactive graph visualization
6. **View Metrics**: Analyze the quality and characteristics of your generated data
7. **Download**: Export your STIX bundle as a JSON file

### Command Line Interface

The STIX generator can also be used directly from the command line:

```bash
# Basic usage with default settings
python -m stix_generator.cli

# Specify object counts
python -m stix_generator.cli --counts "threat-actor:5,malware:10,indicator:15"

# Generate a specific total number of objects
python -m stix_generator.cli --total 100

# Specify output file
python -m stix_generator.cli --output my_stix_bundle.json

# Set random seed for reproducibility
python -m stix_generator.cli --seed 42

# Use a JSON config file
python -m stix_generator.cli --config my_config.json
```

## 🔄 STIX Generation Process

Sakura generates STIX data through a sophisticated multi-step process:

1. **Object Generation**:
   - User selects desired STIX object types and quantities
   - The system prompts the LLM to generate detailed object descriptions
   - Objects are created with realistic attributes and properties

2. **Relationship Generation**:
   - The system analyzes generated objects to identify potential relationships
   - Relationships are created based on object types and attributes
   - The LLM enhances relationships with contextual information

3. **Bundle Creation**:
   - Objects and relationships are converted to STIX 2.1 format
   - A STIX bundle is created containing all generated content
   - The bundle is validated for compliance with STIX standards

4. **Metrics Analysis**:
   - The system calculates quality metrics for the generated bundle
   - Metrics include completeness, consistency, and relationship density
   - Results are displayed to the user for evaluation

## 🔌 API Endpoints

The backend provides the following key API endpoints:

- `GET /api/health`: Check API health status
- `GET /api/objects`: Get available STIX object types
- `POST /api/generate-graph`: Generate STIX data
- `GET /api/download/<filename>`: Download a generated STIX bundle
- `GET /api/files`: List available STIX bundles
- `POST /api/cache/clear`: Clear the generation cache

## ⚙️ Customization

### LLM Settings

You can customize the LLM behavior by modifying the following environment variables:

```
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7
LLM_OBJECT_TEMPERATURE=0.7
LLM_RELATIONSHIP_TEMPERATURE=0.2
MAX_TOKENS=4000
```

### Object Distribution

Default object distributions can be modified in `stix_generator/config.py`.

## 🔧 Troubleshooting

### Common Issues

1. **API Key Issues**:
   - Ensure your OpenAI API key is correctly set in the `.env` file
   - Check that the API key has sufficient quota and permissions

2. **Connection Errors**:
   - Verify that both frontend and backend servers are running
   - Check that the CORS settings allow connections between the servers

3. **Generation Failures**:
   - Check the backend logs for detailed error messages
   - Try reducing the number of objects to generate if hitting rate limits

### Logs

- Backend logs are stored in `stix_generator.log`
- Check the browser console for frontend errors

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created with �� by the Sakura Team 