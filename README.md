A dirty hack for generating some phone books for a hobby group SIP server from a Google sheet.

Some Cisco phones may need this in .htaccess:
`Addtype text/xml .xml`

This script produces following XML phonebooks:

| directory_79x0.xml (and directory_79x0_[1-n].xml) | For Cisco 7940 and 7960 and similar |
| directory.xml | For many other Cisco versions (eg. 79x5) |
| phonebook.xml | For Grandstream devices, refer to this in the phone config with the path that this file will be in. |

