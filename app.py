import streamlit as st
from anipy_api.provider import get_provider, LanguageTypeEnum
from anipy_api.anime import Anime
from streamlit_player import st_player

def main():
    st.markdown("<h1 style='text-align: center; color: #ff6961;'>Anius【アイヌス】🎬</h1>", unsafe_allow_html=True)
    st.write("---")

    # Step 1: Get a provider instance
    provider = get_provider("gogoanime")

    # Step 2: Search for an anime
    query_term = st.text_input("Search for an anime: 🔍", placeholder="Enter an anime name...")

    if query_term:
        search_results = provider.get_search(query_term)
        anime_options = [(result.name, result) for result in search_results]

        # Step 3: Select an anime from the search results
        selected_anime_name, selected_anime_result = st.selectbox("Select an anime: 📽️", options=anime_options)

        if selected_anime_name:
            anime = Anime.from_search_result(provider, selected_anime_result)

            # Step 4: Get episodes
            episodes = anime.get_episodes(lang=LanguageTypeEnum.SUB)
            selected_episode = st.selectbox(f"Select an episode number: 📼 [1-{len(episodes)}]", options=episodes)

            if selected_episode:
                # Step 5: Get the video stream
                stream = anime.get_video(episode=selected_episode, lang=LanguageTypeEnum.SUB, preferred_quality="best")
                st.success(f"Embed Link: 🎥 {stream.embed_url}")

                # Play the video in Streamlit
                st_player(stream.stream_url)

if __name__ == "__main__":
    main()
