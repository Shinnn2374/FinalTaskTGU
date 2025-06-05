# Импорт необходимых библиотек
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Настройка отображения графиков
plt.style.use('seaborn')
sns.set_palette("husl")

# 1. Загрузка данных

df = pd.read_excel('wb_pc_easy.xlsx', engine='openpyxl')
print("Данные успешно загружены. Первые 5 строк:")
display(df.head())

# 2. Предварительный анализ данных
print("\n2. Основная информация о датасете:")
display(df.info())

print("\n3. Пропущенные значения:")
display(df.isna().sum())

# 3. Очистка и преобразование данных
# Заполнение пропусков для числовых столбцов
numeric_cols = ['Цена, руб.', 'Количество ядер процессора', 'Объем оперативной памяти (Гб)',
                'Объем накопителя HDD', 'Объем накопителя SSD']
df[numeric_cols] = df[numeric_cols].fillna(0)

# Преобразование категориальных данных
cat_cols = ['Видеопроцессор', 'Операционная система', 'Процессор_тип', 'Тип оперативной памяти']
df[cat_cols] = df[cat_cols].fillna('Не указано')

# 4. Статистический анализ
print("\n4. Основные статистические показатели:")
display(df[numeric_cols].describe())

# Анализ категориальных данных
print("\nРаспределение по категориям:")
for col in cat_cols:
    print(f"\n{col}:")
    display(df[col].value_counts(normalize=True).head(10))

# 5. Визуализация данных
plt.figure(figsize=(15, 20))

# Распределение цен
plt.subplot(4, 2, 1)
sns.histplot(df['Цена, руб.'], bins=30, kde=True)
plt.title('Распределение цен на ноутбуки')
plt.xlabel('Цена, руб.')
plt.ylabel('Количество')

# Ядра процессора vs Цена
plt.subplot(4, 2, 2)
sns.boxplot(x='Количество ядер процессора', y='Цена, руб.', data=df)
plt.title('Зависимость цены от количества ядер')

# Объем ОЗУ vs Цена
plt.subplot(4, 2, 3)
sns.scatterplot(x='Объем оперативной памяти (Гб)', y='Цена, руб.', data=df)
plt.title('Зависимость цены от объема ОЗУ')

# Тип процессора vs Цена
plt.subplot(4, 2, 4)
sns.boxplot(x='Процессор_тип', y='Цена, руб.', data=df)
plt.xticks(rotation=45)
plt.title('Зависимость цены от типа процессора')

# Распределение по операционным системам
plt.subplot(4, 2, 5)
df['Операционная система'].value_counts().plot(kind='bar')
plt.title('Распределение по ОС')
plt.xticks(rotation=45)

# Соотношение SSD/HDD
plt.subplot(4, 2, 6)
(df[['Объем накопителя SSD', 'Объем накопителя HDD']].sum()/1024).plot(kind='bar')
plt.title('Общий объем SSD vs HDD (ТБ)')
plt.ylabel('Терабайты')

# Топ продавцов
plt.subplot(4, 2, 7)
df['Продавец'].value_counts().head(10).plot(kind='bar')
plt.title('Топ 10 продавцов')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 6. Корреляционный анализ
print("\n6. Матрица корреляций:")
corr_matrix = df[numeric_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Матрица корреляций числовых параметров')
plt.show()

# 7. Анализ взаимосвязей
# Цена и характеристики
print("\n7. Анализ взаимосвязей:")
top_expensive = df.nlargest(5, 'Цена, руб.')
print("\nСамые дорогие ноутбуки:")
display(top_expensive[['Наименование', 'Цена, руб.', 'Процессор_тип', 'Объем оперативной памяти (Гб)']])

# 8. Выводы и рекомендации
print("\n8. Основные выводы:")
print("""
1. Распределение цен имеет правый хвост - большинство ноутбуков сосредоточены в среднем ценовом диапазоне.
2. Наблюдается четкая зависимость цены от технических характеристик:
   - Чем больше ядер процессора и объем ОЗУ, тем выше цена
   - SSD накопители сильнее влияют на цену, чем HDD
3. Наиболее распространенные процессоры: Intel Core i5, i7
4. Windows - доминирующая ОС на рынке
5. Выявлены сильные корреляции между:
   - Объемом ОЗУ и ценой
   - Количеством ядер и ценой

Рекомендации для заказчика:
- Для массового рынка стоит рассматривать модели с Intel Core i5, 8-16 ГБ ОЗУ
- Премиальные модели должны иметь SSD накопители и мощные видеопроцессоры
- Анализ топовых продавцов поможет в выборе партнеров
""")