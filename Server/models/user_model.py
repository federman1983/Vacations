import sqlite3

class User:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect('vacations_db.db')

    @staticmethod
    def create_table():
        with User.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role_id INTEGER NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
                )
            '''
            cursor.execute(sql)
            cursor.close()

    @staticmethod
    def create_user(first_name, last_name, email, password, role_id):
        """
        Create a new user in the database
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address
            password (str): User's hashed password
            role_id (int): User's role ID
            
        Returns:
            int: The ID of the newly created user, or None if creation failed
        """
        try:
            with User.get_db_connection() as connection:
                cursor = connection.cursor()
                sql = '''
                    INSERT INTO users (first_name, last_name, email, password, role_id)
                    VALUES (?, ?, ?, ?, ?)
                '''
                cursor.execute(sql, (first_name, last_name, email, password, role_id))
                connection.commit()
                user_id = cursor.lastrowid
                cursor.close()
                return user_id
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email address
        
        Args:
            email (str): User's email address
            
        Returns:
            dict: User data or None if not found
        """
        try:
            with User.get_db_connection() as connection:
                cursor = connection.cursor()
                sql = 'SELECT * FROM users WHERE email = ?'
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                cursor.close()
                
                if user:
                    return {
                        'user_id': user[0],
                        'first_name': user[1],
                        'last_name': user[2],
                        'email': user[3],
                        'password': user[4],
                        'role_id': user[5]
                    }
                return None
        except sqlite3.Error as e:
            print(f"Error getting user by email: {e}")
            return None

    @staticmethod
    def get_all_users():
        """
        Get all users from database
        
        Returns:
            list: List of all users
        """
        try:
            with User.get_db_connection() as connection:
                cursor = connection.cursor()
                sql = 'SELECT * FROM users'
                cursor.execute(sql)
                users = cursor.fetchall()
                cursor.close()
                
                return [
                    {
                        'user_id': user[0],
                        'first_name': user[1],
                        'last_name': user[2],
                        'email': user[3],
                        'password': user[4],
                        'role_id': user[5]
                    }
                    for user in users
                ]
        except sqlite3.Error as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User's ID
            
        Returns:
            dict: User data or None if not found
        """
        try:
            with User.get_db_connection() as connection:
                cursor = connection.cursor()
                sql = 'SELECT * FROM users WHERE user_id = ?'
                cursor.execute(sql, (user_id,))
                user = cursor.fetchone()
                cursor.close()
                
                if user:
                    return {
                        'user_id': user[0],
                        'first_name': user[1],
                        'last_name': user[2],
                        'email': user[3],
                        'password': user[4],
                        'role_id': user[5]
                    }
                return None
        except sqlite3.Error as e:
            print(f"Error getting user by ID: {e}")
            return None

    @staticmethod
    def update_user(user_id, first_name=None, last_name=None, email=None, role_id=None):
        """
        Update user information
        
        Args:
            user_id (int): User's ID
            first_name (str): New first name
            last_name (str): New last name
            email (str): New email
            role_id (int): New role ID
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            with User.get_db_connection() as connection:
                cursor = connection.cursor()
                
                # Build dynamic update query
                update_fields = []
                values = []
                
                if first_name is not None:
                    update_fields.append('first_name = ?')
                    values.append(first_name)
                if last_name is not None:
                    update_fields.append('last_name = ?')
                    values.append(last_name)
                if email is not None:
                    update_fields.append('email = ?')
                    values.append(email)
                if role_id is not None:
                    update_fields.append('role_id = ?')
                    values.append(role_id)
                
                if not update_fields:
                    return False
                
                values.append(user_id)
                sql = f'UPDATE users SET {", ".join(update_fields)} WHERE user_id = ?'
                
                cursor.execute(sql, values)
                connection.commit()
                cursor.close()
                return True
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def update_user_password(user_id, new_password):
        """
        Update user password
        
        Args:
            user_id (int): User's ID
            new_password (str): New hashed password
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            with User.get_db_connection() as connection:
                cursor = connection.cursor()
                sql = 'UPDATE users SET password = ? WHERE user_id = ?'
                cursor.execute(sql, (new_password, user_id))
                connection.commit()
                cursor.close()
                return True
        except sqlite3.Error as e:
            print(f"Error updating password: {e}")
            return False

    @staticmethod
    def delete_user(user_id):
        """
        Delete user by ID
        
        Args:
            user_id (int): User's ID
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            with User.get_db_connection() as connection:
                cursor = connection.cursor()
                sql = 'DELETE FROM users WHERE user_id = ?'
                cursor.execute(sql, (user_id,))
                connection.commit()
                cursor.close()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False