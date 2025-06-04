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
