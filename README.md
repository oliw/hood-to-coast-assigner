# Hood to Coast 2023 Relay Runner Assignment Script

Welcome to the Hood to Coast 2023 Relay Runner Assignment Script repository! This script is designed to help you efficiently assign runners to legs for the Hood to Coast relay event based on their preferences. By utilizing the power of Python 3, Pipenv, OR-Tools, and PrettyTable, this script aims to streamline the leg assignment process for a smoother relay experience.

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## About

The Hood to Coast 2023 Relay Runner Assignment Script is a tool to help race organizers and teams manage the assignment of runners to specific legs of the relay race. It takes into account the preferences of the runners and optimizes the assignment process to create a balanced and enjoyable race experience.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3
- Pipenv
- OR-Tools
- PrettyTable

### Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/running.git
```

2. Navigate to the project directory:

```bash
cd running
```

3. Install dependencies using Pipenv:

```bash
pipenv install
```

## Usage

1. Open the `course_data.py` file and update it with the relevant information about the relay course and runner preferences.

2. Run the `script.py` file using Pipenv:

```bash
pipenv run python script.py
```

3. The script will generate an optimized assignment of runners to legs based on their preferences and display the results in a tabular format.

## Features

- Efficient optimization using OR-Tools to assign runners to legs.
- Customizable course and runner preference data in `course_data.py`.
- Clear and visually appealing output using PrettyTable.

## Contributing

We welcome contributions from the community! If you have any ideas, suggestions, or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-new-idea`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-new-idea`.
5. Create a pull request explaining your changes.

## License

This project is licensed under the [MIT License](LICENSE).

---

Happy running at the Hood to Coast 2023 Relay! If you encounter any issues or have questions, please feel free to open an issue on this repository.