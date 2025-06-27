
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

## 💼 Licensing & Business Model

This project uses an **Open Core** model.

*   **The Core Application**: The fundamental features of this application are open-source under the **Apache License 2.0**. We believe the core tools for cognitive accessibility should be transparent and available to the community. You are free to inspect, modify, and self-host this core version.
*   **Future "Pro" Features**: We plan to develop advanced, proprietary features (such as team collaboration, advanced integrations, and premium AI capabilities) that will be available as part of a future paid SaaS offering.

This model allows us to build a sustainable business while fostering an open and trusting relationship with our user community.

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, find a bug, or want to improve the code, please feel free to:

1.  Open an issue to discuss the change.
2.  Fork the repository and submit a pull request.

---

*This project is dedicated to creating digital tools that empower, not overwhelm.*
