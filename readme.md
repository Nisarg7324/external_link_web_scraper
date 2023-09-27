# **External Link Web Scraper**

## **Description**

* The Python script will output all the external links mentioned in the HTML document of the URI given by the user.
* I have used *raw requests* for establishing connection. However, redirects (for example, from *http://www.rit.edu* to *https://www.rit.edu*) are handled.
* Hence, if your input URI uses incorrect protocol (HTTP instead of the correct HTTPS), then the connection will be automatically redirected to the correct link suggested by the HTML document sent in response, and the output shown will be of the new redirected link.
* This means that, if you enter your URI as *http://www.rit.edu*, it will automatically show you the output of *https://www.rit.edu*.

NOTE: This script does not require any additional libraries. All the libraries used in this script are natively available within Python3.

## **How to Run?**

The following command is the structure for running the Python script:

```raw
python3 nd_external_ref_webscraper.py <your_link_here>
```

The following are some examples:

```raw
python3 nd_external_ref_webscraper.py http://www.rit.edu
```

```raw
python3 nd_external_ref_webscraper.py https://www.rit.edu
```

```raw
python3 nd_external_ref_webscraper.py https://www.amazon.com
```

## **Assumptions**

There are a few assumptions I made which are listed below:

* If the incorrect protocol is entered by the user, the resultant HTML document contains the correct link in its header's "Location" field.
* The input URI entered by the user is considered the main domain and any links that do not contain the main domain are considered external links. For example, if the user inputs *https://www.rit.edu*, then *https://csec.rit.edu* will be considered an external reference.
* If there are multiple external links of the same domanin present but with different requested page, all such links would be considered unique entries and each of them will be counted. For example, *https://csec.rit.edu/page1* and *https://csec.rit.edu/page2* both are external links with same domain but different requested page. Hence, these links will be considered unique. Thus, there are 2 unique external links in this example.
* I have parsed the whole HTML document sent as response to my raw request. Hence, it is possible that some links might be mentioned in the comment of the code or in any other way that makes it inactive. Such links will also be counted as external links.