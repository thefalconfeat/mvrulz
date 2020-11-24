import crawl as crawler
from datetime import date
from bs4 import BeautifulSoup
import requests
from urllib.request import urlparse, urljoin
import subprocess
import sys

t_movie_link = "https://4movierulz.pw/category/telugu-movie/"
big_start = date(2020, 9, 6)
t_download_output_file = 't-download-output-file.txt'
search_string = 'vintha'
bigg_boss = 'bigg-boss'
size_limit = 2000

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
	print('\t ', split_link[len(split_link)-2])
	
	
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
	search_string = sys.argv[1]
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
