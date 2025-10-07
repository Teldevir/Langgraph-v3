## Локальная установка Ollama (linux)
```shell
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull <модель для эмбединга>
ollama pull <модель для генерации>
```

## Команды
**/start** - старт  
**/chunks** - текущие чанки документа  
**/search <текст>** - поиск по векторной базе  
**<текст>** - генерирует ответ с информацией из векторной базы  
**<документ>** - подгружает документ в векторную базу  

## Для запуска
Для начала нужно создать ботa:  
## шаг 1
Зайти в телеграм и перейти в BotFather  
![botfather](docs/botfather.png)
## шаг2
Создать бота (пример на рисунке)  
![creation](docs/creation.png)
## шаг3
Положить подгружаемый документ в папку *fixtures*
## шаг4
Указать настройки окружения в *.env* файле.
```
APP_BOT_TOKEN - токен бота
APP_PROMPT - промт
APP_DEFAULT_DOC_FILE_PATH - стартовый документ, указать название файла из папки fixtures

OLLAMA_HOST - хост олламы
LANGGRAPH_LANGUAGE_MODEL - основная модель
LANGGRAPH_EMBEDDING_MODEL - модель для эмбединга
LANGGRAPH_TEMPERATURE - температура основной модели
LANGGRAPH_SIMILARITY_SEARCH_K - количество чанков в результате поиска по документам
LANGGRAPH_SEPARATORS - сепараторы для сплиттера, указывать как список (например '["---", "+++"]') 
LANGGRAPH_SPLITTER_CHUNK_SIZE - размер чанка для сплиттера
LANGGRAPH_SPLITTER_CHUNK_OVERLAP - размер перекрытия чанка для сплиттера

```
## шаг4
```bash
docker compose up -d 
```
## P.S.
Первый запуск может идти долго, так как скачиваются все зависимости и после 
сборки контейнеров скачиваются модели для Ollama. 
Лучше выделить 10+ гб оперативной памяти в ресурсах докера.



# Langgraph-v3
# Langgraph-v3
# Langgraph-v3
