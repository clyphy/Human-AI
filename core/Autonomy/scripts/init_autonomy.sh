#!/bin/bash
# Autonomy Project: CachyOS AI & Dev Ecosystem Initialization
# Target: AMD Vega APU (Vulkan Offloading)

set -e

echo ":: Synchronizing CachyOS repositories and updating system..."
sudo pacman -Syu --noconfirm

echo ":: Installing core development affordances and Vulkan compute..."
# clblast and vulkan-radeon ensure llama.cpp/Ollama offload matrix ops to the Vega APU
sudo pacman -S --needed --noconfirm \
    base-devel \
    git \
    rustup \
    nodejs \
    npm \
    python \
    python-pip \
    vulkan-radeon \
    vulkan-icd-loader \
    clblast \
    docker

echo ":: Establishing Rust toolchain..."
rustup default stable

echo ":: Deploying Local AI Backends (Ollama)..."
sudo pacman -S --needed --noconfirm ollama
sudo systemctl enable --now ollama
sudo systemctl enable --now docker

echo ":: Initializing Node-RED and Automation Resonances..."
sudo npm install -g --unsafe-perm node-red
# Installing the Ollama integration for Node-RED workflows
npm install -g node-red-contrib-ollama

echo ":: Fetching Native UIs via AUR (Paru)..."
# Installing Jan AI for local model management and MCP client support
paru -S --needed --noconfirm jan-bin

echo ":: Setting up Model Context Protocol (MCP) environment..."
# Creating a dedicated directory for MCP servers and tools
mkdir -p ~/.config/mcp-servers
cd ~/.config/mcp-servers
# Initializing a basic Node-based MCP server template for system integration
npm init -y
npm install @modelcontextprotocol/sdk

echo "============================================================"
echo ":: System Resonances Established."
echo ":: -> Ollama is running in the background."
echo ":: -> Start Node-RED by executing: node-red"
echo ":: -> Jan AI is available in your application launcher."
echo ":: -> MCP SDK installed in ~/.config/mcp-servers."
echo "============================================================"
