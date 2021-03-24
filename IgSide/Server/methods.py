"""
Methods for the main two files of the current folder.
its been inheriting to each of those files
"""
# !/usr/bin/env python
import asyncio
import logging
import random
import time
from os import mkdir
from pickle import load, dump

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from IgSide import dataIns


def xpath_exists(url, browser):
    """
    check whether the element exists on current page.
    Returns Boolean True if yes and False if no
    url: path to an element
    browser: Chrome
    """
    try:
        browser.find_element_by_css_selector(url)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist


def browser_close(error, browser):
    """
    closes browser, and quits the sessions of initiated browser
    browser: Chrome, selenium webdriber
    error: exeption error
    """
    logging.info(u'Browser has been closed due this error %s', error)
    browser.close()
    browser.quit()


def create(log):
    """
    creates all the files
    log: instagram login
    """
    try:
        mkdir(f'./volume_data/Users/{log}')
    except OSError as error:
        logging.info(u'path exists %s', error)
    with open(f'./volume_data/Users/{log}/{log}_for_likes.txt', 'w') as t:
        t.close()
    with open(f'./volume_data/Users/{log}/{log}_liked_users.txt', 'w') as f:
        f.close()
    with open(f'./volume_data/Users/{log}/{log}_followers.txt', 'w')as f:
        f.close()
    with open(f'./volume_data/Users/{log}/{log}_following.txt', 'w') as f:
        f.close()
    with open(f'./volume_data/Users/{log}/{log}_checked.txt', 'w') as n:
        n.close()
    with open(f'./volume_data/Users/{log}/{log}_unfollowed.txt', 'w') as f:
        f.close()


def sort_for_likes(login):
    """
    deletes the ones containing in both files
    login: instagram login
    """
    with open(f'./volume_data/Users/{login}/{login}_liked_users.txt') as file_liked:
        file_liked.seek(0)
        liked_us = set(file_liked.readlines())
    with open(f'./volume_data/Users/{login}/{login}_for_likes.txt') as file_for_likes:
        file_for_likes.seek(0)
        for_like = set(file_for_likes.readlines())
    for_likes = [item for item in for_like if item not in liked_us]
    # for_likes = [item for item in liked_us if liked_us]
    for_likes = list(for_likes)
    logging.info(u'%s users list for likes was rewriting, the new number of pages is %s against %s before', login, len(for_likes), len(for_like))
    with open(f'./volume_data/Users/{login}/{login}_for_likes.txt', 'w') as file:
        file.writelines(for_likes)


async def collecting_accounts(browser, log):
    """
    makes scrolls and collecting data about followers
    browser: Chrome, selenium webdriver
    log: instagram login
    """
    urls = open_file(log, 'followers')
    o = 0  # counter for while loop
    while urls:
        browser.get(urls.pop(0))
        o += 1
        try:
            await asyncio.sleep(random.randrange(2, 4))
            browser.find_element_by_css_selector(dataIns.followers_button).click()
            await asyncio.sleep(random.randrange(2, 3))
            window = browser.find_element_by_css_selector(dataIns.window)
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', window)
            await asyncio.sleep(random.randrange(1, 2))
            browser.find_element_by_css_selector(dataIns.close_button).click()
            await asyncio.sleep(random.randrange(1, 2))
            browser.find_element_by_css_selector(dataIns.followers_button).click()
            await asyncio.sleep(random.randrange(2, 4))
            window = browser.find_element_by_css_selector(dataIns.window)
            await asyncio.gather(asyncio.create_task(window_scroll_fol(browser, window, log)))
        except Exception as error:
            log_variable_write(u'error %s %s', error, log)
            log_variable_write(u'collecting accounts method was stopped due to reason above, amount of links \
            gotten: %s %s', o, log)
    log_variable_write(u'followers followers adding to likes list is done %s %s',
                       browser.current_url.split('/')[-1], log)


