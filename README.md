# LinkedIn AI/ML Q&A Bot

A professional-grade Python utility that generates expert-level AI/ML responses for LinkedIn using Claude 3.5 Sonnet. This tool helps AI professionals create well-structured, concise responses to technical questions while maintaining a professional tone suitable for LinkedIn.

## Features

- Processes questions and descriptions in a structured format
- Generates responses optimized for LinkedIn's AI/ML audience
- Enforces character limits for optimal LinkedIn post length
- Supports both file-based and interactive input modes
- Comprehensive error handling and logging
- Modular and maintainable code structure

## Prerequisites

- Python 3.8 or higher
- Anthropic API key for Claude 3.5 Sonnet

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd linkedin-qa-bot
```

2. Install required packages:

```bash
pip install anthropic
```

3. Set up your Anthropic API key:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

### Basic Usage

```bash
python linkedin_qa_bot.py
```

This will process the default input file `question&answerformat.md` in the current directory.

### Custom Input File

```bash
python linkedin_qa_bot.py -i path/to/your/input.md
```

### Interactive Mode

```bash
python linkedin_qa_bot.py --interactive
```

### Input Format

Your input file should follow this format:

```markdown
<question>
Your AI/ML related question here
<description>
Detailed context and description of your question here
</description>
</question>
```

## Command Line Options

- `-i, --input`: Specify input file path (default: question&answerformat.md)
- `--interactive`: Use interactive mode for manual input
- `-h, --help`: Show help message and exit

## Error Handling

The script includes comprehensive error handling for:

- Missing API keys
- Invalid input format
- File read/write errors
- API communication issues
- Character limit violations

## Logging

Logs are written to stdout with timestamp and log level. Important events and errors are automatically logged for debugging purposes.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Anthropic for providing the Claude 3.5 Sonnet API
- The AI/ML community on LinkedIn for inspiration
