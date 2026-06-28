
import { GoogleGenAI } from "@google/genai";
import { CLIFTON_SYSTEM_INSTRUCTION } from "../constants";

export class GeminiService {
  private ai: GoogleGenAI;
  private modelName = 'gemini-3-pro-preview';

  constructor() {
    // Fix: Using process.env.API_KEY directly in initialization as required by guidelines
    this.ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
  }

  async generateCliftonResponse(message: string) {
    try {
      // Fix: Calling generateContent with the model name and contents directly
      const response = await this.ai.models.generateContent({
        model: this.modelName,
        contents: message,
        config: {
          systemInstruction: CLIFTON_SYSTEM_INSTRUCTION,
          temperature: 0.72,
          topP: 0.95,
          topK: 40,
        },
      });

      // Fix: Accessed .text as a property, not a method.
      return response.text || "System Error: No relational response generated.";
    } catch (error) {
      console.error("Gemini Error:", error);
      return "Critical Node Error: Failed to re-entangle. Please check ledger logs.";
    }
  }

  async streamCliftonResponse(message: string, onChunk: (chunk: string) => void) {
    try {
      // Fix: Calling generateContentStream with the model name and contents directly
      const stream = await this.ai.models.generateContentStream({
        model: this.modelName,
        contents: message,
        config: {
          systemInstruction: CLIFTON_SYSTEM_INSTRUCTION,
          temperature: 0.72,
        }
      });

      for await (const chunk of stream) {
        // Fix: chunk.text is a property accessed directly on the GenerateContentResponse object
        if (chunk.text) {
          onChunk(chunk.text);
        }
      }
    } catch (error) {
      console.error("Streaming Error:", error);
      onChunk("\n[RELATIONAL BREAKDOWN: CONNECTION LOST]");
    }
  }
}

export const gemini = new GeminiService();