def init():
    """
    browser and logging methods initializing
    returns browser
    func_name: name of the method that raises this method. it is required to determine the loggong file path
    login: instagram login
    """
    options = webdriver.ChromeOptions()
    # proxy = ''  # should be filled with the data from db and added as an argument to options below
    options.add_argument('--proxy-server=217.29.62.222:55909')
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return browser


def open_file(login, func_name):
    """
    opens file and returns it as list
    login: instagram login
    func_name: the name of method that raised this method
    """
    with open(f'./volume_data/Users/{login}/{login}_{func_name}.txt') as y:
        urls = y.readlines()
    return urls


async def window_scroll_fol(browser, window, log):
    """
    executing JS script to scroll window down the button
    browser: Chrome, selenium webdriver
    window: window element on a page that needs to be scrolled
    log: instagram login
    """
    for i in range(random.randrange(5, 9)):
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', window)
        await asyncio.sleep(random.randrange(8, 10))
        if i % 5 == 0:
            await asyncio.sleep(random.randrange(5, 10))
    followers = window.find_elements_by_tag_name('li')
    await asyncio.sleep(random.randrange(2, 4))
    log_variable_write(u' followers followers adding to likes list is done, quantity %s %s', len(followers), log)
    count = 0
    for follower in followers:
        follower_url = follower.find_element_by_tag_name("a").get_attribute("href")
        business_mark_ident = None
        for business_mark in dataIns.business_accounts:
            if business_mark in follower_url:
                business_mark_ident = business_mark
                log_variable_write(u'it has not passed %s tag %s', business_mark, log)

        if not business_mark_ident:
            file_write_one(log, follower_url, 'for_likes')
            count += 1
        else:
            log_variable_write(u'this account was detected as a business one %s %s', business_mark_ident, log)
    followers.clear()
    await asyncio.sleep(random.randrange(1, 2))
    log_variable_write(u'Method of scrolling window of followers has got done, line list uploaded for %s links %s',
                       count, log)


async def window_scroll_self(browser, window, count):
    """
    executing JS script to scroll window down the button
    browser: Chrome, selenium webdriver
    window: window element on a page that needs to be scrolled
    count: the number of followers to determine the amount of scrolls
    """
    # for i in range(count // 11 + 1):
    for i in range(10):
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', window)
        await asyncio.sleep(random.randrange(10, 15))
        # if i % 11 == 0:
        #     await asyncio.sleep(random.randrange(10, 15))


def log_write(message, login):
    """
    message: the message that should be written into log file
    """
    logging.info(message, login)


def log_variable_write(message, variable, login):
    """
    message: the message that should be written into log file
    variable: value that should be passed to logging attribute
    """
    logging.info(message, variable, login)


def file_write_one(login, url, func_name):
    """
    writes one line into the file
    login: instagram login
    url: line that should be written
    func_name: the name of method that raises this method. STRING
    """
    with open(f'./volume_data/Users/{login}/{login}_{func_name}.txt', 'a') as file:
        file.write(url + '\n')


def get_cookies(browser, login):
    """
    method gets cookies using dump and writes it into the file
    browser: Chrome. selenium webdriver
    login: instagram login
    """
    with open(f'./volume_data/Users/{login}/{login}_cookies_insta', 'wb') as file:
        dump(browser.get_cookies(), file)


def going_to_self_page(browser):
    """
    goes to self page using icon in top right and <profile> button
    browser: Chrome. Selenium webdriver
    """
    browser.find_element_by_css_selector(dataIns.my_page_icon).click()
    time.sleep(random.randrange(1, 2))
    browser.find_element_by_css_selector(dataIns.my_page_button).click()


