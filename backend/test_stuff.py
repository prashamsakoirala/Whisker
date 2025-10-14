import pylast

# Replace with your own API key and secret
API_KEY = '2b2a89a1312d55407b627d1b1861df63'
API_SECRET = '684b33f0f99c26f480cb841f0f0a4243'
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

similarity_artists_weight = 0.2

def get_tags(artist_name, num_tags = 5):
    artist = network.get_artist(artist_name)
    top_tags = artist.get_top_tags()

    sorted_tags = sorted(top_tags, key=lambda x: int(x.weight), reverse=True)

    return sorted_tags[:num_tags]

def get_tag_names_and_weights(tags):
    return [(tag.item.get_name(), int(tag.weight)) for tag in tags]

def get_similar_artists(name):
    tags_for_artist = get_tags(name)

    artist_obj = network.get_artist(name)
    similar_artists = artist_obj.get_similar(limit=5)

    similar_artists_sorted = sorted(similar_artists, key=lambda x: x.match, reverse=True)

    return similar_artists_sorted

def get_artist_score(name):
    tags = get_tag_names_and_weights(get_tags(name, 5))
    tag_dict = {tag: value for tag, value in tags}
    similar_artists = get_similar_artists(name)

    # now i want to get the top scores for brent faiyaz based on similar artists

    for similar in similar_artists:
        similar_name = similar.item.get_name()
        similarity_percentage = similar.match
        similarity_weighted_percentage = similarity_percentage * similarity_artists_weight
        similar_tags = get_tag_names_and_weights(get_tags(similar_name, 5))
        for tag, value in similar_tags:
            if tag in tag_dict:
                tag_dict[tag] += value * similarity_weighted_percentage
            else:
                tag_dict[tag] = value * similarity_weighted_percentage

    return tag_dict

def get_scores(name, score_total, percentage_value):
    artist_scores = get_artist_score(name)
    for tag, value in artist_scores.items():
        if tag in score_total:
            score_total[tag] += value * percentage_value
        else:
            score_total[tag] = value * percentage_value
