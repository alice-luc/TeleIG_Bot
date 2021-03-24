from IgSide.Server.methods import *
from IgSide.Server.likes_bot import likebot


class Trial:
    """
    free demo version
    """
    @staticmethod
    async def trial_check_followers(login, browser):
        """
        collects a shorter lost of followers
        :param login:
        :param browser:
        """
        browser.find_element_by_css_selector(dataIns.followers_button).click()
        await asyncio.sleep(random.randrange(2, 3))
        window = browser.find_element_by_css_selector(dataIns.window)
        for i in range(2):
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', window)
            await asyncio.sleep(random.randrange(5, 10))
        followers = window.find_elements_by_tag_name('li')
        o = 0
        for follower in followers:
            follower_url = follower.find_element_by_tag_name("a").get_attribute("href")
            business_marks_counter = None
            for business_mark in dataIns.business_accounts:
                if business_mark in follower_url:
                    business_marks_counter = business_mark
                    log_variable_write(u'it has not passed %s tag %s', business_marks_counter, login)

            if not business_marks_counter:
                file_write_one(login, follower_url, 'followers')
                o += 1
            else:
                log_variable_write(u'this account was detected as a business one %s %s', business_marks_counter, login)
        followers.clear()

    async def trial_run(self, login, password):
        """collecting links for likes"""
        browser = init()
        await asyncio.gather(auth(login, password, browser))
        await asyncio.sleep(2)
        await asyncio.gather(self.trial_check_followers(login, browser))
        await asyncio.sleep(2)
        await asyncio.gather(collecting_accounts(browser, login))
        await asyncio.sleep(2)
        await asyncio.gather(likebot.like_friends(login))


def trial_purchase(tg_id, login, password):
    """
    starts the trial subscription and notifies consumer when its done
    :param tg_id:
    :param login:
    :param password:
    """
    from handlers import notifying

    asyncio.run(trial.trial_run(login, password))
    liked_links = len(open_file(login, 'liked_users'))
    asyncio.run(notifying(tg_id, f'Закончили с лайками на аккаунте \n{login}\n\
    Количество аккаунтов, попавших под раздачу лайков: {liked_links}.\
    Количество лайков: {liked_links*7}\n\n Для получения списка со ссылками напиши @alohayoung'))
