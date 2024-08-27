Version used:
1. Python 3.12.3 == https://www.python.org/downloads/release/python-3123/
2. Selenium 4.19.0 == "pip install selenium == 4.19.0" on terminal

a. Terminal Ver. = Independant Ver., Use hardcoded input and showcase result progress in Terminal

b. DB Ver. = Independant Ver., Use input from DB (Ask DB from author or associate) and showcase result progress in Terminal

c. API Ver. = Use API to call,  Use input from DB (Ask DB from author or associate) and showcase result progress in Terminal. Return error value.

*NSEE (No Such Element Exception) type of Error will showcase slow performance, but this is due to the result of Automation looking for correct value but couldn't found a similar value, wait untill the automation shut itself down before assesing

*KeyError type of Error is due to lack of value provided by DB, as such it has 2 type of interpretation, DB provided face mishaps or it is intentionally blank
