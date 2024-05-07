import anipy_cli
import streamlit as st

def main():
    st.title("Anime Video Player")

    # Step 1: Search for an anime
    query_term = st.text_input("Search for an anime:", "Naruto")
    if query_term:
        entry = anipy_cli.Entry()
        query_class = anipy_cli.query(query_term, entry)
        links_and_names = query_class.get_links()

        # Print the search results with index numbers
        search_results = []
        for i, (link, name) in enumerate(zip(links_and_names[0], links_and_names[1])):
            search_results.append(f"{i+1}. {name}: https://gogoanime.gg{link}")

        # Step 2: Select an anime from the search results
        selected_index = st.selectbox("Select an anime:", search_results)
        if selected_index:
            selected_index = int(selected_index.split(".")[0]) - 1
            entry.category_url = f"https://gogoanime.gg{links_and_names[0][selected_index]}"

            # Step 3: Get the episode handler and retrieve the latest episode
            ep_handler = anipy_cli.epHandler(entry)
            latest_episode = ep_handler.get_latest()

            # Display the list of available episode numbers
            available_episodes = list(range(1, latest_episode + 1))

            # Step 4: Get the user's episode selection
            selected_episode = st.selectbox(f"Select an episode number from [1-{latest_episode}]:", available_episodes)
            if selected_episode:
                entry.ep = selected_episode
                entry = ep_handler.gen_eplink()

                # Step 5: Get the video URL
                video_url_class = anipy_cli.videourl(entry, "best")
                video_url_class.stream_url()
                entry = video_url_class.get_entry()

                # Output the embed link
                st.write(f"Embed Link: {entry.embed_url}")

if __name__ == "__main__":
    main()
