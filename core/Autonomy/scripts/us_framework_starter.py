#!/usr/bin/env python3
"""
"Us" Framework - Human-AI Symbiosis Foundation
Starter implementation for local inference with fallback routing.
"""

import requests
import json
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class InferenceEngine(Enum):
    """Available inference engines."""
    OLLAMA = "ollama"
    JAN = "jan"
    LLAMA_CPP = "llama_cpp"


@dataclass
class InferenceResult:
    """Result from any inference engine."""
    text: str
    engine: InferenceEngine
    tokens: int
    latency_ms: float
    confidence: float = 1.0


class UsFramework:
    """
    Core "Us" Framework for human-AI collaboration.
    
    Handles:
    - Multi-engine inference with intelligent fallback
    - Conversation context management
    - Decision confidence scoring
    - Audit trails for transparency
    """
    
    def __init__(
        self,
        primary_model: str = "mistral:7b",
        context_window: int = 2048,
        temperature: float = 0.7,
        timeout_seconds: int = 60
    ):
        self.primary_model = primary_model
        self.context_window = context_window
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds
        
        # Conversation history for context
        self.conversation_history: list[Dict[str, str]] = []
        
        # Audit trail
        self.audit_log: list[Dict[str, Any]] = []
    
    def _check_engine_health(self, engine: InferenceEngine) -> bool:
        """Check if an inference engine is available."""
        endpoints = {
            InferenceEngine.OLLAMA: ("http://localhost:11434/api/tags", 2),
            InferenceEngine.JAN: ("http://localhost:8000/v1/models", 2),
        }
        
        if engine not in endpoints:
            return False
        
        url, timeout = endpoints[engine]
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except Exception:
            return False
    
    def _get_available_engine(self) -> InferenceEngine:
        """Return the first available engine in priority order."""
        for engine in [InferenceEngine.OLLAMA, InferenceEngine.JAN]:
            if self._check_engine_health(engine):
                return engine
        
        # Fallback to llama.cpp (assumed available locally)
        return InferenceEngine.LLAMA_CPP
    
    def _query_ollama(self, prompt: str) -> Optional[InferenceResult]:
        """Query Ollama inference engine."""
        try:
            start = time.time()
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.primary_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_ctx": self.context_window,
                    }
                },
                timeout=self.timeout_seconds
            )
            
            if response.status_code == 200:
                data = response.json()
                latency = (time.time() - start) * 1000
                
                return InferenceResult(
                    text=data.get("response", ""),
                    engine=InferenceEngine.OLLAMA,
                    tokens=data.get("eval_count", 0),
                    latency_ms=latency,
                    confidence=0.95
                )
        except Exception as e:
            print(f"Ollama error: {e}")
        
        return None
    
    def _query_jan(self, prompt: str) -> Optional[InferenceResult]:
        """Query Jan AI inference engine."""
        try:
            start = time.time()
            response = requests.post(
                "http://localhost:8000/v1/completions",
                json={
                    "model": "default",
                    "prompt": prompt,
                    "max_tokens": 256,
                    "temperature": self.temperature,
                },
                timeout=self.timeout_seconds
            )
            
            if response.status_code == 200:
                data = response.json()
                latency = (time.time() - start) * 1000
                
                return InferenceResult(
                    text=data["choices"][0]["text"],
                    engine=InferenceEngine.JAN,
                    tokens=len(data["choices"][0]["text"].split()),
                    latency_ms=latency,
                    confidence=0.90
                )
        except Exception as e:
            print(f"Jan AI error: {e}")
        
        return None
    
    def query(self, prompt: str, use_context: bool = True) -> InferenceResult:
        """
        Query the "Us" framework with fallback routing.
        
        Args:
            prompt: User query
            use_context: Include conversation history in context
        
        Returns:
            InferenceResult with response and metadata
        """
        
        # Build full prompt with context if requested
        full_prompt = prompt
        if use_context and self.conversation_history:
            context = "\n".join(
                f"{msg['role'].capitalize()}: {msg['content']}"
                for msg in self.conversation_history[-5:]  # Last 5 messages
            )
            full_prompt = f"{context}\nAssistant: {prompt}\nAssistant:"
        
        # Try engines in priority order
        available_engine = self._get_available_engine()
        
        if available_engine == InferenceEngine.OLLAMA:
            result = self._query_ollama(full_prompt)
        elif available_engine == InferenceEngine.JAN:
            result = self._query_jan(full_prompt)
        else:
            raise RuntimeError("No inference engines available")
        
        if not result:
            # Fallback to next available
            for engine in [InferenceEngine.JAN, InferenceEngine.OLLAMA]:
                if engine == available_engine:
                    continue
                if engine == InferenceEngine.JAN:
                    result = self._query_jan(full_prompt)
                elif engine == InferenceEngine.OLLAMA:
                    result = self._query_ollama(full_prompt)
                if result:
                    break
        
        if not result:
            raise RuntimeError("All inference engines failed")
        
        # Record in conversation history
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": result.text})
        
        # Log to audit trail
        self._log_to_audit(prompt, result)
        
        return result
    
    def _log_to_audit(self, prompt: str, result: InferenceResult) -> None:
        """Add entry to audit trail."""
        self.audit_log.append({
            "timestamp": time.time(),
            "prompt": prompt,
            "response": result.text,
            "engine": result.engine.value,
            "latency_ms": result.latency_ms,
            "confidence": result.confidence,
            "tokens": result.tokens,
        })
    
    def get_audit_trail(self) -> list[Dict[str, Any]]:
        """Return audit trail of all queries."""
        return self.audit_log.copy()
    
    def reset_conversation(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
    
    def export_conversation(self, filepath: str) -> None:
        """Export conversation to JSON file."""
        with open(filepath, 'w') as f:
            json.dump({
                "history": self.conversation_history,
                "audit_log": self.audit_log,
            }, f, indent=2)


# Example usage
if __name__ == "__main__":
    # Initialize framework
    us = UsFramework(
        primary_model="mistral:7b",
        context_window=2048,
        temperature=0.7
    )
    
    print("🤖 Us Framework initialized")
    print(f"Primary model: {us.primary_model}")
    print(f"Available engine: {us._get_available_engine().value}")
    print()
    
    # Test queries
    prompts = [
        "What is the meaning of life?",
        "Explain quantum computing briefly.",
        "How would you approach learning a new skill?"
    ]
    
    try:
        for prompt in prompts:
            print(f"📝 Query: {prompt}")
            result = us.query(prompt)
            print(f"🤖 Response ({result.engine.value}, {result.latency_ms:.0f}ms):")
            print(f"   {result.text[:200]}...\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  docker-compose up -d ollama")
    
    # Show audit trail
    print("\n📋 Audit Trail:")
    for entry in us.audit_log:
        print(f"  - {entry['engine']}: {entry['tokens']} tokens, {entry['latency_ms']:.0f}ms")
