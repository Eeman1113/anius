import anipy_cli
import streamlit as st
import time

def main():
    st.markdown("<h1 style='text-align: center; color: #ff6961;'>Anius【アイヌス】🎬</h1>", unsafe_allow_html=True)
    st.write("---")

    # Step 1: Search for an anime
    query_term = st.text_input("Search for an anime: 🔍", placeholder="Enter an anime name...")

    if query_term:
        entry = anipy_cli.Entry()

        # Show progress bar
        progress_text = "Searching for anime..."
        progress_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1, text=progress_text)

        query_class = anipy_cli.query(query_term, entry)
        links_and_names = query_class.get_links()

        # Store search results in backend
        search_results = []
        for link, name in zip(links_and_names[0], links_and_names[1]):
            search_results.append((name, f"https://gogoanime.gg{link}"))

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

                # Output the embed link
                st.success(f"Here You Go: 🎥 {entry.embed_url}")

                # Add download button
                if st.button("Download Episode"):
                    dl_class = anipy_cli.download(entry, "best")
                    dl_class.download()
                    st.balloons()

        progress_bar.empty()

if __name__ == "__main__":
    main()
