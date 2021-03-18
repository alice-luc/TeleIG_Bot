"""
likes
"""
from IgSide.Server.methods import *
from volume_data.insta_log.logger import logger


class LikeBot:
    """
    so the class basically observes the entire project.

    """

    async def like_file(self, login, browser, urls):
        """
        goes through rats list and likes them
        browser: Chrome. Selenium webdriver
        login: instagram login
        urls: list readlines of file that should be liked
        """
        x = 0
        log_variable_write(u' LIKE FILE amount of pages detected for likes: %s %s', len(urls), login)
        sort_for_likes(login)
        urls = open_file(login, 'for_likes')
        for i in urls:
            browser.get(i)
            await asyncio.sleep(random.randrange(2, 3))
            log_variable_write(u' LIKE FILE user link %s %s', i, login)
            file_write_one(login, i, 'liked_users')
            try:
                acc_name = browser.find_element_by_css_selector(dataIns.name).text
            except Exception as error:
                log_variable_write(u' LIKE FILE an error appeared %s %s', error, login)
                acc_name = browser.current_url.split('/')[-2]
            await asyncio.sleep(random.randrange(1, 2))
            log_variable_write(u' LIKE FILE acc name is : %s %s', acc_name, login)
            hrefs = browser.find_elements_by_tag_name('a')
            posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
            posts = []
            c = 0  # counter of posts
            if len(posts_urls) > 7:
                for fi in range(7):
                    posts.append(posts_urls.pop(0))
                    c += 1
            if posts:
                await asyncio.gather(self.like(browser, posts, acc_name))
                log_variable_write(u' LIKE FILE user has been liked: %s %s', acc_name, login)

            if c > 5:
                await asyncio.sleep(random.randrange(850, 950))
                log_variable_write(u' LIKE FILE sleeping for 15 min: %s likes were posted %s', c, login)
                x += 1
            posts_urls.clear()
        log_variable_write(u' LIKE FILE liked %s people %s', x, login)
        await asyncio.sleep(5)

    async def like_friends(self, login):
        """
        likes many friends of your friends
        login: instagram login
        """
        sort_for_likes(login)
        browser = init()
        try:
            set_cookies(login, browser)
            log_write(u' LIKE FRIENDS logged in via cookies %s', login)
        except Exception as error:
            log_variable_write(u' LIKE FRIENDS error with loading cookies %s %s', error, login)
        try:
            urls = open_file(login, 'for_likes')
            log_variable_write(u' LIKE FRIENDS links collected %s %s', len(urls), login)
            await asyncio.gather(self.like_file(login, browser, urls))
            log_write(u' LIKE FRIENDS like loop is completed %s', login)
        except Exception as err:
            log_variable_write(u' LIKE FRIENDS error while like for likes file, Error: %s %s', err, login)
        browser_close(' LIKE FRIENDS no error', browser)

    @staticmethod
    async def like(browser, posts, acc_name):
        """
        method clicks like button if its not clicked yet
        browser: Chrome
        posts: list of posts for getting liked
        acc_name: user's acc name
        """
        while posts:
            browser.get(posts.pop())
            await asyncio.sleep(random.randrange(2, 3))
            try:
                data_post = browser.find_element_by_css_selector(dataIns.post_time).text.split(' ')
            except Exception as error:
                log_variable_write(u'error while data detecting: %s', error)
                data_post = browser.find_element_by_css_selector(dataIns.dataa).get_attribute('datetime').split('-')[0]
            try:
                likes_amount = int(
                    browser.find_element_by_css_selector(dataIns.amount_of_likes).text)  # if its a picture
            except Exception as error:
                log_variable_write(u'error has appeared %s', error)
                likes_amount = int(browser.find_element_by_css_selector(dataIns.amount_of_views).text)  # if its a video
            if likes_amount < 250:
                if data_post[-1] != '2019' and likes_amount <= 150 and data_post[-1] != '2018' and data_post[-1] != '2017':
                    log_variable_write(u' LIKE likes start for: %s %s', acc_name, 'hui')
                    try:
                        check = browser.find_element_by_css_selector(dataIns.like_button).get_attribute('fill')
                        if '26' in check:
                            await asyncio.sleep(random.randrange(3, 5))
                            browser.find_element_by_css_selector(dataIns.like_button).click()
                            log_write(u' LIKE like posted %s', 'hui')
                        await asyncio.sleep(random.randrange(1, 4))
                        if xpath_exists(dataIns.autom_check, browser):
                            log_write(u' LIKE While likes limit was reached, sleeping mod is switched on %s', 'hui')
                            await asyncio.sleep(7200)
                    except Exception as error:
                        log_variable_write(u' LIKE page probably does not exist %s %s', error, 'hui')
            await asyncio.sleep(random.randrange(4, 5))


def like_start(login):
    """
    starts loop
    login: instagram login
    """
    from data.config import admins
    from handlers import notifying
    admin = admins[0]
    logger('likes')
    asyncio.run(likebot.like_friends(login))
    asyncio.run(notifying(admin, f'Х**ня случилась у {login}, глянь логи'))


def auth_start(login, password, tg_id):
    """
    starts authentication loop
    login: instagram login
    password: instagram password
    """
    browser = init()
    logger('auth')
    print('here')
    asyncio.run(auth(login, password, browser))
    asyncio.run(after_auth(login, browser))
    from handlers import notifying
    asyncio.run(notifying(tg_id, '✅\nСбор ссылок закончен, можно приступать к работе. Нажми на /start'))


def first_auth_start(login, password):
    """
    in case if this is the first login, rus the program and allows input security code mechanically
    :param login:
    :param password:
    """
    asyncio.run(first_auth(login, password))


likebot = LikeBot()