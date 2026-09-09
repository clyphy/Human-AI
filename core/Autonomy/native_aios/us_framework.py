#!/usr/bin/env python3
"""
"Us" Framework - Human-AI Symbiosis Foundation
Enhanced with full llama.cpp (River) support.
"""

import requests
import json
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class InferenceEngine(Enum):
    OLLAMA = "ollama"
    JAN = "jan"
    LLAMA_CPP = "llama_cpp"   # River


@dataclass
class InferenceResult:
    text: str
    engine: InferenceEngine
    tokens: int
    latency_ms: float
    confidence: float = 1.0


class UsFramework:
    def __init__(
        self,
        primary_model: str = "tinydolphin",
        context_window: int = 8192,
        temperature: float = 0.7,
        timeout_seconds: int = 90,
        llama_cpp_url: str = "http://127.0.0.1:8080/v1"
    ):
        self.primary_model = primary_model
        self.context_window = context_window
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds
        self.llama_cpp_url = llama_cpp_url
        
        self.conversation_history: List[Dict[str, str]] = []
        self.audit_log: List[Dict[str, Any]] = []
    
    def _check_engine_health(self, engine: InferenceEngine) -> bool:
        """Health checks for all engines."""
        try:
            if engine == InferenceEngine.OLLAMA:
                r = requests.get("http://localhost:11434/api/tags", timeout=2)
                return r.status_code == 200
            elif engine == InferenceEngine.JAN:
                r = requests.get("http://localhost:8000/v1/models", timeout=2)
                return r.status_code == 200
            elif engine == InferenceEngine.LLAMA_CPP:
                r = requests.get(f"{self.llama_cpp_url}/models", timeout=3)
                return r.status_code == 200
        except Exception:
            return False
        return False

    def _get_available_engine(self) -> InferenceEngine:
        """Priority: Local → Most autonomous"""
        priority = [InferenceEngine.LLAMA_CPP, InferenceEngine.OLLAMA, InferenceEngine.JAN]
        for engine in priority:
            if self._check_engine_health(engine):
                return engine
        raise RuntimeError("No inference engines available")

    def _query_llama_cpp(self, prompt: str) -> Optional[InferenceResult]:
        """Query local llama.cpp server (OpenAI compatible)"""
        try:
            start = time.time()
            response = requests.post(
                f"{self.llama_cpp_url}/chat/completions",
                json={
                    "model": self.primary_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.temperature,
                    "max_tokens": 1024,
                },
                timeout=self.timeout_seconds
            )
            
            if response.status_code == 200:
                data = response.json()
                choice = data["choices"][0]
                text = choice["message"]["content"]
                latency = (time.time() - start) * 1000
                
                return InferenceResult(
                    text=text,
                    engine=InferenceEngine.LLAMA_CPP,
                    tokens=choice.get("usage", {}).get("completion_tokens", 0),
                    latency_ms=latency,
                    confidence=0.92
                )
        except Exception as e:
            print(f"llama.cpp (River) error: {e}")
        return None

    # Keep your existing _query_ollama and _query_jan (or I can optimize them too)

    def query(self, prompt: str, use_context: bool = True) -> InferenceResult:
        if use_context and self.conversation_history:
            # Simple context injection (can be improved with better summarization later)
            context_str = "\n".join(
                f"{m['role']}: {m['content']}" 
                for m in self.conversation_history[-6:]
            )
            full_prompt = f"{context_str}\nuser: {prompt}"
        else:
            full_prompt = prompt

        engine = self._get_available_engine()
        
        if engine == InferenceEngine.LLAMA_CPP:
            result = self._query_llama_cpp(full_prompt)
        elif engine == InferenceEngine.OLLAMA:
            result = self._query_ollama(full_prompt)  # your original method
        else:
            result = self._query_jan(full_prompt)

        if not result:
            raise RuntimeError(f"Query failed on {engine.value}")

        # Record history and audit
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": result.text})
        self._log_to_audit(prompt, result)

        return result

    # ... keep your _log_to_audit, get_audit_trail, reset_conversation, export_conversation ...
