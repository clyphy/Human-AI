import { GoogleGenAI } from "@google/genai";
import { ViewOption } from "../types";
import { PROMPT_OPTION_A, PROMPT_OPTION_B } from '../constants';

// Fix: Check for process.env.API_KEY directly to ensure its availability.
if (!process.env.API_KEY) {
  throw new Error("API_KEY environment variable not set");
}

// Fix: Use process.env.API_KEY directly in the constructor as per @google/genai guidelines.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export async function generateDocument(baseText: string, option: ViewOption): Promise<string> {
  let promptTemplate: string;

  if (option === 'A') {
    promptTemplate = PROMPT_OPTION_A;
  } else if (option === 'B') {
    promptTemplate = PROMPT_OPTION_B;
  } else {
    throw new Error("Invalid option selected");
  }

  const prompt = promptTemplate.replace('{baseText}', baseText);

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
    });
    return response.text;
  } catch (error) {
    console.error("Error generating content from Gemini:", error);
    throw new Error("Failed to communicate with the AI model.");
  }
}