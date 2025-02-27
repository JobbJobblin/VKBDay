# VKBDay 🎉

**VKBDay** — это проект, который помогает автоматически отправлять поздравления с Днём рождения вашим друзьям в социальной сети ВКонтакте. Проект использует API ВКонтакте для получения списка друзей и отправки сообщений.

## 📌 Оглавление

- [Установка](#Установка)
- [Настройка](#Настройка)
- [Использование](#Использование)
- [Лицензия](#Лицензия)
- [Контакты](#Контакты)

## 🛠️ Установка

Для начала работы с проектом, склонируйте репозиторий и установите необходимые зависимости.

```bash
# Клонирование репозитория
git clone https://github.com/JobbJobblin/VKBDay.git
cd VKBDay

# Установка зависимостей
pip install -r requirements.txt
```
## ⚙️ Настройка
Получение токена доступа ВКонтакте:

Перейдите по [ссылке](https://vkhost.github.io) и получите access token (у вас должны быть права администратора группы).

Настройка конфигурации:

Создайте файл .env в корневой директории проекта.

Добавьте в него следующий код:

VK_TOKEN = 'ваш_токен_доступа'  
GROUP_ID_MINUS = 'id вашей группы с минусом в начале (-88005553535)'  
GROUP_ID = 'id вашей группы без минуса (88005553535)'

## 🚀 Использование
После настройки, запустите скрипт для отправки поздравлений.

python main.py  
Скрипт запустит интерактивное меню, из которого вы можете создать отложенный пост или же выполнить скрипт по умолчанию.
По умолчанию размещается пост с поздравлением всех именинников группы на текущий момент.

## 📄 Лицензия
Этот проект распространяется под лицензией MIT.

## 📬 Контакты
Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной:

GitHub: [JobbJobblin](https://github.com/JobbJobblin)

Email: JobbJobblin@gmail.com  
Telegram: @SImonFry
