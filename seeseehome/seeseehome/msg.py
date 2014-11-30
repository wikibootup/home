###### All apps
#### users
### user permission level
perm_anonymous = 0
perm_user = 1
perm_member = 2
perm_coremember = 4
perm_graduate = 8
perm_president = 16
perm_all = 31

### edit password
users_change_pwd_error = "ERROR : Change Password"
users_change_pwd_success = "SUCCESS : Change Password"
users_change_pwd_success_info = "Password was changed successfully.\n" + \
    "Please Log in again with your new password"
users_pwd_not_correct = "Password you entered is incorrect."


### password
users_pwd_at_least_6 = "User password length should be at least 6"
users_pwd_at_most_255 = "User password max length is 255"
users_pwd_no_numeric_char = "User password must contain numeric character"
users_pwd_no_alphabet_char = "User password must contain alphabet character"
users_pwd_no_special_char = "User password must contain special character"

### username
users_name_must_be_set = "User name must be set"
users_name_at_most_30 = "User name length is limited to 30"
users_invalid_name = "User name cannot contain special characters" + \
                    "except for under bar_ , hyphen -"

### update user
users_update_without_any_required_fields = \
    "Possible update field : username, email"
sers_update_is_admin_must_be_bool_type = \
    "The type of is_admin argument is must be bool"

### userperm
users_userperm_at_least_1 = "User permission sholud be at least 1"
users_userperm_at_most_31 = "User permission should be at most 31"

### signup
users_signup_error = "ERROR : Sign Up"
users_signup_success = "SUCCESS : Sign Up"
users_signup_success_info = "You can login now"
users_exist_email = "The user email already exist"
users_invalid_email = \
    "Invalid Email.\n" + \
    "It must have user part and domain part between '@'\n" + \
    "Or It might contain invalid special character"   
users_exist_name = "The user name already exist"
users_invalid_pwd = \
    "Invalid password.\n" + \
    "password length is in range 6 ~ 255\n" + \
    "And it should contain numeric character, alphabet character," + \
    "and special character"
users_confirm_pwd_error = \
    "Password you entered is different with password confirmation.\n" + \
    "Please check password" 

### login
users_login_error = "ERROR : Login"
users_login_success = "SUCCESS : Login"
users_non_exist_email = "The email does not exist. Please check Email"
users_login_success_info = "Successfully Login"
users_deactivated = "Deactivated User"
users_invalid = "Invalid email or password"
users_invalid_password = "Invalid user password"

## logout
users_logout_error = "ERROR : Logout"
users_logout_success = "SUCCESS : Logout"
users_logout_error_info = \
    "Logout failed. It seems you accessd the URL without Logged in"
users_logout_success_info = "Successfully Logout"


#### board
### create board
boards_max_number_of_boards = "Max number of boards : " + "10"
boards_name_must_be_set = "Board name must be set"
boards_name_at_most_30 = "Board name is limited to 30"

### get board
boards_board_arg_does_not_exist = "This board argument does not exist"

### createpost
### create post
boards_post_subject_must_be_set = "Subject must be set"
boards_post_subject_at_most_255 = "Subject is limited to 255"
boards_post_content_at_most_65535 = "Content is limited to 63335"

### create board posts
boards_board_arg_error = \
    "Board argument must be Board object"
boards_post_arg_error = \
    "Post argument must be Post object"

### write view
boards_write_error = "ERROR : Write Error"
boards_write_success = "SUCCESS : Write Success"
boards_write_success_info = "You posted successfully"
baords_anonymous_user_access = "Only login user must write a text"
boards_access_perm = "You don't have the permission to access this board"
boards_writer_perm_error = "You cannot write in this board ( pemission )"
