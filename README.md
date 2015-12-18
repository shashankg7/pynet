# pynet
Web Data Extraction from Flat and Nested Records. This is an attempt to build an automated data extraction system which extracted records following similar pattern from a web page without writing any code. Example of such web pages are E-commerce web pages with records of products, web pages with user reviews of product or any page which has data records following same pattern.

# System Design
It follows the research paper titled "NET- A system for Extracting Web Data from Flat and Nested Data Records". Reference of the paper is:
Bing Liu and Yanhong Zhai. "NET - A System for Extracting Web Data from Flat and Nested Data Records." Proceedings of 6th International Conference on Web Information Systems Engineering (WISE-05), 2005

# Requirements
1. lxml 
2. StringIO
3. requests

# Running Command
From the folder net run the following command
python net.py <URL> web / Standard mode, pass URL 
python net.py </path/local/htmlpage.html> local /If you have html page saved on local disk

# Future Work
I have tried to follow the paper I mentioned for designing the system, but unfortunately it doesn't works very well. If you run the program you will get some output related to some text from the program but it is not structured properly. This is version 1.0 of the system. I will try to update it incrementally to work properly. 
In case you are interested in this project do send me a pull request. Thanks !!

