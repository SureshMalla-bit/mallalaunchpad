# modules/analytics.py

import streamlit as st
import pandas as pd
import plotly.express as px

def admin_analytics(db):
    """Displays an admin dashboard with platform usage analytics."""
    st.title("👑 Admin Analytics Dashboard")
    st.markdown("Track platform usage and key performance metrics.")
    
    try:
        # Fetch all users from Firestore
        users_ref = db.collection("users").stream()
        users_list = []
        for user in users_ref:
            user_data = user.to_dict()
            user_data['uid'] = user.id
            users_list.append(user_data)
        
        if not users_list:
            st.info("No user data to display yet.")
            return
            
        df_users = pd.DataFrame(users_list)
        
        # --- Key Metrics ---
        total_users = len(df_users)
        
        # Note: 'last_active' and 'apps_tracked' would need to be implemented
        # For now, we'll use mock data for demonstration
        df_users['last_active'] = pd.to_datetime(df_users['joined']).dt.date
        df_users['apps_tracked'] = [len(list(db.collection('users').document(uid).collection('jobs').stream())) for uid in df_users['uid']]

        active_today = df_users[df_users["last_active"] == pd.to_datetime("today").date()].shape[0]
        total_applications = df_users["apps_tracked"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", f"{total_users} 👤")
        col2.metric("Active Today", f"{active_today} 🔥")
        col3.metric("Total Jobs Tracked", f"{total_applications} 📊")

        st.divider()

        # --- Charts ---
        st.subheader("User Engagement")
        
        # Bar chart for applications per user
        fig = px.bar(
            df_users,
            x='email',
            y='apps_tracked',
            title="Total Jobs Tracked per User",
            labels={'email': 'User Email', 'apps_tracked': 'Number of Jobs'},
            color_discrete_sequence=["#636AF2"]
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("User Data Table")
        st.dataframe(df_users)
        
    except Exception as e:
        st.error(f"Could not load analytics data: {e}")
