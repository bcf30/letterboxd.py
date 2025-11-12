# months doesn't work
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('letterboxd-bigimdbfan30-2025-11-05-15-54-utc/fakeratings.csv')
ratingcounts = df['Rating'].value_counts().sort_index()

print(f'Diary Data Overview:\n------------------------')
print(df.head())
print('\nSummary Statistics:')
print(df.describe())
print('\nFilms by Rating:')
for rating, count in ratingcounts.items():
    print(f'{rating}: {count} films')

numfilms = len(df)
meanrating = df['Rating'].mean()
medianrating = df['Rating'].median()
ratingstd = df['Rating'].std()
moder = ratingcounts.idxmax()

print(f'Total Film Count: {numfilms}'
      f'\nMean Rating: {meanrating:.3f}'
      f'\nMode: {moder} ({ratingcounts[moder]} films with this rating)'
      f'\nStandard Deviation: {ratingstd:.3f}')

if 'Date' in df.columns:
    print('\nWatch Date Bias:\n------------------------')
    df['watchdate'] = pd.to_datetime(df['Date'], errors='coerce')
    if not df['watchdate'].isnull().all():
        # df['watchmonth'] = df['watchdate'].dt.month
        df['watchdayofweek'] = df['watchdate'].dt.day_name()

        dayorder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        dailycounts = df['watchdayofweek'].value_counts()
        dailycounts = dailycounts.reindex(dayorder, fill_value=0)
        print('Films Watched by Day of The Week:')
        for day in dayorder:
            count = dailycounts[day]
            print(f'{day}: {count} films')

        dailyratings = df.groupby('watchdayofweek')['Rating'].mean()
        dailyratings = dailyratings.reindex(dayorder)
        print('\nAverage Rating by Day of The Week:')
        for day in dayorder:
            if pd.notna(dailyratings[day]):
                print(f'{day}: {dailyratings[day]:.2f}')
            else:
                print(f'{day}: No data')

        # monthlycounts = df['watchmonth'].value_counts().sort_index()
        # months = ['January', 'February', 'March', 'April', 'May', 'June',
                  # 'July', 'August', 'September', 'October', 'November', 'December']
        # monthlycounts = monthlycounts.reindex(range(1, 13), fill_value=0)
        # print('\nFilms Watched By Month:')
        # for i, month in enumerate(months, 1):
            # count = monthlycounts.get(i, 0)
            # print(f'{month}: {count} films watched')

        # monthratings = df.groupby('watchmonth')['Rating'].mean()
        # monthratings = monthratings.reindex(range(1, 13))
        # print('\nAverage Rating By Month:')
        # for i, month in enumerate(months, 1):
            # if i in monthratings.index and pd.notna(monthratings[i]):
                # print(f'{month}: {monthratings[i]:.2f}')
            # else:
                # print(f'{month}: No Ratings')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
allratings = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
ratingcountsfixed = df['Rating'].value_counts().reindex(allratings, fill_value=0)
bars = ax1.bar(ratingcountsfixed.index, ratingcountsfixed.values, alpha=0.7, color='skyblue', edgecolor='black',
               width=0.4)
ax1.axvline(meanrating, color='red', linestyle='--', linewidth=2, label=f'Mean: {meanrating:.3f}')
ax1.axvline(medianrating, color='green', linestyle='--', linewidth=2, label=f'Median: {medianrating:.3f}')
ax1.set_xlabel('Rating')
ax1.set_ylabel('Number of Films')
ax1.set_title(f'Rating Distribution\n(std: {ratingstd:.3f})')
ax1.set_xticks(allratings)
ax1.legend()
ax1.grid(alpha=0.3)
for bar, count in zip(bars, ratingcountsfixed.values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2., height, f'{count}', ha='center', va='bottom')
if 'watchdayofweek' in df.columns:
    validdays = [day for day in dayorder if pd.notna(dailyratings[day])]
    validratings = [dailyratings[day] for day in validdays]
    colors = ['lightcoral' if rating < meanrating else 'lightgreen' for rating in validratings]
    bars = ax2.bar(validdays, validratings, alpha=0.7, color=colors)
    ax2.axhline(meanrating, color='red', linestyle='--', linewidth=2, label=f'Overall Mean: {meanrating:.3f}')
    ax2.set_xlabel('Day of Week')
    ax2.set_ylabel('Average Rating')
    ax2.set_title('Average Rating by Day of Week')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend()
    ax2.grid(alpha=0.3)
    for bar, rating in zip(bars, validratings):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height, f'{rating:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()