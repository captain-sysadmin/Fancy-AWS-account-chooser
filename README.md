# What is this?
This is a crappy AWS SSO account selector that allows you to quick choose which account to retrieve credentials for. 

It assumes that you've configured your aws cli with `aws sso configure` and that you have a number of `[profile your_account]` with the key `sso_session` in there as well.


# config
if you want it to update your default aws profile you will need to add:
```
source ~/.aws_includes
alias ap="source ~/.aws_includes && cat ~/.aws_includes"
```
to your shell so that you don't need to reload your shell all the time. 

# install
`pip install -r requirements.txt`

# screen shot
<img width="613" alt="Screenshot 2025-06-04 at 11 25 29" src="https://github.com/user-attachments/assets/3a2954f8-b3c6-4966-9fcf-f6eb785478e0" />

# usage
Run `python3 selector.py`
* use the mouse to select which account you want
* hit enter to select (or click it with your mouse)
* <tab> to select the "get AWS credentials" button
* if it works, you should get a new browser window pop up, and the programme will quit. 
