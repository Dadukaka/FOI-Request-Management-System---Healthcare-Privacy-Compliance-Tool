import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="FOI Request Management System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #1e3a8a 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .urgent-card {
        background: #fef2f2;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        margin: 0.5rem 0;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        display: inline-block;
    }
    .success-box {
        background: #f0fdf4;
        border: 2px solid #86efac;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'requests' not in st.session_state:
    st.session_state.requests = [
        {
            'id': 'FOI-2024-001',
            'requester_name': 'John Smith',
            'request_type': 'Personal Health Information',
            'date_received': '2024-11-01',
            'due_date': '2024-12-01',
            'status': 'In Progress',
            'assigned_to': 'Sarah Johnson',
            'legislation_type': 'PHIPA',
            'description': 'Request for complete medical records from 2020-2024',
            'third_party_notification': False,
            'fee_estimate': 0,
            'extension_granted': False
        },
        {
            'id': 'FOI-2024-002',
            'requester_name': 'Law Firm ABC',
            'request_type': 'Legal/Insurance',
            'date_received': '2024-11-15',
            'due_date': '2024-12-15',
            'status': 'Pending Review',
            'assigned_to': 'Michael Chen',
            'legislation_type': 'FIPPA',
            'description': 'Incident reports and security footage from June 2024',
            'third_party_notification': True,
            'fee_estimate': 120,
            'extension_granted': False
        },
        {
            'id': 'FOI-2024-003',
            'requester_name': 'Jane Doe',
            'request_type': 'Audit Logs',
            'date_received': '2024-10-20',
            'due_date': '2024-11-19',
            'status': 'In Progress',
            'assigned_to': 'Sarah Johnson',
            'legislation_type': 'PHIPA',
            'description': 'Access logs for patient health record #12345',
            'third_party_notification': False,
            'fee_estimate': 0,
            'extension_granted': False
        }
    ]

# Helper functions
def calculate_due_date(received_date, legislation):
    """Calculate due date based on legislation (30 days for PHIPA/FIPPA/MFIPPA)"""
    date_obj = datetime.strptime(received_date, '%Y-%m-%d')
    due_date = date_obj + timedelta(days=30)
    return due_date.strftime('%Y-%m-%d')

def calculate_fee(request_type, legislation):
    """Calculate estimated fee based on request type and legislation"""
    if request_type == 'Personal Health Information' and legislation == 'PHIPA':
        return 0
    elif legislation == 'FIPPA':
        return 30  # Application fee
    elif legislation == 'MFIPPA':
        return 5  # Application fee
    return 0

def get_days_remaining(due_date):
    """Calculate days remaining until due date"""
    due = datetime.strptime(due_date, '%Y-%m-%d')
    today = datetime.now()
    diff = (due - today).days
    return diff

def get_status_color(status):
    """Return color code for status"""
    colors = {
        'Pending Review': '#fef3c7',
        'In Progress': '#dbeafe',
        'Completed': '#d1fae5',
        'Overdue': '#fee2e2',
        'Extended': '#e9d5ff'
    }
    return colors.get(status, '#f3f4f6')

def get_status_badge(status):
    """Generate HTML for status badge"""
    color = get_status_color(status)
    return f'<span class="status-badge" style="background-color: {color};">{status}</span>'

# Sidebar Navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "All Requests", "New Request", "Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About This Tool")
st.sidebar.info(
    "FOI Request Management System helps track and manage Freedom of Information "
    "requests under PHIPA, FIPPA, and MFIPPA legislation."
)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>📋 FOI Request Management System</h1>
    <p>Healthcare Privacy & Access Management Tool</p>
</div>
""", unsafe_allow_html=True)

# DASHBOARD PAGE
if page == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Calculate statistics
    df = pd.DataFrame(st.session_state.requests)
    total_requests = len(df)
    pending = len(df[df['status'] == 'Pending Review'])
    in_progress = len(df[df['status'] == 'In Progress'])
    completed = len(df[df['status'] == 'Completed'])
    
    # Calculate overdue
    overdue = 0
    for req in st.session_state.requests:
        if get_days_remaining(req['due_date']) < 0 and req['status'] != 'Completed':
            overdue += 1
    
    # Display statistics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card" style="border-top: 4px solid #3b82f6;">
            <h3 style="color: #3b82f6; margin: 0;">Total Requests</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(total_requests), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card" style="border-top: 4px solid #f59e0b;">
            <h3 style="color: #f59e0b; margin: 0;">Pending Review</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(pending), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="border-top: 4px solid #10b981;">
            <h3 style="color: #10b981; margin: 0;">In Progress</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(in_progress), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card" style="border-top: 4px solid #ef4444;">
            <h3 style="color: #ef4444; margin: 0;">Overdue</h3>
            <h1 style="margin: 0.5rem 0;">{}</h1>
        </div>
        """.format(overdue), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Urgent Attention Section
    st.subheader("⚠️ Urgent Attention Required")
    
    urgent_requests = []
    for req in st.session_state.requests:
        days_left = get_days_remaining(req['due_date'])
        if days_left <= 5 and req['status'] != 'Completed':
            urgent_requests.append({**req, 'days_left': days_left})
    
    urgent_requests.sort(key=lambda x: x['days_left'])
    
    if urgent_requests:
        for req in urgent_requests:
            days_text = f"{abs(req['days_left'])} days overdue" if req['days_left'] < 0 else f"{req['days_left']} days remaining"
            color = "#dc2626" if req['days_left'] < 0 else "#ea580c"
            
            st.markdown(f"""
            <div class="urgent-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{req['id']} - {req['requester_name']}</strong><br>
                        <span style="color: #6b7280; font-size: 0.875rem;">{req['request_type']}</span>
                    </div>
                    <div style="text-align: right;">
                        <strong style="color: {color}; font-size: 1.125rem;">{days_text}</strong><br>
                        <span style="color: #6b7280; font-size: 0.875rem;">Due: {req['due_date']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No urgent requests at this time")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Activity
    st.subheader("📅 Recent Requests")
    recent_df = df.sort_values('date_received', ascending=False).head(5)
    
    for _, row in recent_df.iterrows():
        with st.expander(f"{row['id']} - {row['requester_name']} ({row['status']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Type:** {row['request_type']}")
                st.write(f"**Legislation:** {row['legislation_type']}")
                st.write(f"**Received:** {row['date_received']}")
            with col2:
                st.write(f"**Due Date:** {row['due_date']}")
                st.write(f"**Assigned To:** {row['assigned_to']}")
                st.write(f"**Fee:** ${row['fee_estimate']}")

# ALL REQUESTS PAGE
elif page == "All Requests":
    st.header("📑 All FOI Requests")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=['Pending Review', 'In Progress', 'Completed', 'Extended', 'Overdue'],
            default=[]
        )
    with col2:
        legislation_filter = st.multiselect(
            "Filter by Legislation",
            options=['PHIPA', 'FIPPA', 'MFIPPA'],
            default=[]
        )
    with col3:
        search_term = st.text_input("Search by Requester Name or ID")
    
    # Filter requests
    filtered_requests = st.session_state.requests.copy()
    
    if status_filter:
        filtered_requests = [r for r in filtered_requests if r['status'] in status_filter]
    
    if legislation_filter:
        filtered_requests = [r for r in filtered_requests if r['legislation_type'] in legislation_filter]
    
    if search_term:
        filtered_requests = [r for r in filtered_requests if 
                            search_term.lower() in r['requester_name'].lower() or 
                            search_term.lower() in r['id'].lower()]
    
    st.markdown(f"**Showing {len(filtered_requests)} of {len(st.session_state.requests)} requests**")
    st.markdown("---")
    
    # Display requests
    if filtered_requests:
        for req in filtered_requests:
            days_left = get_days_remaining(req['due_date'])
            
            with st.expander(f"**{req['id']}** - {req['requester_name']} - {req['status']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Request Type:** {req['request_type']}")
                    st.write(f"**Legislation:** {req['legislation_type']}")
                    st.write(f"**Date Received:** {req['date_received']}")
                    st.write(f"**Due Date:** {req['due_date']}")
                
                with col2:
                    st.write(f"**Assigned To:** {req['assigned_to']}")
                    st.write(f"**Status:** {req['status']}")
                    days_color = "🔴" if days_left < 0 else "🟡" if days_left <= 5 else "🟢"
                    days_text = f"{abs(days_left)} days overdue" if days_left < 0 else f"{days_left} days remaining"
                    st.write(f"**Time Remaining:** {days_color} {days_text}")
                    st.write(f"**Fee Estimate:** ${req['fee_estimate']}")
                
                with col3:
                    st.write(f"**Third-Party Notice:** {'Yes' if req['third_party_notification'] else 'No'}")
                    st.write(f"**Extension Granted:** {'Yes' if req['extension_granted'] else 'No'}")
                
                st.markdown("**Description:**")
                st.info(req['description'])
                
                # Action buttons
                st.markdown("---")
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if req['status'] == 'Pending Review':
                        if st.button(f"▶️ Start Processing", key=f"start_{req['id']}"):
                            for r in st.session_state.requests:
                                if r['id'] == req['id']:
                                    r['status'] = 'In Progress'
                            st.success("Status updated to In Progress")
                            st.rerun()
                
                with action_col2:
                    if req['status'] == 'In Progress' and not req['extension_granted']:
                        if st.button(f"⏰ Grant Extension", key=f"extend_{req['id']}"):
                            for r in st.session_state.requests:
                                if r['id'] == req['id']:
                                    current_due = datetime.strptime(r['due_date'], '%Y-%m-%d')
                                    new_due = current_due + timedelta(days=30)
                                    r['due_date'] = new_due.strftime('%Y-%m-%d')
                                    r['extension_granted'] = True
                                    r['status'] = 'Extended'
                            st.success("30-day extension granted")
                            st.rerun()
                
                with action_col3:
                    if req['status'] in ['In Progress', 'Extended']:
                        if st.button(f"✅ Mark Complete", key=f"complete_{req['id']}"):
                            for r in st.session_state.requests:
                                if r['id'] == req['id']:
                                    r['status'] = 'Completed'
                            st.success("Request marked as completed")
                            st.rerun()
    else:
        st.info("No requests found matching your filters")

# NEW REQUEST PAGE
elif page == "New Request":
    st.header("➕ Create New FOI Request")
    
    with st.form("new_request_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            requester_name = st.text_input("Requester Name *", placeholder="Full name or organization")
            request_type = st.selectbox(
                "Request Type *",
                options=[
                    "Personal Health Information",
                    "General Records",
                    "Security and Incident Footage",
                    "Audit Logs",
                    "Legal/Insurance",
                    "Correction Request",
                    "Estate/Deceased Patient Access"
                ]
            )
            date_received = st.date_input("Date Received *", value=datetime.now())
        
        with col2:
            legislation_type = st.selectbox(
                "Legislation Type *",
                options=["PHIPA", "FIPPA", "MFIPPA"]
            )
            assigned_to = st.text_input("Assigned To", placeholder="Staff member name")
            third_party = st.checkbox("Third-party notification required")
        
        description = st.text_area(
            "Request Description *",
            placeholder="Provide detailed description of the information being requested...",
            height=150
        )
        
        submitted = st.form_submit_button("Create Request", use_container_width=True)
        
        if submitted:
            if requester_name and request_type and legislation_type and description:
                # Calculate values
                date_received_str = date_received.strftime('%Y-%m-%d')
                due_date = calculate_due_date(date_received_str, legislation_type)
                fee = calculate_fee(request_type, legislation_type)
                
                # Generate new ID
                new_id = f"FOI-2024-{str(len(st.session_state.requests) + 1).zfill(3)}"
                
                # Create new request
                new_request = {
                    'id': new_id,
                    'requester_name': requester_name,
                    'request_type': request_type,
                    'date_received': date_received_str,
                    'due_date': due_date,
                    'status': 'Pending Review',
                    'assigned_to': assigned_to if assigned_to else 'Unassigned',
                    'legislation_type': legislation_type,
                    'description': description,
                    'third_party_notification': third_party,
                    'fee_estimate': fee,
                    'extension_granted': False
                }
                
                st.session_state.requests.append(new_request)
                
                st.markdown("""
                <div class="success-box">
                    <h3>✅ Request Created Successfully!</h3>
                    <p><strong>Request ID:</strong> {}</p>
                    <p><strong>Due Date:</strong> {}</p>
                    <p><strong>Estimated Fee:</strong> ${}</p>
                </div>
                """.format(new_id, due_date, fee), unsafe_allow_html=True)
                
                st.balloons()
            else:
                st.error("Please fill in all required fields (*)")

# ANALYTICS PAGE
elif page == "Analytics":
    st.header("📈 Analytics & Reports")
    
    df = pd.DataFrame(st.session_state.requests)
    
    # Requests by Status
    st.subheader("Requests by Status")
    status_counts = df['status'].value_counts()
    st.bar_chart(status_counts)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Requests by Type
        st.subheader("Requests by Type")
        type_counts = df['request_type'].value_counts()
        st.write(type_counts)
    
    with col2:
        # Requests by Legislation
        st.subheader("Requests by Legislation")
        leg_counts = df['legislation_type'].value_counts()
        st.write(leg_counts)
    
    # Timeline Analysis
    st.subheader("Timeline Analysis")
    on_time = 0
    at_risk = 0
    overdue_count = 0
    
    for req in st.session_state.requests:
        days = get_days_remaining(req['due_date'])
        if req['status'] == 'Completed':
            on_time += 1
        elif days < 0:
            overdue_count += 1
        elif days <= 5:
            at_risk += 1
        else:
            on_time += 1
    
    timeline_col1, timeline_col2, timeline_col3 = st.columns(3)
    
    with timeline_col1:
        st.metric("On Time", on_time)
    with timeline_col2:
        st.metric("At Risk (≤5 days)", at_risk)
    with timeline_col3:
        st.metric("Overdue", overdue_count)
    
    # Export Data
    st.subheader("📥 Export Data")
    if st.button("Download All Requests as CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"foi_requests_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p><strong>FOI Request Management System</strong> | Developed for Healthcare Privacy Management</p>
    <p style="font-size: 0.875rem;">Supports PHIPA, FIPPA, and MFIPPA compliance requirements</p>
</div>
""", unsafe_allow_html=True)