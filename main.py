import udemy_cat_development
import teachinguide_api

# /development -> only one category
UDEMY_API_URL = 'https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={}&page_size=60&subcategory=' \
                '&instructional_level=&lang=&price=&duration=&closed_captions=&sort=newest&category_id=288&' \
                'source_page=category_page&locale=pl_PL&currency=pln&navigation_locale=en_US&skip_price=true' \
                '&sos=pc&fl=cat'

x = 0

while x != 10:
    ud = udemy_cat_development.scrape_udemy(UDEMY_API_URL)
    x += 1

# TEACHINGUIDE_API_URL = "https://teachinguide.azure-api.net/course-coupon?sortCol=created_d&sortDir=DESC&length=100" \
#                        "&page={}&inkw=&discount=100&language=English&ignore=true&"
#
# teachgd = teachinguide_api.scrape_teachinguide(TEACHINGUIDE_API_URL)


















# aa = udemy_cat_development.do_smth()

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
