# 1. Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Load Excel File
file_path = 'youtube_growth_tracker.xlsx'  
df = pd.read_excel(file_path)

# 3. Data Cleaning & Preprocessing
# a) Check missing values
print("Missing values:\n", df.isnull().sum())

# b) Fill missing values for ALL columns
df.fillna({
    'Video ID': 'Unknown',
    'Title': 'Untitled',
    'Category': 'Unknown',
    'Views': 0,
    'Likes': 0,
    'CTR %': 0,
    'Watch Time (min)': 0,
    'Subs Gained': 0,
    'Subs Lost': 0
}, inplace=True)

df['Upload Date'] = pd.to_datetime(df['Upload Date'], errors='coerce').dt.date

# c) Remove duplicate rows
df.drop_duplicates(inplace=True)

# d) Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# e) Ensure numeric columns are numeric
numeric_cols = ['views', 'likes', 'ctr_%', 'watch_time_(min)', 'subs_gained', 'subs_lost']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# f) Add net_subscribers column
df['net_subscribers'] = df['subs_gained'] - df['subs_lost']

# 4. Data Analysis

print("Average views:", df['views'].mean())
print("Max likes:", df['likes'].max(), "Min likes:", df['likes'].min())
print("Video count by category:\n", df['category'].value_counts())
print("Top videos by net subscribers:\n", df.sort_values(by='net_subscribers', ascending=False)[['title', 'net_subscribers']])
print("Average views per category:\n", df.groupby('category')['views'].mean())

# 5. Data Visualization

# a) Bar Chart - Top 10 categories by video count
plt.figure(figsize=(8,5))
top_categories = df['category'].value_counts().head(10)
sns.barplot(x=top_categories.index, y=top_categories.values)
plt.title('Bar Chart of Top 10 Video Categories')
plt.xlabel('Category',fontweight='bold')
plt.ylabel('Number of Videos',fontweight='bold')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('bar_chart_categories.png')
plt.show()

# b) Pie Chart - Category distribution (Top 5)
plt.figure(figsize=(6,6))
top5 = df['category'].value_counts().head(5)
plt.pie(top5.values, labels=top5.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Pie Chart of Top 5 Categories Distribution')
plt.tight_layout()
plt.savefig('pie_chart_categories.png')
plt.show()

# c) Histogram - Views distribution
plt.figure(figsize=(8,5))
sns.histplot(df['views'], bins=20, kde=True, color='skyblue')
plt.title('Histogram of Distribution of Views')
plt.xlabel('Views',fontweight='bold')
plt.ylabel('Frequency',fontweight='bold')
plt.tight_layout()
plt.savefig('histogram_views.png' )
plt.show()

# d) Scatter Plot - Views vs Likes
plt.figure(figsize=(8,5))
sns.scatterplot(x='views', y='likes', data=df, hue='category', palette='Set2', alpha=1)
plt.title('Scatterplot of Views vs Likes by Category')
plt.xlabel('Views',fontweight='bold')
plt.ylabel('Likes',fontweight='bold')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('scatter_views_likes.png')
plt.show()

# e) Line Chart - Net Subscribers trend (Top 20 videos)
plt.figure(figsize=(10,5))
top_videos = df.sort_values(by='net_subscribers', ascending=False).head(20)
plt.plot(top_videos['video_id'], top_videos['net_subscribers'], marker='o', linestyle='-', color='green')
plt.xticks(rotation=0)
plt.title('Line Chart of Top 20 Videos by Net Subscribers')
plt.xlabel('Video ID', fontweight='bold')
plt.ylabel('Net Subscribers',fontweight='bold')
plt.tight_layout()
plt.savefig('line_net_subscribers.png')
plt.show()

# 6. Save cleaned data and charts
df.to_excel('youtube_data_trackers.xlsx', index=False)
print("Script executed successfully. Cleaned data and charts saved.")
