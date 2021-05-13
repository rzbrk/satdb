#!/bin/bash

# This script downloads a session cookie from space-track.org that is valid
# for ~ 2 hours.

# Function to print message with time tag
tt_print () {
    message=${1}
    tt=$(date --utc "+%Y-%m-%d %H:%M:%S")
    echo "${tt}: ${message}"
}

# Parameter --verbose is used to set to verbose mode
if [[ "${@,,}" == *"--verbose"* ]]; then
    verbose="true"
else
    verbose="false"
fi

if [ "${verbose}" == "true" ]; then
    tt_print "Execute ${0} . . ."
    tt_print "  Flag --verbose set?: ${verbose}"
fi

# Source the file holding the space-track.org credentials. Search for the
# credential file in the order defined in the following list:
#credfile_list=("./space-track.cred" "$HOME/.space-track.cred" "/etc/space-track.cred")
credfile_list=("./satdb.yaml" "$HOME/.satdb.yaml" "/etc/satdb.yaml")

if [ "${verbose}" == "true" ]; then
    tt_print "Searching for file with space-track.org credentials"
fi

credfile=""
for file in "${credfile_list[@]}"
do
    if [ -f "${file}" ]; then
        credfile=${file}
        break
    fi
done

# If no credential file is found, exiting
if [ "${credfile}" == "" ]; then
    tt_print "No credentials file found. Exiting."
    exit 1
fi

# Initialize variables that must be defined in the credentials file
user=""
password=""

if [ "${verbose}" == "true" ]; then
    tt_print "Using credentials file: ${credfile}"
fi

# Now, actually source the file
#source ${credfile}
user=$(niet spacetrack.user ${credfile})
password=$(niet spacetrack.password ${credfile})

# Check if variables "user" and password are defined (not empty)"
if [ "${user}" == "" ]; then
    tt_print "User not defined in ${credfile}. Exiting."
    exit 1
fi
if [ "${password}" == "" ]; then
    tt_print "Password not defined in ${credfile}. Exiting."
    exit 1
fi

# Download cookie file
if [ "${verbose}" == "true" ]; then
    tt_print "Downloading cookie file"
fi
cookie=$(mktemp -t "stcookie.XXXXXXXXXX")
loginurl="https://www.space-track.org/ajaxauth/login"
curl -s -c ${cookie} -b ${cookie} ${loginurl} -d "identity=${user}&password=${password}" > /dev/null

if [ "${verbose}" == "true" ]; then
    tt_print "Downloaded cookie file: ${cookie}"
fi

# Get the time of validity from the cookie
valid_unix=$(cat ${cookie} | grep "#HttpOnly_" | awk '{print $5}')
valid=$(date -d @${valid_unix})
if [ "${verbose}" == "true" ]; then
    tt_print "Cookie valid until: ${valid}"
fi

# Output the name of the cookie file
echo "Cookie: ${cookie}"

if [ "${verbose}" == "true" ]; then
    tt_print "Finished."
fi

