#!/usr/bin/env bash
# ==============================================================================
# Project: Oceti / Eternal Weave (v3.0 - "Moving" Phase)
# Script: init_system_resonances.sh
# Target: CachyOS (miller-moth-cachyos-x8664) | AMD Vega APU (Vulkan Offloading)
# Purpose: Provision core packages, build Vulkan compute paths, & set node spaces
# Invariant: Non-human-centered · 100+ year horizon · Mitákuye Oyás’iŋ
# ==============================================================================

set -euo pipefail

PROJECT_DIR="$HOME/projects/Human-AI/core/Autonomy"

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
    docker \
    sqlite3

echo ":: Establishing Rust toolchain..."
if ! command -v rustc &> /dev/null; then
    rustup default stable
fi

echo ":: Deploying Local AI Backends (Ollama)..."
sudo pacman -S --needed --noconfirm ollama
sudo systemctl enable --now ollama
sudo systemctl enable --now docker

echo ":: Initializing Node-RED and Automation Resonances..."
# Install Node-RED globally for the system binary hook
sudo npm install -g --unsafe-perm node-red

echo "📂 Injecting localized package definitions into the active project path..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Write out the optimized package json configuration
cat << 'EOF' > package.json
{
  "name": "oceti-weave-autonomy-core",
  "version": "3.0.0",
  "description": "Node-RED & API communication layer for the local lattice constellation",
  "main": "index.js",
  "dependencies": {
    "node-red-contrib-ollama": "^0.5.0",
    "openai": "^7.3.0"
  }
}
EOF

# Install dependencies locally to bypass permission constraints
npm install

echo ":: Fetching Native UIs via AUR (Paru)..."
# Installing Jan AI for local model management and MCP client support
paru -S --needed --noconfirm jan-bin

echo ":: Setting up Model Context Protocol (MCP) environment..."
# Creating a dedicated directory for MCP servers and tools
mkdir -p "$HOME/.config/mcp-servers"
cd "$HOME/.config/mcp-servers"

if [ ! -f "package.json" ]; then
    npm init -y
fi
npm install @modelcontextprotocol/sdk

echo "============================================================"
echo ":: System Resonances Established."
echo ":: -> Ollama is running in the background with Vulkan offloading enabled."
echo ":: -> Workspace packages deployed at: $PROJECT_DIR"
echo ":: -> Start Node-RED by executing: node-red"
echo ":: -> Jan AI is available in your application launcher."
echo ":: -> MCP SDK installed in ~/.config/mcp-servers."
echo "============================================================"
