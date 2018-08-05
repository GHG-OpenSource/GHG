# GHG
Provides Security to GitHub Organization 


Requirements:

Python 2.7
 And Update the libraries


PROVIDE THE CONFIGURATION PROPERTIES IN THE "GHG" FILE

[GitHub]:
GitHub organization name
GitHub owner credentials

[AWS-SES]:
Access key id
Access secret key


Run the modules individually or schedule them:

mfacheck_demo.py         ---     It removes the users without MFA from your GitHub organization and notifies them if you                                       provide SES properties in GHG file

PrivateRepoCheck_demo.py  --     It checks for any public repos in the organization and makes them provate. It has the                                         notification capability too.

OutsideCollaborts_demo.py --     It removes the non members/outside collaborators of the organization.

awskeys_demo.py           --     This module helps us to find out the URLs of the files that contain AWS keys.Prone to false                                    positives (finetune it according to the organization)

Please look at each script and update the email addresses.
Complete the GHG config file with GitHub credentials and AWS SES credentials

For AWS key credential scanning:
Search string is fixed as “AWS access key” to find out only access keys. 
You can add any other search string to get files that contain the string. :)


