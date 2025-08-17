#  AI Productivity Gains Tracker

A Streamlit-based web application for tracking sprint productivity gains across team leaders and their dotted teams.

## ✨ Features

- **Team Data Entry**: Leaders can input productivity gains for each sprint
- **Admin Control**: Only Adityakarthik can access export/email functionality  
- **Excel Export**: Download sprint data as formatted Excel files
- **Email Integration**: Send reports directly to stakeholders
- **Sprint Management**: Track multiple sprint periods with date ranges
- **Secure Authentication**: Password-protected admin access

##  Installation

1. Clone the repository:
```bash
git clone https://github.com/adityakarthikrTR/AI-prod-gains-.git
cd AI-prod-gains-
```

2. Create virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

##  Usage

1. Start the application:
```bash
streamlit run app.py --server.port 8505
```

2. Open in browser: http://localhost:8505

### For Team Leaders:
- Use "Team Data Entry" tab
- Select sprint dates
- Fill productivity data
- Click "Save Data"

### For Admin (Adityakarthik):
- Go to "Admin Actions" tab
- Login with credentials:
  - Username: `Adityakarthik`
  - Password: `admin123`
- View/download/email reports

##  Data Format

The application tracks:
- **Name of the leader**
- **Productivity Gains (In Hours)** 
- **+ Productivity Gains (Dotted Team) (In Hours)**

Supports flexible text input like "40 hours", "N/A", "~25 hrs", etc.

##  Security

- Username/password authentication for admin
- Secure password hashing (SHA-256)
- Session-based access control
- Team members can only enter data, not export

##  Email Integration

Reports are automatically sent to: `rakhi.purohit@thomsonreuters.com`

To enable email functionality:
1. Configure SMTP settings in the code
2. Set up sender email credentials
3. Update email server parameters

##  Technical Stack

- **Backend**: Python, SQLite
- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Excel Export**: openpyxl
- **Authentication**: hashlib (SHA-256)

##  Project Structure

```
AI-prod-gains-/
 app.py              # Main Streamlit application
 requirements.txt    # Python dependencies
 .gitignore         # Git ignore rules
 README.md          # Project documentation
 data.db            # SQLite database (auto-created)
```

##  Configuration

### Admin Credentials
- Username: `Adityakarthik`
- Password: `admin123` (change in production!)

### Email Settings
Update in `app.py`:
```python
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```

##  Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

##  License

This project is for internal Thomson Reuters use.

##  Author

**Adityakarthik** - Thomson Reuters

##  Support

For issues or questions, contact the development team.

---

*Sprint Productivity Tracker v2.0 | Admin: Adityakarthik | Email: rakhi.purohit@thomsonreuters.com*
