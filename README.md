# Exercise - From GitHub to FreshDesk

### Files included:
* Git_Fresh.py
* unit_tests.py
- - - 

## Git_Fresh.py
- - - 
```
def obtain_os_env_var(var_name):
```
- This is a function for getting the environmental variable from the Operating System.
- If you do not have one already, you may want to create a token in GitHub and save it as an environmetal variable in
 the settings of your pc from 'System properties'.
- You can also create a token in FreshDesk. Since the platform is paid, I cannot create an account and generate a token myself.
```
def get_authenticated_github_user(url, token):
```
- Function for extracting all the information about the user as a response with GET method: the ULR, the headers with Authorization token as requested from GitHub.
If the request succeeded, we return this info.
  
```
def get_console_arguments():
```
- Getting all the arguments that have been given to the console when starting
the python program. I am using argparse library to add the arguments and then parse them
  into them into a variable called "args". Then we just extract and return the username and the freshdesk subdomain.
  
- We can use either of these syntaxes ('--username', '-u') and ('--fdesk-sd', '-f') to run the program. I have added also
"--help" to see how to write the correct syntax.
  
```
def create_freshdesk_user_info(github_user_info):
```
- This is a function for creating the dictionary object in a FreshDesk style
with credentials that I find compatible and sufficient (name, id, email, twitter_id). 
  
- With github_user_info['login'], I am taking the name of our github user.
Same goes for the extraction of the id, email and twitter_id.
  
```
def check_if_freshdesk_user_exists(freshdesk_subdomain, freshdesk_token, freshdesk_user_info):
```
- Checking whether a user exists in freshdesk.
- We are requesting the url with the freshdesk_subdomain that we have extracted earlier.
The response is done with url, the params (the user name) and the authorization, which is 
  different from the one of GitHub and uses a different syntax with the freshdesk_token and 
  "X" written at the end, as described in the documentation.
- The response would be a list of users:
    * If the list is empty, that means there is no such user and it creates one with the given credentials
    * If the list has one item, that means that there exists such a user and we have to update him with the given id
    * If the list has more than one, it prints a message to narrow down the research
    * If the status code is not 200, that means there is somewhere a mistake in the API
    
- If the user doesn't exist, it would return a negative number since all IDs are positive

```
def create_freshdesk_user(freshdesk_subdomain, freshdesk_token, freshdesk_user_info):
```
- Creates a user
- The request consists of the specific format: url with the specific subdomain, headers, user info and authorization as described above.
- If the status code is 201, that means user is created successfully

```
def update_freshdesk_user(freshdesk_subdomain, freshdesk_token, freshdesk_user_info, id):
```
- Same thing as in creating the user, but the only difference here is that we add the ID of the user 
in the url in order to update it.
- If the status code is 200, the request has been successful

```
def main():
```
The main function is responsible for running the whole code:
- It is taking the arguments from the console
- Obtaining the environmental tokens for GitHub and FreshDesk
- If there is no such token, we stop. Otherwise, we get the info for the user from GitHub + its username
- If the username we have extracted is different from the one we have as an argument, then we close.
- Then we create the user info for FreshDesk.
- We check whether the user exists: if so -> update, otherwise -> create.


### Note:
Since FreshDesk is paid, I could not test the whole process.

### How to run:
You can run it by opening the python terminal and writing:
* python Git_Fresh.py --username USERNAME --fdesk-sd SUBDOMAIN

## unit_tests.py
- - -
I have created 4 tests to check whether the functionality of several of my functions work as supposed.

```
def test_frehdesk_user_info_email(self):
```
- I have hardcoded a git user and check whether the email is different from null. Since it is null
 it retrieves 'N/A'.
  
```
def test_frehdesk_user_info_twitter_username(self):
```

- Hardcoding a git user and checking whether the twitter_id is different from null. Since it is not, 
it retrieves 'N/A'.
  
```
def test_not_authenticated_github_user(self):
```
- Hardcoding a random token and checking whether it would give us a info for a user. Since it is wrong
 it would give us 'None'.
  
```
def test_freshdesk_user_existance(self):
```
- Hardcoding freshdesk token, subdomain and user and checking whether it exists or not. Since not, it retrieves -3.

### How to run:

You can run it by opening the python terminal and writing:
- python unit_tests.py

... and you can see the tests passing.
