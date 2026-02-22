# 🐸 SapoPeppo: AI-Powered ICPC & IOI Coach

SapoPeppo is an intelligent pedagogical assistant built in Python, designed specifically to support the competitive programming club "Boscosoft" in their training for international competitions like the ICPC and IOI.

### 🎥 Live Demonstration
*(Arrastra y suelta tu video .mp4 justo aquí, y borra esta línea en español)*

## 🚀 The Problem
High-performance competitive programming training often leads to silent frustration when students hit technical walls (e.g., repeated Time Limit Exceeded errors on Codeforces). SapoPeppo prevents dropout by providing instant, context-aware pedagogical hints instead of just giving away the solution.

## 🧠 Core Architecture
* **Language:** Python 3
* **LLM Integration:** Llama 3 (via Groq API) for ultra-fast natural language processing and pedagogical prompting.
* **Real-Time Context:** Integrates with the `Codeforces API` to dynamically fetch the student's current rating and rank. The AI uses this data to adjust its explanation complexity (e.g., using real-world analogies for Newbies, and Big O notation for Experts).
* **Interface:** Discord (`discord.py`), providing a seamless experience within the students' natural communication hub.

## ⚙️ Features
- **Dynamic Prompting:** The AI adapts its technical vocabulary based on the user's Codeforces rating.
- **C++ Template Enforcement:** Strictly adheres to the club's standard competitive programming C++ macros and structure when generating code skeletons.
- **Contextual Memory:** Maintains a short-term conversation history per user for fluid, multi-turn technical follow-ups.
- **Message Chunking:** Automatically handles Discord's 2000-character limit for long technical explanations.


https://github.com/user-attachments/assets/b37b0fe0-72da-4c67-9567-8d19d5b8504b


