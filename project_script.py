# %%
# imports
import numpy as np
import pandas as pd

# plotting
import matplotlib
#matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import warnings
warnings.simplefilter('ignore', FutureWarning)

'imports complete'

# %%
raw_rave_albums = pd.read_csv('C:/Users/owenf/OneDrive/VSCode/Personal/Owen Bot/Rave Album Swap Datasheet - Sheet1.csv')
raw_rave_albums.head()

# %%
# Removing 'nan' string and replacing it with 'N/A' for each genre spot that doesn't have a labeled genre

# Function that removes 'nan' and replaces it with 'N/A'
def remove_nan(n):
    if str(n).lower() == 'nan':
        return 'N/A'
    else:
        return n

# Fixes for each individual column
genre2_fix = raw_rave_albums['Genre 2'].apply(remove_nan)
genre3_fix = raw_rave_albums['Genre 3'].apply(remove_nan)

# New table with fixed columns
rave_albums_genre_fix = raw_rave_albums.drop(['Genre 2', 'Genre 3'], axis=1)
rave_albums_genre_fix['Genre 2'] = genre2_fix
rave_albums_genre_fix['Genre 3'] = genre3_fix
rave_albums_genre_fix = rave_albums_genre_fix[['Album', 'Artist', 'Genre 1', 'Genre 2', 'Genre 3', 'User Submitted']]
rave_albums_genre_fix.head(10)

# %%
all_genres = rave_albums_genre_fix['Genre 1'].values
all_genres = np.append(all_genres, rave_albums_genre_fix['Genre 2'].values)
all_genres = np.append(all_genres, rave_albums_genre_fix['Genre 3'].values)

# %%
# Remove all instances of 'N/A' in genre list
all_genres = all_genres[all_genres != 'N/A']

# %%
# Count number of albums submitted statistic
num_albums = len(raw_rave_albums['Album'])
num_albums

# %%
unique_genres = np.unique(all_genres)
len(unique_genres)

# %%
# Top genres submitted in swaps
top_genres = pd.DataFrame(all_genres, columns=['Genre']).groupby('Genre').size().reset_index(name='Count')
top_genres = top_genres.sort_values(by='Count', ascending=False)
top_genres.head(10)

# %%
# Top users who submitted albums
all_users = raw_rave_albums['User Submitted']
top_users = pd.DataFrame(all_users, columns=['User Submitted']).groupby('User Submitted').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
top_users.head(10)

# %%
user_list = top_users['User Submitted'].values
user_list

# %%
user_count_list = top_users['Count'].values
user_count_list

# %%
# Most popular genres graph
top_10_genres = top_genres['Genre'][:10]
top_10_genres_count = top_genres['Count'][:10]
top_10_genres = pd.DataFrame({'Genre': top_10_genres, 'Count': top_10_genres_count})
top_10_genres.plot.barh(x='Genre', y='Count')

# %%
# Top artists submitted graph
all_artists = raw_rave_albums['Artist']
top_artists = pd.DataFrame(all_artists, columns=['Artist']).groupby('Artist').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
top_artists.head(5)

# %%
artist_array = top_artists['Artist'].values
artist_array

# %%
# Top artists graph
top_10_artists = top_artists['Artist'][:10]
top_10_artists_count = top_artists['Count'][:10]
top_10_artists = pd.DataFrame({'Artist': top_10_artists, 'Count': top_10_artists_count})
top_10_artists.plot.barh(x='Artist', y='Count')

# %%
def user_album_combo(col1, col2):
    return col1 + ' - ' + col2
rave_with_useralbum = raw_rave_albums.apply(lambda row: user_album_combo(row['Album'], row['User Submitted']), axis=1)
rave_with_useralbum

# %%
genre_table = pd.DataFrame({'Genres': all_genres})
genre_table[genre_table['Genres'].str.contains('Jazz')]

# %%
artist_list = raw_rave_albums['Artist'].tolist()
all_artist_list_lower = [artist.lower() for artist in artist_list]
print(all_artist_list_lower)
artist_count_list = pd.Series(all_artist_list_lower).value_counts()
print(artist_count_list)
artist_count_list.columns = ['Artist', 'Count']
print(artist_count_list)
# %%
