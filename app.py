import anipy_cli
import streamlit as st
import tempfile
from pathlib import Path

def main():
    st.markdown("<h1 style='text-align: center; color: #ff6961;'>Anius【アイヌス】🎬</h1>", unsafe_allow_html=True)
    st.write("---")

    # Step 1: Search for an anime
    query_term = st.text_input("Search for an anime: 🔍", placeholder="Enter an anime name...")

    if query_term:
        entry = anipy_cli.Entry()
        query_class = anipy_cli.query(query_term, entry)
        links_and_names = query_class.get_links()

        # Store search results in backend with serial numbers
        search_results = []
        for i, (link, name) in enumerate(zip(links_and_names[0], links_and_names[1]), start=1):
            search_results.append((f"{i}. {name}", f"https://gogoanime.gg{link}"))

        # Step 2: Select an anime from the search results
        selected_anime = st.selectbox("Select an anime: 📽️", options=[name for name, _ in search_results])

        if selected_anime:
            selected_url = next(url for name, url in search_results if name == selected_anime)
            entry.category_url = selected_url

            # Step 3: Get the episode handler and retrieve the latest episode
            ep_handler = anipy_cli.epHandler(entry)
            latest_episode = ep_handler.get_latest()

            # Display the list of available episode numbers
            available_episodes = list(range(1, latest_episode + 1))

            # Step 4: Get the user's episode selection
            selected_episode = st.selectbox(f"Select an episode number: 📼 [1-{latest_episode}]", available_episodes)

            if selected_episode:
                entry.ep = selected_episode
                entry = ep_handler.gen_eplink()

                # Step 5: Get the video URL
                video_url_class = anipy_cli.videourl(entry, "best")
                video_url_class.stream_url()
                entry = video_url_class.get_entry()
                #output is: Entry(show_name='', category_url='https://gogoanime.gg/category/naruto-shippuuden-movie-2-kizuna', ep_url='https://gogoanime3.co//naruto-shippuuden-movie-2-kizuna-episode-1', embed_url='https://embtaku.pro/streaming.php?id=NDA1ODg=&title=Naruto+Shippuuden+Movie+2%3A+Kizuna+Episode+1&typesub=SUB', stream_url='https://www049.vipanicdn.net/streamhls/7a5f81683439c04fa17f5250c3c5438f/ep.1.1709241222.m3u8', ep=1, latest_ep=1, quality='hls')

                # Output the embed link
                st.success(f"Embed Link: 🎥 {entry.embed_url}")

                st.video(f"{entry.stream_url}",autoplay=False)

                # Play the video in Streamlit
                # video_html = f'<video width="100%" height="auto" controls><source src="{entry.stream_url}" type="video/mp4"></video>'
                # st.markdown(video_html, unsafe_allow_html=True)
                # from streamlit_player import st_player
                # st_player(f"{entry.stream_url}")



if __name__ == "__main__":
    main()
