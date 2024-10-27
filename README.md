# LLM-Robot

This repository showcases how to build agentic LLM pipelines for controlling robots using [Haystack](https://haystack.deepset.ai/) and [deepset Cloud](https://www.deepset.ai/cloud). The project is centered around a hexapot robot that can be controlled via APIs, with an LLM integrated to provide reasoning capabilities and handle function calls dynamically.

## Features

- **Haystack Integration**: Utilizes Haystack pipelines to process commands and control robot functionalities.
- **LLM-Driven Control**: Leverages LLMs for decision-making, allowing the robot to understand and execute complex commands.
- **API Exposure**: Robot functionalities (e.g., LEDs, movements) are accessible through well-defined APIs, enabling remote and automated control.
- **Agent-Based Architecture**: Employs an agentic approach for controlling the robot, handling input parsing, reasoning, and action execution.

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/llm-robot.git
   cd llm-robot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**: Update the `.env` file with necessary configurations (API keys, Haystack setup, etc.).

4. **Run the Agent**:
   ```bash
   python run_agent.py
   ```

## Usage

- Use the provided endpoints to send commands to the robot.
- Explore the predefined Haystack pipelines for various functionalities.
- Modify and extend the pipeline logic to adapt to new commands or robot features.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References

- [Agentic LLM Pipelines for Robots with Haystack and deepset Cloud](https://medium.com/gopenai/agentic-llm-pipelines-for-robots-with-haystack-and-deepset-cloud-07f6319f29e6)
