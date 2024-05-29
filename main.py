from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def initialize_browser():
    options = Options()
    options.headless = True  # Запуск в фоновом режиме без графического интерфейса
    service = Service(executable_path='/Users/asp_er/Downloads/geckodriver')  # Укажите путь к geckodriver
    browser = webdriver.Firefox(service=service, options=options)
    return browser

def search_wikipedia(browser, query):
    browser.get('https://www.wikipedia.org/')
    search_input = browser.find_element(By.NAME, 'search')
    search_input.send_keys(query)
    search_input.submit()

def get_paragraphs(browser):
    paragraphs = browser.find_elements(By.CSS_SELECTOR, 'div.mw-parser-output > p')
    return [p.text for p in paragraphs]

def get_internal_links(browser):
    links = browser.find_elements(By.CSS_SELECTOR, 'div.mw-parser-output a[href^="/wiki/"]')
    return [(link.text, link.get_attribute('href')) for link in links]

def main():
    try:
        browser = initialize_browser()
    except Exception as e:
        print(f"Ошибка при инициализации браузера: {e}")
        return

    try:
        query = input("Введите запрос для поиска на Википедии: ")
        search_wikipedia(browser, query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")

            choice = input("Введите номер действия: ")

            if choice == '1':
                paragraphs = get_paragraphs(browser)
                for i, paragraph in enumerate(paragraphs):
                    print(f"Параграф {i + 1}: {paragraph}\n")
            elif choice == '2':
                links = get_internal_links(browser)
                for i, (text, url) in enumerate(links):
                    print(f"{i + 1}. {text} ({url})")

                link_choice = input("Введите номер ссылки для перехода: ")
                if link_choice.isdigit():
                    link_choice = int(link_choice) - 1
                    if 0 <= link_choice < len(links):
                        browser.get(links[link_choice][1])
                    else:
                        print("Некорректный номер ссылки, попробуйте снова.")
                else:
                    print("Введите корректное число.")
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод, попробуйте снова.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
