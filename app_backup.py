import datetime as dt
import pandas as pd
import streamlit as st
import sqlite3
from io import BytesIO
import hashlib

# Admin configuration
ADMIN_USERNAME = "Adityakarthik"
ADMIN_PASSWORD_HASH = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"  # "admin123"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_admin(username, password):
    return (username.strip() == ADMIN_USERNAME and 
            hash_password(password) == ADMIN_PASSWORD_HASH)

def init_db():
    with sqlite3.connect("data.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                leader TEXT,
                gains TEXT,
                dotted_gains TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')

def get_sprint_data(start_date, end_date):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.execute(
            "SELECT leader, gains, dotted_gains FROM entries WHERE start_date=? AND end_date=?",
            (start_date.isoformat(), end_date.isoformat())
        )
        return cursor.fetchall()

def save_sprint_data(start_date, end_date, data_rows):
    with sqlite3.connect("data.db") as conn:
        conn.execute(
            "DELETE FROM entries WHERE start_date=? AND end_date=?",
            (start_date.isoformat(), end_date.isoformat())
        )
        
        for row in data_rows:
            if row[0] and str(row[0]).strip():
                conn.execute(
                    "INSERT INTO entries (leader, gains, dotted_gains, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
                    (str(row[0]).strip(), str(row[1]).strip(), str(row[2]).strip(), 
                     start_date.isoformat(), end_date.isoformat())
                )
        conn.commit()

def create_excel_file(dataframe, start_date, end_date):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        info_df = pd.DataFrame({
            'Sprint Information': ['Start Date', 'End Date', 'Generated On'],
            'Value': [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        info_df.to_excel(writer, sheet_name='Sprint Info', index=False)
        dataframe.to_excel(writer, sheet_name='Productivity Data', index=False)
    return output.getvalue()

st.set_page_config(page_title="Sprint Productivity Tracker", layout="wide")
st.title(" Sprint Productivity Tracker")
st.markdown("**Team can update data | Only Adityakarthik can export/email**")

init_db()

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(" Sprint Start Date", value=dt.date.today() - dt.timedelta(days=14))
with col2:
    end_date = st.date_input(" Sprint End Date", value=dt.date.today())

st.divider()

tab1, tab2 = st.tabs([" Team Data Entry", " Admin Actions (Adityakarthik Only)"])

with tab1:
    st.subheader("Team Data Entry")
    st.info("Enter productivity gains for the selected sprint period. Use text like '40 hours', 'N/A', '~25 hrs', etc.")
    
    existing_data = get_sprint_data(start_date, end_date)
    
    if existing_data:
        df_data = [[str(row[0]), str(row[1]), str(row[2])] for row in existing_data]
    else:
        df_data = [["", "", ""], ["", "", ""], ["", "", ""]]
    
    df = pd.DataFrame(df_data, columns=[
        "Name of the leader",
        "Productivity Gains (In Hours)",
        "+ Productivity Gains (Dotted Team) (In Hours)"
    ]).astype(str)
    
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Name of the leader": st.column_config.TextColumn("Name of the leader", width="medium"),
            "Productivity Gains (In Hours)": st.column_config.TextColumn("Productivity Gains (In Hours)", width="medium"),
            "+ Productivity Gains (Dotted Team) (In Hours)": st.column_config.TextColumn("+ Productivity Gains (Dotted Team) (In Hours)", width="medium")
        }
    )
    
    if st.button(" Save Data", type="primary"):
        try:
            data_to_save = []
            for _, row in edited_df.iterrows():
                data_to_save.append((
                    str(row["Name of the leader"]),
                    str(row["Productivity Gains (In Hours)"]),
                    str(row["+ Productivity Gains (Dotted Team) (In Hours)"])
                ))
            
            save_sprint_data(start_date, end_date, data_to_save)
            st.success(" Data saved successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error saving data: {str(e)}")

with tab2:
    st.subheader("Admin Actions - Adityakarthik Only")
    st.warning(" This section is restricted to admin access only")
    
    col1, col2 = st.columns(2)
    with col1:
        admin_username = st.text_input(" Username:", placeholder="Enter your username")
    with col2:
        admin_password = st.text_input(" Password:", type="password", placeholder="Enter your password")
    
    if st.button(" Login as Admin", type="secondary"):
        if verify_admin(admin_username, admin_password):
            st.session_state.admin_authenticated = True
            st.session_state.admin_username = admin_username
            st.success(f" Welcome {admin_username}! You are authenticated as admin.")
            st.rerun()
        else:
            st.error(" Invalid credentials. Access denied.")
            st.session_state.admin_authenticated = False
    
    if st.session_state.get('admin_authenticated', False):
        st.success(f" Logged in as: {st.session_state.get('admin_username', 'Admin')}")
        
        if st.button(" Logout", type="secondary"):
            st.session_state.admin_authenticated = False
            st.session_state.admin_username = None
            st.rerun()
        
        st.divider()
        
        sprint_data = get_sprint_data(start_date, end_date)
        
        if sprint_data:
            display_df = pd.DataFrame(sprint_data, columns=[
                "Name of the leader",
                "Productivity Gains (In Hours)",
                "+ Productivity Gains (Dotted Team) (In Hours)"
            ])
            
            st.subheader(" Current Sprint Data")
            st.dataframe(display_df, use_container_width=True)
            
            excel_data = create_excel_file(display_df, start_date, end_date)
            filename = f"productivity_tracker_{start_date}_{end_date}.xlsx"
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label=" Download Excel File",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="secondary"
                )
            
            with col2:
                if st.button(" Send Email to Rakhi", type="primary"):
                    st.info(" Sending email with Excel attachment...")
                    
                    import smtplib
                    from email.mime.multipart import MIMEMultipart
                    from email.mime.base import MIMEBase
                    from email import encoders
                    from email.mime.text import MIMEText
                    
                    try:
                        # Create the email
                        msg = MIMEMultipart()
                        msg['From'] = "productivity.tracker@company.com"
                        msg['To'] = "rakhi.purohit@thomsonreuters.com"
                        msg['Subject'] = f"Sprint Productivity Report - {start_date} to {end_date}"
                        
                        body = f"""Dear Rakhi,

Please find attached the Sprint Productivity Report for the period:
From: {start_date.strftime('%B %d, %Y')}
To: {end_date.strftime('%B %d, %Y')}

The report includes productivity gains from team leaders and their dotted teams.

Best regards,
{st.session_state.admin_username}
Sprint Productivity Tracker System"""
                        
                        msg.attach(MIMEText(body, 'plain'))
                        
                        # Attach Excel file
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(excel_data)
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                        msg.attach(part)
                        
                        st.success(" Email prepared with Excel attachment!")
                        st.info(" **Email Details:**")
                        st.write(f"**To:** rakhi.purohit@thomsonreuters.com")
                        st.write(f"**Subject:** Sprint Productivity Report - {start_date} to {end_date}")
                        st.write(f"**Attachment:** {filename}")
                        st.warning(" **Note:** To enable actual email sending, configure SMTP settings in the code.")
                        
                    except Exception as e:
                        st.error(f"Email preparation failed: {str(e)}")
            
            st.info(" Target Email: **rakhi.purohit@thomsonreuters.com**")
        else:
            st.warning(" No data available for the selected sprint period.")
    else:
        st.info(" Please login with admin credentials to access export and email features.")
        st.markdown('''
        **Admin Credentials:**
        - **Username:** Adityakarthik
        - **Password:** admin123
        ''')

st.divider()
st.caption("Sprint Productivity Tracker v2.0 | Admin: Adityakarthik | Email: rakhi.purohit@thomsonreuters.com")
