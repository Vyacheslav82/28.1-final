from pages.auth_page import AuthPage

from pages.elements import *

from settings import *

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import pytest





@pytest.fixture

def chrome_options(chrome_options):

    chrome_options.add_argument("--start-maximized")

    return chrome_options





def test_auth_by_email_positive(selenium):

    #Авторизация пользователя с валидным email и паролем

    page = AuthPage(selenium)

    page.enter_username(AuthEmail.email)

    page.enter_pass(AuthEmail.password)

    page.btn_click()



    assert page.get_relative_link() == '/account_b2c/page'





def test_auth_by_email_negative(selenium):

    #Авторизация пользователя с невалидным сочетанием email/пароль

    page = AuthPage(selenium)

    page.enter_username(AuthEmail.email)

    page.enter_pass(InvalidData.password)

    page.btn_click()



    assert page.get_relative_link() != '/account_b2c/page'

    assert page.find_el(*wrong_log_pass_message).text == 'Неверный логин или пароль'





def test_auth_by_phonenumber_positive(selenium):

    #Авторизация пользователя с валидным номером телефона и паролем

    page = AuthPage(selenium)

    page.enter_username(AuthPhone.phone)

    page.enter_pass(AuthPhone.password)

    page.btn_click()



    assert page.get_relative_link() == '/account_b2c/page'





def test_auth_by_phonenumber_negative(selenium):

    #Авторизация пользователя с невалидным телефоном/паролем

    page = AuthPage(selenium)

    page.enter_username(AuthPhone.phone)

    page.enter_pass(InvalidData.password)

    page.btn_click()



    assert page.get_relative_link() != '/account_b2c/page'

    assert page.find_el('xpath', '//*[@id="page-right"]/div/div/p').text == 'Неверный логин или пароль'







def test_auth_by_login_positive(selenium):

    # Авторизация пользователя с валидным сочетанием логин/пароль

    page = AuthPage(selenium)

    page.enter_username(AuthLogin.login)

    page.enter_pass(AuthLogin.password)

    page.btn_click()



    assert page.get_relative_link() == '/account_b2c/page'



def test_auth_by_login_negative(selenium):

    #Авторизация пользователя с невалидным сочетанием логин/пароль

    page = AuthPage(selenium)

    page.enter_username(InvalidData.login)

    page.enter_pass(InvalidData.password)

    page.btn_click()



    assert page.get_relative_link() != '/account_b2c/page'

    assert page.find_el('xpath', '//*[@id="page-right"]/div/div/p').text == 'Неверный логин или пароль'



def test_auth_with_maxlens(selenium):

    #Проверка ввода в поля логина и пароля строки длиной >2500 символов

    page = AuthPage(selenium)

    page.enter_username(MAXData.login*500)

    page.enter_pass(MAXData.password*500)

    page.btn_click()



    assert page.find_el(*internal_error_message_text).text == 'Internal Server Error'



def test_placeholder(selenium):

    #Проверка автозамены типа регистрации при вводе определенного типа данных (телефон, почта, логин, номер лицевой счет)

    page = AuthPage(selenium)

    page.enter_username(AuthEmail.email)

    page.enter_pass('anypass')



    assert page.placeholder.text == 'Электронная почта'





    page = AuthPage(selenium)

    page.enter_username('89179176738')

    page.enter_pass('anypass')



    assert page.placeholder.text == 'Мобильный телефон'



    page = AuthPage(selenium)

    page.enter_username('login123')

    page.enter_pass('anypass')



    assert page.placeholder.text == 'Логин'



    page = AuthPage(selenium)

    page.enter_username('123456789999')

    page.enter_pass('anypass')



    assert page.placeholder.text == 'Лицевой счёт'





def test_forget_password(selenium):

    #Проверка перехода по ссылке "забыл пароль"

    page = AuthPage(selenium)

    page.forget_password_link.click()



    assert page.find_el(*res_pass_text).text == 'Восстановление пароля'





def test_registration(selenium):

    #Проверка перехода по ссылке "Зарегистрироваться"

    page = AuthPage(selenium)

    page.registration_link.click()



    assert page.find_el(*reg_page_text).text == 'Регистрация'





def test_chat(selenium):

    #Открытие и авторизация в чате, проверка получения приветственного сообщения в чате

    page = AuthPage(selenium)

    page.find_el(*widget_bar).click()

    page.find_el(*username_chat).send_keys('Пунзер')

    page.find_el(*phone_chat).send_keys('9179176738')

    page.find_el(*button_chat).click()



    assert WebDriverWait(page.driver, 5).until(EC.text_to_be_present_in_element(chat_message, chat_fmessage))





def test_auth_vk(selenium):

    #Проверка перехода по ссылке авторизации пользователя через VK

    page = AuthPage(selenium)

    page.vk_button.click()



    assert page.get_base_url() == 'oauth.vk.com'





def test_auth_ok(selenium):

    #Проверка перехода по ссылке авторизации пользователя через сайт одноклассники

    page = AuthPage(selenium)

    page.ok_button.click()



    assert page.get_base_url() == 'connect.ok.ru'





def test_auth_moymir(selenium):

    #Проверка перехода по ссылке авторизации пользователя через сайт Мой мир

    page = AuthPage(selenium)

    page.mailru_button.click()



    assert page.get_base_url() == 'connect.mail.ru'





def test_auth_google(selenium):

    #Проверка перехода по ссылке авторизации пользователя через Google

    page = AuthPage(selenium)

    page.google_botton.click()



    assert page.get_base_url() == 'accounts.google.com'





def test_auth_yandex(selenium):

    #Проверка перехода по ссылке авторизации пользователя через Yandex

    page = AuthPage(selenium)

    page.ya_button.click()



    assert page.get_base_url() == 'passport.yandex.ru'





def test_agreement(selenium):

    #Проверка открытия ссылок, ведущих на страницу пользовательского соглашения

    page = AuthPage(selenium)

    original_window = page.driver.current_window_handle

    page.find_el(*link_user_agreement_auth_form).click()

    WebDriverWait(page.driver, 5).until(EC.number_of_windows_to_be(2))

    for window_handle in page.driver.window_handles:

        if window_handle != original_window:

            page.driver.switch_to.window(window_handle)

            break

    window_title = page.driver.execute_script("return window.document.title")



    assert window_title == 'User agreement'



    page.driver.close()

    page.driver.switch_to.window(original_window)

    page.find_el(*link_user_agreement_footer_f).click()

    WebDriverWait(page.driver, 5).until(EC.number_of_windows_to_be(2))

    for window_handle in page.driver.window_handles:

        if window_handle != original_window:

            page.driver.switch_to.window(window_handle)

            break



    assert window_title == 'User agreement'



    page.driver.close()

    page.driver.switch_to.window(original_window)

    page.find_el(*link_user_agreement_footer_s).click()

    WebDriverWait(page.driver, 5).until(EC.number_of_windows_to_be(2))

    for window_handle in page.driver.window_handles:

        if window_handle != original_window:

            page.driver.switch_to.window(window_handle)

            break



    assert window_title == 'User agreement'

