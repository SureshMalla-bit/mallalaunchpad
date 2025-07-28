import streamlit as st
import pandas as pd
import plotly.express as px

def admin_analytics(db):
    """Displays an admin dashboard with platform usage analytics."""
    st.title("👑 Admin Analytics Dashboard")
    st.markdown("Track platform usage and key performance metrics.")

    try:
        users_ref = db.collection("users").stream()
        users_list = []

        for user in users_ref:
            user_data = user.to_dict()
            user_data['uid'] = user.id
            users_list.append(user_data)

        if not users_list:
            st.info("No user data found.")
            return

        df_users = pd.DataFrame(users_list)

        # Fallback for 'joined' missing
        if 'joined' not in df_users.columns:
            df_users['joined'] = pd.to_datetime("today")

        df_users['last_active'] = pd.to_datetime(df_users['joined']).dt.date
        df_users['apps_tracked'] = [
            len(list(db.collection('users').document(uid).collection('jobs').stream()))
            for uid in df_users['uid']
        ]

        active_today = df_users[df_users["last_active"] == pd.to_datetime("today").date()].shape[0]
        total_users = len(df_users)
        total_applications = df_users["apps_tracked"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", f"{total_users} 👥")
        col2.metric("Active Today", f"{active_today} 🔥")
        col3.metric("Total Jobs Tracked", f"{total_applications} 📄")

        st.divider()
        st.subheader("📊 User Engagement Overview")

        fig = px.bar(
            df_users,
            x="uid",
            y="apps_tracked",
            labels={"uid": "User ID", "apps_tracked": "Tracked Jobs"},
            title="📈 Jobs Tracked Per User",
            color_discrete_sequence=["#636AF2"]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🧾 Raw User Data")
        st.dataframe(df_users)

    except Exception as e:
        st.error(f"⚠️ Could not load analytics: {e}")
