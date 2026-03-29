# Инструкция по запуску автотестов
## 1. Установить Google Chrome по ссылке https://www.google.com/intl/ru_ru/chrome/
## 2. Установить Git на ПК для своей ОС, следуя инструкции по ссылке https://git-scm.com/install/
## 3. Установить Python 3.13 по ссылке https://www.python.org/downloads (на Python 3.12 также должно работать)
## 4. Установить Allure на ПК для своей ОС, следуя инструкции по ссылке https://allurereport.org/docs/v3/install/
## 5. Установить Pycharm на ПК для своей ОС, следуя инструкциям по ссылке https://www.jetbrains.com/pycharm/download/
## 6. Установить Docker на ПК для своей ОС, следуя инструкции по ссылке https://docs.docker.com/desktop/ (выбрать ОС в поле Next Steps), затем перезагрузить ПК и запустить установленный Docker.
## 7. Перейти по ссылке https://github.com/Shpeeton/diplom и клонировать репозиторий к себе на ПК.
## 8. Открыть Pycharm, открыть проект со скачанным репозиторием и установить зависимости из файла reqiurements.txt
### Если возникает ошибка, необходимо создать окружение - использовать в терминале команды:  
### python -m venv venv
### venv\Scripts\activate
### pip install pytest==7.4.0 selenium==4.15.0 allure-pytest==2.13.2 pymysql==1.1.0 pg8000==1.31.5
## 9. Открыть терминал в папке с репозиторием и ввести команду docker-compose up -d
## 10. В терминале ввести команду pytest tests/ --alluredir=allure-results --tb=no
## 11. Для просмотра отчета в allure - ввести в терминале команду allure serve allure-results