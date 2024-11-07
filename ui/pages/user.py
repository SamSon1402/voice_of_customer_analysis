import streamlit as st


def _render_users_overview(self):
        """Render users overview section"""
        stats = self.user_service.get_user_statistics()

        # User metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", stats['total_users'])
        with col2:
            st.metric("Active Users", stats['active_users'])
        with col3:
            st.metric("New Users (30d)", stats['new_users'])
        with col4:
            st.metric("Admin Users", stats['admin_users'])

        # User growth chart
        growth_data = self.user_service.get_user_growth_data()
        fig = px.line(
            growth_data,
            x='date',
            y='users',
            title="User Growth Over Time"
        )
        st.plotly_chart(fig)

        # Role distribution
        role_data = self.user_service.get_role_distribution()
        fig = px.pie(
            role_data,
            values='count',
            names='role',
            title="Users by Role"
        )
        st.plotly_chart(fig)

    def _render_user_management(self):
        """Render user management section"""
        st.subheader("User Management")

        # Create new user button
        if st.button("Create New User"):
            self._show_create_user_form()

        # User search and filters
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("Search Users")
        with col2:
            role_filter = st.multiselect(
                "Filter by Role",
                ["ADMIN", "ANALYST", "USER"]
            )

        # Get users
        users = self.user_service.get_users(
            search=search,
            roles=role_filter
        )

        # Display users
        if users:
            for user in users:
                with st.expander(f"{user['email']} - {user['role']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Username:** {user['username']}")
                        st.write(f"**Full Name:** {user.get('full_name', 'N/A')}")
                        st.write(f"**Status:** {user['status']}")
                        st.write(f"**Last Login:** {user.get('last_login', 'Never')}")
                    with col2:
                        if st.button("Edit", key=f"edit_{user['id']}"):
                            self._show_edit_user_form(user)
                        if st.button("Delete", key=f"delete_{user['id']}"):
                            if st.confirm(f"Delete user {user['email']}?"):
                                self.user_service.delete_user(user['id'])
                                st.success("User deleted successfully")
                                st.experimental_rerun()

    def _show_create_user_form(self):
        """Show create user form"""
        with st.form("create_user"):
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            full_name = st.text_input("Full Name")
            role = st.selectbox(
                "Role",
                ["USER", "ANALYST", "ADMIN"]
            )
            
            if st.form_submit_button("Create User"):
                try:
                    self.user_service.create_user({
                        "email": email,
                        "username": username,
                        "password": password,
                        "full_name": full_name,
                        "role": role
                    })
                    st.success("User created successfully")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error creating user: {str(e)}")

    def _show_edit_user_form(self, user):
        """Show edit user form"""
        with st.form("edit_user"):
            email = st.text_input("Email", value=user['email'])
            full_name = st.text_input("Full Name", value=user.get('full_name', ''))
            role = st.selectbox(
                "Role",
                ["USER", "ANALYST", "ADMIN"],
                index=["USER", "ANALYST", "ADMIN"].index(user['role'])
            )
            status = st.selectbox(
                "Status",
                ["ACTIVE", "INACTIVE", "SUSPENDED"],
                index=["ACTIVE", "INACTIVE", "SUSPENDED"].index(user['status'])
            )
            
            if st.form_submit_button("Update User"):
                try:
                    self.user_service.update_user(
                        user['id'],
                        {
                            "email": email,
                            "full_name": full_name,
                            "role": role,
                            "status": status
                        }
                    )
                    st.success("User updated successfully")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error updating user: {str(e)}")

    def _render_roles_permissions(self):
        """Render roles and permissions section"""
        st.subheader("Roles & Permissions")

        # Create new role
        if st.button("Create New Role"):
            self._show_create_role_form()

        # Display roles
        roles = self.user_service.get_roles()
        for role in roles:
            with st.expander(role['name']):
                st.write("**Permissions:**")
                for perm in role['permissions']:
                    st.write(f"- {perm}")
                    
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_role_{role['name']}"):
                        self._show_edit_role_form(role)
                with col2:
                    if st.button("Delete", key=f"delete_role_{role['name']}"):
                        if st.confirm(f"Delete role {role['name']}?"):
                            self.user_service.delete_role(role['name'])
                            st.success("Role deleted successfully")
                            st.experimental_rerun()

    def _render_activity_logs(self):
        """Render user activity logs"""
        st.subheader("User Activity Logs")

        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                datetime.now() - timedelta(days=7)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                datetime.now()
            )

        # Get activity logs
        logs = self.user_service.get_activity_logs(start_date, end_date)

        if logs:
            # Activity visualization
            activity_df = pd.DataFrame(logs)
            fig = px.histogram(
                activity_df,
                x='timestamp',
                color='action',
                title="User Activity Distribution"
            )
            st.plotly_chart(fig)

            # Detailed logs table
            st.dataframe(
                activity_df[['timestamp', 'user', 'action', 'details']],
                hide_index=True
            )