async def check_followers(login, browser):
    """
    checks followers by scrolling followers window till the end and collecting data into file <login>_followers.txt
    login: instagram login
    browser: Chrome. Selenium webdriver
    """
    n = 0  # number of followers that would be collected from followers' window after scrolling
    await asyncio.sleep(random.randrange(3, 4))
    try:
        log_write(u'check followers start %s', login)
        followers_count = int(browser.find_element_by_css_selector(dataIns.followers_number).text.replace(',', ''))
    except Exception as error:
        followers_amount = browser.find_element_by_css_selector(dataIns.followers_button)
        followers_count = int(followers_amount.get_attribute('title').replace(',', ''))
        log_variable_write(u' CHECK FOLLOWERS error raised %s %s', error, login)
        log_variable_write(u' CHECK FOLLOWERS what has been gotten from button %s %s', followers_amount, login)
        log_variable_write(u' CHECK FOLLOWERS what has been gotten from title %s %s', followers_count, login)
    await asyncio.sleep(random.randrange(2, 3))
    try:
        browser.find_element_by_css_selector(dataIns.foler_but).click()
        await asyncio.sleep(random.randrange(2, 3))
        window = browser.find_element_by_css_selector(dataIns.window)
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', window)
        await asyncio.sleep(random.randrange(1, 2))
        browser.find_element_by_css_selector(dataIns.close_button).click()
        await asyncio.sleep(random.randrange(2, 3))
        browser.find_element_by_css_selector(dataIns.foler_but).click()
        await asyncio.sleep(random.randrange(3, 4))
        window = browser.find_element_by_css_selector(dataIns.window)
        await asyncio.gather(window_scroll_self(browser, window, followers_count))
        log_variable_write(u' CHECK FOLLOWERS scrolling is done, starting to collect data %s %s', login, login)
        scrolled_window = browser.find_element_by_css_selector(dataIns.scroll_window)
        all_url = scrolled_window.find_elements_by_tag_name('li')
        await asyncio.sleep(1)
        log_variable_write(u' CHECK FOLLOWERS volume_data collected, list is going to be updated by %s %s',
                           len(all_url), login)
        for url in all_url:
            url = url.find_element_by_tag_name("a").get_attribute("href")
            file_write_one(login, url, 'followers')
            n += 1
        all_url.clear()
        browser.find_element_by_css_selector(dataIns.close_button).click()
        log_variable_write(u' CHECK FOLLOWERS followers list uploaded for  %s %s', n, login)
    except Exception as error:
        log_variable_write(u' CHECK FOLLOWERS while followers check error raised, error %s %s', error, login)
        log_variable_write(u' CHECK FOLLOWERS the number of accounts that were written to a file %s %s', n, login)


async def check_following(login, browser):
    """
    checks followers by scrolling followers window till the end and collecting data into file <login>_followers.txt
    login: instagram login
    browser: Chrome. Selenium webdriver
    """
    n = 0
    try:
        log_write(u' CHECK FOLLOWING check follows starts %s', login)
        following_count = int(browser.find_element_by_css_selector(dataIns.following_number).text.replace(',', ''))
    except Exception as error:
        following_amount = browser.find_element_by_css_selector(dataIns.following_button)
        following_count = int(following_amount.get_attribute('title').replace(',', ''))
        log_variable_write(u' CHECK FOLLOWING while trying to cout follows error raised %s %s', error, login)
        log_variable_write(u' CHECK FOLLOWING what has been gotten from button %s %s', following_amount, login)
        log_variable_write(u' CHECK FOLLOWING what has been gotten from title %s %s', following_count, login)
    await asyncio.sleep(random.randrange(1, 2))
    try:
        browser.find_element_by_css_selector(dataIns.following_button).click()
        await asyncio.sleep(random.randrange(2, 3))
        window = browser.find_element_by_css_selector(dataIns.window)
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', window)
        await asyncio.sleep(random.randrange(1, 2))
        browser.find_element_by_css_selector(dataIns.close_button).click()
        await asyncio.sleep(random.randrange(1, 2))
        browser.find_element_by_css_selector(dataIns.following_button).click()
        await asyncio.sleep(random.randrange(2, 3))
        window = browser.find_element_by_css_selector(dataIns.window)
        await asyncio.gather(window_scroll_self(browser, window, following_count))
        log_variable_write(u' CHECK FOLLOWING follows count is done, trying to collect links %s %s', following_count, login)
        all_url = window.find_elements_by_tag_name('li')
        await asyncio.sleep(1)
        log_variable_write(u' CHECK FOLLOWING follows list is going to be updated by %s %s', len(all_url), login)
        for url in all_url:
            url = url.find_element_by_tag_name("a").get_attribute("href")
            file_write_one(login, url, 'following')
            n += 1
        all_url.clear()
        browser.find_element_by_css_selector(dataIns.close_button).click()
        log_variable_write(u' CHECK FOLLOWING  method is completed, following list uploaded for %s %s', n, login)
    except:
        log_variable_write(u' CHECK FOLLOWING while following check error raised, the number of written links is %s %s', n, login)


