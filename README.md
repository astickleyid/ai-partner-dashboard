# AI Partner Dashboard

A Streamlit-based web application for managing AI partnership capabilities and memory configurations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

## Features

- 🔐 **Secure Authentication** - Password-protected admin access with SHA-256 hashing
- 📊 **Skill Capability Dashboard** - Track and manage AI capabilities across multiple categories
- 🧠 **Memory Stack Dashboard** - Organize and maintain AI memory configurations
- 💾 **Data Persistence** - CSV-based storage for easy data management
- ✏️ **Interactive Editing** - Add, edit, and delete rows with inline data editor
- 📥 **Export Functionality** - Download data as CSV files
- 🔍 **Search & Filter** - Find and organize data quickly

## Screenshots

### Admin Setup
![Admin Setup](https://github.com/user-attachments/assets/eb8afea3-452a-4d7b-893f-c9145564c5c3)

### Login Page
![Login Page](https://github.com/user-attachments/assets/eff80f82-f2b1-43f5-9377-4f56e68ddf37)

### Skill Capability Dashboard
![Capabilities Dashboard](https://github.com/user-attachments/assets/87bfef7b-47e9-4d6d-a4a8-a63c6ba3570a)

### Memory Stack Dashboard
![Memory Stack Dashboard](https://github.com/user-attachments/assets/5df829ea-1063-411a-aba8-41a9a149709d)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/astickleyid/ai-partner-dashboard.git
   cd ai-partner-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run ai_partner_dashboard.py
   ```

4. **Access the dashboard**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - Create your admin account on first run

## Usage

### First Time Setup

1. When you first run the application, you'll see an "Administrator Setup" screen
2. Create a username and password for the admin account
3. Click "Set Administrator" to save your credentials
4. Refresh the page and log in with your credentials

### Managing Capabilities

The **Skill Capability Dashboard** tracks AI capabilities across these categories:
- Research & Analysis
- Creative Thinking
- Execution Support
- Memory & Alignment
- Self-Auditing

Each capability has:
- **Category**: The skill category name
- **Description**: What the capability entails
- **Level (1-5)**: Proficiency level from 1 (basic) to 5 (expert)

**Actions:**
- ✏️ Click any cell to edit
- ➕ Click "Add row" to create new entries
- 🗑️ Select rows and delete them
- 💾 Changes are saved automatically
- 📥 Export data using "Download as CSV"

### Managing Memory Stack

The **Memory Stack Dashboard** organizes AI memory into sections:
- Identity Core
- Vision & Long-Term Objectives
- Values Stack
- Strategic Preferences
- Feedback Loop
- Memory Containers

Each section has:
- **Section**: The memory category name
- **Description**: Purpose of this memory section
- **Editable**: Whether the section can be modified

**Actions:** Same as Skill Capability Dashboard

## Data Storage

Data is stored in CSV files in the application directory:
- `capabilities.csv` - Skill capability data
- `memory_stack.csv` - Memory stack data
- `auth.json` - Admin credentials (hashed)

**Note:** These files are automatically created with default data on first run.

## Configuration

You can modify the default data in `ai_partner_dashboard.py`:
- `def_capabilities` - Default capability data
- `def_memory_stack` - Default memory stack data

## Security Notes

⚠️ **Important Security Considerations:**

1. **Production Use**: This application uses basic authentication suitable for personal use. For production environments, consider:
   - Implementing proper session management
   - Using a secure authentication framework
   - Adding HTTPS support
   - Implementing rate limiting
   - Using a proper database instead of CSV files

2. **Password Security**: Passwords are hashed using SHA-256. While better than plaintext, consider using bcrypt or Argon2 for production use.

3. **Access Control**: Currently supports single admin user. Multi-user support would require additional development.

4. **File Permissions**: Ensure `auth.json` and CSV files have appropriate file permissions in your deployment environment.

## Development

### Project Structure

```
ai-partner-dashboard/
├── ai_partner_dashboard.py    # Main application file
├── requirements.txt            # Python dependencies
├── ANALYSIS_REPORT.md         # Detailed analysis and testing report
├── README.md                  # This file
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore rules
├── .devcontainer/             # Dev container configuration
├── capabilities.csv           # Generated on first run (not in git)
├── memory_stack.csv           # Generated on first run (not in git)
└── auth.json                  # Generated on first run (not in git)
```

### Running in Development Mode

```bash
streamlit run ai_partner_dashboard.py --server.runOnSave true
```

This enables auto-reload when you make code changes.

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Port Already in Use

If port 8501 is already in use:
```bash
streamlit run ai_partner_dashboard.py --server.port 8502
```

### Module Not Found Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Data Not Persisting

Check file permissions for the application directory. The application needs write access to create CSV files.

### Forgot Admin Password

Delete the `auth.json` file and restart the application to create a new admin account:
```bash
rm auth.json
streamlit run ai_partner_dashboard.py
```

## Known Issues

See [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md) for detailed analysis of current issues and planned improvements.

Current known issues:
- Login form remains visible after authentication
- No logout functionality
- Error messages shown even when default data loads successfully
- No session persistence across page refreshes

## Roadmap

- [ ] Implement session state management
- [ ] Add logout functionality
- [ ] Improve error handling and messaging
- [ ] Add data validation
- [ ] Add password change functionality
- [ ] Implement data backup/restore
- [ ] Add visualizations and analytics
- [ ] Multi-user support with role-based access
- [ ] Database backend option

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [Pandas](https://pandas.pydata.org/) for data management

## Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Review the [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md) for detailed documentation

---

**Version:** 1.0.0  
**Last Updated:** October 2025
