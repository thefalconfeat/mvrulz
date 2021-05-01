import crawl as crawler
from datetime import date
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse, urljoin
import subprocess
import sys

search_db = {
	"telugu": "https://4movierulz.pe/category/telugu-movie/",
	"tamil": "",
	"hollywood": "https://4movierulz.pe/category/hollywood-movie-2020/",
	"search": "https://4movierulz.pe/?s=",
	"main": "https://4movierulz.pe/"
}

dummy_links = [
	"download-movierulz-app",
	"dvdrip",
	"tamil-movie",
	"bollywood-movie-2021",
	"bollywood-movie-2020",
	"malayalam-movie-online",
	"hindi-dubbed-movie",
	"bengali-movie",
	"bollywood-movie-2019",
	"adult-18",
	"bollywood-movie-2018",
	"telugu-movie",
	"telugu-dubbed-movie-2",
	"requested-movies",
	"featured",
	"hollywood-movie-2018",
	"bollywood-movie-free",
	  "tamil-movies-2019",
	  "punjabi-movie",
	  "tamil-movies-2021",
	  "movies-by-genres-and-years",
	  "contact-us",
	  "hollywood-movie-2020",
	  "malayalam-movie-2020",
	  "telugu-movies-2021",
	  "malayalam-movie-2019",
	  "hollywood-movie-2019",
	  "hollywood-movie-2020",
	  "others-movies",
	  "malayalam-movie-2021",
	  "tamil-movies-2020",
	  "latest-songs",
	  "multi-audio-dubbed-movies",
	  "tamil-dubbed-movie-2",
	  "telugu-movie",
	  "telugu-movies-2020",
	  "malayalam-movie",
	  "telugu-movies-2019",
	  "tamil-movie-free",
	  "adult-movie",
	  "hollywood-movie-2017"
	
]
t_movie_link = "https://4movierulz.pw/category/telugu-movie/"
big_start = date(2020, 9, 6)
t_download_output_file = 't-download-output-file.txt'
search_string = 'vintha'
bigg_boss = 'bigg-boss'
size_limit = 3000

def is_magnet(url):
	"""
	Checks whether `url` is a valid torrent link or not.
	"""
	# print("url is: ", url)
	return url.startswith("magnet")

def convert_to_mb(size):
	print("input is :", size)
	size_quantity = float(size.split()[0])
	if 'gb' in size:
		size_quantity = size_quantity*1024
		print("update size is: ", size_quantity)
	if size_quantity > size_limit:
		size_quantity = 0
	return size_quantity

def find_torrent_links(url):
	print("Now finding the torrent links in the link:", url)
	soup = BeautifulSoup(requests.get(url).content, "html.parser")
	torrent_links = dict()
	for a_tag in soup.findAll("a"):
		href = a_tag.attrs.get("href")
		if href == "" or href is None:
			# href empty tag
			continue
		# parsed_href = urlparse(href)
		# # remove URL GET parameters, URL fragments, etc.
		# href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
		if not is_magnet(href):
			# not a valid URL
			continue
		if href in torrent_links:
			# already in the set
			continue
		print("Html for tag :", convert_to_mb(a_tag.contents[2].string))

		torrent_links[convert_to_mb(a_tag.contents[2].string)] = href
	return torrent_links

def big_boss_today():
	print("this is today's big boss torrent link")
	urls = crawler.get_all_website_links(t_movie_link)
	today = date.today()
	no_of_days = today - big_start
	print("today is:", no_of_days.days)
	today_link = ''
	print(" urls are :", urls)
	for link in urls:
		print(" link is :", link)
		if (bigg_boss in link) and (str(no_of_days.days) in link):
			print("Found the link:", link)
			today_link = link
	return today_link

def print_title(link):
	split_link = link.split('/')
	l_link = split_link[len(split_link)-2]
	if l_link not in dummy_links:
		print('\t ', l_link)
	
	
def get_title_link(title):
	print("this is today's torrent link for ", title)
	urls = crawler.get_all_website_links(t_movie_link)
	title_link = ''
	#print(" urls are :", urls)
	for link in urls:
		print_title(link)
		if (title in link):
			print("Found the link:", link)
			title_link = link
	return title_link

def list_link_titles():
	print("Here are the titles available for you to download")
	urls = crawler.get_all_website_links(t_movie_link)
	for link in urls:
		print_title(link)

def pick_torrent_link_by_size(torrent_links):
	print("\nNow picking the appropriate size torrent file")
	biggest_file_link = torrent_links[max(list(torrent_links))]
	return biggest_file_link

def download_torrent(torrent_link):
	print("\nNow downloading the torrent from: ", torrent_link)
	command = ['transmission-cli', '-D', '-u', '5', '-w', '/home/hari/Downloads/media/bigg-boss', torrent_link]
	print("command: ", command)
	# command = ['pwd']
	output_file = open(t_download_output_file, 'w+')
	p = subprocess.Popen(command,
		universal_newlines=True, stdin=output_file, stdout=output_file)
	output, error = p.communicate()

	print("Return code is: ", output, error)

if __name__ == "__main__":
	print("Running mvrulz with arguments: ", sys.argv)
	db = sys.argv[1]
	t_movie_link = search_db[db]
	search_string = sys.argv[2]
	if "list"==search_string:
		list_link_titles()
	if db=="search":
		t_movie_link=t_movie_link+search_string.replace('-', '+')
	print("********\n\nsearch string and movie links", search_string, t_movie_link)	
	if bigg_boss in search_string:
		today_link = big_boss_today()
	else:
		today_link = get_title_link(search_string)
	print("Today's link is: ", today_link)
	if today_link != "":
		torrent_links = find_torrent_links(today_link)
		print("Torrent links:", torrent_links)
		torrent_final_link = pick_torrent_link_by_size(torrent_links)
		print("\n\n\nFinal torrent link is: ", torrent_final_link)
		download_torrent(torrent_final_link)
	else:
		print("Link for today's bigg-boss show is not available")