def set_cookies(login, browser):
    """
    sets cookies, requires login and browser
    browser: Chrome
    """

    browser.get(dataIns.url)
    time.sleep(1)
    for cookie in load(open(f'./volume_data/Users/{login}/{login}_cookies_insta', 'rb')):
        browser.add_cookie(cookie)
    logging.info(u' SET COOKIES cookies are set %s %s', time.ctime(), login)
    time.sleep(1)
    browser.refresh()
    time.sleep(1)
    if xpath_exists(dataIns.not_now_button, browser):
        browser.find_element_by_css_selector(dataIns.not_now_button).click()
        time.sleep(1)


async def after_auth(login, browser):
    """
    makes a queue of tasks to be ran after the auth method
    :param login:
    :param browser:
    """
    await asyncio.sleep(random.randrange(2,4))
    await asyncio.gather(check_followers(login, browser))
    await asyncio.gather(check_following(login, browser))
    await asyncio.gather(collecting_accounts(browser, login))
    browser_close('the end', browser)


async def auth(log, passw, browser):
    """
    requires login and password
    once user is legged in authentication goes through cookies
    creates a connection with Chrome and passes it
    """
    create(log)
    try:
        set_cookies(log, browser)
        log_write(u'logged in via cookies', log)
    except FileNotFoundError:
        try:
            browser.get(dataIns.url)
            await asyncio.sleep(random.randrange(2, 3))
            login = browser.find_element_by_css_selector(dataIns.log_input)
            await asyncio.sleep(random.randrange(1, 2))
            login.send_keys(log)
            log_write(u'past login %s', log)
            password = browser.find_element_by_css_selector(dataIns.pass_input)
            await asyncio.sleep(random.randrange(1, 2))
            password.send_keys(passw)
            log_write(u'past password %s', log)
            await asyncio.sleep(random.randrange(1, 3))
            browser.find_element_by_css_selector(dataIns.login_button).click()
            await asyncio.sleep(5)
            log_write(u'setting cookies %s', log)
            get_cookies(browser, log)
            log_write(u'cookies are gotten %s', log)
        except Exception as error:
            log_variable_write(u'error raised %s %s', error, log)
    going_to_self_page(browser)


async def first_auth(log, passw):
    """
    a method that freezes for some time and allows to enter a security code manually
    :param log:
    :param passw:
    """
    browser = init()
    try:
        browser.get(dataIns.url)
        await asyncio.sleep(random.randrange(2, 3))
        login = browser.find_element_by_css_selector(dataIns.log_input)
        await asyncio.sleep(random.randrange(1, 2))
        login.send_keys(log)
        log_write(u'past login %s', log)
        password = browser.find_element_by_css_selector(dataIns.pass_input)
        await asyncio.sleep(random.randrange(1, 2))
        password.send_keys(passw)
        log_write(u'past password %s', log)
        await asyncio.sleep(random.randrange(1, 3))
        browser.find_element_by_css_selector(dataIns.login_button).click()
        get_cookies(browser, login)
        await asyncio.sleep(3600)
    except Exception as error:
        log_variable_write(u'error raised %s %s', error, log)
    browser_close('no error', browser)
