import scrape_courses



# promo = scrape_courses.scrape_pepper(url)

# szkolenia_kursy = scrape_courses.scrape_pepper_szkolenia_kursy()
# udemy = scrape_courses.scrape_pepper_udemy()


urls = {'szkolenia i kursy': 'https://www.pepper.pl/grupa/szkolenia-i-kursy?page={}',
        'uslugi i subskrypcje': 'https://www.pepper.pl/grupa/uslugi-i-subskrypcje?page={}',
        'udemy.com': 'https://www.pepper.pl/promocje/udemy.com?page={}'}


szkolenia_kursy = scrape_courses.scrape_pepper(urls['szkolenia i kursy'])

uslugi_subskrypcje = scrape_courses.scrape_pepper(urls['uslugi i subskrypcje'])

udemy = scrape_courses.scrape_pepper(urls['udemy.com'])
