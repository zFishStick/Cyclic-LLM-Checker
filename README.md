# Cyclic-LLM-Checker
Repository for the "Semantic web &amp; Social network" project

## Methodology used
1. Give input to Gemini
2. Gemini generates output
3. Check output with DeepSeek
4. If output is reliable, return output to user
5. If output is not verified, DeepSeek generate a new output based on Gemini's output
6. Output is evaluated by Gemini
7. Gemini performs same process as DeepSeek to verify the new output
8. Loop until output is reliable