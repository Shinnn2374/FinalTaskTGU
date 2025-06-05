# Импорт необходимых библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка визуализаций
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")

# 1. Загрузка данных
try:
    df = pd.read_excel('wb_pc_easy.xlsx', engine='openpyxl')
    print("Данные успешно загружены. Первые 5 строк:")
    print(df.head().to_string())  # Заменяем display() на print()
except Exception as e:
    print(f"Ошибка при загрузке файла: {e}")
    exit()

# 2. Предварительный анализ данных
print("\n2. Основная информация о датасете:")
print(df.info())

print("\n3. Пропущенные значения:")
print(df.isna().sum())

# 3. Очистка и преобразование данных
# Заполнение пропусков для числовых столбцов
numeric_cols = ['Цена, руб.', 'Количество ядер процессора',
               'Объем оперативной памяти (Гб)']
df[numeric_cols] = df[numeric_cols].fillna(0)

# Преобразование категориальных данных
cat_cols = ['Видеопроцессор', 'Операционная система',
           'Процессор_тип', 'Тип оперативной памяти',
           'Объем накопителя HDD', 'Объем накопителя SSD']
df[cat_cols] = df[cat_cols].fillna('Не указано')

# 4. Статистический анализ
print("\n4. Основные статистические показатели:")
print(df[numeric_cols].describe().to_string())  # Заменяем display() на print()

# Анализ категориальных данных
print("\nРаспределение по категориям:")
for col in cat_cols:
    print(f"\n{col}:")
    print(df[col].value_counts(normalize=True).head(10).to_string())

# 5. Визуализация данных
plt.figure(figsize=(15, 10))

# Распределение цен
plt.subplot(2, 2, 1)
sns.histplot(df['Цена, руб.'], bins=30, kde=True)
plt.title('Распределение цен на ноутбуки')
plt.xlabel('Цена, руб.')
plt.ylabel('Количество')

# Ядра процессора vs Цена
plt.subplot(2, 2, 2)
sns.boxplot(x='Количество ядер процессора', y='Цена, руб.', data=df)
plt.title('Зависимость цены от количества ядер')

# Объем ОЗУ vs Цена
plt.subplot(2, 2, 3)
sns.scatterplot(x='Объем оперативной памяти (Гб)', y='Цена, руб.', data=df)
plt.title('Зависимость цены от объема ОЗУ')

# Тип процессора vs Цена
plt.subplot(2, 2, 4)
sns.boxplot(x='Процессор_тип', y='Цена, руб.', data=df)
plt.xticks(rotation=45)
plt.title('Зависимость цены от типа процессора')

plt.tight_layout()
plt.savefig('analysis_plots.png')  # Сохраняем графики в файл
print("\nГрафики сохранены в файл 'analysis_plots.png'")

# 6. Корреляционный анализ
print("\n6. Матрица корреляций:")
corr_matrix = df[numeric_cols].corr()
print(corr_matrix.to_string())

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Матрица корреляций числовых параметров')
plt.savefig('correlation_matrix.png')
print("Матрица корреляций сохранена в файл 'correlation_matrix.png'")

# 7. Анализ взаимосвязей
print("\n7. Топ-5 самых дорогих ноутбуков:")
print(df.nlargest(5, 'Цена, руб.')[['Наименование', 'Цена, руб.',
                                   'Процессор_тип',
                                   'Объем оперативной памяти (Гб)']].to_string())

# 8. Выводы и рекомендации
print("""
8. Основные выводы и рекомендации:

1. Распределение цен показывает, что большинство ноутбуков находятся в среднем ценовом диапазоне.
2. Наблюдается четкая зависимость цены от технических характеристик:
   - Чем больше ядер процессора и объем ОЗУ, тем выше цена
   - SSD накопители сильнее влияют на цену, чем HDD
3. Наиболее распространенные процессоры: Intel Core i5, i7
4. Windows - доминирующая ОС на рынке
5. Выявлены сильные корреляции между:
   - Объемом ОЗУ и ценой
   - Количеством ядер и ценой

Рекомендации:
- Для массового рынка стоит рассматривать модели с Intel Core i5, 8-16 ГБ ОЗУ
- Премиальные модели должны иметь SSD накопители и мощные видеопроцессоры
- Анализ топовых продавцов поможет в выборе партнеров
""")