## test_task

# task_1
https://docs.google.com/spreadsheets/d/1iqcUaKSdomCiKLMID7XqlKv8oEQOqXuSOHHkx0fZQ5k/edit#gid=0
Прокидував запити асинхронно циклом три рази, кожна нова ітерація достукається лише до посилань по яким не було відповіді. Зробив трохи інший деліметер, щоб було зручно записувати ексепшени на місця пропусків. Не найкраще рішення, проте задумка в тому щоб знати причину пропущенного значення. Розмір картинки розраховувався через Pillow. Був варіант зробити це через массив нампі, проте як показала практика - покращення продуктивності не спостерігаються. 

# task_2

https://docs.google.com/spreadsheets/d/1iqcUaKSdomCiKLMID7XqlKv8oEQOqXuSOHHkx0fZQ5k/edit#gid=0
Останній тиждень маю проблеми зі зв'язком, тому в пайплайні використовувалась тільки одна таблиця, якщо закоментувати 49й рядок, то скрипт витягне всі таблиці з датасету. Конкуренція реалізована за допомогою багатопоточності в ThreadPoolExecutor, оскільки асинхронна обробка не представляється можливою.

# task_3

https://docs.google.com/spreadsheets/d/16-WCrjMnWeu7EyYn1vALkksTd3d-qU_-/edit#gid=1313533535
Був взятий каталог нерухомості, на його основі була побудована таблиця. Ціна, площа та місто були отримані з ленти, де розташовані всі пропозиції. Поверх та загальна кількість поверхів були отримані уже безпосередньо з анкет при переході. Була реалізована пагінація, тобто в скрипті можна вказати кількість сторінок які потрібно зпарсити. В даному випадку вийшло всього три сторінки(слабкий інтернет).
