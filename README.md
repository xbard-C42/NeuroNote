
# NeuroProject Manager 🧠

> An AI-powered project management application designed from the ground up to support the cognitive strengths and challenges of neurodivergent users, particularly those with AuDHD (Autism + ADHD).

This tool isn't just another task manager. It's a focused environment built on principles of cognitive accessibility, designed to reduce executive dysfunction, prevent overwhelm, and provide AI-driven scaffolding for planning and execution.

## ✨ Core Features

*   **AI-Powered Task Breakdown**: Enter a large, vague idea (e.g., "Launch new product"), and the AI assistant will break it down into small, concrete, actionable steps.
*   **Customizable Views**: Switch between a simple **List View** and a visual **Kanban Board** to track tasks in the way that best suits your mental model.
*   **AI Progress Dashboard**: Get encouraging, jargon-free summaries of your progress and gentle nudges on what to tackle next.
*   **Multi-Provider AI**: Choose your preferred AI backend. The app supports:
    *   Google Gemini
    *   OpenAI (ChatGPT)
    *   Anthropic (Claude)
    *   Local LLMs via Ollama
*   **Deep Accessibility Controls**:
    *   High Contrast Mode
    *   Reduced Motion Mode
    *   Adjustable Font Sizes (Small, Medium, Large)
*   **Editable Project Pages**: Simple, auto-saving pages within each project for brain-dumping, notes, and moodboards without the fear of losing work.
*   **Safe Project Deletion**: A "Danger Zone" with confirmation steps to prevent accidental deletion of important projects.

## 🚀 Getting Started

This project is currently a self-contained, single-file web application. No complex setup is required.

1.  **Download the Code**: Clone this repository or download the `index.html` file.
2.  **Open in Browser**: Open the `index.html` file directly in a modern web browser (like Chrome, Firefox, or Edge).
3.  **Configure AI (Required for AI features)**:
    *   Click the **"Add"** button to create your first project.
    *   Once a project is selected, click the **"⚙️ Settings"** button.
    *   Navigate to the **AI Provider** section.
    *   Select your desired provider (e.g., Gemini, OpenAI, Ollama).
    *   Enter the required API keys or endpoint information.
    *   Click **"Save Settings"**.

The application is now ready to use!

## 🛠️ Technology Stack

*   **Frontend**: React (via CDN), HTML5, CSS3
*   **JavaScript Transpilation**: Babel (via CDN)
*   **AI Integrations**:
    *   `@google/generative-ai` for Google Gemini
    *   Direct REST API calls for OpenAI, Anthropic, and Ollama
*   **Persistence**: Browser `localStorage` is used to save settings and accessibility preferences. The project data is currently stored in a mock database in memory.

C42 OS Proprietary License v1.0

Copyright (c) 2024 [Your Name/Company]

IMPORTANT: This software is proprietary and commercially licensed.

1. GRANT OF RIGHTS
   Subject to the terms of this license, you are granted a non-exclusive, 
   non-transferable right to:
   a) Use this software for personal evaluation purposes only
   b) View and study the source code for educational purposes only

2. RESTRICTIONS
   You may NOT:
   a) Use this software for any commercial purposes
   b) Distribute, sublicense, or sell copies of this software
   c) Modify, adapt, or create derivative works
   d) Remove or alter any proprietary notices
   e) Reverse engineer (except as permitted by law)

3. RESERVATION OF RIGHTS
   All rights not expressly granted are reserved. This includes but is not 
   limited to patents, trademarks, copyrights, and trade secrets.

4. COMMERCIAL LICENSING
   Commercial use requires a separate commercial license. 
   Contact: licensing@c42os.com

5. FUTURE OPEN SOURCE TRANSITION
   The copyright holder reserves the right to release future versions 
   under open source licenses at their sole discretion.

6. NO WARRANTY
   This software is provided "AS IS" without warranty of any kind.

7. LIMITATION OF LIABILITY
   In no event shall the copyright holder be liable for any damages.

8. TERMINATION
   This license terminates automatically if you breach any terms.

For commercial licensing inquiries: licensing@c42os.com
For other questions: legal@c42os.com

This license protects the investment in revolutionary consciousness 
computing research while preserving the option for future open source 
contribution to humanity.

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, find a bug, or want to improve the code, please feel free to:

1.  Open an issue to discuss the change.
2.  Fork the repository and submit a pull request.

---

*This project is dedicated to creating digital tools that empower, not overwhelm.*
