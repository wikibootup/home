###### All apps
#### users
### password
users_pwd_at_least_6 = "user password length should be at least 6"
users_pwd_at_most_255 = "user password max length is 255"
users_pwd_no_numeric_char = "user password must contain numeric character"
users_pwd_no_alphabet_char = "user password must contain alphabet character"
users_pwd_no_special_char = "user password must contain special character"

### username
users_name_must_be_set = "username must be set"
users_name_at_most_30 = "user name length is limited to 30"
users_invalid_name = "user name cannot contain special characters" + \
                    "except for under bar_ , hyphen -"

### update user
users_update_without_any_required_fields = \
    "possible update field : username, email"

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
    "The two passwords are different. Please check password" 

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
boards_name_must_be_set = "board name must be set"
boards_name_at_most_30 = "board name is limited to 30"

### createpost
### create post
boards_post_subject_must_be_set = "subject must be set"
boards_post_subject_at_most_255 = "subject is limited to 255"
boards_post_content_must_be_set = "content must be set"
boards_post_content_at_most_255 = "content is limited to 255"

### create board posts
boards_board_arg_error = \
    "board argument must be Board object"
boards_post_arg_error = \
    "post argument must be Post object"


