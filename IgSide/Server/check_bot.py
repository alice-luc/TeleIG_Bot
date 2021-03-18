"""
Check class
it inherits methods and like start class
"""
from IgSide.Server.methods import *


class Check:
    """
    Check class mostly be using once a while
    """
    async def unfollow_bots(self, login):
        """
        Checks following pages, checks followers, counts their follows pages and block them if there are too many
        login: instagram login
        """
        log_write(u' UNFOLLOW BOTS method is started %s', login)
        browser = init()
        try:
            set_cookies(login, browser)
            log_write(u' UNFOLLOW BOTS logged in via cookies %s', login)
        except Exception as error:
            log_variable_write(u' UNFOLLOW BOTS error with loading cookies %s %s', error, login)
        going_to_self_page(browser)
        await asyncio.sleep(random.randrange(1, 2))
        await asyncio.gather(check_following(login, browser))
        await asyncio.gather(check_followers(login, browser))
        un = 0  # temp variable for unfollowed accounts' counting
        urls = set(open_file(login, 'followers'))
        following = set(open_file(login, 'following'))
        unfollowed = set(open_file(login, 'checked'))
        urls = [url for url in urls if url not in following and url not in unfollowed]
        urls = list(urls)
        log_variable_write(u' UNFOLLOW BOTS follows ad following lists were loaded, \
                            checking starts for %s users %s', len(urls), login)

        while urls:
            browser.get(urls.pop())
            await asyncio.sleep(random.randrange(4, 6))
            try:
                user_following_count = int(
                    browser.find_element_by_css_selector(dataIns.following_number).text.replace(',',
                                                                                                ''))
                user_followers_count = int(
                    browser.find_element_by_css_selector(dataIns.followers_number).text.replace(',',
                                                                                                ''))
                await asyncio.sleep(random.randrange(2, 4))
            except Exception as error:
                log_variable_write(u' UNFOLLOW BOTS error raised %s %s', error, login)
                log_variable_write(u' UNFOLLOW BOTS BF what has been gotten about followers %s %s', user_followers_count, login)
                log_variable_write(u' UNFOLLOW BOTS BF what has been gotten about follows %s %s', user_following_count, login)
                user_following_count = int(
                    browser.find_element_by_css_selector(dataIns.following_button).get_attribute('title').replace(',',
                                                                                                                  ''))
                user_followers_count = int(
                    browser.find_element_by_css_selector(dataIns.followers_button).get_attribute('title').replace(',',
                                                                                                                  ''))
                log_variable_write(u' UNFOLLOW BOTS what has been gotten about followers %s %s', user_followers_count, login)
                log_variable_write(u' UNFOLLOW BOTS what has been gotten about follows %s %s', user_following_count, login)
            url = browser.current_url
            # if url not in following:
            #
            #     if url not in unfollowed:

            if user_following_count > user_followers_count * 5 and user_following_count > 200:

                await asyncio.gather(self.unfollow(browser))
                log_variable_write(u' UNFOLLOW BOTS unfollowed %s *5 follows and > 200 following', url, login)
                un += 1
                file_write_one(login, url, 'checked')
                file_write_one(login, url, 'unfollowed')

            elif user_following_count > 2000:
                un += 1
                file_write_one(login, url, 'unfollowed')
                file_write_one(login, url, 'checked')
                await asyncio.gather(self.unfollow(browser))
                log_variable_write(u' UNFOLLOW BOTS unfollowed %s, >2000 follows %s', url, login)

            else:
                file_write_one(login, url, 'checked')
                log_variable_write(u' UNFOLLOW BOTS passed the check %s %s', url, login)
            #     else:
            #         file_write_one(login, url, 'checked')
            #         log_variable_write(u' UNFOLLOW BOTS passed the check *5 and >200 %s %s', url, login)
            # else:
            #     file_write_one(login, url, 'checked')
            #     log_variable_write(u' UNFOLLOW BOTS %s is being followed by user %s %s', url, login)
            await asyncio.sleep(random.randrange(10, 20))
        log_variable_write(u' UNFOLLOW BOTS  totally unfollowed %s %s', un, login)
        browser_close(' UNFOLLOW BOTS end of method', browser)

    @staticmethod
    async def unfollow(browser):
        """
        blocks user and then unblocks him
        browser: Chrome
        """
        count = 0  # to be raised if the user is blocked successfully
        try:
            browser.find_element_by_css_selector(dataIns.three_dots_button).click()
            await asyncio.sleep(random.randrange(2, 4))
            browser.find_element_by_css_selector(dataIns.block_this_user_button).click()
            await asyncio.sleep(random.randrange(2, 4))
            browser.find_element_by_css_selector(dataIns.block_sure_button).click()
            await asyncio.sleep(random.randrange(2, 4))
            if xpath_exists(dataIns.autom_check, browser):
                log_write(u' UNFOLLOW atomization check has been failed while unfollowing, turning off for 2 hours %s', 'hui')
                browser.find_element_by_css_selector(dataIns.autom_check_report).click()
                await asyncio.sleep(7200)
            browser.find_element_by_css_selector(dataIns.dismiss_button).click()
            await asyncio.sleep(random.randrange(3, 4))
            count += 1
            browser.refresh()
            await asyncio.sleep(random.randrange(1, 3))
            acc_name = browser.find_element_by_css_selector(dataIns.name).text
            try:
                if count != 0:
                    await asyncio.sleep(random.randrange(2, 5))
                    browser.find_element_by_css_selector(dataIns.unblock_button).click()
                    await asyncio.sleep(random.randrange(3, 5))
                    browser.find_element_by_css_selector(dataIns.unblock_sure_button).click()
                    await asyncio.sleep(random.randrange(3, 5))
                    if xpath_exists(dataIns.autom_check,browser):
                        log_write(u' UNFOLLOW atomization check has been failed while unfollowing, turning off for 2 \
                        hours %s', 'hui')
                        browser.find_element_by_css_selector(dataIns.autom_check_report).click()
                        await asyncio.sleep(7200)
                    else:
                        browser.find_element_by_css_selector(dataIns.dismiss_button).click()
                        await asyncio.sleep(random.randrange(1, 3))
                else:
                    log_variable_write(u' UNFOLLOW user is already blocked %s %s', acc_name, 'hui')
            except Exception as error:
                log_variable_write(u' UNFOLLOW no such element, link is not real %s %s', error, 'hui')
                await asyncio.sleep(2)
            log_variable_write(u' UNFOLLOW user was blocked %s %s', acc_name, 'hui')
        except Exception as error:
            log_variable_write(u' UNFOLLOW blocking failed %s %s', error, 'hui')
        await asyncio.sleep(random.randrange(1200, 1800))

    def rats_detection(self, login):
        followers = set(open_file(login,'followers'))
        following = set(open_file(login, 'following'))
        rats = [follow for follow in following if follow not in followers]
        if rats:
            return list(rats)
        else:
            return None


def unfollow_bots_start(login, tg_ig):
    """
    starts loop
    login: instagram login
    """
    from volume_data.insta_log.logger import logger

    # from handlers import notifying
    logger('unfollow_bots')
    asyncio.run(check.unfollow_bots(login))
    from handlers import notifying
    asyncio.run(notifying(tg_ig, '✅\nОчистка подписчиков от ботов закончена'))


check = Check()
