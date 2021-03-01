import scrape_courses
import udemy_cat_development

# /development -> only one category
API_URL = 'https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={}&page_size=16&subcategory=&instructional_' \
      'level=&lang=&price=&duration=&closed_captions=&category_id=288&source_page=category_page&locale=pl_PL' \
      '&currency=pln&navigation' \
      '_locale=en_US&skip_price=true&sos=pc&fl=cat'

ud = udemy_cat_development.scrape_udemy(API_URL)


# promo = scrape_courses.scrape_pepper(url)

# szkolenia_kursy = scrape_courses.scrape_pepper_szkolenia_kursy()
# udemy = scrape_courses.scrape_pepper_udemy()


# urls = {'szkolenia i kursy': 'https://www.pepper.pl/grupa/szkolenia-i-kursy?page={}',
#         'uslugi i subskrypcje': 'https://www.pepper.pl/grupa/uslugi-i-subskrypcje?page={}',
#         'udemy.com': 'https://www.pepper.pl/promocje/udemy.com?page={}'}

# szkolenia_kursy = scrape_courses.scrape_pepper(urls['szkolenia i kursy'])
#
# uslugi_subskrypcje = scrape_courses.scrape_pepper(urls['uslugi i subskrypcje'])
#
# udemy = scrape_courses.scrape_pepper(urls['udemy.com'])
