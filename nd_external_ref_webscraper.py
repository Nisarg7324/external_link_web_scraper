'''
#############################
# Name: Nisarg Kiritbhai Dave
# External Link Web Scraper
#############################
'''

import socket
import sys
import ssl

def establish_connection(host, protocol, request, connection):
	html_response = ""
	if(protocol == "http"):
		connection.connect((host, 80))
		connection.send(request.encode())
		html_response += connection.recv(8192).decode()
		connection.close()
	elif(protocol == "https"):
		context = ssl.create_default_context()
		secure_connection = context.wrap_socket(connection, server_hostname=host)
		secure_connection.connect((host, 443))
		secure_connection.send(request.encode())
		data = secure_connection.recv(8192).decode()
		html_response += data
		while(data != ""):
			data = secure_connection.recv(8192).decode()
			html_response += data
		connection.close()
	return html_response


# Input example: http://www.rit.edu/example/page.html
# All future examples are based on this above input example

# Extract protocol
# Example: http
protocol = sys.argv[1].split("://")[0]

# Extract URL
# Example: www.rit.edu/example/page.html
main_url = sys.argv[1].split("//")[1]

# Extract host
# Example: www.rit.edu
host = main_url.split("/")[0]

# Extract requested page
# Example: /example/page.html
requested_page = main_url[len(host):]
if(requested_page == ""):
	requested_page = "/"

# Create our own request
custom_request = "GET " + requested_page + " HTTP/1.1\r\n"
custom_request += "Accept-encoding: identity\r\n"
custom_request += "Host: " + host + "\r\n"
custom_request += "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/69.3.9\r\n"
custom_request += "Connection: close\r\n\r\n"

# Establish connection
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
html_response = establish_connection(host, protocol, custom_request, connection)

#print(html_response)

print() # Just here for better visibility

# Handling redirects
# If Location field mentioned in html_response, then we have to redirect to that location
if(("Location: http://" in html_response) or ("Location: https://" in html_response)):
	start = html_response.find("Location: ") + len("Location: ")
	end = html_response.find("\r", start)
	new_input = html_response[start:end]
	protocol = new_input.split("://")[0]
	main_url = new_input.split("//")[1]
	host = main_url.split("/")[0]
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	html_response = establish_connection(host, protocol, custom_request, connection)
	print("Your entered URI is being redirected to: " + new_input)
	print("Showing results for: " + new_input)
	print()

# Modify html_response to replace whitespaces with simple space
html_response_modified = html_response.replace("\n", " ")
html_response_modified = html_response.replace("\t", " ")
html_response_modified = html_response.replace("\r", " ")

# Split modified HTML response to parts separated by space
html_response_modified_parts = html_response_modified.split(" ")

# Extract external references/links
external_references = []
external_references_temp = []
for part in html_response_modified_parts:
	if("http" in part):
		possible_references = part.split("http")
		possible_references.pop(0)
		for sub_part in possible_references:
			i = 0
			temp_reference = ""
			while(i < len(sub_part)):
				if(sub_part[i] == '"' or sub_part[i] == "'"):
					break
				temp_reference += sub_part[i]
				i += 1
			temp_link = "http" + temp_reference
			external_references_temp.append(temp_link)
for links in external_references_temp:
	if((host not in links) and (("http://" in links) or ("https://" in links))):
		external_references.append(links)

# Print all external references
print("The following are all the external references present in " + sys.argv[1])
print()
count = 1
for link in external_references:
	print("Link " + str(count) + ": " + link)
	count += 1
print()
print("Total " + str(len(external_references)) + " external references found!")
