import utils
website_link = ""
search_keyword = "" # this keyword is used to download images from the web


#result = utils.image_downloader(search_keyword, limit =10)
result = "success"
if result == "success":
    print("Image download successful!")
    #web scraping
    scraped_content = utils.scrape_clean_content(website_link)
    print(scraped_content)

    #calling gemini to get the content in malayalam
    text_for_audio =  utils.get_content(scraped_content)

    #generating audio
    print(utils.create_audio(text_for_audio))
else:
    print("Image download failed.")

