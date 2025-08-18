# Sprint Productivity Tracker - Version Guide

This repository contains two versions of the Sprint Productivity Tracker application:

## 📱 app.py - **Simple Interface** (Recommended)
- **Original clean 3-tab interface** - preferred by users
- **Universal Excel export** - anyone can export data
- **Basic automation** - export button includes auto-save and SharePoint browser opening
- **Lightweight and fast** - minimal dependencies
- **Admin authentication** - Adityakarthik only for data management

### Features:
-  Simple data entry form
-  Clean data viewing 
-  One-click Excel export with automation
-  Auto-saves to SharePoint_Ready folder
-  Opens SharePoint destination automatically
-  Admin controls for data management

### Run Simple Version:
`powershell
cd "C:\Users\6128787\Documents\productivity-tracker"
$env:TRACKER_ADMIN_CODE = "admin"
streamlit run app.py --server.port 8506
`

##  app_with_auto_upload.py - **Automated Interface**
- **Complex automated interface** with advanced features
- **Multiple upload methods** - PowerShell PnP, Microsoft Graph, hybrid solutions
- **Enhanced UI** - comprehensive automation controls
- **Full automation** - complete SharePoint integration attempts
- **Advanced error handling** - network security workarounds

### Features:
-  All features from simple version
-  Advanced SharePoint upload automation
-  Multiple auto-save locations
-  PowerShell PnP integration attempts
-  Microsoft Graph API exploration
-  Network security compatible solutions
-  Enhanced error reporting

### Run Automated Version:
`powershell
cd "C:\Users\6128787\Documents\productivity-tracker"
$env:TRACKER_ADMIN_CODE = "admin"
streamlit run app_with_auto_upload.py --server.port 8505
`

##  Recommendation

**Use app.py** for daily productivity tracking - it has the clean interface you prefer with automation added invisibly to the export button.

**Use app_with_auto_upload.py** if you need advanced automation features or want to experiment with different upload methods.

##  Admin Access
- **Username:** Adityakarthik
- **Password:** admin
- **Email Target:** rakhi.purohit@thomsonreuters.com

##  SharePoint Destination
Both versions save to and open:
https://trten.sharepoint.com/sites/CPT-RPurohit/Shared Documents/General/2025/BLR productivity gains

##  Network Access
- **Local:** http://localhost:8506 (simple) or http://localhost:8505 (automated)
- **Network:** http://192.168.1.11:8506 or http://192.168.1.11:8505
- **Team Access:** Share network URL with your team members

---
*Created: August 18, 2025*
*Author: GitHub Copilot for Adityakarthik*
