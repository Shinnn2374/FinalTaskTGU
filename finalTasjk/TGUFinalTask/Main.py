import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Установка стиля Seaborn
sns.set(style="whitegrid")

# Загрузка данных
df = pd.read_excel('hh_easy.xlsx')

# Предварительный просмотр данных
print(df.head())
print(df.info())

# 1. Анализ профессиональных ролей
professional_roles = df['professional_roles'].value_counts().head(10)

# 2. Анализ требований к опыту работы
experience_dist = df['experience'].value_counts(normalize=True) * 100

# 3. Анализ графиков работы
schedule_dist = df['schedule'].value_counts(normalize=True) * 100

# 4. Анализ типов занятости
employment_dist = df['employment'].value_counts(normalize=True) * 100

# 5. Анализ ключевых навыков
all_skills = df['key_skills'].str.split(', ').explode()
top_skills = all_skills.value_counts().head(20)

# 6. Анализ зарплатных предложений
df['salary_mid'] = (df['salary_from'] + df['salary_to']) / 2

# Визуализация результатов
plt.figure(figsize=(15, 12))

# График распределения профессиональных ролей
plt.subplot(2, 2, 1)
sns.barplot(y=professional_roles.index, x=professional_roles.values,
            hue=professional_roles.index, palette='viridis', orient='h', legend=False)
plt.title('Распределение профессиональных ролей', pad=20, fontsize=14)
plt.xlabel('Количество вакансий', fontsize=12)
plt.ylabel('')
plt.grid(axis='x')
plt.xlim(0, professional_roles.max() * 1.1)

# График распределения опыта работы
plt.subplot(2, 2, 2)
sns.barplot(y=experience_dist.index, x=experience_dist.values,
            hue=experience_dist.index, palette='viridis', orient='h', legend=False)
plt.title('Требования к опыту работы', pad=20, fontsize=14)
plt.xlabel('Доля вакансий, %', fontsize=12)
plt.ylabel('')
plt.grid(axis='x')
plt.xlim(0, 100)

# График распределения графиков работы
plt.subplot(2, 2, 3)
sns.barplot(y=schedule_dist.index, x=schedule_dist.values,
            hue=schedule_dist.index, palette='viridis', orient='h', legend=False)
plt.title('Графики работы', pad=20, fontsize=14)
plt.xlabel('Доля вакансий, %', fontsize=12)
plt.ylabel('')
plt.grid(axis='x')
plt.xlim(0, 100)

# График топ-10 ключевых навыков
plt.subplot(2, 2, 4)
sns.barplot(y=top_skills.head(10).index, x=top_skills.head(10).values,
            hue=top_skills.head(10).index, palette='viridis', orient='h', legend=False)
plt.title('Топ-10 ключевых навыков', pad=20, fontsize=14)
plt.xlabel('Количество упоминаний', fontsize=12)
plt.ylabel('')
plt.grid(axis='x')
plt.xlim(0, top_skills.max() * 1.1)

plt.tight_layout()
plt.show()

# Дополнительные графики
plt.figure(figsize=(15, 5))

# График распределения зарплат
plt.subplot(1, 2, 1)
sns.histplot(df['salary_mid'], bins=20, kde=True, color='skyblue')
plt.title('Распределение зарплат', pad=20, fontsize=14)
plt.xlabel('Зарплата, руб.', fontsize=12)
plt.ylabel('Количество вакансий', fontsize=12)
plt.grid(axis='y')

# График зависимости зарплаты от опыта работы
plt.subplot(1, 2, 2)
sns.boxplot(y='experience', x='salary_mid', data=df,
            hue='experience', palette='pastel', orient='h', legend=False)
plt.title('Зависимость зарплаты от опыта работы', pad=20, fontsize=14)
plt.xlabel('Зарплата, руб.', fontsize=12)
plt.ylabel('')
plt.grid(axis='x')

plt.tight_layout()
plt.show()

# Анализ вакансий с частичной занятостью и гибким графиком
part_time_flex = df[(df['employment'] == 'частичная занятость') | (df['schedule'] == 'гибкий график')]
part_time_roles = part_time_flex['professional_roles'].value_counts().head(10)
part_time_skills = part_time_flex['key_skills'].str.split(', ').explode().value_counts().head(10)

# График для вакансий с частичной занятостью/гибким графиком
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
sns.barplot(y=part_time_roles.index, x=part_time_roles.values,
            hue=part_time_roles.index, palette='viridis', orient='h', legend=False)
plt.title('Топ профессий с гибкими условиями', pad=20, fontsize=14)
plt.xlabel('Количество вакансий', fontsize=12)
plt.ylabel('')
plt.grid(axis='x')

plt.subplot(1, 2, 2)
sns.barplot(y=part_time_skills.index, x=part_time_skills.values,
            hue=part_time_skills.index, palette='viridis', orient='h', legend=False)
plt.title('Топ навыков для гибких вакансий', pad=20, fontsize=14)
plt.xlabel('Количество упоминаний', fontsize=12)
plt.ylabel('')
plt.grid(axis='x')

plt.tight_layout()
plt.show()